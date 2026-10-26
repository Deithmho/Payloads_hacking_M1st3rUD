# 📖 Autenticación rota: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

La identidad se establece con una credencial, un factor adicional y una sesión. Un fallo en cualquiera de las transiciones puede permitir entrar como otra persona o conservar acceso tras una revocación.

El límite de confianza relevante es **cliente frente a servicio de identidad**. La aplicación recibe **credenciales y estado de sesión** y debería **verificar cada factor y crear una sesión vinculada al usuario**. La vulnerabilidad aparece cuando **una ruta emite o acepta una sesión sin completar la verificación**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se inicia sesión con una cuenta de prueba y se registran cookies y cambios de estado.
2. **Procesamiento:** Se repite una ruta protegida sin autenticación o en un estado intermedio.
3. **Ruptura del control:** El backend confía en un indicador del cliente o en una sesión previa.
4. **Observación:** Se compara el resultado con una cuenta no autenticada y otra autenticada.

## 🧭 Contextos y variantes

**Dónde buscar:** login web, SSO, aplicaciones móviles con API y servicios que comparten middleware.

| Variante | Diferencia técnica |
| --- | --- |
| **Salto de flujo** | La ruta final se invoca sin completar el paso anterior. |
| **Sesión residual** | Una sesión anterior sigue siendo válida tras logout o cambio de contraseña. |
| **Enumeración** | Las diferencias de respuesta filtran existencia de cuentas; por sí solas no son toma de cuenta. |

## 🔗 Cadenas y dependencias

Una recuperación de contraseña débil puede producir una sesión válida; si además la autorización por objeto falla, esa sesión permite acceder a objetos de otros usuarios. Cada salto se comprueba por separado.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede ir de exposición limitada hasta toma de cuenta. Demostrar una acción protegida con una identidad que no debería poder hacerla, sin tocar datos ajenos. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Dibujar estados: anónimo, contraseña aceptada, MFA pendiente, autenticado y sesión revocada.
- Probar la misma ruta en cada estado con dos cuentas propias.
- Observar regeneración de identificador de sesión tras login.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Centralizar la autenticación en el servidor, validar transiciones, regenerar sesión al autenticar e invalidar tokens al revocar. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: autenticación](https://portswigger.net/web-security/authentication) — mecanismos y laboratorios.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
