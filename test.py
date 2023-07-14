from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPSocketOpenError

ldap_server = 'ad-server-1.smtp-group.mg'
ldap_base = 'dc=smtp-group, dc=mg'


def ldap_user(username, password):
    organisation = 'smtp-group'
    user = f"{organisation}\\{username}"
    try:
        server = Server(ldap_server, get_info=ALL)
        info = Connection(server, user=user, password=password)
        connexion = info.bind()
        return connexion

    except LDAPSocketOpenError:
        print("-------------------------------------------")
        print(f"FATAL ERROR in service: ")
        print("-------------------------------------------")
        raise


spec = ldap_user(username='muriel.raharison', password='F4u4gbC5',)

print(spec)