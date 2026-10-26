# 🗡️ Configuración insegura de OAuth: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. URI no registrada

**Objetivo:** Verificar comparación exacta sin entregar código a terceros.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=https%3A%2F%2F{CONTROLLED_HOST}%2Fcallback&state=prueba-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El servidor debe rechazar una URI no registrada antes de emitir código.

### 2. State ausente

**Objetivo:** Comparar flujo legítimo con uno sin estado.

```http
GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI_REGISTRADA} HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El cliente debe rechazar respuestas sin vinculación de estado; no concluir por el comportamiento del proveedor solo.

### 3. PKCE ausente

**Objetivo:** Verificar que un cliente público exija challenge S256.

```http
GET /authorize?response_type=code&client_id={CLIENT_PUBLICO}&redirect_uri={REDIRECT_URI_REGISTRADA}&state=prueba-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El rechazo es lo esperado si PKCE es obligatorio; la aceptación de autorización no prueba que el código pueda canjearse.

### 4. Emisor alterno

**Objetivo:** Comparar metadatos y respuesta de dos proveedores configurados.

```text
Flujo A: iss={EMISOR_A}, state={STATE_A}
Flujo B: iss={EMISOR_B}, state={STATE_B}
No mezclar códigos reales entre cuentas ajenas.
```

**Interpretación:** El cliente debe ligar cada respuesta al emisor del flujo iniciado.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
