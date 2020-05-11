TEST_OCF_ACCOUNTS = (
    'sanjay',  # an old, sorried account with kerberos princ
    'alec',  # an old, sorried account with no kerberos princ
    'guser',  # an account specifically made for testing
    'nonexist',  # this account does not exist
)

TESTER_CALNET_UIDS = (
    872544,   # daradib
    1034192,  # ckuehl
    869331,   # tzhu
    1031366,  # mattmcal
    1099131,  # dkessler
    1101587,  # jvperrin
    1511731,  # ethanhs
    1623751,  # cooperc
    1619256,  # jaw
)

# comma separated tuples of CalLink OIDs and student group names
TEST_GROUP_ACCOUNTS = (
    (91740, 'The Testing Group'),  # needs to have a real OID, so boo
    (46187, 'Open Computing Facility'),  # good old ocf
    (46692, 'Awesome Group of Awesome'),  # boo another real OID
    (92029, 'eXperimental Computing Facility'),  # our sister org
)
