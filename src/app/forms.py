_email_field = {
    "id": "email",
    "name": "email",
    "type": "email",
    "autocomplete": "email",
    "label": "Електронна пошта"
}

_password_field = {
    "id": "password",
    "name": "password",
    "type": "password",
    "autocomplete": "current-password",
    "label": "Пароль"
}

user_roles = {
    "Волонтер": "volunteer",
    "Організація": "organization"
}

login_form = {
    "email": _email_field,
    "password": _password_field
}

register_form = {
    "email": _email_field,
    "password": _password_field,
    "password_confirm": {
        "id": "password_confirm",
        "name": "password_confirm",
        "type": "password",
        "autocomplete": "",
        "label": "Повторіть пароль"
    },
    "user_role": {
        "id": "user_role",
        "name": "user_role",
        "label": "Роль",
        "options": user_roles
    }
}
