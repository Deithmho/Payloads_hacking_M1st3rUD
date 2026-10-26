# 📖 Bypass de MFA: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

MFA debe ser una condición del estado autenticado que el servidor verifica en cada ruta sensible, no una pantalla adicional que el cliente pueda saltar.

El límite de confianza relevante es **primer factor frente a sesión plenamente autenticada**. La aplicación recibe **cookie o token emitido tras contraseña** y debería **bloquear recursos hasta completar segundo factor**. La vulnerabilidad aparece cuando **la sesión intermedia se acepta en rutas finales**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se inicia sesión con la contraseña de una cuenta propia y se detiene antes de MFA.
2. **Procesamiento:** Se invoca una ruta protegida con esa sesión intermedia.
3. **Ruptura del control:** Se compara contra la sesión tras MFA y otra sin iniciar sesión.
4. **Observación:** Se confirma una operación protegida en el estado intermedio.

## 🧭 Contextos y variantes

**Dónde buscar:** login web, APIs móviles, recuperación de cuenta y cambio de factor.

| Variante | Diferencia técnica |
| --- | --- |
| **Salto de ruta** | Recursos aceptan sesión pendiente. |
| **Remember device** | Token de dispositivo confiable no está ligado al equipo. |
| **Recuperación** | Un flujo alterno elimina MFA sin prueba equivalente. |
| **OTP débil** | Falta de caducidad o bloqueo facilita intentos; no se asume bypass sin prueba. |

## 🔗 Cadenas y dependencias

Si un reset de contraseña crea una sesión ya marcada como MFA completado, el flujo de recuperación puede servir como bypass. Validar el estado en ambos caminos.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

El acceso a datos o acciones protegidas sin segundo factor puede ser alto o crítico según privilegio. Ver una página de MFA omitida no prueba acceso efectivo. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Comparar sesión antes y después de MFA.
- Probar API y UI en cada estado.
- Revisar recuperación, cambio de factor y nuevos dispositivos.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Modelar MFA como estado servidor, exigirlo por recurso, ligar tokens de confianza al dispositivo y proteger los flujos de recuperación. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: autenticación](https://portswigger.net/web-security/authentication) — mecanismos y laboratorios.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
