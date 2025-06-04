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

create_event_form = {
    "title": {
        "id": "title",
        "name": "title",
        "type": "text",
        "autocomplete": "",
        "label": "Назва події"
    },
    "description": {
        "id": "description",
        "name": "description",
        "type": "text",
        "autocomplete": "",
        "label": "Деталі події"
    },
    "date": {
        "id": "date",
        "name": "date",
        "type": "date",
        "autocomplete": "",
        "label": "Дата події"
    },
    "location": {
        "id": "location",
        "name": "location",
        "type": "text",
        "autocomplete": "",
        "label": "Місце події"
    },
    "categories": {
        "id": "categories",
        "name": "categories",
        "type": "text",
        "autocomplete": "",
        "label": "#Категорії"
    },
}

register_event_form = {
    "name": {
        "id": "name",
        "name": "name",
        "type": "text",
        "autocomplete": "",
        "label": "Ім'я"
    },
    "surname": {
        "id": "surname",
        "name": "surname",
        "type": "text",
        "autocomplete": "",
        "label": "Прізвище"
    },
    "phone": {
        "id": "phone",
        "name": "phone",
        "type": "tel",
        "autocomplete": "",
        "label": "Ваш телефон"
    },
    "location": {
        "id": "location",
        "name": "location",
        "type": "text",
        "autocomplete": "",
        "label": "Ваша локація"
    }
}

statuses = {
    "pending": "Очікується",
    "confirmed": "Підтверджено",
    "cancelled": "Відхилено"
}
