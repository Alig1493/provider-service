from django.conf.urls import url, include

from provider_service.users.views import UserDetailsView

app_name = "users"

urlpatterns = [
    url(r"^", include("rest_auth.urls")),
    url(r"^registration/", include("rest_auth.registration.urls")),
    url(r"^details/", UserDetailsView.as_view(), name="details"),
]
