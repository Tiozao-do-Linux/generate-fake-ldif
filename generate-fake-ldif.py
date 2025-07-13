# Generate fake entries for Active Directory in LDIF format
# Author: Jarbas
# Date: 2023-06-26

import sys
import random

from unidecode import unidecode

from faker import Faker
from faker.providers import person

# Random values
employeeType_s = ['Analista','Desenvolvedor','Gestor','Administrador']
userAccountControl_s = ['512','514']

# Some variables
cn=givenName=sn=company=department=description=displayName=sAMAccountName=''
userPrincipalName=mail=employeeNumber=employeeType=info=initials=title=''
telephoneNumber=physicalDeliveryOfficeName=c=l=st=streetAddress=''
userAccountControl=''

# Fixed
objectCategory='CN=Person,CN=Schema,CN=Configuration'

# Generate a random CPF (only for pt_BR)
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

existing_logins = set()
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
    # Create a Faker instance with the locale
    fake = Faker(LANGUAGE)
    fake.add_provider(person)

    for i in range(num_rows):
        login,givenName,sn = generate_unique_login(existing_logins)
        name = generate_name_from_login(login)
        employeeNumber = fake.passport_number()
        email = f'{login}@{DOMAIN}'
        department = fake.company_suffix()
        company = fake.company()
        title = fake.prefix()
        telephoneNumber = fake.msisdn()
        physicalDeliveryOfficeName = fake.street_name()
        info = fake.catch_phrase()
        description = fake.administrative_unit()
        streetAddress = fake.street_address()
        l = fake.city()
        st = fake.state()
        c = fake.current_country_code()
        employeeType = random.choice(employeeType_s)
        userAccountControl = random.choice(userAccountControl_s)

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
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <number of records> <domain.tld> <language>")
        sys.exit(1)

    num_rows = int(sys.argv[1])
    DOMAIN_TLD = sys.argv[2]
    LANGUAGE = sys.argv[3]

    DC = ",".join(f"DC={part}" for part in DOMAIN_TLD.lower().split("."))
    DOMAIN=DOMAIN_TLD.lower()

    # Create a Faker instance with the pt_BR locale
    fake = Faker(LANGUAGE)
    fake.add_provider(person)

    main(num_rows)
