# 🗡️ Exposición de API keys y secretos: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Inventario local sin valores

**Objetivo:** Buscar archivos candidatos sin imprimir secretos.

```bash
rg -l -i "(api[_-]?key|secret|token)" ./dist
```

**Interpretación:** Un match es candidato; clasificar antes de reportar.

### 2. Permiso mínimo

**Objetivo:** Usar endpoint de identidad inocuo si hay autorización.

```http
GET /api/whoami HTTP/1.1
Host: {PROVEEDOR_AUTORIZADO}
Authorization: Bearer {CLAVE_CANDIDATA}
```

**Interpretación:** No pegar ni almacenar la clave; detenerse tras confirmar identidad/scopes.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
