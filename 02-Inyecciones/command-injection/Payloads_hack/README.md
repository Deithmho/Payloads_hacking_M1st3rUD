# 🗡️ Inyección de comandos del sistema: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Separador inocuo

**Objetivo:** Buscar salida de un marcador sin cambiar estado.

```text
127.0.0.1; printf prueba-123
```

**Interpretación:** La cadena debe aparecer como salida del proceso y no como simple reflejo HTML.

### 2. Sustitución de comandos

**Objetivo:** Comprobar otra sintaxis de shell.

```text
127.0.0.1$(printf prueba-123)
```

**Interpretación:** Una diferencia repetible con control literal apoya la hipótesis; no prueba privilegios.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
