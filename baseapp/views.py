from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EmailUserCreationForm
# Create your views here.
from django.views.generic.base import View

User = get_user_model()


class InterestsView(View):
    def get(self, request, username=None):
        user = request.user
        if username:
            owner = get_object_or_404(User, username=username)
        elif not user.is_authenticated:
            return redirect('login')
        else:
            owner = user
        can_modify = False

        # if user.is_authenticated or True:
        #    print(request.session.get_expiry_age())

        if user.pk == owner.pk:
            can_modify = True

        context = {
            'owner': owner,
            'can_modify': can_modify,
        }
        return render(request, 'baseapp/interests.html', context)


class RememberLoginView(LoginView):
    def form_valid(self, form):
        if self.request.POST.get('remember_me', False):  # don't remember me I am sorry
            self.request.session.set_expiry(60 * 60 * 1)
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class SignUpView(View):
    def get(self, request):
        context = {
            "form": EmailUserCreationForm,
        }

        return render(request, 'registration/signup.html', context)

    def post(self, request):
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            context = {
                "form": form,
            }
        return render(request, 'registration/signup.html', context)