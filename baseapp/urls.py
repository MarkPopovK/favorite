from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from .views import InterestsView, RememberLoginView
from .forms import RememberAuthForm

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('self_interests')), name='home'),
    path('interests/', InterestsView.as_view(), name='self_interests'),
    path('interests/<str:username>', InterestsView.as_view(), name='interests'),
    path('login/', RememberLoginView.as_view(form_class=RememberAuthForm, redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
