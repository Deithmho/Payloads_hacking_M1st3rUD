# Subdomain Takeover: banco ampliado de verificación

> La condición decisiva es que el nombre DNS en alcance apunte a un recurso de tercero reclamable y que, en una prueba autorizada, el subdominio sirva un marcador propio. Un CNAME huérfano, una respuesta 404 o una firma de herramienta son indicios que requieren validación.

[← Payloads básicos](README.md) · [← Índice ampliado](Catalogo_PATT.md)

## Payloads básicos

### 1. CNAME y direcciones del subdominio

```bash
dig +short CNAME subdominio.example.test
dig +short A subdominio.example.test
dig +short AAAA subdominio.example.test
```

**Uso:** anota la cadena DNS y el proveedor final. Repite con el DNS autoritativo si hay respuestas discrepantes.

### 2. Cadena CNAME completa

```bash
dig CNAME subdominio.example.test
dig CNAME alias-del-proveedor.example.test
```

**Uso:** distingue un alias intermedio activo de un destino desasignado.

### 3. Respuesta HTTP del Host exacto

```bash
curl -sS -D - -o /dev/null 'https://subdominio.example.test/'
```

**Uso:** registra estado, redirección y cabeceras sin inferir reclamabilidad del código.

### 4. Control de wildcard DNS

```bash
dig +short CNAME prueba-aleatoria-001.example.test
dig +short CNAME prueba-aleatoria-002.example.test
```

**Uso:** si nombres inexistentes resuelven igual que el candidato, evalúa un wildcard antes de reportar cada nombre como hallazgo independiente.

## Payloads por contexto

### 5. Diferencia entre resolutores

```bash
dig @1.1.1.1 +short CNAME subdominio.example.test
dig @8.8.8.8 +short CNAME subdominio.example.test
```

**Uso:** ayuda a detectar caché DNS o cambios recientes; consulta también la zona autoritativa.

### 6. Delegación NS específica

```bash
dig +short NS subdominio.example.test
dig +trace subdominio.example.test
```

**Uso:** una delegación a servidores descontrolados es distinta del CNAME. Confirma titularidad y posibilidad real de controlar la zona.

### 7. Correo del subdominio

```bash
dig +short MX subdominio.example.test
dig +short TXT subdominio.example.test
```

**Uso:** documenta MX, SPF y verificaciones de proveedor sin enviar correo a terceros. No atribuyas captura de correo sin demostrar control autorizado.

### 8. Reclamación de recurso en una cuenta de laboratorio

```text
Nombre DNS en alcance: subdominio.example.test
Recurso anterior: {RECURSO_DESASIGNADO_DEL_PROVEEDOR}
Recurso propio: {RECURSO_EN_CUENTA_AUTORIZADA}
Contenido servido: takeover-proof-{NONCE}
```

**Uso:** sigue las reglas del programa y del proveedor. Publica solo un marcador inocuo y retíralo al terminar.

### 9. Confirmación del contenido servido

```bash
curl -sS 'https://subdominio.example.test/' | rg 'takeover-proof-{NONCE}'
```

**Uso:** el marcador debe aparecer bajo el Host exacto en alcance. Una página propia accesible solo por la URL del proveedor no demuestra control del subdominio.

## Payloads avanzados y cadenas

### 10. Alcance de cookie de prueba

```http
Set-Cookie: sesion_de_prueba={VALOR_REDACTADO}; Domain=.example.test; Path=/; Secure; HttpOnly
```

**Uso:** verifica solo con una cuenta propia si una cookie de dominio amplio llegaría al subdominio; no guardes valores completos de sesión.

### 11. Confianza CORS hacia el subdominio

```http
GET /api/test-profile HTTP/1.1
Host: app.example.test
Origin: https://subdominio.example.test
Cookie: sesion_de_prueba={VALOR_PROPIO}
```

**Uso:** busca una respuesta con `Access-Control-Allow-Origin` que autorice ese origen y confirma en navegador, con datos propios, si puede leerla.

### 12. Redirect URI de una aplicación OAuth propia

```text
redirect_uri=https://subdominio.example.test/oauth/callback
```

**Uso:** revisa un cliente OAuth de prueba y valida coincidencia exacta; no solicites tokens ajenos.

### 13. Confianza CSP

```http
Content-Security-Policy: script-src 'self' https://subdominio.example.test
```

**Uso:** la cadena requiere que una página en alcance cargue scripts desde el subdominio y que se haya demostrado control efectivo.

### 14. Limpieza y verificación final

```text
1. Guardar DNS, respuesta HTTP con marcador y hora.
2. Quitar el marcador y desvincular el recurso de prueba según el acuerdo.
3. Verificar que el Host ya no sirve contenido controlado.
4. Reportar la condición DNS y las cadenas solo si cada paso se comprobó.
```

## Fuentes

- [HackTricks — Toma de control de dominio y subdominio](https://book.hacktricks.wiki/es/pentesting-web/domain-subdomain-takeover.html).
- [Can I Take Over XYZ — firmas y condiciones por proveedor](https://github.com/EdOverflow/can-i-take-over-xyz).

---

[← Payloads básicos](README.md) · [← Índice ampliado](Catalogo_PATT.md)
