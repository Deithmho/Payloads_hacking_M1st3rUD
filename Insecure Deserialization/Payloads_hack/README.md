# 🗡️ Deserialización insegura: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Firmas de formato para reconocer entradas

```text
Java ObjectInputStream: AC ED 00 05
PHP serialize: O:4:"User":0:{}
Python pickle: 80 04 / 80 05 (según protocolo)
JSON con discriminador: {"@type":"...","value":"..."}
```

**Cuándo usarlo:** Son indicadores de formato, no confirmación de ejecución. Usar solo datos propios.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Deserialization/README.md).


### PHP: valores serializados inocuos

```php
echo serialize(["marca" => "canary-{NONCE}"]);
echo serialize((object)["marca" => "canary-{NONCE}"]);
```

**Cuándo usarlo:** Comparar aceptación de array y objeto en laboratorio; el segundo activa rutas de objeto al deserializar.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/deserialization).


## 🧭 Payloads por contexto

### JSON polimórfico por framework

```text
{"@class":"com.ejemplo.Marca","value":"canary-{NONCE}"}
{"@type":"com.ejemplo.Marca","value":"canary-{NONCE}"}
{"$type":"Ejemplo.Marca, Ensamblado","value":"canary-{NONCE}"}
```

**Cuándo usarlo:** Cada campo pertenece a un ecosistema distinto; usar solo si el binder admite tipos aportados por cliente.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Deserialization/README.md).


## 🔥 Payloads avanzados

### Métodos mágicos de PHP en sandbox

```php
class Marca {
  public function __wakeup() { echo "wake-{NONCE}"; }
  public function __destruct() { echo "destroy-{NONCE}"; }
}
$s = serialize(new Marca());
unserialize($s);
```

**Cuándo usarlo:** Demuestra el momento de ejecución de callbacks en un programa propio; no es una gadget chain de un producto.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/deserialization/exploiting).


## 🔬 Pruebas guiadas por escenario

### 1. Byte alterado en cookie serializada

**Objetivo:** Medir integridad antes de estudiar clases/gadgets.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: state={COOKIE_PROPIA_CON_UN_BYTE_ALTERADO}
```

**Interpretación:** La sesión debe rechazarse. Una excepción de parser solo identifica un formato posible; no implica ejecución.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/deserialization).

### 2. Objeto JSON frente a escalar

**Objetivo:** Verificar que el esquema rechace tipos inesperados.

```json
{"userId":{"valor":"{ID_PROPIO}"}}
```

**Interpretación:** Comparar con `{"userId":"{ID_PROPIO}"}`. Si ambos se aceptan, identificar qué propiedad usa la aplicación.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/deserialization).

### 3. Firma de Java serialization

**Objetivo:** Reconocer un stream Java sin ejecutarlo.

```bash
xxd -l 8 {ARCHIVO_PROPIO}  # buscar AC ED 00 05
```

**Interpretación:** El magic byte confirma formato, no deserialización insegura. Analizar clases permitidas en entorno de prueba.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization).

### 4. PHP serialize de dato inocuo

**Objetivo:** Distinguir valor escalar de objeto serializado en un laboratorio PHP.

```php
echo serialize(["marca" => "prueba-{NONCE}"]);
```

**Interpretación:** No sustituirlo en una sesión ajena. Un cambio de estado requiere observar uso del valor tras `unserialize`.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization).

### 5. Clase PHP de laboratorio con método mágico

**Objetivo:** Mostrar cuándo una acción ocurre al deserializar, sin gadget del producto.

```php
class Marca { public function __wakeup() { echo "prueba-{NONCE}"; } }
$s = serialize(new Marca());
unserialize($s);
```

**Interpretación:** Solo laboratorio propio: la salida demuestra `__wakeup` durante `unserialize`, no una vulnerabilidad en otro producto.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/deserialization/exploiting).

### 6. Pickle con canary inocuo

**Objetivo:** Mostrar en laboratorio que pickle.loads invoca el comportamiento de un objeto serializado.

```python
import pickle
class Marca:
    def __reduce__(self):
        return (print, ("CANARY-{NONCE}",))
blob = pickle.dumps(Marca())
pickle.loads(blob)
```

**Interpretación:** El print demuestra ejecución local durante la carga; no enviar blobs a servicios ajenos ni concluir vulnerabilidad sin entrada deserializada real.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization).

### 7. Propiedad booleana serializada

**Objetivo:** Solo si una cookie propia contiene un objeto PHP serializado sin protección, cambiar una propiedad booleana observada.

```text
Fragmento original: s:7:"isAdmin";b:0;
Variación de laboratorio: s:7:"isAdmin";b:1;
```

**Interpretación:** Se requiere el objeto real y mismo formato; confirmar cambio de privilegio efectivo. Si hay firma válida obligatoria, una modificación debe rechazarse.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/deserialization/exploiting).

### 8. Tipo polimórfico JSON

**Objetivo:** Probar si el backend acepta una marca de clase aportada por el cliente.

```json
{"@class":"com.ejemplo.dto.Marca","value":"prueba-{NONCE}"}
```

**Interpretación:** Solo si el framework usa polimorfismo de tipos; aceptar el JSON no demuestra carga de clase ni gadget.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization).

### 9. PHP __destruct inocuo

**Objetivo:** Mostrar la ejecución diferida de un método mágico al liberar un objeto.

```php
class Marca { public function __destruct() { echo "prueba-{NONCE}"; } }
$o = new Marca(); unset($o);
```

**Interpretación:** Laboratorio local. Sirve para razonar sobre cadenas de gadgets sin ejecutar comandos.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Deserialization).

### 10. YAML con tag explícito

**Objetivo:** Comprobar que un parser YAML rechaza tipos no permitidos.

```yaml
!!python/tuple ["prueba-{NONCE}", 1]
```

**Interpretación:** Solo en laboratorio Python; un parser seguro lo rechazará o tratará como datos.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/deserialization).

### 11. Firma HMAC alterada

**Objetivo:** Separar integridad del formato serializado.

```http
Cookie: state={BLOB_SERIALIZADO_PROPIO}.{FIRMA_HMAC_CON_UN_BYTE_CAMBIADO}
```

**Interpretación:** Rechazo confirma integridad de esa cookie; no concluye sobre otros formatos o endpoints.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/deserialization).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
