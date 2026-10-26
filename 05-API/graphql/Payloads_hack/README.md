# 🗡️ GraphQL: introspección, inyección y autorización: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Introspección mínima

**Objetivo:** Inventariar si el programa la permite.

```json
{"query":"{__schema{queryType{name}}}"}
```

**Interpretación:** Un esquema visible no equivale a hallazgo; buscar controles por campo.

### 2. Nodo controlado

**Objetivo:** Comparar autorización entre dos cuentas propias.

```json
{"query":"query($id:ID!){node(id:$id){id}}","variables":{"id":"{ID_CONTROLADO_B}"}}
```

**Interpretación:** Con sesión A, el nodo de B debe denegarse o filtrarse.

### 3. Argumento hacia sink

**Objetivo:** Comparar un marcador SQL literal contra una condición en un resolver de búsqueda propio.

```json
{"query":"query($q:String!){search(q:$q){id}}","variables":{"q":"prueba' AND '1'='1"}}
```

**Interpretación:** Solo si `search` existe y usa SQL; una respuesta diferente requiere controles verdadero/falso y puede ser validación normal.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
