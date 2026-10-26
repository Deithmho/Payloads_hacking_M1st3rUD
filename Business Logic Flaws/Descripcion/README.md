# 📖 Fallos de lógica de negocio: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

La aplicación implementa reglas de dominio a través de múltiples pasos. Una ruta alternativa, orden inesperado o valor límite puede violar una invariante aunque cada endpoint valide tipos y permisos por separado.

El límite de confianza relevante es **un flujo multietapa con objetos propios frente a la máquina de estados de negocio**. La aplicación recibe **un flujo multietapa con objetos propios** y debería **validar invariantes en cada transición servidor**. La vulnerabilidad aparece cuando **una secuencia no prevista salta una regla**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un flujo multietapa con objetos propios en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en la máquina de estados de negocio.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si una secuencia no prevista salta una regla.
4. **Observación:** El estado final del objeto propio contradice una regla explícita y el flujo normal no lo permite.

## 🧭 Contextos y variantes

**Dónde buscar:** e-commerce, pagos de prueba, reservas, cupones y onboarding.

| Variante | Diferencia técnica |
| --- | --- |
| **Salto de paso** | Se invoca una transición final sin condición previa. |
| **Valor extremo** | Cero, negativo o límite supera una suposición. |
| **Secuencia inversa** | El orden de operaciones cambia el resultado. |
| **Confusión de roles** | Una acción se aplica al actor equivocado. |

## 🔗 Cadenas y dependencias

Una carrera puede permitir dos usos de una promoción; la regla rota es de negocio, la primitive es concurrencia. Documentar ambos sin duplicar hallazgos.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

La severidad exige cuantificar pérdida, acceso o abuso demostrable en entorno de prueba; no extrapolar a producción sin evidencias. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un flujo multietapa con objetos propios y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en la máquina de estados de negocio.
- Confirmar: El estado final del objeto propio contradice una regla explícita y el flujo normal no lo permite.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Formalizar estados e invariantes, verificar condiciones en backend y cubrir secuencias anómalas con pruebas. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: lógica de negocio](https://portswigger.net/web-security/logic-flaws) — análisis de flujos.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
