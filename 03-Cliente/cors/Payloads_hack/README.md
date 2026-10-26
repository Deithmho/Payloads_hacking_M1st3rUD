# 🗡️ CORS mal configurado: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Origen arbitrario

**Objetivo:** Comparar cabeceras para origen no confiable.

```bash
curl -i -H "Origin: https://{CONTROLLED_HOST}" "https://{ORIGEN}/api/me"
```

**Interpretación:** Revisar ACAO, ACAC y contenido, luego confirmar en navegador.

### 2. Origen null

**Objetivo:** Comprobar aceptación de origen opaco.

```bash
curl -i -H "Origin: null" "https://{ORIGEN}/api/me"
```

**Interpretación:** `ACAO: null` solo es relevante si el navegador puede enviar sesión y leer datos.

### 3. Sufijo de subdominio

**Objetivo:** Comprobar coincidencia de host mal anclada.

```bash
curl -i -H "Origin: https://{DOMINIO_CON_SUFÍJO_PARECIDO_CONTROLADO}" "https://{ORIGEN}/api/me"
```

**Interpretación:** Usar un dominio propio parecido al permitido; verificar ACAO exacto y `Vary: Origin`.

### 4. Lectura con credenciales

**Objetivo:** Confirmar en navegador con cuenta propia.

```js
fetch("https://{ORIGEN}/api/me", {credentials:"include"}).then(r=>r.text()).then(x=>console.log(x.length)).catch(console.error)
```

**Interpretación:** Una lectura exitosa desde origen no confiable con cookie y dato privado confirma la cadena; registrar marcador, no contenido.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
