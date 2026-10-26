# 🛡️ Payloads Hacking M1st3rUD

**Manual de campo en español para pentesting web, APIs y bug bounty autorizado.** Cada tema separa el mecanismo, contexto, variantes, evidencia y corrección de los ejemplos técnicos listos para adaptar. El catálogo contiene **61 temas**, incluyendo las categorías solapadas solicitadas: una misma raíz técnica puede tener guías de aplicación distintas.

> **Uso ético:** emplear solo en laboratorios, activos propios o programas con autorización y alcance vigentes. Respetar límites de frecuencia, datos, concurrencia y divulgación. Los ejemplos son pruebas mínimas; un resultado llamativo no equivale a una vulnerabilidad validada.

## 🧭 Cómo usar este repositorio

1. Abrir `Descripcion/README.md` para entender el límite de confianza y la señal de confirmación.
2. Elegir una prueba de `Payloads_hack/README.md`, reemplazar marcadores y ejecutar un único cambio por vez.
3. Comparar con un control negativo y registrar la evidencia mínima; detenerse antes de afectar datos ajenos.
4. Calcular severidad a partir del impacto comprobado, no del nombre de la técnica.

Los directorios de cada tema contienen **exactamente dos subcarpetas**, en este orden editorial: `Descripcion/` y `Payloads_hack/`.

## 🔐 Autenticación, sesión y autorización

1. [Autenticación rota](01-Autenticacion-y-sesion/autenticacion-rota/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/autenticacion-rota/Payloads_hack/README.md)
2. [Ataques contra JWT](01-Autenticacion-y-sesion/jwt/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/jwt/Payloads_hack/README.md)
3. [Configuración insegura de OAuth](01-Autenticacion-y-sesion/oauth/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/oauth/Payloads_hack/README.md)
4. [Fallos de validación SAML](01-Autenticacion-y-sesion/saml/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/saml/Payloads_hack/README.md)
5. [Fijación de sesión](01-Autenticacion-y-sesion/fijacion-sesion/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/fijacion-sesion/Payloads_hack/README.md)
6. [Envenenamiento del enlace de recuperación](01-Autenticacion-y-sesion/reset-password-poisoning/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/reset-password-poisoning/Payloads_hack/README.md)
7. [Bypass de MFA](01-Autenticacion-y-sesion/mfa-bypass/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/mfa-bypass/Payloads_hack/README.md)
8. [IDOR](01-Autenticacion-y-sesion/idor/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/idor/Payloads_hack/README.md)
9. [Control de acceso roto y elevación de privilegios](01-Autenticacion-y-sesion/control-acceso/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/control-acceso/Payloads_hack/README.md)
10. [Mass assignment](01-Autenticacion-y-sesion/mass-assignment/Descripcion/README.md) · [payloads](01-Autenticacion-y-sesion/mass-assignment/Payloads_hack/README.md)

## 💉 Inyecciones

1. [SQL injection](02-Inyecciones/sql-injection/Descripcion/README.md) · [payloads](02-Inyecciones/sql-injection/Payloads_hack/README.md)
2. [NoSQL injection](02-Inyecciones/nosql-injection/Descripcion/README.md) · [payloads](02-Inyecciones/nosql-injection/Payloads_hack/README.md)
3. [Inyección de comandos del sistema](02-Inyecciones/command-injection/Descripcion/README.md) · [payloads](02-Inyecciones/command-injection/Payloads_hack/README.md)
4. [XML External Entity (XXE)](02-Inyecciones/xxe/Descripcion/README.md) · [payloads](02-Inyecciones/xxe/Payloads_hack/README.md)
5. [Server-Side Template Injection (SSTI)](02-Inyecciones/ssti/Descripcion/README.md) · [payloads](02-Inyecciones/ssti/Payloads_hack/README.md)
6. [LDAP injection](02-Inyecciones/ldap-injection/Descripcion/README.md) · [payloads](02-Inyecciones/ldap-injection/Payloads_hack/README.md)
7. [CRLF injection](02-Inyecciones/crlf-injection/Descripcion/README.md) · [payloads](02-Inyecciones/crlf-injection/Payloads_hack/README.md)
8. [Header injection](02-Inyecciones/header-injection/Descripcion/README.md) · [payloads](02-Inyecciones/header-injection/Payloads_hack/README.md)
9. [Host header injection](02-Inyecciones/host-header-injection/Descripcion/README.md) · [payloads](02-Inyecciones/host-header-injection/Payloads_hack/README.md)
10. [Email header injection](02-Inyecciones/email-header-injection/Descripcion/README.md) · [payloads](02-Inyecciones/email-header-injection/Payloads_hack/README.md)
11. [XPath injection](02-Inyecciones/xpath-injection/Descripcion/README.md) · [payloads](02-Inyecciones/xpath-injection/Payloads_hack/README.md)
12. [Code injection / eval](02-Inyecciones/code-injection/Descripcion/README.md) · [payloads](02-Inyecciones/code-injection/Payloads_hack/README.md)

## 🧭 Cliente y navegador

1. [Cross-Site Scripting (XSS)](03-Cliente/xss/Descripcion/README.md) · [payloads](03-Cliente/xss/Payloads_hack/README.md)
2. [Cross-Site Request Forgery (CSRF)](03-Cliente/csrf/Descripcion/README.md) · [payloads](03-Cliente/csrf/Payloads_hack/README.md)
3. [Clickjacking](03-Cliente/clickjacking/Descripcion/README.md) · [payloads](03-Cliente/clickjacking/Payloads_hack/README.md)
4. [CORS mal configurado](03-Cliente/cors/Descripcion/README.md) · [payloads](03-Cliente/cors/Payloads_hack/README.md)
5. [Prototype pollution](03-Cliente/prototype-pollution/Descripcion/README.md) · [payloads](03-Cliente/prototype-pollution/Payloads_hack/README.md)
6. [Open redirect](03-Cliente/open-redirect/Descripcion/README.md) · [payloads](03-Cliente/open-redirect/Payloads_hack/README.md)
7. [Cross-Site WebSocket Hijacking](03-Cliente/websocket-hijacking/Descripcion/README.md) · [payloads](03-Cliente/websocket-hijacking/Payloads_hack/README.md)
8. [Vulnerabilidades de postMessage](03-Cliente/postmessage/Descripcion/README.md) · [payloads](03-Cliente/postmessage/Payloads_hack/README.md)
9. [DOM clobbering](03-Cliente/dom-clobbering/Descripcion/README.md) · [payloads](03-Cliente/dom-clobbering/Payloads_hack/README.md)

## 🧱 Servidor, peticiones y lógica

1. [Server-Side Request Forgery (SSRF)](04-Servidor-y-logica/ssrf/Descripcion/README.md) · [payloads](04-Servidor-y-logica/ssrf/Payloads_hack/README.md)
2. [Deserialización insegura](04-Servidor-y-logica/deserializacion/Descripcion/README.md) · [payloads](04-Servidor-y-logica/deserializacion/Payloads_hack/README.md)
3. [Race condition](04-Servidor-y-logica/race-condition/Descripcion/README.md) · [payloads](04-Servidor-y-logica/race-condition/Payloads_hack/README.md)
4. [Fallos de lógica de negocio](04-Servidor-y-logica/business-logic/Descripcion/README.md) · [payloads](04-Servidor-y-logica/business-logic/Payloads_hack/README.md)
5. [Bypass de rate limit](04-Servidor-y-logica/rate-limit-bypass/Descripcion/README.md) · [payloads](04-Servidor-y-logica/rate-limit-bypass/Payloads_hack/README.md)
6. [Path Traversal y LFI](04-Servidor-y-logica/path-traversal-lfi/Descripcion/README.md) · [payloads](04-Servidor-y-logica/path-traversal-lfi/Payloads_hack/README.md)
7. [Remote File Inclusion (RFI)](04-Servidor-y-logica/rfi/Descripcion/README.md) · [payloads](04-Servidor-y-logica/rfi/Payloads_hack/README.md)
8. [Vulnerabilidades de subida de archivos](04-Servidor-y-logica/file-upload/Descripcion/README.md) · [payloads](04-Servidor-y-logica/file-upload/Payloads_hack/README.md)
9. [HTTP Request Smuggling](04-Servidor-y-logica/request-smuggling/Descripcion/README.md) · [payloads](04-Servidor-y-logica/request-smuggling/Payloads_hack/README.md)
10. [HTTP Parameter Pollution](04-Servidor-y-logica/http-parameter-pollution/Descripcion/README.md) · [payloads](04-Servidor-y-logica/http-parameter-pollution/Payloads_hack/README.md)
11. [Web cache poisoning](04-Servidor-y-logica/web-cache-poisoning/Descripcion/README.md) · [payloads](04-Servidor-y-logica/web-cache-poisoning/Payloads_hack/README.md)
12. [Web Cache Deception](04-Servidor-y-logica/web-cache-deception/Descripcion/README.md) · [payloads](04-Servidor-y-logica/web-cache-deception/Payloads_hack/README.md)

## 🔌 API y GraphQL

1. [GraphQL: introspección, inyección y autorización](05-API/graphql/Descripcion/README.md) · [payloads](05-API/graphql/Payloads_hack/README.md)
2. [Exposición de API keys y secretos](05-API/api-key-leakage/Descripcion/README.md) · [payloads](05-API/api-key-leakage/Payloads_hack/README.md)
3. [BOLA: autorización rota por objeto](05-API/bola/Descripcion/README.md) · [payloads](05-API/bola/Payloads_hack/README.md)
4. [BFLA: autorización rota por función](05-API/bfla/Descripcion/README.md) · [payloads](05-API/bfla/Payloads_hack/README.md)
5. [Exposición excesiva de datos en API](05-API/excessive-data-exposure/Descripcion/README.md) · [payloads](05-API/excessive-data-exposure/Payloads_hack/README.md)
6. [Límites insuficientes de recursos en API](05-API/resource-limits/Descripcion/README.md) · [payloads](05-API/resource-limits/Payloads_hack/README.md)
7. [Mass assignment en APIs](05-API/api-mass-assignment/Descripcion/README.md) · [payloads](05-API/api-mass-assignment/Payloads_hack/README.md)
8. [SSRF mediante webhooks](05-API/webhook-ssrf/Descripcion/README.md) · [payloads](05-API/webhook-ssrf/Payloads_hack/README.md)
9. [Prompt injection en funciones web con LLM](05-API/web-llm-prompt-injection/Descripcion/README.md) · [payloads](05-API/web-llm-prompt-injection/Payloads_hack/README.md)

## 🌐 Infraestructura y misceláneos

1. [Subdomain takeover](06-Infraestructura/subdomain-takeover/Descripcion/README.md) · [payloads](06-Infraestructura/subdomain-takeover/Payloads_hack/README.md)
2. [DNS rebinding](06-Infraestructura/dns-rebinding/Descripcion/README.md) · [payloads](06-Infraestructura/dns-rebinding/Payloads_hack/README.md)
3. [Tabnabbing y engaño de pestañas](06-Infraestructura/tabnabbing/Descripcion/README.md) · [payloads](06-Infraestructura/tabnabbing/Payloads_hack/README.md)
4. [Divulgación de información](06-Infraestructura/information-disclosure/Descripcion/README.md) · [payloads](06-Infraestructura/information-disclosure/Payloads_hack/README.md)
5. [Configuración de seguridad incorrecta](06-Infraestructura/security-misconfiguration/Descripcion/README.md) · [payloads](06-Infraestructura/security-misconfiguration/Payloads_hack/README.md)
6. [SSRF hacia metadatos cloud](06-Infraestructura/cloud-metadata-ssrf/Descripcion/README.md) · [payloads](06-Infraestructura/cloud-metadata-ssrf/Payloads_hack/README.md)
7. [Zip Slip](06-Infraestructura/zip-slip/Descripcion/README.md) · [payloads](06-Infraestructura/zip-slip/Payloads_hack/README.md)
8. [CORS con credenciales](06-Infraestructura/cors-credenciales/Descripcion/README.md) · [payloads](06-Infraestructura/cors-credenciales/Payloads_hack/README.md)
9. [Clickjacking y framing](06-Infraestructura/clickjacking-framing/Descripcion/README.md) · [payloads](06-Infraestructura/clickjacking-framing/Payloads_hack/README.md)

## 📚 Referencias y criterio editorial

- [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/), [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) y [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) aportan taxonomía y metodología.
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics) aporta mecanismos y laboratorios reproducibles.
- [HackTricks](https://book.hacktricks.wiki/) y [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) inspiran la navegación operativa. El texto de este proyecto es original y las técnicas se contrastan con referencias enlazadas en cada guía.
- [YesWeHack, análisis de confusión sintáctica](https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits) y [PortSwigger Research](https://portswigger.net/research/) se usan como ejemplos de investigación pública. [Fuentes y criterios](FUENTES.md) explica la diferencia entre una investigación pública, un laboratorio y un relato secundario.

## 🧾 Contribuciones y calidad

Las mejoras deben mantener la estructura, explicar precondiciones, incluir una prueba de control, enlazar fuentes y evitar datos de terceros. [Guía de contribución](CONTRIBUIR.md).

---

**Créditos:** OWASP, PortSwigger, HackTricks, PayloadsAllTheThings y autores de investigaciones públicas citadas. Los enlaces se ofrecen como fuentes, no como reproducción de sus textos.
