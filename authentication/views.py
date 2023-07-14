from django.shortcuts import render, redirect
from .service import check_user_ldap
from .models import User
from .forms import LDAPLoginForm


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LDAPLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            username = str(username).lower()
            password = form.cleaned_data.get('password')
            authorise = check_user_ldap(username, password)
            if authorise:
                specific_user = User.objects.filter(username=username)

                if specific_user:
                    request.session['user_session'] = True
                    print('CONNECTED')
                    return redirect('home:index')
                else:
                    print("CAN'T CONNECTED because not in DB")
                    return redirect('auth:login')
            else:
                print("CAN'T CONNECTED because not in LDAP")
                return redirect('auth:login')
        else:
            print("CAN'T CONNECTED because champs INVALID")
            return redirect('auth:login')
    else:
        if request.session.get('user_session', True):
            return redirect('home:index')
        else:
            form = LDAPLoginForm()

    context = {
        'form': form
    }

    return render(request, 'authentication/login.html', context)


def logout_view(request):
    request.session["user_session"] = False
    return redirect('auth:login')
