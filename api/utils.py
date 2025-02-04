from users.models import Profile, Skill
from projects.models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateLogic(request, dataset, result):
    page = request.GET.get('page', 1)
    paginator = Paginator(dataset, result)
    
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        dataset = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        dataset = paginator.page(page)
        
    scr_range = range(1, paginator.num_pages + 1)
    
    return scr_range, dataset, paginator

def searchProfiles(request):
    search_query = ''
    
    if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')
            
    skills = Skill.objects.filter(name__icontains=search_query)
    
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills))
    
    return profiles, search_query

def searchProjects(request):
    search_query = ''
    
    if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')
            
    tags = Tag.objects.filter(name__icontains=search_query)
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags))

    return projects, search_query

def paginateProjects(request, projects, result):
    page = request.GET.get('page', 1)
    paginator = Paginator(projects, result)
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
        
    scr_range = range(1, paginator.num_pages + 1)
    
    return scr_range, projects, paginator
    