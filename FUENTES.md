# 📚 Fuentes, casos y criterio de evidencia

## Jerarquía editorial

1. **Normas y guías primarias:** OWASP WSTG, API Security Top 10, documentación de estándares (RFC) y especificaciones de proveedor.
2. **Investigación reproducible:** PortSwigger Research, Web Security Academy y publicaciones técnicas con precondiciones y pruebas observables.
3. **Relatos de hunters:** YesWeHack, HackerOne, Bugcrowd y Medium. Una historia del autor orienta hipótesis, pero no se convierte automáticamente en hallazgo confirmado si el informe original no es público.

Cada capítulo enlaza sus fuentes. Los ejemplos están redactados de forma original y usan dominios, cuentas y objetos de prueba. Se evita copiar payloads largos sin explicar su contexto y se descartan atribuciones sin enlace verificable.

Los bancos de `Payloads_hack/` agrupan variantes **básicas**, **por contexto** y **avanzadas**. Una lista de rutas, cabeceras o cuerpos representa alternativas que se prueban por separado; las precondiciones junto al bloque indican cuándo tienen sentido. Los escenarios guiados explican la señal mínima y los falsos positivos.

## Casos públicos útiles para razonar

| Fuente | Técnica documentada | Qué enseña | Límite de la fuente |
| --- | --- | --- | --- |
| [PortSwigger Research, HTTP Desync Attacks](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn) | Desincronización entre parsers y cadenas con caché | Probar cada capa y descartar falsos positivos de conexión reutilizada | Los impactos pertenecen a los sistemas investigados allí. |
| [PortSwigger Research, Practical Web Cache Poisoning](https://portswigger.net/research/practical-web-cache-poisoning) | Entrada no incluida en la clave de caché | Confirmar entrega a una segunda sesión, no solo reflejo | Un marcador en una respuesta propia no prueba caché compartida. |
| [YesWeHack, confusión sintáctica](https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits) | Normalización de URL, cache poisoning, SSRF y lectura de archivos | La combinación de parsers puede cambiar el alcance de una primitive | Los objetivos se describen sin nombre; no extrapolar impacto. |
| [Medium, relato de IDOR multi-tenant](https://medium.com/@ssherlock1/my-first-bug-on-hackerone-a-simple-idor-that-taught-me-a-lot-157c7ef46dd7) | ID de organización cambiado en una API | El objeto y el tenant son límites de autorización distintos | Es testimonio del autor; el artículo no enlaza el reporte original. |
| [HackerOne, Nextcloud #2705507](https://hackerone.com/reports/2705507) | IDOR en información compartida de Tables | El impacto real depende de los datos expuestos | Informe divulgado; no trasladar su severidad a otro producto. |
| [HackerOne, race condition #1132171](https://hackerone.com/reports/1132171) | Feedback enviado varias veces | Verificar el efecto final, no solo dos respuestas correctas | Informe divulgado de severidad baja en ese flujo. |
| [HackerOne, Basecamp #3943339](https://hackerone.com/reports/3943339) | XSS reflejado y cadena entre cuentas | Demostrar privilegio y acción lograda tras la ejecución | Informe divulgado de un producto y flujo específicos. |
| [HackerOne, QIWI #816254](https://hackerone.com/reports/816254) y [Semrush #312543](https://hackerone.com/reports/312543) | SQLi y XXE | Los efectos posteriores dependen de permisos del motor y parser | HackerOne los selecciona como ejemplos de informes de calidad; enlaces a informes divulgados. |

## Antes de citar un writeup en una guía

- Identificar **quién** lo publicó y si la divulgación fue autorizada.
- Verificar **request, response, precondiciones y efecto**, no solo el título o la recompensa.
- Distinguir **laboratorio** de incidente real y **relato autoafirmado** de reporte divulgado por la plataforma.
- No reproducir datos personales, credenciales, cookies, tokens ni capturas sensibles.
- Revalidar versiones y mitigaciones: un caso antiguo puede ilustrar el mecanismo sin describir el comportamiento actual.

## Referencias base

- [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/)
- [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/)
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics)
- [HackTricks](https://book.hacktricks.wiki/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

---

[← Índice general](README.md)
