from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

def paginateProfiles(request, profiles, result):
    page = request.GET.get('page')
    paginator = Paginator(profiles, result)
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
        
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 4)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
        
    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles, paginator
    