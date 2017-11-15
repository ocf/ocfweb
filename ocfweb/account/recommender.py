from random import randint

from ocflib.account.creation import validate_username


def recommend(real_name, n):
    name_fields = real_name.split()
    for i in range(len(name_fields)):
        name_fields[i] = name_fields[i].lower()

    recs = []

    for i in range(len(name_fields)):
        rec = ''
        for j in range(len(name_fields)):
            if i == j:
                rec += name_fields[j][0]
            else:
                rec += name_fields[j]
        try:
            validate_username(rec, real_name)
            if len(recs) < n:
                recs.append(rec)
        except Exception:
            pass

    attempts = 0
    while len(recs) < n and attempts < 20:
        rec = ''
        for name_field in name_fields:
            rand_index = randint(1, len(name_field))
            rec += name_field[:rand_index]
        if rec not in recs:
            try:
                validate_username(rec, real_name)
                recs.append(rec)
            except Exception:
                pass
        attempts += 1

    return recs
