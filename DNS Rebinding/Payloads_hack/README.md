# 🗡️ DNS rebinding: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Dos respuestas A de laboratorio

**Objetivo:** Observar cambio de respuesta DNS en dominio propio.

```bash
dig +short A {DOMINIO_REBIND_PROPIO}
sleep 3
dig +short A {DOMINIO_REBIND_PROPIO}
```

**Interpretación:** El cambio confirma configuración del laboratorio, no una vulnerabilidad de la aplicación.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

### 2. TTL de prueba

**Objetivo:** Comprobar que las respuestas del dominio de laboratorio tienen vida corta.

```bash
dig {DOMINIO_REBIND_PROPIO} A +noall +answer
```

**Interpretación:** Los resolvers pueden imponer TTL mínimo; registrar el valor real antes de atribuir comportamiento.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

### 3. Primera conexión pública

**Objetivo:** Enviar una URL cuyo DNS inicial apunta a un servidor propio.

```json
{"url":"http://{DOMINIO_REBIND_PROPIO}:{PUERTO_LAB}/canary"}
```

**Interpretación:** La primera respuesta debe llegar a un canary propio. No dirigir la segunda a redes ajenas.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf).

### 4. Segunda conexión a IP de laboratorio

**Objetivo:** Comprobar revalidación de IP al resolver de nuevo.

```text
DNS 1: {DOMINIO_REBIND_PROPIO} -> {IP_PUBLICA_PROPIA}
DNS 2: {DOMINIO_REBIND_PROPIO} -> {IP_PRIVADA_LAB_PROPIA}
```

**Interpretación:** Solo en laboratorio propio; observar conexión real a la segunda IP y controles de red.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

### 5. Host HTTP conservado

**Objetivo:** Verificar que el cliente HTTP envía Host del nombre original.

```http
GET /canary HTTP/1.1
Host: {DOMINIO_REBIND_PROPIO}
```

**Interpretación:** El servidor del laboratorio debe registrar Host e IP local de destino; no confundirlo con DNS normal.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/ssrf).

### 6. Redirección y nueva resolución

**Objetivo:** Probar la política de destino en cada salto controlado.

```text
302 Location: http://{DOMINIO_REBIND_PROPIO}/segunda
A inicial: {IP_PUBLICA_PROPIA}
A posterior: {IP_PRIVADA_LAB_PROPIA}
```

**Interpretación:** Un validador robusto comprueba cada resolución y cada redirección. Usar dos hosts propios.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

### 7. Familias IPv4 e IPv6

**Objetivo:** Comprobar que el filtro resuelve y valida A y AAAA.

```bash
dig +short A {DOMINIO_REBIND_PROPIO}
dig +short AAAA {DOMINIO_REBIND_PROPIO}
```

**Interpretación:** Una familia no filtrada solo es relevante si la aplicación la conecta efectivamente.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
