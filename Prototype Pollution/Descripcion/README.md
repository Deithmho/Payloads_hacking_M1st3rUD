# 📖 Prototype pollution: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

En JavaScript, un merge profundo que acepta claves como `__proto__` puede modificar propiedades heredadas por otros objetos. Se requiere además un gadget que lea esa propiedad para alcanzar impacto.

El límite de confianza relevante es **claves anidadas de JSON o query frente a merge de objetos JavaScript**. La aplicación recibe **claves anidadas de JSON o query** y debería **bloquear claves peligrosas y usar estructuras sin prototipo**. La vulnerabilidad aparece cuando **se escribe en el prototipo en lugar de un objeto aislado**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza claves anidadas de JSON o query en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en merge de objetos JavaScript.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si se escribe en el prototipo en lugar de un objeto aislado.
4. **Observación:** Una propiedad marcador aparece en un objeto nuevo del mismo contexto y desaparece tras reiniciar; no se infiere un gadget sin observar su uso.

## 🧭 Contextos y variantes

**Dónde buscar:** SPAs, Node.js, bibliotecas de merge y configuración dinámica.

| Variante | Diferencia técnica |
| --- | --- |
| **Cliente** | La contaminación afecta el JavaScript de una página. |
| **Servidor** | Afecta un proceso compartido de Node.js. |
| **Gadget** | Una lectura posterior convierte la propiedad en XSS, cambio de lógica u otro efecto. |

## 🔗 Cadenas y dependencias

Una propiedad `isAdmin` heredada solo eleva privilegios si un control de acceso la usa; documentar esa lectura y su efecto.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

La contaminación aislada es una primitive; la severidad depende del gadget reproducido y su alcance. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar claves anidadas de JSON o query y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en merge de objetos JavaScript.
- Confirmar: Una propiedad marcador aparece en un objeto nuevo del mismo contexto y desaparece tras reiniciar; no se infiere un gadget sin observar su uso.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Rechazar `__proto__`, `constructor` y `prototype` al fusionar datos; fijar propiedades propias en decisiones sensibles. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: prototype pollution](https://portswigger.net/web-security/prototype-pollution) — fuentes, gadgets y sinks.
- [PortSwigger: DOM](https://portswigger.net/web-security/dom-based) — fuentes y sinks.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
