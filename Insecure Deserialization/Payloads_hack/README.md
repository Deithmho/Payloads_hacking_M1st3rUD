# 🗡️ Deserialización insegura: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Byte alterado en cookie serializada

**Objetivo:** Medir integridad antes de estudiar clases/gadgets.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: state={COOKIE_PROPIA_CON_UN_BYTE_ALTERADO}
```

**Interpretación:** La sesión debe rechazarse. Una excepción de parser solo identifica un formato posible; no implica ejecución.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/deserialization).

### 2. Objeto JSON frente a escalar

**Objetivo:** Verificar que el esquema rechace tipos inesperados.

```json
{"userId":{"valor":"{ID_PROPIO}"}}
```

**Interpretación:** Comparar con `{"userId":"{ID_PROPIO}"}`. Si ambos se aceptan, identificar qué propiedad usa la aplicación.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/deserialization).

### 3. Firma de Java serialization

**Objetivo:** Reconocer un stream Java sin ejecutarlo.

```bash
xxd -l 8 {ARCHIVO_PROPIO}  # buscar AC ED 00 05
```

**Interpretación:** El magic byte confirma formato, no deserialización insegura. Analizar clases permitidas en entorno de prueba.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization).

### 4. PHP serialize de dato inocuo

**Objetivo:** Distinguir valor escalar de objeto serializado en un laboratorio PHP.

```php
echo serialize(["marca" => "prueba-{NONCE}"]);
```

**Interpretación:** No sustituirlo en una sesión ajena. Un cambio de estado requiere observar uso del valor tras `unserialize`.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization).

### 5. Clase PHP de laboratorio con método mágico

**Objetivo:** Mostrar cuándo una acción ocurre al deserializar, sin gadget del producto.

```php
class Marca { public function __wakeup() { echo "prueba-{NONCE}"; } }
$s = serialize(new Marca());
unserialize($s);
```

**Interpretación:** Solo laboratorio propio: la salida demuestra `__wakeup` durante `unserialize`, no una vulnerabilidad en otro producto.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/deserialization/exploiting).

### 6. Pickle frente a JSON

**Objetivo:** Reconocer la necesidad de sustituir formatos de objetos por datos.

```python
import pickle, json
propio = {"marca":"prueba-{NONCE}"}
print(pickle.dumps(propio).hex()[:24]); print(json.dumps(propio))
```

**Interpretación:** No cargar pickles de terceros. `pickle.loads` puede ejecutar comportamiento de objetos arbitrarios.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization).

### 7. Token de sesión expirado

**Objetivo:** Separar fallo de expiración de manipulación de deserialización.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: state={BLOB_PROPIO_EXPIRADO}
```

**Interpretación:** Debe rechazarse. Si se acepta, documentar el control temporal independientemente de una posible gadget chain.

**Fuente técnica:** [documentación de la técnica](https://portswigger.net/web-security/deserialization).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
