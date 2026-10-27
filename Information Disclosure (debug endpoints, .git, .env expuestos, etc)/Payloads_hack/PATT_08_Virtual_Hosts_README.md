# Divulgación de información: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Virtual Hosts/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Virtual%20Hosts/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Virtual Host / Herramientas

```ps1
    prips 93.184.216.0/24 | hakoriginfinder -h https://example.com:443/foo
```

```ps1
    gobuster vhost -u https://example.com -w /path/to/wordlist.txt
```

## 2. Virtual Host / Metodología

```http
GET / HTTP/1.1
Host: example.com
```

```ps1
<VirtualHost *:80>
    ServerName site-a.com
    DocumentRoot /var/www/a
</VirtualHost>

<VirtualHost *:80>
    ServerName site-b.com
    DocumentRoot /var/www/b
</VirtualHost>
```

```http
GET / HTTP/1.1
Host: site-a.com
```

```http
GET / HTTP/1.1
Host: site-b.com
```

## 3. Metodología / Fingerprinting VHOSTs

```ps1
curl -H "Host: admin.example.com" http://10.10.10.10/
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
