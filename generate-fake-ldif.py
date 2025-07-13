# Generate fake entries for Active Directory
# Certify that you have Faker installed before running the script. You can install it using pip install faker.
# Author: Jarbas
# Date: 2023-06-26

import sys
import random

from unidecode import unidecode

from faker import Faker
from faker.providers import person

# Random values
company_s = ["Matriz", "Filial 01", "Filial 02", "Filial 03", "Filial 04" ]
department_s = ["NOC", "RH", "TI", "Financeiro", "Marketing"]
employeeType_s = ['Analista','Desenvolvedor','Gestor','Administrador']
title_s = ['Sr','Sra']
telephoneNumber_s = ['+556711112222','+556733334444','+556755556666']
userAccountControl_s = ['512','514']
l_s = ['Campo Grande','Rio de Janeiro','Brasília','São Paulo','Porto Velho','Goiânia','Belo Horizonte']
physicalDeliveryOfficeName_s = ['Escritório #1', 'Escritório #2', 'Escritório #3', 'Escritório #4']
info_s = ['Informação #1', 'Informação #2', 'Informação #3']
description_s = ['Descrição #1', 'Descrição #2', 'Descrição #3']
st_s=['MS', 'MG', 'DF', 'RJ', 'SP', 'GO', 'RO']

# Some variables
cn=givenName=sn=company=department=description=displayName=sAMAccountName=''
userPrincipalName=mail=employeeNumber=employeeType=info=initials=title=''
telephoneNumber=physicalDeliveryOfficeName=c=l=st=streetAddress=''
userAccountControl=''

# Fixed
_REALM = "SEUDOMINIO.COM.BR"
objectCategory='CN=Person,CN=Schema,CN=Configuration'
c='BR'
DC = ",".join(f"DC={part}" for part in _REALM.lower().split("."))
DOMAIN=_REALM.lower()

# Create a Faker instance with the pt_BR locale
fake = Faker('pt_BR')
fake.add_provider(person)

existing_logins = set()

def generate_cpf():
    def calculate_digit(cpf):
        total = 0
        for i, digit in enumerate(cpf):
            total += int(digit) * (10 - i)
        remainder = total % 11
        return str(11 - remainder) if remainder > 1 else '0'

    cpf = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        cpf.append(calculate_digit(cpf))
    return ''.join(map(str, cpf))


def generate_unique_login(existing_logins):
#    givenName = unidecode(fake.first_name().lower()).replace(" ", "_")
##    givenName = givenName.replace(" ", "_")
#    sn = unidecode(fake.last_name().lower()).replace(" ", "_")
##    sn = sn.replace(" ", "_")
#    login = f"{givenName}.{sn}"
    givenName = fake.first_name()
    sn = fake.last_name()
    first = unidecode(givenName.split(' ')[0].lower())
    len_last=len(sn.split(' '))
    last = unidecode(sn.split(' ')[len_last-1].lower())
    login = f"{first}.{last}"

    while login in existing_logins:
#        givenName = unidecode(fake.first_name().lower()).replace(" ", "_")
#        sn = unidecode(fake.last_name().lower()).replace(" ", "_")
#        login = f"{givenName}.{sn}"
        givenName = fake.first_name()
        sn = fake.last_name()
        first = unidecode(givenName.split(' ')[0].lower())
        len_last=len(sn.split(' '))
        last = unidecode(sn.split(' ')[len_last-1].lower())
        login = f"{first}.{last}"

    existing_logins.add(login)
    return [login,givenName,sn]


def generate_name_from_login(login):
    parts = login.split('.')
    capitalized_parts = [part.capitalize() for part in parts]
    return ' '.join(capitalized_parts)

def main(num_rows):
    for i in range(num_rows):
        login,givenName,sn = generate_unique_login(existing_logins)
        name = generate_name_from_login(login)
        employeeNumber = fake.rg() #generate_cpf()
        email = f'{login}@{DOMAIN}'
        department = fake.company_suffix() #fake.department() #random.choice(department_s)
        company = fake.company() #random.choice(company_s)
        employeeType = random.choice(employeeType_s)
        title = fake.prefix() #random.choice(title_s)
        telephoneNumber = fake.msisdn() #fake.phone_number() #random.choice(telephoneNumber_s)
        userAccountControl = random.choice(userAccountControl_s)
        physicalDeliveryOfficeName = fake.street_name() #random.choice(physicalDeliveryOfficeName_s)
        info = fake.catch_phrase() #random.choice(info_s)
        description = fake.neighborhood() #random.choice(description_s)
        streetAddress = fake.street_address() #f"Rua {random.randint(1, 100)}, {random.randint(1, 100)}"
        l = fake.city() #random.choice(l_s)
        st = random.choice(st_s)
        c = fake.current_country_code()

        print(f'''# Employee Fake #{i+1}
dn: CN={login},CN=Users,{DC}
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: {login}
sAMAccountName: {login}
userPrincipalName: {login}@{DOMAIN}
givenName: {givenName}
sn: {sn}
initials: {givenName[0].upper()}.{sn[0].upper()}.
name: {name}
displayName: {givenName} {sn} - {company}/{st}
employeeNumber: {employeeNumber}
employeeType: {employeeType}
description: {description}
mail: {email}
l: {l}
st: {st}
c: {c}
telephoneNumber: +{telephoneNumber}
title: {title}
info: {info}
streetAddress: {streetAddress}
o: {company}
company: {company}
department: {department}
physicalDeliveryOfficeName: {physicalDeliveryOfficeName}
userAccountControl: {userAccountControl}
objectCategory: {objectCategory},{DC}
uid: {login}
gecos: {givenName} {sn} - {company}/{st}
unixHomeDirectory: /home/users/{login}
loginShell: /bin/bash
uidNumber: {i+10001}
gidNumber: 513
''')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <num_rows>")
        sys.exit(1)
    num_rows = int(sys.argv[1])
    main(num_rows)
