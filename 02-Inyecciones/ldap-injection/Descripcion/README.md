# 📖 LDAP injection: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Una aplicación compone filtros LDAP con entrada sin escapar. Caracteres `*`, `(`, `)` o `\` pueden cambiar la expresión y ampliar resultados.

El límite de confianza relevante es **un nombre de usuario o búsqueda de directorio frente a un filtro LDAP**. La aplicación recibe **un nombre de usuario o búsqueda de directorio** y debería **escapar según RFC 4515 y separar estructura de valores**. La vulnerabilidad aparece cuando **los caracteres del usuario cambian el árbol del filtro**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un nombre de usuario o búsqueda de directorio en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en un filtro LDAP.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si los caracteres del usuario cambian el árbol del filtro.
4. **Observación:** La cuenta propia devuelve resultados diferentes entre texto literal y filtro manipulado, con controles repetidos.

## 🧭 Contextos y variantes

**Dónde buscar:** login corporativo, directorios, grupos y libreta de contactos.

| Variante | Diferencia técnica |
| --- | --- |
| **Comodín** | Un `*` sustituye parte de una igualdad. |
| **Filtro booleano** | Paréntesis añadidos alteran la lógica. |
| **Atributo** | El usuario influye en el nombre de atributo en código dinámico. |

## 🔗 Cadenas y dependencias

Un filtro ampliado usado para seleccionar la primera cuenta puede devenir bypass de autenticación, pero requiere demostrar la sesión creada.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Desde enumeración de directorio hasta suplantación según el flujo y la validación de contraseña. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un nombre de usuario o búsqueda de directorio y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en un filtro LDAP.
- Confirmar: La cuenta propia devuelve resultados diferentes entre texto literal y filtro manipulado, con controles repetidos.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Escapar valores de filtro, fijar atributos permitidos y no utilizar el primer resultado como identidad autenticada. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real.

## 📚 Fuentes

- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
