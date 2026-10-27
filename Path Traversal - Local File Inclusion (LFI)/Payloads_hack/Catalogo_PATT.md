# Banco ampliado: Path Traversal y LFI

Este índice ordena los ejemplos técnicos reproducidos o adaptados de PayloadsAllTheThings por documento y situación. Los títulos explican el contexto en español y conservan los nombres técnicos de motores y funciones; el código mantiene la sintaxis de origen. Consulta primero [los payloads básicos y las pruebas guiadas](README.md).

**Versión de origen:** [3ac27901c711](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a) · [Licencia MIT y atribución](../../LICENCIA_PATT.md).

| Documento técnico | Apartados | Bloques de código | Variantes en línea |
| --- | ---: | ---: | ---: |
| [Recorrido de directorios](PATT_01_Directory_Traversal_README.md) | 15 | 26 | 42 |
| [Inclusión de archivos](PATT_02_File_Inclusion_README.md) | 10 | 12 | 9 |
| [Wrappers](PATT_03_File_Inclusion_Wrappers.md) | 10 | 19 | 38 |
| [LFI-to-RCE](PATT_04_File_Inclusion_LFI_to_RCE.md) | 14 | 23 | 35 |

## Diccionarios de payloads para Intruder y fuzzing

Cada archivo conserva sus líneas de origen y se debe usar con el punto de entrada y la profundidad adecuados. No ejecutar los diccionarios completos contra un programa sin comprobar sus límites de frecuencia y volumen.

| Lista | Líneas | Fuente |
| --- | ---: | --- |
| [Directory_Traversal_Intruder_deep_traversal.txt](PATT_LISTA_Directory_Traversal_Intruder_deep_traversal.txt) | 912 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Directory%20Traversal/Intruder/deep_traversal.txt) |
| [Directory_Traversal_Intruder_directory_traversal.txt](PATT_LISTA_Directory_Traversal_Intruder_directory_traversal.txt) | 140 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Directory%20Traversal/Intruder/directory_traversal.txt) |
| [Directory_Traversal_Intruder_dotdotpwn.txt](PATT_LISTA_Directory_Traversal_Intruder_dotdotpwn.txt) | 21144 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Directory%20Traversal/Intruder/dotdotpwn.txt) |
| [Directory_Traversal_Intruder_traversals-8-deep-exotic-encoding.txt](PATT_LISTA_Directory_Traversal_Intruder_traversals-8-deep-exotic-encoding.txt) | 887 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Directory%20Traversal/Intruder/traversals-8-deep-exotic-encoding.txt) |
| [File_Inclusion_Intruders_BSD-files.txt](PATT_LISTA_File_Inclusion_Intruders_BSD-files.txt) | 13 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/BSD-files.txt) |
| [File_Inclusion_Intruders_JHADDIX_LFI.txt](PATT_LISTA_File_Inclusion_Intruders_JHADDIX_LFI.txt) | 879 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/JHADDIX_LFI.txt) |
| [File_Inclusion_Intruders_LFI-FD-check.txt](PATT_LISTA_File_Inclusion_Intruders_LFI-FD-check.txt) | 39 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/LFI-FD-check.txt) |
| [File_Inclusion_Intruders_LFI-WindowsFileCheck.txt](PATT_LISTA_File_Inclusion_Intruders_LFI-WindowsFileCheck.txt) | 69 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/LFI-WindowsFileCheck.txt) |
| [File_Inclusion_Intruders_Linux-files.txt](PATT_LISTA_File_Inclusion_Intruders_Linux-files.txt) | 62 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/Linux-files.txt) |
| [File_Inclusion_Intruders_List_Of_File_To_Include.txt](PATT_LISTA_File_Inclusion_Intruders_List_Of_File_To_Include.txt) | 911 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/List_Of_File_To_Include.txt) |
| [File_Inclusion_Intruders_List_Of_File_To_Include_NullByteAdded.txt](PATT_LISTA_File_Inclusion_Intruders_List_Of_File_To_Include_NullByteAdded.txt) | 319 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/List_Of_File_To_Include_NullByteAdded.txt) |
| [File_Inclusion_Intruders_Mac-files.txt](PATT_LISTA_File_Inclusion_Intruders_Mac-files.txt) | 8 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/Mac-files.txt) |
| [File_Inclusion_Intruders_Traversal.txt](PATT_LISTA_File_Inclusion_Intruders_Traversal.txt) | 4521 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/Traversal.txt) |
| [File_Inclusion_Intruders_Web-files.txt](PATT_LISTA_File_Inclusion_Intruders_Web-files.txt) | 14 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/Web-files.txt) |
| [File_Inclusion_Intruders_Windows-files.txt](PATT_LISTA_File_Inclusion_Intruders_Windows-files.txt) | 212 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/Windows-files.txt) |
| [File_Inclusion_Intruders_dot-slash-PathTraversal_and_LFI_pairing.txt](PATT_LISTA_File_Inclusion_Intruders_dot-slash-PathTraversal_and_LFI_pairing.txt) | 886 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/dot-slash-PathTraversal_and_LFI_pairing.txt) |
| [File_Inclusion_Intruders_php-filter-iconv.txt](PATT_LISTA_File_Inclusion_Intruders_php-filter-iconv.txt) | 50 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/php-filter-iconv.txt) |
| [File_Inclusion_Intruders_simple-check.txt](PATT_LISTA_File_Inclusion_Intruders_simple-check.txt) | 10 | [Origen](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/File%20Inclusion/Intruders/simple-check.txt) |

---

[← Guía principal](README.md) · [← Índice general](../../README.md)
