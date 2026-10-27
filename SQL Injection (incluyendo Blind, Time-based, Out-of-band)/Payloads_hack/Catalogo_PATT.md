# Banco ampliado: SQL injection

Este índice ordena los ejemplos técnicos reproducidos o adaptados de PayloadsAllTheThings por documento y situación. Los títulos explican el contexto en español y conservan los nombres técnicos de motores y funciones; el código mantiene la sintaxis de origen. Consulta primero [los payloads básicos y las pruebas guiadas](README.md).

**Versión de origen:** [3ac27901c711](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a) · [Licencia MIT y atribución](../../LICENCIA_PATT.md).

| Documento técnico | Apartados | Bloques de código | Variantes en línea |
| --- | ---: | ---: | ---: |
| [Inyección SQL](PATT_01_SQL_Injection_README.md) | 22 | 35 | 138 |
| [Inyección MySQL](PATT_02_SQL_Injection_MySQL_Injection.md) | 38 | 56 | 111 |
| [Inyección PostgreSQL](PATT_03_SQL_Injection_PostgreSQL_Injection.md) | 19 | 23 | 43 |
| [Inyección MSSQL](PATT_04_SQL_Injection_MSSQL_Injection.md) | 22 | 37 | 30 |
| [SQLite Inyección](PATT_05_SQL_Injection_SQLite_Injection.md) | 10 | 9 | 23 |
| [OracleSQL Inyección](PATT_06_SQL_Injection_OracleSQL_Injection.md) | 17 | 15 | 38 |
| [DB2 Inyección](PATT_07_SQL_Injection_DB2_Injection.md) | 9 | 5 | 38 |
| [BigQuery Inyección](PATT_08_SQL_Injection_BigQuery_Injection.md) | 5 | 2 | 10 |
| [Cassandra Inyección](PATT_09_SQL_Injection_Cassandra_Injection.md) | 4 | 4 | 7 |
| [SQLmap](PATT_10_SQL_Injection_SQLmap.md) | 17 | 28 | 18 |

## Diccionarios de payloads para Intruder y fuzzing

Cada archivo conserva sus líneas de origen y se debe usar con el punto de entrada y la profundidad adecuados. No ejecutar los diccionarios completos contra un programa sin comprobar sus límites de frecuencia y volumen.

| Lista | Líneas | Fuente |
| --- | ---: | --- |
| [SQL_Injection_Intruder_Auth_Bypass.txt](PATT_LISTA_SQL_Injection_Intruder_Auth_Bypass.txt) | 78 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/Auth_Bypass.txt) |
| [SQL_Injection_Intruder_Auth_Bypass2.txt](PATT_LISTA_SQL_Injection_Intruder_Auth_Bypass2.txt) | 121 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/Auth_Bypass2.txt) |
| [SQL_Injection_Intruder_FUZZDB_MSSQL-WHERE_Time.txt](PATT_LISTA_SQL_Injection_Intruder_FUZZDB_MSSQL-WHERE_Time.txt) | 40 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/FUZZDB_MSSQL-WHERE_Time.txt) |
| [SQL_Injection_Intruder_FUZZDB_MSSQL.txt](PATT_LISTA_SQL_Injection_Intruder_FUZZDB_MSSQL.txt) | 17 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/FUZZDB_MSSQL.txt) |
| [SQL_Injection_Intruder_FUZZDB_MSSQL_Enumeration.txt](PATT_LISTA_SQL_Injection_Intruder_FUZZDB_MSSQL_Enumeration.txt) | 15 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/FUZZDB_MSSQL_Enumeration.txt) |
| [SQL_Injection_Intruder_FUZZDB_MYSQL.txt](PATT_LISTA_SQL_Injection_Intruder_FUZZDB_MYSQL.txt) | 6 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/FUZZDB_MYSQL.txt) |
| [SQL_Injection_Intruder_FUZZDB_MySQL-WHERE_Time.txt](PATT_LISTA_SQL_Injection_Intruder_FUZZDB_MySQL-WHERE_Time.txt) | 45 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/FUZZDB_MySQL-WHERE_Time.txt) |
| [SQL_Injection_Intruder_FUZZDB_MySQL_ReadLocalFiles.txt](PATT_LISTA_SQL_Injection_Intruder_FUZZDB_MySQL_ReadLocalFiles.txt) | 3 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/FUZZDB_MySQL_ReadLocalFiles.txt) |
| [SQL_Injection_Intruder_FUZZDB_Oracle.txt](PATT_LISTA_SQL_Injection_Intruder_FUZZDB_Oracle.txt) | 56 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/FUZZDB_Oracle.txt) |
| [SQL_Injection_Intruder_FUZZDB_Postgres_Enumeration.txt](PATT_LISTA_SQL_Injection_Intruder_FUZZDB_Postgres_Enumeration.txt) | 20 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/FUZZDB_Postgres_Enumeration.txt) |
| [SQL_Injection_Intruder_Generic_ErrorBased.txt](PATT_LISTA_SQL_Injection_Intruder_Generic_ErrorBased.txt) | 154 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/Generic_ErrorBased.txt) |
| [SQL_Injection_Intruder_Generic_Fuzz.txt](PATT_LISTA_SQL_Injection_Intruder_Generic_Fuzz.txt) | 12 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/Generic_Fuzz.txt) |
| [SQL_Injection_Intruder_Generic_TimeBased.txt](PATT_LISTA_SQL_Injection_Intruder_Generic_TimeBased.txt) | 105 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/Generic_TimeBased.txt) |
| [SQL_Injection_Intruder_Generic_UnionSelect.txt](PATT_LISTA_SQL_Injection_Intruder_Generic_UnionSelect.txt) | 424 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/Generic_UnionSelect.txt) |
| [SQL_Injection_Intruder_SQLi_Polyglots.txt](PATT_LISTA_SQL_Injection_Intruder_SQLi_Polyglots.txt) | 2 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/SQL%20Injection/Intruder/SQLi_Polyglots.txt) |

---

[← Guía principal](README.md) · [← Índice general](../../README.md)
