# 🗡️ Web Cache Deception: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Sufijo estático

**Objetivo:** Probar con ruta propia y nombre único.

```http
GET /account/{ID_PROPIO}/prueba-123.css HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_PROPIA}
```

**Interpretación:** Repetir sin cookie y comparar contenido; no usar recursos ajenos.

### 2. Control anónimo

**Objetivo:** Descartar contenido público.

```http
GET /account/{ID_PROPIO}/prueba-123.css HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Solo hay fuga si aparecen datos privados de la cuenta de prueba.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
