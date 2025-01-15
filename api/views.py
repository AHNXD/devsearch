from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer, ProfileSerializer
from projects.models import Project, Review, Tag
from users.models import Profile
from rest_framework import status

@api_view(['GET'])
def getRoutes(request):
    
    routes = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},
        {'POST':'api/projects/id/vote'},
        {'POST':'api/users/token'},   
        {'POST':'api/users/token/refresh'}
    ]
    
    return Response(routes)

#-----Auth-----
@api_view(['POST'])
def createAccount(request):
    data = request.data
    
    profile = Profile(
        name=data.get('name'),
        username=data.get('username'),
        location=data.get('location'),
        email=data.get('email'),
        short_intro=data.get('short_intro'),
        bio=data.get('bio'),
        social_github=data.get('social_github'),
        social_linkedin=data.get('social_linkedin'),
        social_youtube=data.get('social_youtube'),
        social_website=data.get('social_website'),
    )
    try:
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response({'state': True,'msg':'created', 'profile':serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'state': False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#-----Project-----
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    print('User:', request.user)
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProject(request, id):
    print('User:', request.user)
    projects = Project.objects.get(id=id)
    serializer = ProjectSerializer(projects, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, id):
    project = Project.objects.get(id=id)
    user = request.user.profile
    data = request.data
    
    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,

    )
    
    review.value =  data['value']
    review.body = data['body']
    
    review.save()
    
    project.getVoteCount
    
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removeTag(request, id):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)

    return Response('Tag was deleted!')