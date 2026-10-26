# 🗡️ Subdomain takeover: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. CNAME colgante

**Objetivo:** Identificar CNAME que apunta a un recurso retirado.

```bash
dig +short CNAME {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** Un CNAME sin recurso no prueba que un tercero pueda reclamarlo; validar requisitos del proveedor.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

### 2. Cadena de resolución

**Objetivo:** Comprobar si el destino CNAME todavía resuelve.

```bash
dig +short A {DESTINO_CNAME}
dig +short AAAA {DESTINO_CNAME}
```

**Interpretación:** NXDOMAIN puede ser candidato, pero hay servicios que impiden el alta sin prueba de dominio.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/10-Test_for_Subdomain_Takeover/).

### 3. Huella HTTP del proveedor

**Objetivo:** Confirmar página de error del servicio con Host en alcance.

```http
GET / HTTP/1.1
Host: {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** La huella puede ser genérica o estar cacheada; comprobar contra documentación actual del proveedor.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

### 4. Registros de verificación

**Objetivo:** Buscar TXT que impida el alta de un recurso por terceros.

```bash
dig +short TXT {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** La ausencia de TXT no prueba takeover; cada plataforma tiene un proceso de verificación diferente.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

### 5. Delegación NS

**Objetivo:** Verificar si una zona delegada tiene nameservers abandonados.

```bash
dig +short NS {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** Controlar una delegación puede tener mayor alcance; no registrar dominios ajenos para demostrarlo.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/10-Test_for_Subdomain_Takeover/).

### 6. Verificación de control con canary

**Objetivo:** Documentar control real solo si la política permite reclamar el recurso.

```text
Proveedor: {RECURSO_DE_PRUEBA_PROPIO}
Contenido servido: takeover-proof-{NONCE}
Host comprobado: {SUBDOMINIO_AUTORIZADO}
```

**Interpretación:** Probar con página inocua, mantenerla privada y liberar/restaurar el recurso al terminar.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

### 7. Certificado y nombre

**Objetivo:** Comprobar si un servicio exige control del certificado para asociar el host.

```bash
openssl s_client -connect {SUBDOMINIO_AUTORIZADO}:443 -servername {SUBDOMINIO_AUTORIZADO} </dev/null
```

**Interpretación:** La falta de certificado válido puede bloquear el takeover en algunos proveedores; no es prueba suficiente sola.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
