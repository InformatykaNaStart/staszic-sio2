from django.contrib.auth.models import Group

from django_auth_ldap.backend import LDAPBackend
from django_auth_ldap.config import LDAPGroupType, PosixGroupType

import ldap
import re

class StaszicLDAPBackend(LDAPBackend):
    default_settings = dict(
            SERVER_URI = 'ldaps://ad.staszic.waw.pl',
            USER_DN_TEMPLATE = "cn=%(user)s,cn=Users,dc=ad,dc=staszic,dc=waw,dc=pl",
            USER_ATTR_MAP = dict(
                    first_name = 'givenName',
                    last_name = 'sn',
                    email = 'mail'
                ),
            BIND_AS_AUTHENTICATING_USER = True,
            GROUP_TYPE = LDAPGroupType(),
            GROUP_SEARCH = LDAPGroupType(),
        )

    def is_valid_group_name(self, name):
        if name in ('others', 'staff'): return True
        if re.match(r'^k\d\d_[a-h]$', name): return True
        if re.match(r'^gim\d\d_[a-h]$', name): return True
        return False

    def authenticate_ldap_user(self, ldap_user, password):
        user = super(StaszicLDAPBackend, self).authenticate_ldap_user(ldap_user, password)

        if user is None: return None

        for dn in ldap_user.attrs['memberof']:
            dn_parts = ldap.dn.str2dn(dn,flags=ldap.DN_FORMAT_LDAPV3)
            (_, group_name, _), = dn_parts[0]

            if self.is_valid_group_name(group_name):
                self.add_user_to_group(user, group_name)

        return user

    def add_user_to_group(self, user, group_name):
        group, _ = Group.objects.get_or_create(name = 'LDAP :: {}'.format(group_name))

        group.user_set.add(user)
