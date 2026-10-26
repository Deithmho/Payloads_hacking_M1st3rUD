# 🗡️ Bypass de rate limit: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Línea base de tres intentos

**Objetivo:** Estimar contador sin fuerza bruta.

```bash
for n in 1 2 3; do curl -s -o /dev/null -w "%{http_code}\n" "https://{ORIGEN}/api/test-owned"; done
```

**Interpretación:** Ausencia de 429 no demuestra límite ausente; puede haber ventana mayor o control silencioso.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Brute%20Force%20Rate%20Limit).

### 2. X-Forwarded-For no confiable

**Objetivo:** Comprobar si el contador usa un valor aportado por cliente.

```http
GET /api/test-owned HTTP/1.1
Host: {ORIGEN}
X-Forwarded-For: 192.0.2.10
```

**Interpretación:** Comparar con control sin cabecera y pocas solicitudes; cambios de IP en logs no prueban bypass del límite.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Brute%20Force%20Rate%20Limit).

### 3. X-Real-IP no confiable

**Objetivo:** Probar un segundo encabezado de proxy con IP de documentación.

```http
GET /api/test-owned HTTP/1.1
Host: {ORIGEN}
X-Real-IP: 192.0.2.11
```

**Interpretación:** La decisión debe provenir de proxy confiable. No usar IPs de terceros.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Brute%20Force%20Rate%20Limit).

### 4. Cuenta frente a IP

**Objetivo:** Distinguir si el control protege a la identidad o solo a la conexión.

```text
Misma cuenta propia desde dos sesiones de prueba; 2 solicitudes por sesión; mismo endpoint.
```

**Interpretación:** Si el contador se separa por sesión, cuantificar ventana y precondiciones antes de afirmar riesgo de fuerza bruta.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication/auth-lab-usernames).

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

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Brute%20Force%20Rate%20Limit).

### 6. Método alterno

**Objetivo:** Detectar si la cuota cubre solo un método.

```http
GET /api/test-owned?action=check HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Solo comparar si GET y POST ejecutan la misma operación; un endpoint diferente no basta.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Brute%20Force%20Rate%20Limit).

### 7. Respuesta 429 y Retry-After

**Objetivo:** Registrar ventana real sin excederla.

```bash
curl -i "https://{ORIGEN}/api/test-owned" | rg -i "HTTP/|retry-after|ratelimit"
```

**Interpretación:** Una cabecera es señal de política, pero el efecto debe verificarse con un caso permitido.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/authentication).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
