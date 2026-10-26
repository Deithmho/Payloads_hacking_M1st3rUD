# 📖 SQL injection: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

Un valor controlado alcanza el texto de una consulta SQL en lugar de enlazarse como parámetro. El motor interpreta operadores y comentarios como parte de la consulta, y la aplicación puede devolver datos o diferencias observables.

El límite de confianza relevante es **un parámetro de búsqueda o ID frente a la construcción de SQL**. La aplicación recibe **un parámetro de búsqueda o ID** y debería **usar consultas parametrizadas**. La vulnerabilidad aparece cuando **el dato se concatena como SQL**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** Se localiza un parámetro de búsqueda o ID en una solicitud legítima y se fija una línea base.
2. **Procesamiento:** El servicio procesa la entrada en la construcción de SQL.
3. **Ruptura del control:** Se modifica una sola propiedad para comprobar si el dato se concatena como SQL.
4. **Observación:** Comparar respuestas para condición verdadera y falsa sobre datos de prueba; errores, retardos y tráfico OAST son señales distintas, no prueba automática de extracción.

## 🧭 Contextos y variantes

**Dónde buscar:** filtros REST, buscadores, informes y aplicaciones legacy.

| Variante | Diferencia técnica |
| --- | --- |
| **Error-based** | Un error de parser revela la consulta. |
| **Boolean blind** | La respuesta cambia según una condición. |
| **Time-based** | Un retardo condicionado funciona cuando no hay respuesta visible. |
| **Out-of-band** | El motor provoca una conexión a un dominio controlado si dispone de esa función. |

## 🔗 Cadenas y dependencias

SQLi con permisos de escritura podría alterar roles y provocar elevación; el alcance depende de privilegios de la cuenta de base de datos, no del payload.

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

Puede exponer o modificar datos; la prueba mínima debe limitarse a una fila propia o un marcador sin volcar tablas. La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

- Localizar un parámetro de búsqueda o ID y registrar una solicitud válida.
- Comparar el comportamiento con una variación inocua y otra de control en la construcción de SQL.
- Confirmar: Comparar respuestas para condición verdadera y falsa sobre datos de prueba; errores, retardos y tráfico OAST son señales distintas, no prueba automática de extracción.
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

Parametrizar consultas, evitar concatenación dinámica de identificadores y usar privilegios mínimos en la base. La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

La [guía de calidad de HackerOne](https://docs.hackerone.com/en/articles/8475116-quality-reports) enlaza el [informe #816254 de QIWI](https://hackerone.com/reports/816254), descrito como SQL injection con una cadena hacia ejecución remota. Esa consecuencia requiere permisos y pasos propios del caso; no se atribuye a cualquier SQLi.

## 📚 Fuentes

- [PortSwigger: SQL injection](https://portswigger.net/web-security/sql-injection) — variantes y confirmación.
- [PortSwigger: SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet) — sintaxis específica por motor.
- [OWASP Web Security Testing Guide](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/) — metodología de validación.
- [HackerOne: QIWI, informe 816254](https://hackerone.com/reports/816254) — reporte divulgado citado por HackerOne.

---

[← Índice general](../../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
