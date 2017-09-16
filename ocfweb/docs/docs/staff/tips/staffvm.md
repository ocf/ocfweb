[[!meta title="On your staff VM"]]

## Essentials

Your vm's environment is determined by the ldap entry for the machine.

    johnsnow@~$ kinit johnsnow/admin ldapvi cn=whitewalker
    ### ...LDIF
    #...
    # whitewalker, Hosts, OCF.Berkeley.EDU
    dn: cn=whitewalker,ou=Hosts,dc=OCF,dc=Berkeley,dc=EDU
    objectClass: device
    objectClass: ocfDevice
    cn: whitewalker
    ipHostNumber: 169.229.226.256
    type: server
    puppetVar: owner=johnsnow
    environment: johnsnow
    #...
