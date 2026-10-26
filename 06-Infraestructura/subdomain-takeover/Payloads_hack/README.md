# 🗡️ Subdomain takeover: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. DNS

**Objetivo:** Identificar destino exacto.

```bash
dig +short CNAME {SUBDOMINIO_EN_ALCANCE}
```

**Interpretación:** Correlacionar con configuración del proveedor; no asumir por CNAME solamente.

### 2. Respuesta del proveedor

**Objetivo:** Inspeccionar error sin crear recurso.

```bash
curl -i "https://{SUBDOMINIO_EN_ALCANCE}/"
```

**Interpretación:** Verificar reclamabilidad según documentación del proveedor y reglas del programa.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
