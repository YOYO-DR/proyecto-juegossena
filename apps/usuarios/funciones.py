from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def validar_patron_correo(email):
    try:
        validate_email(email)
        return True
    except:
        return False

def validar_contra(contra, usuario=None):
    try:
        validate_password(contra, usuario)
        return [True]
    except ValidationError as e:
        errors = e.error_list
        errores = []
        for error in errors:
            errores.append(str(error))
        return [False, errores]
