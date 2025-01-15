from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from .utils import searchProjects, paginateProjects



def projects(request):
    # return HttpResponse('Here are some projects')
    projects, search_query = searchProjects(request) 
    
    custom_range, projects, paginator = paginateProjects(request, projects, 6)
    
    context = {'projects': projects, 'search_query': search_query, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, id):
    #return HttpResponse('Single project ' + str(id))
    # project = None
    # for p in projectsList:
    #     if p['id'] is id:
    #         project = p
    form = ReviewForm()
    project = Project.objects.get(id=id)
    tags = project.tags.all()
    reviews = project.review_set.all()
    context = {'project': project,
                'tags': tags,
                'reviews': reviews,
                'form' : form
            }
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        project.getVoteCount
        messages.success(request, 'Review Added!')
        
        
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="Login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False) 
            project.owner = profile
            project.save()
            return redirect('Account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="Login")
def updateProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newTags = request.POST.get('newTags').replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('Account')
    context = {'form': form, 'project': project}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="Login")
def deleteProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('Projects')
    context = {'project': project}
    return render(request, 'projects/delete_project.html', context)

@login_required(login_url="Login")
def removeTag(request, p_id, t_id):

    project = Project.objects.get(id=p_id)
    tag = Tag.objects.get(id=t_id)

    project.tags.remove(tag)
    form = ProjectForm(instance=project)
    context = {'form': form, 'project': project}
    return redirect('UpdateProject',project.id)