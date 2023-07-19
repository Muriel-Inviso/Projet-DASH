from datetime import timedelta
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import User
from .forms import LDAPLoginForm
from .service import check_user_ldap


def login_view(request):
    if request.method == 'POST':
        form = LDAPLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            username = str(username).lower()
            password = form.cleaned_data.get('password')

            # Check if the username exists in the local SQLite database
            specific_user = User.objects.filter(username=username)
            if specific_user:
                # If the user exists in the local database, check LDAP credentials
                authorise = check_user_ldap(username, password)
                if authorise:
                    # If LDAP credentials are valid, create a session for the user
                    request.session['user_session'] = True

                    # Set the session expiration time to 15 minutes (adjust as needed)
                    request.session.set_expiry(timedelta(minutes=15).total_seconds())

                    return redirect('home:index')
                else:
                    # Invalid LDAP credentials, do not create a session
                    return redirect('auth:login')
            else:
                # User not found in the local database, do not create a session
                return redirect('auth:login')
        else:
            # Form validation failed, do not create a session
            return redirect('auth:login')
    else:
        if request.session.get('user_session', False):
            # If the user is already authenticated, update the session expiration
            request.session.update_expiry(timedelta(minutes=15).total_seconds())
            return redirect('home:index')
        else:
            form = LDAPLoginForm()

    context = {
        'form': form
    }

    return render(request, 'authentication/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('auth:login')
