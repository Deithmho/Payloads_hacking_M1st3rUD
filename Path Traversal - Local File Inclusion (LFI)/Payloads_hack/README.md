# 🗡️ Path Traversal y LFI: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Traversal relativo

**Objetivo:** Leer un marcador propio situado fuera del directorio servido.

```bash
curl --path-as-is "https://{ORIGEN}/download?file=../../marcador-{NONCE}.txt"
```

**Interpretación:** Solo confirma traversal si el contenido único del archivo aparece. `--path-as-is` evita normalización del cliente.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-path-traversal).

### 2. Separadores codificados

**Objetivo:** Comprobar si un decoder posterior crea `../`.

```text
..%2f..%2fmarcador-{NONCE}.txt
```

**Interpretación:** Comparar con el marcador literal y con URL de control; dependerá del orden de decodificación.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

### 3. Doble codificación

**Objetivo:** Detectar dos capas de URL decoding.

```text
..%252f..%252fmarcador-{NONCE}.txt
```

**Interpretación:** Solo funciona si una capa decodifica `%25` y otra `%2f`; no asumirlo por un 200.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-path-traversal).

### 4. Filtro no recursivo

**Objetivo:** Comprobar si eliminar `../` una vez deja un nuevo segmento.

```text
....//....//marcador-{NONCE}.txt
```

**Interpretación:** Debe leerse el canary externo; un error con ruta normalizada ayuda a entender el filtro.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

### 5. Ruta absoluta

**Objetivo:** Verificar si el prefijo base se ignora.

```text
/{RUTA_ABSOLUTA_CANARY_PROPIO}/marcador-{NONCE}.txt
```

**Interpretación:** Usar un archivo colocado por el tester en laboratorio; no solicitar `/etc/passwd`.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-path-traversal).

### 6. Windows con barra inversa

**Objetivo:** Probar normalización en un servidor Windows de laboratorio.

```text
..\..\marcador-{NONCE}.txt
```

**Interpretación:** En Linux puede ser literal; verificar tecnología antes de interpretar.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

### 7. Punto y coma en proxy Java

**Objetivo:** Comprobar parsing distinto entre proxy y contenedor.

```text
..;/..;/marcador-{NONCE}.txt
```

**Interpretación:** Requiere stack compatible; registrar ruta vista por frontend y backend si hay logs autorizados.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

### 8. Byte nulo histórico

**Objetivo:** Verificar solo en laboratorio legacy con archivo propio.

```text
../../marcador-{NONCE}.txt%00.jpg
```

**Interpretación:** La mayoría de stacks modernos rechaza `%00`; una respuesta 200 no prueba truncamiento.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/file-path-traversal).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
