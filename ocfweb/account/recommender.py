from ocflib.account.creation import validate_username

from random import randint

def recommend(first_name, last_name, n):
    first_name = first_name.lower()
    last_name = last_name.lower()

    recommendations = []
    attempts = 0
    while len(recommendations) < n and attempts < 20:
        first_rand = randint(1, len(first_name))
        last_rand = randint(1, len(last_name))
        first_generated = first_name[:first_rand]
        last_generated = last_name[:last_rand]
        recommendation = first_generated+last_generated
        if recommendation not in recommendations:
            try:
                validate_username(recommendation, first_name+last_name)
                recommendations.append(recommendation)
            except:
                pass
        attempts += 1
    return recommendations
