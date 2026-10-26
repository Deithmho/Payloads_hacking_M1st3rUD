# 🗡️ Race condition: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Dos solicitudes controladas

**Objetivo:** Detectar doble aceptación en recurso de prueba.

```bash
printf "%s\n" 1 2 | xargs -P2 -I{} curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Authorization: Bearer {TOKEN_A}" "https://{ORIGEN}/api/test-owned/{ID_PROPIO}/redeem"
```

**Interpretación:** Registrar estado inicial/final; no usar cargas altas ni activos monetarios reales.

### 2. Control secuencial

**Objetivo:** Distinguir carrera de regla de negocio ordinaria.

```bash
for n in 1 2; do curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Authorization: Bearer {TOKEN_A}" "https://{ORIGEN}/api/test-owned/{OTRO_ID_PROPIO}/redeem"; done
```

**Interpretación:** Si el resultado paralelo difiere del secuencial de forma repetible, investigar atomicidad.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
