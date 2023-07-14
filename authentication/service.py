from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPException

ldap_server = 'ad-server-1.smtp-group.mg'
ldap_base = 'dc=smtp-group, dc=mg'


def check_user_ldap(username, password, ):
    organisation = 'smtp-group'
    user = f"{organisation}\\{username}"
    try:
        server = Server(ldap_server, get_info=ALL)
        print(server)
        info = Connection(server, user=user, password=password)
        print(info)
        connexion = info.bind()
        return connexion

    except LDAPException:
        print("-------------------------------------------")
        print(f"Unable to connect to LDAP server ")
        print("-------------------------------------------")
        return False
