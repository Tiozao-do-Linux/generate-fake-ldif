
# How does it work?

😎 Have you ever needed to populate an LDAP database in Samba4 with hundreds or thousands of [fake users](https://pypi.org/project/Faker/) for testing?

😎 Yes! The purpose of this repository is to generate a file in LDIF format with fake data that can be used in the population.

## ❓Main doubts

* How do I perform this population?
    * When your Samba4 is provisioned but not yet initialized, use `ldbadd -H /var/lib/samba/private/sam.ldb /tmp/fake.ldif`
* Where has this strategy been used?
    * In this script https://github.com/Tiozao-do-Linux/samba4-addc/blob/main/provision/post-provision.sh

## 🚀 It's very simple to use

### Cloning, installing, generating your image locally

```shell
# Download clone project
git clone https://github.com/Tiozao-do-Linux/generate-fake-ldif.git

# Create virtualenvironment
python -m venv .venv
. .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# OR install each one
pip install faker unidecode

# Build docker image
docker build -t jarbelix/generate-fake-ldif .
```

### Using my image 😁

> [!NOTE]
>  🎯 If you just want to use my image to run a docker container which is available at https://hub.docker.com/u/jarbelix

## Generate fake data with 1000 records for the domain TIOZAODOLINUX.COM in the file /tmp/fake.ldif

* The **first parameter** is the desired number of records.
* The **second parameter** is the fully qualified domain.

```shell
# Run docker container with ARGs <number of records> <dfully qualified domain name>
docker run --rm -it jarbelix/generate-fake-ldif 1000 TIOZAODOLINUX.COM pt_BR > /tmp/fake.ldif
```

## Some small examples of use:

### Just a single registration for EXAMPLE.COM in en_US locale


```shell
docker run --rm -it jarbelix/generate-fake-ldif 1 EXAMPLE.COM en_US
```

```ldif
# Employee Fake #1
dn: CN=valerie.terry,CN=Users,DC=example,DC=com
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: valerie.terry
sAMAccountName: valerie.terry
userPrincipalName: valerie.terry@example.com
givenName: Valerie
sn: Terry
initials: V.T.
name: Valerie Terry
displayName: Valerie Terry - Hughes and Sons/South Carolina
employeeNumber: Z16905903
employeeType: Analista
description: North Carolina
mail: valerie.terry@example.com
l: West Danielborough
st: South Carolina
c: US
telephoneNumber: +2349714778943
title: Ms.
info: Reactive logistical array
streetAddress: 628 Tiffany Ramp
o: Hughes and Sons
company: Hughes and Sons
department: Group
physicalDeliveryOfficeName: Andrew Ways
userAccountControl: 512
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=example,DC=com
uid: valerie.terry
gecos: Valerie Terry - Hughes and Sons/South Carolina
unixHomeDirectory: /home/users/valerie.terry
loginShell: /bin/bash
uidNumber: 10001
gidNumber: 513
```

### Two entries for EXAMPLE.COM.BR in pt_BR

```shell
docker run --rm -it jarbelix/generate-fake-ldif 2 EXAMPLE.COM.BR pt_BR
```

```ldif
# Employee Fake #1
dn: CN=barbara.machado,CN=Users,DC=example,DC=com,DC=br
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: barbara.machado
sAMAccountName: barbara.machado
userPrincipalName: barbara.machado@example.com.br
givenName: Bárbara
sn: Machado
initials: B.M.
name: Barbara Machado
displayName: Bárbara Machado - Marques/Sergipe
employeeNumber: 320403209
employeeType: Gestor
description: Rondônia
mail: barbara.machado@example.com.br
l: Oliveira
st: Sergipe
c: BR
telephoneNumber: +5521936080198
title: Sr.
info: A possibilidade de concretizar seus projetos direto da fonte
streetAddress: Condomínio Vieira, 27
o: Marques
company: Marques
department: S.A.
physicalDeliveryOfficeName: Rua Luiza da Rosa
userAccountControl: 512
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=example,DC=com,DC=br
uid: barbara.machado
gecos: Bárbara Machado - Marques/Sergipe
unixHomeDirectory: /home/users/barbara.machado
loginShell: /bin/bash
uidNumber: 10001
gidNumber: 513

# Employee Fake #2
dn: CN=gabriel.mota,CN=Users,DC=example,DC=com,DC=br
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: gabriel.mota
sAMAccountName: gabriel.mota
userPrincipalName: gabriel.mota@example.com.br
givenName: Gabriel
sn: da Mota
initials: G.D.
name: Gabriel Mota
displayName: Gabriel da Mota - Cassiano/Ceará
employeeNumber: O62633019
employeeType: Desenvolvedor
description: Amapá
mail: gabriel.mota@example.com.br
l: Sousa de Costela
st: Ceará
c: BR
telephoneNumber: +5581963290425
title: Sra.
info: O poder de conseguir sem preocupação
streetAddress: Aeroporto Pires, 222
o: Cassiano
company: Cassiano
department: e Filhos
physicalDeliveryOfficeName: Passarela Castro
userAccountControl: 514
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=example,DC=com,DC=br
uid: gabriel.mota
gecos: Gabriel da Mota - Cassiano/Ceará
unixHomeDirectory: /home/users/gabriel.mota
loginShell: /bin/bash
uidNumber: 10002
gidNumber: 513
```
