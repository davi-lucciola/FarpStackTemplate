from email_validator import validate_email


def email_validator(email: str) -> str:
    try:
        validate_email(email)
    except:
        raise ValueError('Email inválido.')

    return email


def password_validator(password: str):
    if password.strip() == '':
        raise ValueError('Sua senha não pode ser vazia.')

    password_min_length = 4
    if len(password) < password_min_length:
        ValueError(
            f'Sua senha deve conter pelo menos {password_min_length} caracteres.'
        )

    return password
