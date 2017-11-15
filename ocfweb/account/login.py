from ocflib.account.creation import validate_username

from random import randint

class username_suggester:
    def __init__(self, first, last):
        self.first = first.lower()
        self.last = last.lower()
        self.fullname = first + ' ' + last
        self.max_removes = len(self.fullname) - 3
        self.names = []
        self.runner = False

    def generate(self):
        self.names = []
        # Sucks for you...
        if len(self.fullname) < 4:
            return self.names

        if self.runner == False:
            self.runner = True
            nameCombined = self.first + self.last
            firstInitial = self.first[0] + self.last
            lastInitial = self.first + self.last[0]
            for x in [nameCombined, firstInitial, lastInitial]:
                self._validate(x)
            if len(self.names) < 3:
                self._get_three()
        else:
            self._get_three()

        return self.names

    def _get_three(self):
        attempts = 0
        while len(self.names) < 3 and attempts < 20:
            first_rand = randint(0, abs(self.max_removes - 1))
            last_rand = randint(0, abs(self.max_removes - first_rand) - 1)
            #print('DEBUG: {} {}'.format(first_rand, last_rand))
            first_generated = self.first[:first_rand]
            last_generated = self.last[:last_rand]
            self._validate(first_generated + last_generated)
            attempts += 1

    def _validate(self, suggested):
        try:
            validate_username(suggested, self.fullname)
            if suggested not in self.names:
                self.names.append(suggested)
        except:
            # Username failed
            pass
