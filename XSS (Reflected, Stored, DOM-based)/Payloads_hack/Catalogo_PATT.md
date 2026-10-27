# Banco ampliado: Cross-Site Scripting (XSS)

Este índice ordena los ejemplos técnicos reproducidos o adaptados de PayloadsAllTheThings por documento y situación. Los títulos explican el contexto en español y conservan los nombres técnicos de motores y funciones; el código mantiene la sintaxis de origen. Consulta primero [los payloads básicos y las pruebas guiadas](README.md).

**Versión de origen:** [3ac27901c711](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a) · [Licencia MIT y atribución](../../LICENCIA_PATT.md).

| Documento técnico | Apartados | Bloques de código | Variantes en línea |
| --- | ---: | ---: | ---: |
| [XSS Inyección](PATT_01_XSS_Injection_README.md) | 26 | 34 | 6 |
| [1 - XSS Evasión de filtros](PATT_02_XSS_Injection_1_XSS_Filter_Bypass.md) | 37 | 52 | 33 |
| [2 - XSS Polyglot](PATT_03_XSS_Injection_2_XSS_Polyglot.md) | 1 | 11 | 0 |
| [3 - XSS Comunes Evasión de WAF](PATT_04_XSS_Injection_3_XSS_Common_WAF_Bypass.md) | 6 | 15 | 0 |
| [4 - Evasión de CSP](PATT_05_XSS_Injection_4_CSP_Bypass.md) | 8 | 9 | 16 |
| [5 - XSS in Angular](PATT_06_XSS_Injection_5_XSS_in_Angular.md) | 4 | 33 | 2 |
| [CSS Inyección](PATT_07_CSS_Injection_README.md) | 8 | 12 | 17 |
| [XS-Leak](PATT_08_XS_Leak_README.md) | 1 | 1 | 0 |

## Diccionarios de payloads para Intruder y fuzzing

Cada archivo conserva sus líneas de origen y se debe usar con el punto de entrada y la profundidad adecuados. No ejecutar los diccionarios completos contra un programa sin comprobar sus límites de frecuencia y volumen.

| Lista | Líneas | Fuente |
| --- | ---: | --- |
| [XSS_Injection_Intruders_0xcela_event_handlers.txt](PATT_LISTA_XSS_Injection_Intruders_0xcela_event_handlers.txt) | 105 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/0xcela_event_handlers.txt) |
| [XSS_Injection_Intruders_BRUTELOGIC-XSS-JS.txt](PATT_LISTA_XSS_Injection_Intruders_BRUTELOGIC-XSS-JS.txt) | 17 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/BRUTELOGIC-XSS-JS.txt) |
| [XSS_Injection_Intruders_BRUTELOGIC-XSS-STRINGS.txt](PATT_LISTA_XSS_Injection_Intruders_BRUTELOGIC-XSS-STRINGS.txt) | 110 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/BRUTELOGIC-XSS-STRINGS.txt) |
| [XSS_Injection_Intruders_IntrudersXSS.txt](PATT_LISTA_XSS_Injection_Intruders_IntrudersXSS.txt) | 179 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/IntrudersXSS.txt) |
| [XSS_Injection_Intruders_JHADDIX_XSS.txt](PATT_LISTA_XSS_Injection_Intruders_JHADDIX_XSS.txt) | 110 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/JHADDIX_XSS.txt) |
| [XSS_Injection_Intruders_MarioXSSVectors.txt](PATT_LISTA_XSS_Injection_Intruders_MarioXSSVectors.txt) | 330 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/MarioXSSVectors.txt) |
| [XSS_Injection_Intruders_RSNAKE_XSS.txt](PATT_LISTA_XSS_Injection_Intruders_RSNAKE_XSS.txt) | 73 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/RSNAKE_XSS.txt) |
| [XSS_Injection_Intruders_XSSDetection.txt](PATT_LISTA_XSS_Injection_Intruders_XSSDetection.txt) | 202 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/XSSDetection.txt) |
| [XSS_Injection_Intruders_XSS_Polyglots.txt](PATT_LISTA_XSS_Injection_Intruders_XSS_Polyglots.txt) | 16 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/XSS_Polyglots.txt) |
| [XSS_Injection_Intruders_jsonp_endpoint.txt](PATT_LISTA_XSS_Injection_Intruders_jsonp_endpoint.txt) | 57 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/jsonp_endpoint.txt) |
| [XSS_Injection_Intruders_port_swigger_xss_cheatsheet_event_handlers.txt](PATT_LISTA_XSS_Injection_Intruders_port_swigger_xss_cheatsheet_event_handlers.txt) | 114 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/port_swigger_xss_cheatsheet_event_handlers.txt) |
| [XSS_Injection_Intruders_xss_alert.txt](PATT_LISTA_XSS_Injection_Intruders_xss_alert.txt) | 667 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/xss_alert.txt) |
| [XSS_Injection_Intruders_xss_alert_identifiable.txt](PATT_LISTA_XSS_Injection_Intruders_xss_alert_identifiable.txt) | 667 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/xss_alert_identifiable.txt) |
| [XSS_Injection_Intruders_xss_payloads_quick.txt](PATT_LISTA_XSS_Injection_Intruders_xss_payloads_quick.txt) | 39 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/xss_payloads_quick.txt) |
| [XSS_Injection_Intruders_xss_swf_fuzz.txt](PATT_LISTA_XSS_Injection_Intruders_xss_swf_fuzz.txt) | 24 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XSS%20Injection/Intruders/xss_swf_fuzz.txt) |

---

[← Guía principal](README.md) · [← Índice general](../../README.md)
