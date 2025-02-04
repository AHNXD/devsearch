from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from ..serializers import ProjectSerializer, ProfileSerializer, SkillsSerializer, MessageSerializer
from projects.models import Project, Review
from users.models import Profile, Skill, Message
from rest_framework import status
from ..utils import searchProfiles, paginateLogic

#-----Auth-----
@api_view(['POST'])
def createAccount(request):
    data = request.data
    
    try:
        profile = Profile.objects.create(
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
        serializer = ProfileSerializer(profile)
        context = {'state': True, 'msg': 'Account created successfully', 'profile': serializer.data}
        return Response(context, status=status.HTTP_201_CREATED)
    except Exception as e:
        context = {'state': False, 'msg': str(e)}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    if hasattr(request.user.auth_token, 'delete'):
        request.user.auth_token.delete()
        
    context = {
                'state': True,
                'msg': 'Loged Out!',
            }
    return Response(context)
#-----User-----
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, id):
    try:
        project = Project.objects.get(id=id)
        user = request.user.profile
        data = request.data
        
        review, created = Review.objects.get_or_create(
            owner=user,
            project=project,
        )
        
        review.value = data['value']
        review.body = data['body']
        review.save()
        
        project.getVoteCount
        
        serializer = ProjectSerializer(project, many=False)
        context = {'state': True, 'msg': 'Vote added successfully', 'project': serializer.data}
        return Response(context)
    except Project.DoesNotExist:
        return Response({'state': False, 'msg': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'state': False, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    range, profiles, paginator = paginateLogic(request, profiles, request.GET.get('in_page', 6))
    
    serializer = ProfileSerializer(profiles, many=True)
    
    context = {
                'state': True,
                'msg': '',
                'data': {
                    'profiles' : serializer.data,
                    'search_query': search_query, 
                    'paginator': {
                        'num_pages': paginator.num_pages,
                        'current_page': profiles.number,
                        'range': list(range)
                    },
                }
            }
    return Response(context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
        profile_serializer = ProfileSerializer(profile, many=False)
        topSkills = SkillsSerializer(profile.skill_set.exclude(description__exact=""), many=True)
        otherSkills = SkillsSerializer(profile.skill_set.filter(description=""), many=True)
        projects = ProjectSerializer(profile.project_set.all(), many=True)
        
        context = {
            'state': True,
            'msg': '',
            "data": {
                'profile': profile_serializer.data, 
                'projects': projects.data, 
                'topSkills': topSkills.data, 
                'otherSkills': otherSkills.data
            }
        }
        return Response(context)
    except Profile.DoesNotExist:
        return Response({'state': False, 'msg': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userAccount(requset):
    profile = ProfileSerializer(requset.user.profile, many=False)
    projects = ProjectSerializer(profile.project_set.all(), many=True)
    
    context = {
            'state': True,
            'msg': '',
            "data": {
                'profile':profile, 
                'projects':projects
            }
    }
    return Response(context)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def editAccount(request): 
    profile = request.user.profile
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        context = {
            'state': True,
            'msg': 'Profile updated successfully',
            "data": {
                'profile': serializer.data, 
            }
        }
        return Response(context)
    else:
        context = {
            'state': False,
            'msg': 'Validation error',
            'errors': serializer.errors
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSkill(request):
    profile = request.user.profile
    serializer = SkillsSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(owner=profile)
        context = {
            'state': True,
            'msg': 'Skill created successfully',
            'data': {
                'skill': serializer.data
            }
        }
        return Response(context, status=status.HTTP_201_CREATED)
    else:
        context = {
            'state': False,
            'msg': 'Validation error',
            'errors': serializer.errors
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteSkill(request,id):
    profile = request.user.profile
    try:
        skill = profile.skill_set.get(id=id)
        skill.delete()
        context = {
            'state': True,
            'msg': 'Skill deleted successfully',
        }
        return Response(context)
    except Skill.DoesNotExist:
        return Response({'state': False, 'msg': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateSkill(request,id):
    profile = request.user.profile
    try:
        skill = profile.skill_set.get(id=id)
        serializer = SkillsSerializer(skill, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            context = {
                'state': True,
                'msg': 'Skill updated successfully',
                "data": {
                    'skill': serializer.data, 
                }
            }
            return Response(context)
        else:
            context = {
                'state': False,
                'msg': 'Validation error',
                'errors': serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    except Skill.DoesNotExist:
        return Response({'state': False, 'msg': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inbox(request):
    profile = request.user.profile
    userMessages = profile.messages.all()
    serializer = MessageSerializer(userMessages, many=True)
    unreadCount = userMessages.filter(is_read=False).count()
    
    context = {
        'state': True,
        'msg': '',
        'data': {
            'userMessages': serializer.data, 
            "unreadCount": unreadCount
        }
    }
    return Response(context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def viewMessage(request, id):
    profile = request.user.profile
    try:
        message = profile.messages.get(id=id)
        if not message.is_read:
            message.is_read = True
            message.save()
        serializer = MessageSerializer(message, many=False)
        context = { 
            'state': True,
            'msg': '',
            'data': {
                'message': serializer.data
            }
        }
        return Response(context)
    except Message.DoesNotExist:
        return Response({'state': False, 'msg': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendMessage(request, receiver_id):
    profile = request.user.profile
    try:
        receiver = Profile.objects.get(id=receiver_id)
        serializer = MessageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(sender=profile, receiver=receiver)
            context = {
                'state': True,
                'msg': 'Message sent successfully',
                'data': {
                    'message': serializer.data
                }
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                'state': False,
                'msg': 'Validation error',
                'errors': serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        return Response({'state': False, 'msg': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)
