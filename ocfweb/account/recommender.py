from random import randint
from typing import Any
from typing import List

from ocflib.account.creation import validate_username
from ocflib.account.creation import ValidationError
from ocflib.account.creation import ValidationWarning


def recommend(real_name: str, n: int) -> List[Any]:
    name_fields: List[str] = [name.lower() for name in real_name.split()]

    # Can reimplement name_field_abbrevs to only remove vowels or consonants
    name_field_abbrevs: List[List[str]] = [[] for i in range(len(name_fields))]
    for i in range(len(name_fields)):
        name_field = name_fields[i]
        for j in range(1, len(name_field) + 1):
            name_field_abbrevs[i].append(name_field[:j])

    unvalidated_recs = name_field_abbrevs[0]
    for i in range(1, len(name_fields)):
        new_unvalidated_recs = []
        for name_field_abbrev in name_field_abbrevs[i]:
            for rec in unvalidated_recs:
                new_unvalidated_recs.append(rec + name_field_abbrev)
        unvalidated_recs = new_unvalidated_recs

    validated_recs: List[Any] = []
    while len(validated_recs) < n and len(unvalidated_recs) > 0:
        rec = unvalidated_recs.pop(randint(0, len(unvalidated_recs) - 1))
        try:
            validate_username(rec, real_name)
            validated_recs.append(rec)
        except (ValidationError, ValidationWarning):
            pass  # Account name wasn't valid, skip this recommendation
    return validated_recs
