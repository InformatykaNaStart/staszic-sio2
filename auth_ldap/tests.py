from django.test import SimpleTestCase
from staszic.auth_ldap.backends import StaszicLDAPBackend

class LDAPBackendTests(SimpleTestCase):
    def test_valid_group_names(self):
        backend = StaszicLDAPBackend()

        self.assertTrue(backend.is_valid_group_name('staff'))
        self.assertTrue(backend.is_valid_group_name('others'))
        self.assertTrue(backend.is_valid_group_name('k03_d'))
        self.assertTrue(backend.is_valid_group_name('gim17_c'))
        self.assertTrue(backend.is_valid_group_name('k16_b'))

        self.assertFalse(backend.is_valid_group_name('k16_ba'))
        self.assertFalse(backend.is_valid_group_name('gim16_ba'))
        self.assertFalse(backend.is_valid_group_name('lo16_k'))
        self.assertFalse(backend.is_valid_group_name('root'))
        self.assertFalse(backend.is_valid_group_name('k7_d'))

