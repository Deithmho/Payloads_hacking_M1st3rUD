# 📖 Ataques contra JWT: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un JWT firmado no cifra su contenido. La seguridad depende de verificar la firma con claves y algoritmos fijados por el servidor y de validar emisor, audiencia, expiración y propósito del token.

El límite de confianza relevante es **cabecera JWT no confiable frente al verificador**. La aplicación recibe **header, claims y firma del token** y debería **fijar algoritmo y clave esperados fuera del token**. La vulnerabilidad aparece cuando **la cabecera del token elige el algoritmo o la ubicación de la clave sin restricciones**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se captura un token emitido para una cuenta propia.
2. **Procesamiento:** Se decodifican header y claims sin asumir que decodificar equivale a validar.
3. **Ruptura del control:** Se altera una propiedad y se firma o deja sin firma según el escenario de laboratorio.
4. **Observación:** Se compara el recurso protegido con token válido, alterado y ausente.

## 🧭 Contextos y variantes

**Dónde buscar:** APIs con bearer tokens, federación SSO, microservicios y pasarelas que validan JWT.

| Variante | Diferencia técnica |
| --- | --- |
| **alg none** | Aceptación de un token sin firma por verificación desactivada. |
| **kid** | Identificador de clave tratado como ruta o selector no confiable. |
| **JWK/jku** | Aceptación de una clave aportada por el atacante sin confianza previa. |
| **Secreto débil** | Clave HMAC adivinable en un entorno de pruebas autorizado. |

## 🔗 Cadenas y dependencias

Si un JWT alterado cambia `sub` o `role` y la API confía en él, el siguiente eslabón es acceso por objeto o función. Primero se demuestra la aceptación criptográfica; luego la autorización efectiva.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Una firma omitida o clave atacante puede permitir suplantación o elevación. Un JWT visible en el cliente no es por sí mismo una fuga, pues sus claims no están cifrados. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Comprobar algoritmo esperado y rechazo de `none` con una cuenta propia.
- Comparar token válido, claim modificado con firma inválida y token expirado.
- Verificar que `kid`, `jwk` y `jku` no provocan carga de claves externas.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Fijar algoritmos admitidos, asociar claves a emisores confiables y validar `iss`, `aud`, `exp` y propósito; ignorar referencias de clave no autorizadas. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [PortSwigger: JWT](https://portswigger.net/web-security/jwt) — mecanismos y laboratorios.
- [RFC 8725](https://datatracker.ietf.org/doc/html/rfc8725) — buenas prácticas de JWT.
- [HackTricks: JWT](https://book.hacktricks.wiki/es/pentesting-web/hacking-jwt-json-web-tokens.html) — catálogo de variantes que requiere contraste por implementación.

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
