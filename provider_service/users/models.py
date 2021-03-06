from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

from provider_service.extra.models import Language, Currency
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.
    Email and password are required. Other fields are optional.
    A more descriptive tutorial can be found here
    http://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/
    """
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    name = models.CharField(_("name"), max_length=128, blank=True)
    phone_number = models.CharField(_("phone"), max_length=128, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, blank=True, null=True)
    is_staff = models.BooleanField(_("staff status"), default=False,
                                   help_text=_("Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(_("active"), default=True,
                                    help_text=_("Designates whether this user should be treated as active. "
                                                "Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.name
