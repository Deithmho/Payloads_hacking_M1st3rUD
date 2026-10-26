# 🗡️ Divulgación de información: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Archivo de configuración

**Objetivo:** Verificar exposición mínima sin imprimir valores.

```bash
curl -s -o /dev/null -w "%{http_code} %{size_download}\n" "https://{ORIGEN}/.env"
```

**Interpretación:** El 200 puede ser fallback SPA; inspeccionar solo lo imprescindible y redactar.

### 2. Metadatos Git

**Objetivo:** Distinguir archivo real de página genérica.

```bash
curl -i "https://{ORIGEN}/.git/HEAD"
```

**Interpretación:** Buscar formato `ref: refs/heads/...`; no clonar contenido fuera de alcance.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
