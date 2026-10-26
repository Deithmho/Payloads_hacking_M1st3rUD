# 🗡️ CORS con credenciales: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Cabeceras preliminares

**Objetivo:** Observar política para origen no confiable.

```bash
curl -i -H "Origin: https://{CONTROLLED_HOST}" -H "Cookie: session={COOKIE_PROPIA}" "https://{ORIGEN}/api/me"
```

**Interpretación:** Confirmar en navegador; curl no aplica reglas CORS ni SameSite.

### 2. Prueba navegador

**Objetivo:** Leer únicamente perfil propio desde origen controlado.

```js
fetch("https://{ORIGEN}/api/me", {credentials:"include"}).then(r=>r.text()).then(x=>console.log(x.length)).catch(console.error)
```

**Interpretación:** Usar navegador con sesión de prueba; registrar solo longitud o marcador, no datos privados.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
