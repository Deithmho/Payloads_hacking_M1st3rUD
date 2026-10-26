# 🗡️ Fallos de validación SAML: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Firma inválida

**Objetivo:** Comprobar que el servicio rechaza una aserción alterada.

```xml
<saml:Attribute Name="role"><saml:AttributeValue>prueba</saml:AttributeValue></saml:Attribute>
```

**Interpretación:** Modificar una respuesta propia sin actualizar firma debe invalidarla.

### 2. Replay controlado

**Objetivo:** Reenviar una respuesta usada de la cuenta de prueba.

```http
POST /saml/acs HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

SAMLResponse={RESPUESTA_PROPIA_YA_USADA}
```

**Interpretación:** La respuesta repetida debe rechazarse o quedar ligada a su transacción original.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
