# 🛡️ Payloads Hacking M1st3rUD

**Manual de campo en español para pentesting web, APIs y bug bounty autorizado.** Cada tema separa el mecanismo, contexto, variantes, evidencia y corrección de los ejemplos técnicos listos para adaptar. El catálogo contiene **61 temas, 312 bloques de payloads y 669 escenarios de prueba**, incluyendo las categorías solapadas solicitadas: una misma raíz técnica puede tener guías de aplicación distintas.

> **Uso ético:** emplear solo en laboratorios, activos propios o programas con autorización y alcance vigentes. Respetar límites de frecuencia, datos, concurrencia y divulgación. Los ejemplos son pruebas mínimas; un resultado llamativo no equivale a una vulnerabilidad validada.

## 📊 Cobertura

| Área | Temas | Bancos | Escenarios |
| --- | ---: | ---: | ---: |
| 🔐 Autenticación y sesión | 10 | 58 | 135 |
| 💉 Inyecciones | 12 | 75 | 144 |
| 🧭 Client-Side | 9 | 50 | 111 |
| 🧱 Server-Side Request y lógica | 12 | 53 | 117 |
| 🔌 API específicas | 9 | 37 | 94 |
| 🌐 Infraestructura y misceláneos | 9 | 39 | 68 |

## 🧭 Cómo usar este repositorio

1. Abrir `Descripcion/README.md` para entender el límite de confianza y la señal de confirmación.
2. En `Payloads_hack/README.md`, empezar por **Payloads básicos**, elegir una variante por contexto y consultar las pruebas guiadas para interpretar el resultado.
3. Comparar con un control negativo y registrar la evidencia mínima; detenerse antes de afectar datos ajenos.
4. Calcular severidad a partir del impacto comprobado, no del nombre de la técnica.

Cada vulnerabilidad tiene su carpeta en la raíz, con el nombre de la lista solicitada y **exactamente dos subcarpetas**: `Descripcion/` y `Payloads_hack/`. En nombres que contenían `/`, se usa ` - ` porque la barra separa directorios en Git.

## 🔐 Autenticación y sesión

1. [Broken Authentication](Broken%20Authentication/Descripcion/README.md) · [payloads](Broken%20Authentication/Payloads_hack/README.md)
2. [JWT Attacks (alg none, kid injection, weak secret, JWK injection)](JWT%20Attacks%20%28alg%20none%2C%20kid%20injection%2C%20weak%20secret%2C%20JWK%20injection%29/Descripcion/README.md) · [payloads](JWT%20Attacks%20%28alg%20none%2C%20kid%20injection%2C%20weak%20secret%2C%20JWK%20injection%29/Payloads_hack/README.md)
3. [OAuth Misconfiguration](OAuth%20Misconfiguration/Descripcion/README.md) · [payloads](OAuth%20Misconfiguration/Payloads_hack/README.md)
4. [SAML Injection](SAML%20Injection/Descripcion/README.md) · [payloads](SAML%20Injection/Payloads_hack/README.md)
5. [Session Fixation](Session%20Fixation/Descripcion/README.md) · [payloads](Session%20Fixation/Payloads_hack/README.md)
6. [Password Reset Poisoning](Password%20Reset%20Poisoning/Descripcion/README.md) · [payloads](Password%20Reset%20Poisoning/Payloads_hack/README.md)
7. [2FA - MFA Bypass](2FA%20-%20MFA%20Bypass/Descripcion/README.md) · [payloads](2FA%20-%20MFA%20Bypass/Payloads_hack/README.md)
8. [Insecure Direct Object Reference (IDOR)](Insecure%20Direct%20Object%20Reference%20%28IDOR%29/Descripcion/README.md) · [payloads](Insecure%20Direct%20Object%20Reference%20%28IDOR%29/Payloads_hack/README.md)
9. [Broken Access Control - Privilege Escalation](Broken%20Access%20Control%20-%20Privilege%20Escalation/Descripcion/README.md) · [payloads](Broken%20Access%20Control%20-%20Privilege%20Escalation/Payloads_hack/README.md)
10. [Mass Assignment](Mass%20Assignment/Descripcion/README.md) · [payloads](Mass%20Assignment/Payloads_hack/README.md)

## 💉 Inyecciones

1. [SQL Injection (incluyendo Blind, Time-based, Out-of-band)](SQL%20Injection%20%28incluyendo%20Blind%2C%20Time-based%2C%20Out-of-band%29/Descripcion/README.md) · [payloads](SQL%20Injection%20%28incluyendo%20Blind%2C%20Time-based%2C%20Out-of-band%29/Payloads_hack/README.md)
2. [NoSQL Injection](NoSQL%20Injection/Descripcion/README.md) · [payloads](NoSQL%20Injection/Payloads_hack/README.md)
3. [Command Injection - OS Command Injection](Command%20Injection%20-%20OS%20Command%20Injection/Descripcion/README.md) · [payloads](Command%20Injection%20-%20OS%20Command%20Injection/Payloads_hack/README.md)
4. [XXE (XML External Entity)](XXE%20%28XML%20External%20Entity%29/Descripcion/README.md) · [payloads](XXE%20%28XML%20External%20Entity%29/Payloads_hack/README.md)
5. [SSTI (Server-Side Template Injection)](SSTI%20%28Server-Side%20Template%20Injection%29/Descripcion/README.md) · [payloads](SSTI%20%28Server-Side%20Template%20Injection%29/Payloads_hack/README.md)
6. [LDAP Injection](LDAP%20Injection/Descripcion/README.md) · [payloads](LDAP%20Injection/Payloads_hack/README.md)
7. [CRLF Injection](CRLF%20Injection/Descripcion/README.md) · [payloads](CRLF%20Injection/Payloads_hack/README.md)
8. [Header Injection](Header%20Injection/Descripcion/README.md) · [payloads](Header%20Injection/Payloads_hack/README.md)
9. [Host Header Injection](Host%20Header%20Injection/Descripcion/README.md) · [payloads](Host%20Header%20Injection/Payloads_hack/README.md)
10. [Email Header Injection](Email%20Header%20Injection/Descripcion/README.md) · [payloads](Email%20Header%20Injection/Payloads_hack/README.md)
11. [XPath Injection](XPath%20Injection/Descripcion/README.md) · [payloads](XPath%20Injection/Payloads_hack/README.md)
12. [Code Injection (Eval - RCE)](Code%20Injection%20%28Eval%20-%20RCE%29/Descripcion/README.md) · [payloads](Code%20Injection%20%28Eval%20-%20RCE%29/Payloads_hack/README.md)

## 🧭 Client-Side

1. [XSS (Reflected, Stored, DOM-based)](XSS%20%28Reflected%2C%20Stored%2C%20DOM-based%29/Descripcion/README.md) · [payloads](XSS%20%28Reflected%2C%20Stored%2C%20DOM-based%29/Payloads_hack/README.md)
2. [CSRF](CSRF/Descripcion/README.md) · [payloads](CSRF/Payloads_hack/README.md)
3. [Clickjacking](Clickjacking/Descripcion/README.md) · [payloads](Clickjacking/Payloads_hack/README.md)
4. [CORS Misconfiguration](CORS%20Misconfiguration/Descripcion/README.md) · [payloads](CORS%20Misconfiguration/Payloads_hack/README.md)
5. [Prototype Pollution](Prototype%20Pollution/Descripcion/README.md) · [payloads](Prototype%20Pollution/Payloads_hack/README.md)
6. [Open Redirect](Open%20Redirect/Descripcion/README.md) · [payloads](Open%20Redirect/Payloads_hack/README.md)
7. [WebSocket Hijacking](WebSocket%20Hijacking/Descripcion/README.md) · [payloads](WebSocket%20Hijacking/Payloads_hack/README.md)
8. [PostMessage Vulnerabilities](PostMessage%20Vulnerabilities/Descripcion/README.md) · [payloads](PostMessage%20Vulnerabilities/Payloads_hack/README.md)
9. [DOM Clobbering](DOM%20Clobbering/Descripcion/README.md) · [payloads](DOM%20Clobbering/Payloads_hack/README.md)

## 🧱 Server-Side Request y lógica

1. [SSRF (Server-Side Request Forgery)](SSRF%20%28Server-Side%20Request%20Forgery%29/Descripcion/README.md) · [payloads](SSRF%20%28Server-Side%20Request%20Forgery%29/Payloads_hack/README.md)
2. [Insecure Deserialization](Insecure%20Deserialization/Descripcion/README.md) · [payloads](Insecure%20Deserialization/Payloads_hack/README.md)
3. [Race Condition](Race%20Condition/Descripcion/README.md) · [payloads](Race%20Condition/Payloads_hack/README.md)
4. [Business Logic Flaws](Business%20Logic%20Flaws/Descripcion/README.md) · [payloads](Business%20Logic%20Flaws/Payloads_hack/README.md)
5. [Rate Limit Bypass](Rate%20Limit%20Bypass/Descripcion/README.md) · [payloads](Rate%20Limit%20Bypass/Payloads_hack/README.md)
6. [Path Traversal - Local File Inclusion (LFI)](Path%20Traversal%20-%20Local%20File%20Inclusion%20%28LFI%29/Descripcion/README.md) · [payloads](Path%20Traversal%20-%20Local%20File%20Inclusion%20%28LFI%29/Payloads_hack/README.md)
7. [Remote File Inclusion (RFI)](Remote%20File%20Inclusion%20%28RFI%29/Descripcion/README.md) · [payloads](Remote%20File%20Inclusion%20%28RFI%29/Payloads_hack/README.md)
8. [File Upload Vulnerabilities](File%20Upload%20Vulnerabilities/Descripcion/README.md) · [payloads](File%20Upload%20Vulnerabilities/Payloads_hack/README.md)
9. [Request Smuggling (HTTP Request Smuggling)](Request%20Smuggling%20%28HTTP%20Request%20Smuggling%29/Descripcion/README.md) · [payloads](Request%20Smuggling%20%28HTTP%20Request%20Smuggling%29/Payloads_hack/README.md)
10. [HTTP Parameter Pollution](HTTP%20Parameter%20Pollution/Descripcion/README.md) · [payloads](HTTP%20Parameter%20Pollution/Payloads_hack/README.md)
11. [Cache Poisoning](Cache%20Poisoning/Descripcion/README.md) · [payloads](Cache%20Poisoning/Payloads_hack/README.md)
12. [Web Cache Deception](Web%20Cache%20Deception/Descripcion/README.md) · [payloads](Web%20Cache%20Deception/Payloads_hack/README.md)

## 🔌 API específicas

1. [GraphQL Injection - Introspection Abuse](GraphQL%20Injection%20-%20Introspection%20Abuse/Descripcion/README.md) · [payloads](GraphQL%20Injection%20-%20Introspection%20Abuse/Payloads_hack/README.md)
2. [API Key Leakage - Exposed Secrets](API%20Key%20Leakage%20-%20Exposed%20Secrets/Descripcion/README.md) · [payloads](API%20Key%20Leakage%20-%20Exposed%20Secrets/Payloads_hack/README.md)
3. [Broken Object Level Authorization (BOLA)](Broken%20Object%20Level%20Authorization%20%28BOLA%29/Descripcion/README.md) · [payloads](Broken%20Object%20Level%20Authorization%20%28BOLA%29/Payloads_hack/README.md)
4. [Broken Function Level Authorization (BFLA)](Broken%20Function%20Level%20Authorization%20%28BFLA%29/Descripcion/README.md) · [payloads](Broken%20Function%20Level%20Authorization%20%28BFLA%29/Payloads_hack/README.md)
5. [Excessive Data Exposure](Excessive%20Data%20Exposure/Descripcion/README.md) · [payloads](Excessive%20Data%20Exposure/Payloads_hack/README.md)
6. [Lack of Resources & Rate Limiting (API)](Lack%20of%20Resources%20%26%20Rate%20Limiting%20%28API%29/Descripcion/README.md) · [payloads](Lack%20of%20Resources%20%26%20Rate%20Limiting%20%28API%29/Payloads_hack/README.md)
7. [Mass Assignment en APIs](Mass%20Assignment%20en%20APIs/Descripcion/README.md) · [payloads](Mass%20Assignment%20en%20APIs/Payloads_hack/README.md)
8. [SSRF vía Webhooks](SSRF%20v%C3%ADa%20Webhooks/Descripcion/README.md) · [payloads](SSRF%20v%C3%ADa%20Webhooks/Payloads_hack/README.md)
9. [Web LLM Prompt Injection](Web%20LLM%20Prompt%20Injection/Descripcion/README.md) · [payloads](Web%20LLM%20Prompt%20Injection/Payloads_hack/README.md)

## 🌐 Infraestructura y misceláneos

1. [Subdomain Takeover](Subdomain%20Takeover/Descripcion/README.md) · [payloads](Subdomain%20Takeover/Payloads_hack/README.md)
2. [DNS Rebinding](DNS%20Rebinding/Descripcion/README.md) · [payloads](DNS%20Rebinding/Payloads_hack/README.md)
3. [Clickbait - Tabnabbing](Clickbait%20-%20Tabnabbing/Descripcion/README.md) · [payloads](Clickbait%20-%20Tabnabbing/Payloads_hack/README.md)
4. [Information Disclosure (debug endpoints, .git, .env expuestos, etc)](Information%20Disclosure%20%28debug%20endpoints%2C%20.git%2C%20.env%20expuestos%2C%20etc%29/Descripcion/README.md) · [payloads](Information%20Disclosure%20%28debug%20endpoints%2C%20.git%2C%20.env%20expuestos%2C%20etc%29/Payloads_hack/README.md)
5. [Security Misconfiguration (headers faltantes, CSP débil, etc)](Security%20Misconfiguration%20%28headers%20faltantes%2C%20CSP%20d%C3%A9bil%2C%20etc%29/Descripcion/README.md) · [payloads](Security%20Misconfiguration%20%28headers%20faltantes%2C%20CSP%20d%C3%A9bil%2C%20etc%29/Payloads_hack/README.md)
6. [SSRF a Cloud Metadata (AWS - GCP - Azure)](SSRF%20a%20Cloud%20Metadata%20%28AWS%20-%20GCP%20-%20Azure%29/Descripcion/README.md) · [payloads](SSRF%20a%20Cloud%20Metadata%20%28AWS%20-%20GCP%20-%20Azure%29/Payloads_hack/README.md)
7. [Zip Slip](Zip%20Slip/Descripcion/README.md) · [payloads](Zip%20Slip/Payloads_hack/README.md)
8. [Insecure CORS + Credentials](Insecure%20CORS%20%2B%20Credentials/Descripcion/README.md) · [payloads](Insecure%20CORS%20%2B%20Credentials/Payloads_hack/README.md)
9. [Clickjacking + Framing](Clickjacking%20%2B%20Framing/Descripcion/README.md) · [payloads](Clickjacking%20%2B%20Framing/Payloads_hack/README.md)

## 📚 Referencias y criterio editorial

- [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/), [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) y [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) aportan taxonomía y metodología.
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics) aporta mecanismos y laboratorios reproducibles.
- [HackTricks](https://book.hacktricks.wiki/) y [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) inspiran la navegación operativa. El texto de este proyecto es original y las técnicas se contrastan con referencias enlazadas en cada guía.
- [YesWeHack, análisis de confusión sintáctica](https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits) y [PortSwigger Research](https://portswigger.net/research/) se usan como ejemplos de investigación pública. [Fuentes y criterios](FUENTES.md) explica la diferencia entre una investigación pública, un laboratorio y un relato secundario.

## 🧾 Contribuciones y calidad

Las mejoras deben mantener la estructura, explicar precondiciones, incluir una prueba de control, enlazar fuentes y evitar datos de terceros. [Guía de contribución](CONTRIBUIR.md).

---

**Créditos:** OWASP, PortSwigger, HackTricks, PayloadsAllTheThings y autores de investigaciones públicas citadas. Los enlaces se ofrecen como fuentes, no como reproducción de sus textos.
