from fastapi import status
from fastapi.testclient import TestClient

from api.user.dto.create_user_dto import CreateUserDTO
from api.user.user_repository import UserRepository


create_user_dto = CreateUserDTO(
    name='Davi', email='validteste@email.com', password='validpass'
)


def test_sign_up_missing_fields(client: TestClient):
    response = client.post('/users/sign-up', json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()
    assert data is not None

    detail: dict = data.get('detail')
    assert len(detail) == 3
    assert detail[0].get('type') == 'missing'
    assert detail[0].get('loc')[1] == 'name'

    assert detail[1].get('type') == 'missing'
    assert detail[1].get('loc')[1] == 'email'

    assert detail[2].get('type') == 'missing'
    assert detail[2].get('loc')[1] == 'password'


def test_sign_up_invalid_email(client: TestClient):
    payload = create_user_dto.model_dump()
    payload.update({'email': 'jorjao'})

    response = client.post('/users/sign-up', json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()
    assert data is not None

    detail: dict = data.get('detail')
    assert len(detail) == 1

    assert detail[0].get('type') == 'value_error'
    assert detail[0].get('loc')[1] == 'email'


def test_sign_up_password_blank(client: TestClient):
    payload = create_user_dto.model_dump()
    payload.update({'password': ''})

    response = client.post('/users/sign-up', json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()
    assert data is not None

    detail: dict = data.get('detail')
    assert len(detail) == 1

    assert detail[0].get('type') == 'value_error'
    assert detail[0].get('loc')[1] == 'password'


def test_sign_up_password_is_to_short(client: TestClient):
    payload = create_user_dto.model_dump()
    payload.update({'password': '132'})

    response = client.post('/users/sign-up', json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()
    assert data is not None

    detail: dict = data.get('detail')
    assert len(detail) == 1

    assert detail[0].get('type') == 'value_error'
    assert detail[0].get('loc')[1] == 'password'


def test_sign_up_email_already_exists(client: TestClient, user_repository: UserRepository):
    email = 'admin@email.com'
    user_in_db = user_repository.find_by_email(email)

    assert user_in_db is not None

    payload = create_user_dto.model_dump()
    payload.update({'email': email})

    response = client.post('/users/sign-up', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    assert data is not None

    detail: dict = data.get('detail')
    assert detail is not None
    assert detail == 'Usuário já cadastrado com esse email.'

def test_sign_up_successfully(client: TestClient, user_repository: UserRepository):
    payload = create_user_dto.model_dump()
    response = client.post('/users/sign-up', json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data is not None

    detail: dict = data.get('detail')
    assert detail is not None
    assert detail == 'Usuário cadastrado com sucesso.'

    sign_up_user = user_repository.find_by_email(create_user_dto.email)

    assert sign_up_user is not None
    assert sign_up_user.id is not None
    assert sign_up_user.check_password(create_user_dto.password) is True
