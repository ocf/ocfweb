[[!meta title="Useful staff VM tricks"]]

## Essentials
Your vm's environment is determined by the puppet entry for the machine.
```
johnsnow@~$ kinit johnsnow/admin ldapvi cn=whitewalker
### ...LDOF
#...
# whitewalker, Hosts, OCF.Berkeley.EDU
dn: cn=pox,ou=Hosts,dc=OCF,dc=Berkeley,dc=EDU
objectClass: device
objectClass: ocfDevice
cn: whitewalker
ipHostNumber: 169.229.226.256
type: server
puppetVar: owner=johnsnow
environment: johnsnow
#...
```
