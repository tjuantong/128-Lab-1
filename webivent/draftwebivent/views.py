from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from draftwebivent.forms import RegistrationForm, UserProfileForm, EditProfileForm, EditUserProfileForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'draftwebivent/homePage.html')

def typeUser(request):
    return render(request, 'draftwebivent/typeUser.html')

def web(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
 
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)   #assign user to profile.user
            profile.user = user                         #associate all info to the user (one-to-one field)
            profile.save()
            messages.success(request, "Account successfully created.")
            return redirect('/login')

        else:
            form = RegistrationForm(request.POST)
            profile_form = UserProfileForm(request.POST)

            args = {'form': form, 'profile_form': profile_form}
            return render(request, 'draftwebivent/web.html', args)
        
    else:
        form = RegistrationForm()
        profile_form = UserProfileForm()

        args = {'form': form, 'profile_form': profile_form} #can refer the form to the template
        
        return render(request, 'draftwebivent/web.html', args)


def loginPage(request):
    return render(request, 'draftwebivent/login.html')


def login(request):
    if request.method == "POST":
        user_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=user_name, password=password)

        if user is not None:
            request.session['username'] = user_name   #for login redirect in session timeout         
            auth.login(request, user)
            args = {'user': request.user, 'name': request.session['username']}
            return redirect('/userdashboard')

        else:
            messages.error(request, 'Invalid username or password. Please input valid details.')
            return redirect('login')

    else:
        
        return render(request, 'draftwebivent/login.html')

#import login_required decorator
#will redirect user to login page with LOGIN_URL if user isn't logged in and would try to access the logout page
@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Successfully logged out.')
    return render(request, 'draftwebivent/logout.html')

def userdashboard(request):
    if 'username' in request.session:
        args = {'user': request.user}
        return render(request, 'draftwebivent/userdashboard.html', args)
    else:
        return render(request, 'draftwebivent/logout.html')
    

def myProfile(request):
    if 'username' in request.session:
        return render(request, 'draftwebivent/myProfile.html')
    else:
        return render(request, 'draftwebivent/logout.html')

def saveProfile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = EditUserProfileForm(request.POST, instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save()
            return redirect('/myProfile')
            
        else:
            messages.info(request, 'input required fields')
            return redirect('editProfile')

    else:

        form = EditProfileForm(instance=request.user)
        profile_form = EditUserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'draftwebivent/editProfile.html')
   

def editProfile(request):
    if 'username' in request.session:
        if request.method == "POST":
            form = EditProfileForm(request.POST, instance=request.user)
            profile_form = EditUserProfileForm(request.POST, instance=request.user.userprofile)

            if form.is_valid() and profile_form.is_valid():
                user = form.save()
                profile = profile_form.save()

                return redirect('/myProfile')
                
            else:
                messages.info(request, 'invalid credentials')
                return redirect('editProfile')

        else:
            form = EditProfileForm(instance=request.user)
            profile_form = EditUserProfileForm(instance=request.user.userprofile)

        context = {
                    'form': form,
                    'profile_form': profile_form
        }

        return render(request, 'draftwebivent/editProfile.html', context)
    
    else:
         return render(request, 'draftwebivent/logout.html')
