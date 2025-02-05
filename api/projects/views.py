from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from ..serializers import ProjectSerializer
from projects.models import Project, Tag
from rest_framework import status
from ..utils import searchProjects, paginateLogic

#-----Project-----
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    try:
        # Search and paginate projects
        projects, search_query = searchProjects(request)
        range, projects, paginator = paginateLogic(request, projects, request.GET.get('in_page', 6))
        
        # Serialize the projects
        serializer = ProjectSerializer(projects, many=True)
        
        # Prepare the response
        context = {
            'state': True,
            'msg': 'Projects loaded successfully',
            'data': {
                'projects': serializer.data,
                'search_query': search_query,
                'paginator': {
                    'num_pages': paginator.num_pages,
                    'current_page': projects.number,
                    'range': list(range)
                }
            }
        }
        return Response(context, status=status.HTTP_200_OK)
    
    except Exception as e:
        context = {
            'state': False,
            'msg': str(e)
        }
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProject(request, id):
    try:
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project, many=False)
        
        context = {
            'state': True,
            'msg': 'Project loaded successfully',
            'data': {
                'project': serializer.data
            }
        }
        return Response(context, status=status.HTTP_200_OK)
    
    except Project.DoesNotExist:
        context = {
            'state': False,
            'msg': 'Project not found'
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        context = {
            'state': False,
            'msg': str(e)
        }
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def createProject(request):
    profile = request.user.profile
    data = request.data

    try:
        # Handle tags (if provided)
        new_tags = data.get('newTags', '')
        tags = [tag.strip() for tag in new_tags.replace(",", " ").split()] if new_tags else []

        # Create the project
        serializer = ProjectSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            project = serializer.save(owner=profile)

            # Add tags to the project
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                project.tags.add(tag)

            context = {
                'state': True,
                'msg': 'Project created successfully',
                'data': serializer.data
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                'state': False,
                'msg': 'Validation error',
                'errors': serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        context = {
            'state': False,
            'msg': str(e)
        }
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def updateProject(request, id):
    profile = request.user.profile

    try:
        project = profile.project_set.get(id=id)
        data = request.data

        # Handle tags (if provided)
        new_tags = data.get('newTags', '')
        tags = [tag.strip() for tag in new_tags.replace(",", " ").split()] if new_tags else []

        # Update the project
        serializer = ProjectSerializer(project, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_project = serializer.save()

            # Clear existing tags and add new ones
            updated_project.tags.clear()
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                updated_project.tags.add(tag)

            context = {
                'state': True,
                'msg': 'Project updated successfully',
                'data': serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                'state': False,
                'msg': 'Validation error',
                'errors': serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        context = {
            'state': False,
            'msg': 'Project not found'
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        context = {
            'state': False,
            'msg': str(e)
        }
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProject(request, id):
    try:
        user = request.user.profile
        project = user.project_set.get(id=id)
        
        # Serialize the project before deleting it
        serializer = ProjectSerializer(project, many=False)
        project.delete()
        
        context = {
            'state': True,
            'msg': 'Project deleted successfully',
            'data': {
                'project': serializer.data
            }
        }
        return Response(context, status=status.HTTP_200_OK)
    
    except Project.DoesNotExist:
        context = {
            'state': False,
            'msg': 'Project not found'
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        context = {
            'state': False,
            'msg': str(e)
        }
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeTag(request):
    try:
        tag_id = request.data.get('tag')
        project_id = request.data.get('project')

        if not tag_id or not project_id:
            context = {
                'state': False,
                'msg': 'Both tag ID and project ID are required'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        project = Project.objects.get(id=project_id)
        tag = Tag.objects.get(id=tag_id)

        # Remove the tag from the project
        project.tags.remove(tag)
        
        # Serialize the updated project
        serializer = ProjectSerializer(project, many=False)
        
        context = {
            'state': True,
            'msg': 'Tag removed successfully',
            'data': {
                'project': serializer.data
            }
        }
        return Response(context, status=status.HTTP_200_OK)
    
    except Project.DoesNotExist:
        context = {
            'state': False,
            'msg': 'Project not found'
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    except Tag.DoesNotExist:
        context = {
            'state': False,
            'msg': 'Tag not found'
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        context = {
            'state': False,
            'msg': str(e)
        }
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)