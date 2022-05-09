class InvalidNameError(Exception):
    def __str__(self):
        return f'The entered name is invalid'


class InvalidUsernameError(Exception):
    def __str__(self):
        return 'Invalid username'


class PasswordMinLengthError(Exception):
    def __str__(self):
        return 'The entered password is shorter than the allowed length'


class InvalidEmailError(Exception):
    def __str__(self):
        return 'The entered email is invalid'


class PasswordIncludeLowercaseError(Exception):
    def __str__(self):
        return 'The entered password must includes one of lowercase letter'


class PasswordIncludeUppercaseError(Exception):
    def __str__(self):
        return 'The entered password must includes one of uppercase letter'


class PasswordIncludeDigitsError(Exception):
    def __str__(self):
        return 'The entered password must includes one of digit'


class PasswordIncludeSpecialSymbolError(Exception):
    def __str__(self):
        return f'The entered password must includes one of special character: \n' \
               f'{app.config.get("ALLOWED_SPECIAL_SYMBOLS")}'


class OTPTryError(Exception):
    def __str__(self):
        return 'the number of login attempts exceeded'
