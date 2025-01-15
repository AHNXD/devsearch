from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

from django.db.models import Q
from .utils import searchProfiles, paginateProfiles

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # the commit false mean the user will not be saved to the database
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, "User account Created!")
            login(request, user)
            return redirect('account')
            #return redirect("Login")
        else:
            messages.error(request, "An error!")
    
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def loginUser(request):
    page = 'login'
    context = {'page': page}
    
    if request.user.is_authenticated:
        return redirect('Profiles')
    
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User name dosnt exist!')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Welecom!")
            return redirect(request.GET['next'] if 'next' in request.GET else 'Profiles')
        else:
            messages.error(request, 'Username or Password is incorrect')
            
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, "Loged out!")
    return redirect("Login")

def profile(request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles, paginator = paginateProfiles(request, profiles, 6)

    context = {'profiles' : profiles, 'search_query': search_query, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'users/profile.html', context)

def userProfile(request, id):
    profile = Profile.objects.get(id=id)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    projects = profile.project_set.all()
    context = {'profile':profile, 'projects':projects, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='Login')
def userAccount(requset):
    profile = requset.user.profile
    projects = profile.project_set.all()
    
    context = {'profile':profile, 'projects':projects}
    return render(requset, 'users/account.html', context)

@login_required(login_url='Login')
def editAccount(request): 
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated!")
            return redirect('EditAccount')
    context = {'form': form}
    return render(request, "users/profile_form.html", context)

@login_required(login_url='Login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False) 
            skill.owner = profile
            skill.save()
            return redirect('Account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='Login')
def deleteSkill(request,id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=id)
    if request.method == 'POST':
        skill.delete()
        return redirect('Account')
    context = {'skill': skill}
    return render(request, 'users/delete_skill.html', context)

@login_required(login_url='Login')
def updateSkill(request,id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=id)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save() 
            return redirect('Account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='Login')
def inbox(request):
    profile = request.user.profile
    userMessages = profile.messages.all()
    unreadCount = userMessages.filter(is_read=False).count()
    context = {'userMessages':userMessages, "unreadCount":unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='Login')
def viewMessage(request, id):
    profile = request.user.profile
    message = profile.messages.get(id=id)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)

@login_required(login_url='Login')
def sendMessage(request, receiver_id):
    profile = request.user.profile
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = profile
            receiver_profile = Profile.objects.get(id=receiver_id)
            message.receiver = receiver_profile
            message.save()
            return redirect('UserProfile', {'profile':receiver_profile})
            
    
    context = {'form':form,"receiver_id":receiver_id}
    return render(request, 'users/message_form.html', context)
    