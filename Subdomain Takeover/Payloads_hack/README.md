# 🗡️ Subdomain takeover: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Registros que pueden quedar colgantes

```bash
dig +short CNAME {SUBDOMINIO_AUTORIZADO}
dig +short A {SUBDOMINIO_AUTORIZADO}
dig +short AAAA {SUBDOMINIO_AUTORIZADO}
dig +short NS {SUBDOMINIO_AUTORIZADO}
```

**Cuándo usarlo:** Un registro colgante es candidato; reclamarlo depende de verificación y reglas del proveedor.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).


### Comprobación del destino CNAME

```bash
dig +short A {DESTINO_CNAME}
dig +short AAAA {DESTINO_CNAME}
dig +short TXT {SUBDOMINIO_AUTORIZADO}
```

**Cuándo usarlo:** NXDOMAIN o ausencia de TXT no prueban control por terceros; contrastar con documentación del proveedor.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).


## 🧭 Payloads por contexto

### Respuesta HTTP y TLS del host

```bash
curl -sS -D - -o /dev/null "https://{SUBDOMINIO_AUTORIZADO}/"
openssl s_client -connect {SUBDOMINIO_AUTORIZADO}:443 -servername {SUBDOMINIO_AUTORIZADO} </dev/null
```

**Cuándo usarlo:** Ejecutar una línea cada vez. Un error o certificado inválido solo identifica estado; no establece reclamabilidad.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).


## 🔥 Payloads avanzados

### Prueba inocua de control cuando esté permitida

```text
Recurso propio reservado: {RECURSO_CANARY}
Host: {SUBDOMINIO_AUTORIZADO}
Cuerpo publicado: takeover-proof-{NONCE}
Retirada: eliminar DNS huérfano o transferir el recurso al propietario.
```

**Cuándo usarlo:** La demostración requiere autorización explícita para asociar el subdominio; no dejarlo liberado al terminar.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/10-Test_for_Subdomain_Takeover/).


## 🔬 Pruebas guiadas por escenario

### 1. CNAME colgante

**Objetivo:** Identificar CNAME que apunta a un recurso retirado.

```bash
dig +short CNAME {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** Un CNAME sin recurso no prueba que un tercero pueda reclamarlo; validar requisitos del proveedor.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

### 2. Cadena de resolución

**Objetivo:** Comprobar si el destino CNAME todavía resuelve.

```bash
dig +short A {DESTINO_CNAME}
dig +short AAAA {DESTINO_CNAME}
```

**Interpretación:** NXDOMAIN puede ser candidato, pero hay servicios que impiden el alta sin prueba de dominio.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/10-Test_for_Subdomain_Takeover/).

### 3. Huella HTTP del proveedor

**Objetivo:** Confirmar página de error del servicio con Host en alcance.

```http
GET / HTTP/1.1
Host: {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** La huella puede ser genérica o estar cacheada; comprobar contra documentación actual del proveedor.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

### 4. Registros de verificación

**Objetivo:** Buscar TXT que impida el alta de un recurso por terceros.

```bash
dig +short TXT {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** La ausencia de TXT no prueba takeover; cada plataforma tiene un proceso de verificación diferente.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

### 5. Delegación NS

**Objetivo:** Verificar si una zona delegada tiene nameservers abandonados.

```bash
dig +short NS {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** Controlar una delegación puede tener mayor alcance; no registrar dominios ajenos para demostrarlo.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/10-Test_for_Subdomain_Takeover/).

### 6. Verificación de control con canary

**Objetivo:** Documentar control real solo si la política permite reclamar el recurso.

```text
Proveedor: {RECURSO_DE_PRUEBA_PROPIO}
Contenido servido: takeover-proof-{NONCE}
Host comprobado: {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** Servir solo un marcador inocuo. Coordinar la retirada del DNS o la reserva definitiva antes de liberar el recurso: dejar el CNAME colgante reabre el riesgo.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

### 7. Certificado y nombre

**Objetivo:** Registrar el comportamiento TLS actual del subdominio candidato.

```bash
openssl s_client -connect {SUBDOMINIO_AUTORIZADO}:443 -servername {SUBDOMINIO_AUTORIZADO} </dev/null
```

**Interpretación:** El certificado observado no demuestra si el proveedor permite asociar o reclamar el host. Confirmar los requisitos de alta por separado.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
