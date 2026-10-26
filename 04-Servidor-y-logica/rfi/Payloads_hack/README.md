# 🗡️ Remote File Inclusion (RFI): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Recurso de texto propio

**Objetivo:** Comprobar inclusión sin código.

```http
GET /view?template=https%3A%2F%2F{CONTROLLED_HOST}%2Fmarcador.txt HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Distinguir fetch/SSRF de interpretación del contenido.

### 2. Control local

**Objetivo:** Verificar el comportamiento esperado.

```http
GET /view?template=plantilla-permitida HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar salida y error con la URL remota.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
