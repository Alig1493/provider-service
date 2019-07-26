from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError

from provider_service.extra.models import Language, Currency

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    language = serializers.SlugRelatedField(slug_field="name", queryset=Language.objects.all())
    currency = serializers.SlugRelatedField(slug_field="name", queryset=Currency.objects.all())
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2",
                  "phone_number", "language", "currency"]

    def validate_email(self, email):
        return get_adapter().validate_unique_email(email)

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def save(self, request):
        password = self.validated_data.pop("password1", None)
        self.validated_data.pop("password2", None)
        user = User.objects.create(**self.validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def _validate_email(self, email, password):
        # Should return 404 if no user found with this email
        # This is intentional as per requirements and specification
        user = get_object_or_404(User, email__iexact=email)
        if user and user.check_password(password):
            return user

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = self._validate_email(email, password)
        else:
            msg = _("Must include 'email' and 'password'.")
            raise ValidationError(msg)

        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise ValidationError(msg)

        if not user.is_active:
            msg = _("User account is disabled.")
            raise ValidationError(msg)

        # Everything passed. That means password is accepted. So return the user
        attrs["user"] = user
        return attrs


class UserDetailsSerializer(ModelSerializer):
    language = serializers.SlugRelatedField(slug_field="name", queryset=Language.objects.all())
    currency = serializers.SlugRelatedField(slug_field="name", queryset=Currency.objects.all())

    class Meta:
        model = User
        fields = ("id", "name", "phone_number", "email",
                  "language", "currency", "is_superuser")
        read_only_fields = ("id", "is_superuser",)


class UserPublicSerializer(ModelSerializer):

    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = ("id", "name", "email")
