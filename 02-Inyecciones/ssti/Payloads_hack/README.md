# 🗡️ Server-Side Template Injection (SSTI): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Expresión aritmética

**Objetivo:** Detectar evaluación sin efectos.

```text
{{7*7}}
```

**Interpretación:** El resultado `49` debe contrastarse con reflejo literal y otras transformaciones.

### 2. Sintaxis alternativa

**Objetivo:** Distinguir motores antes de profundizar.

```text
${7*7}
```

**Interpretación:** Interpretar solo si la respuesta muestra cálculo atribuible al motor.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
