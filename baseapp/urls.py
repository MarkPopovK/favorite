from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView, RedirectView
# from .views import HomeView
from .views import InterestsView, RememberLoginView, SignUpView, EditInterested
from .forms import RememberAuthForm

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('self_interests')), name='home'),
    path('interests/', InterestsView.as_view(), name='self_interests'),
    path('interests/<str:username>', InterestsView.as_view(), name='interests'),
    path('login/', RememberLoginView.as_view(form_class=RememberAuthForm, redirect_authenticated_user=True), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit_interested/', EditInterested.as_view(), name='edit_interested')
]
