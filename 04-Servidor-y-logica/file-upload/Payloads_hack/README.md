# 🗡️ Vulnerabilidades de subida de archivos: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Tipo contradictorio

**Objetivo:** Verificar validación más allá de MIME.

```http
POST /api/upload HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: multipart/form-data; boundary=prueba

--prueba
Content-Disposition: form-data; name="file"; filename="marcador.txt"
Content-Type: image/png

prueba-123
--prueba--
```

**Interpretación:** Revisar almacenamiento y tipo servido; no inferir ejecución.

### 2. Nombre con doble extensión

**Objetivo:** Observar normalización del nombre propio.

```text
marcador.prueba.txt
```

**Interpretación:** Usar contenido inerte y comprobar nombre/ruta final.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
