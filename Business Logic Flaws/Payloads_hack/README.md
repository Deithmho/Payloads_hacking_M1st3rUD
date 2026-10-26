# 🗡️ Fallos de lógica de negocio: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Cantidad cero

**Objetivo:** Comprobar una invariante de cantidad en carrito de laboratorio.

```json
{"productId":"{PRODUCTO_PROPIO}","quantity":0}
```

**Interpretación:** Verificar total, stock y pedido final; un 200 sin persistencia no prueba fallo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/logic-flaws).

### 2. Cantidad negativa

**Objetivo:** Comprobar si el cálculo usa signo sin validarlo.

```json
{"productId":"{PRODUCTO_PROPIO}","quantity":-1}
```

**Interpretación:** No finalizar compras reales. Un total negativo solo es hallazgo si llega a una transacción o crédito no previsto.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Business%20Logic%20Errors).

### 3. Precio aportado por cliente

**Objetivo:** Confirmar que el servidor recalcula el precio del catálogo.

```json
{"productId":"{PRODUCTO_PROPIO}","quantity":1,"unitPrice":0.01}
```

**Interpretación:** El backend debe ignorar el precio cliente. Comparar total en pedido de prueba, no solo eco JSON.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/logic-flaws).

### 4. Salto de estado

**Objetivo:** Invocar la transición final sin el paso previo.

```http
POST /api/test-orders/{ID_PROPIO}/confirm HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Registrar estado anterior y posterior; si la transición es permitida por diseño, no hay fallo.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/logic-flaws).

### 5. Reutilización de cupón

**Objetivo:** Verificar límite de un uso con dos objetos de prueba secuenciales.

```json
{"orderId":"{ID_PROPIO_2}","coupon":"{CUPON_DE_PRUEBA_YA_USADO}"}
```

**Interpretación:** Comprobar descuento final y regla documentada; no automatizar cupones de producción.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Business%20Logic%20Errors).

### 6. Invariante entre cuentas propias

**Objetivo:** Comprobar si una operación se aplica al actor correcto.

```json
{"fromAccount":"{CUENTA_A}","toAccount":"{CUENTA_B}","amount":1,"currency":"TEST"}
```

**Interpretación:** Usar saldo simulado; validar autorización sobre ambas cuentas y reversibilidad.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/logic-flaws).

### 7. Descuento acumulado

**Objetivo:** Verificar si dos promociones incompatibles se aplican juntas.

```json
{"cartId":"{CARRITO_PROPIO}","coupons":["{CUPON_A}","{CUPON_B}"]}
```

**Interpretación:** Confirmar política y total persistido en entorno de pruebas.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Business%20Logic%20Errors).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
