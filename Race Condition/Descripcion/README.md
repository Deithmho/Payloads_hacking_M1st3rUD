# 📖 Race condition: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Dos operaciones concurrentes leen un estado antes de que una actualización se confirme. Si ambas superan el mismo chequeo, pueden consumir un recurso o aplicar una regla más veces de lo permitido.

El límite de confianza relevante es **dos solicitudes sobre el mismo recurso propio frente a la transacción de negocio**. La aplicación recibe **dos solicitudes sobre el mismo recurso propio** y debería **usar atomicidad, bloqueo o idempotencia según operación**. La vulnerabilidad aparece cuando **chequeo y escritura no son indivisibles**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza dos solicitudes sobre el mismo recurso propio en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en la transacción de negocio.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si chequeo y escritura no son indivisibles.
4. **Observación:** Dos solicitudes controladas producen un resultado incompatible con la regla y el estado final se verifica.

## 🧭 Contextos y variantes

**Dónde buscar:** cupones, saldos de laboratorio, límites, invitaciones y canje de tokens.

| Variante | Diferencia técnica |
| --- | --- |
| **Limit overrun** | Se consume el mismo permiso más de una vez. |
| **Multi-endpoint** | Dos rutas comparten un estado transitorio. |
| **Partial construction** | Un objeto incompleto queda visible antes de finalizar. |

## 🔗 Cadenas y dependencias

La ausencia de idempotencia en pagos puede amplificar una race; hacer solo pruebas reversibles y con autorización específica para transacciones.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Depende del activo duplicado o del estado inconsistente. Un doble `200` sin doble efecto no prueba race. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar dos solicitudes sobre el mismo recurso propio y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en la transacción de negocio.
- Confirmar: Dos solicitudes controladas producen un resultado incompatible con la regla y el estado final se verifica.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Aplicar transacciones atómicas, restricciones únicas, idempotency keys y pruebas de concurrencia en staging. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

El [informe divulgado #1132171 de HackerOne](https://hackerone.com/reports/1132171) describió múltiples envíos de feedback por condición de carrera. Su severidad fue baja en ese contexto; la primitive concurrente no determina por sí misma una pérdida económica.

## 📚 Fuentes

- [PortSwigger: race conditions](https://portswigger.net/web-security/race-conditions) — ventanas de carrera.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [HackerOne: race condition, informe 1132171](https://hackerone.com/reports/1132171) — reporte divulgado sobre feedback duplicado.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
