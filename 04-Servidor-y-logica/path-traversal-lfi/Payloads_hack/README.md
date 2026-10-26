# 🗡️ Path Traversal y LFI: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Traversal a canary

**Objetivo:** Buscar archivo propio fuera del directorio servido.

```http
GET /download?name=..%2F..%2Fmarcador-prueba.txt HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** El marcador debe ser único y colocado por el tester; un 200 genérico no cuenta.

### 2. Doble codificación

**Objetivo:** Identificar orden de decodificación.

```http
GET /download?name=..%252F..%252Fmarcador-prueba.txt HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar con control de ruta literal y normalización real.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
