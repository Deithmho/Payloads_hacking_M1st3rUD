# 📖 BFLA: autorización rota por función: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una API ofrece una operación que el rol actual no debería invocar, incluso si el objeto referido es suyo. La diferencia con BOLA es el permiso para usar la función, no el permiso sobre un ID.

El límite de confianza relevante es **método y ruta API de rol privilegiado frente a handler de función**. La aplicación recibe **método y ruta API de rol privilegiado** y debería **autorizar función según rol/atributos del principal**. La vulnerabilidad aparece cuando **el handler solo verifica autenticación o depende de la UI**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza método y ruta API de rol privilegiado en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en handler de función.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el handler solo verifica autenticación o depende de la UI.
4. **Observación:** Una cuenta de rol bajo ejecuta una función de rol alto sobre un recurso de prueba y se verifica el efecto.

## 🧭 Contextos y variantes

**Dónde buscar:** endpoints admin, exportación, invitaciones, cambios de roles y métodos alternativos.

| Variante | Diferencia técnica |
| --- | --- |
| **Ruta no visible** | El endpoint existe aunque la UI lo oculte. |
| **Método** | Un verbo alterno llega a función privilegiada. |
| **Versión** | Una API antigua carece del mismo middleware. |

## 🔗 Cadenas y dependencias

BFLA en creación de invitaciones puede combinarse con mass assignment para emitir invitación admin; ambas condiciones requieren evidencia.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

El acceso a una función sensible puede ser alto; recibir 200 sin operación exitosa no confirma privilegio. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar método y ruta API de rol privilegiado y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en handler de función.
- Confirmar: Una cuenta de rol bajo ejecuta una función de rol alto sobre un recurso de prueba y se verifica el efecto.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Denegar por defecto por función y método; compartir políticas entre versiones de API y probar roles bajos. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP API5:2023 BFLA](https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization/) — autorización por función.
- [PortSwigger: pruebas API](https://portswigger.net/web-security/api-testing) — descubrimiento de superficie.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
