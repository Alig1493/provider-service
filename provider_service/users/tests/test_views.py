import pytest
from django.urls import reverse

from provider_service.extra.tests.factories import CurrencyFactory, LanguageFactory
from .factories import fake, User, UserFactory


class TestRegistration:
    url = reverse("v1:users:rest_register")
    test_password = "test_pass"
    phone_number = fake.phone_number()
    language = None
    currency = None

    @pytest.fixture
    def register_data(self, db):
        self.language = LanguageFactory()
        self.currency = CurrencyFactory()
        data = {
            "email": fake.email(),
            "name": fake.name(),
            "phone_number": self.phone_number,
            "currency": self.currency.name,
            "language": self.language.name,
            "password1": self.test_password,
            "password2": self.test_password,
        }
        return data

    def test_user_registration_success(self, client, register_data, db):
        request = client.post(self.url, register_data)
        user = User.objects.filter(id=request.data["user"]["id"],
                                   phone_number=self.phone_number,
                                   language=self.language,
                                   currency=self.currency,
                                   is_active=True)

        assert request.status_code == 201
        assert user.exists()
        assert user[0].check_password(self.test_password)

    def test_password_mismatch(self, client, register_data, db):
        register_data["password2"] = fake.word()

        request = client.post(self.url, register_data)

        assert request.status_code == 400

    def test_unique_email(self, client, register_data, db):
        UserFactory(email=register_data["email"])

        request = client.post(self.url, register_data)

        assert request.status_code == 400


class TestLogin:

    url = reverse("v1:users:rest_login")
    password = "test_pass"

    def test_login(self, user, client):

        assert user.check_password(self.password)

        data = {
            "email": user.email,
            "password": self.password
        }

        request = client.post(self.url, data)

        assert request.status_code == 200
        assert request.data["user"]["email"] in user.email

    def test_wrong_email_login(self, user, client):

        data = {
            "email": fake.email(),
            "password": self.password
        }

        request = client.post(self.url, data)

        assert request.status_code == 404

    def test_wrong_password_login(self, user, client):

        data = {
            "password": fake.word()
        }

        request = client.post(self.url, data)

        assert request.status_code == 400


class TestLogout:

    url = reverse("v1:users:rest_logout")

    def test_logout(self, auth_client):

        request = auth_client.post(self.url)

        assert request.status_code == 200


class TestUserDetails:

    url = reverse("v1:users:details")

    def test_retrieve_user_details(self, auth_client, user):
        request = auth_client.get(self.url)

        assert request.status_code == 200
        assert user.name == request.data.get("name")
        assert user.phone_number == request.data.get("phone_number")
        assert user.email == request.data.get("email")
        assert user.language.name == request.data.get("language")
        assert user.currency.name == request.data.get("currency")

    def test_patch_user_details(self, auth_client, user):
        language = LanguageFactory(name="en_uk")
        assert not user.language.name == language.name

        patch_data = {
            "language": language.name
        }

        request = auth_client.patch(self.url, data=patch_data)

        user.refresh_from_db()
        assert request.status_code == 200
        assert user.language.name == language.name

    def test_delete_user(self, auth_client, user):
        user_id = user.id

        request = auth_client.delete(self.url)

        assert request.status_code == 204
        assert not User.objects.filter(id=user_id).count()
