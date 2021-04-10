from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import GroupSerializer, UserSerializer
from .models import Group, User
from rest_framework import status
import json
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
@api_view(["GET"])
@csrf_exempt
def get_groups(user_request):
    user_payload = json.loads(user_request.body)
    user = User.objects.get(user_id=user_payload["user_id"])
    groups = user.groups
    serializer = GroupSerializer(groups, many=True)
    return JsonResponse({'groups': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
@csrf_exempt
def get_user_details(user_request):
    user_payload = json.loads(user_request.body)
    user = User.objects.get(user_id=user_payload["user_id"])
    serializer = UserSerializer(user)
    return JsonResponse({'user': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
def associate_user_to_group(request):
    payload = json.loads(request.body)
    user = User.objects.get(user_id=payload["user_id"])
    group = Group.objects.get(group_name=payload["group_name"])
    user.groups.add(group)
    serializer = GroupSerializer(group)
    return JsonResponse({'groups': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
def create_user(request):
    try:
        payload = json.loads(request.body)
        first_name = payload["first_name"]
        last_name = payload["last_name"]
        fname = User.objects.get(first_name=first_name)
        lname =User.objects.get(last_name=last_name)
        user = User(first_name=first_name, last_name=last_name)
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse({'user': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except:
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@csrf_exempt
def create_group(request):
    try:
        payload = json.loads(request.body)
        group_name = payload["group_name"]
        group = Group(group_name=group_name)
        group.save()
        serializer = GroupSerializer(group)
        return JsonResponse({'group': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except:
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
@csrf_exempt
def update_user(request,user_id):
    payload = json.loads(request.body)
    try:
        user_item=User.objects.get(user_id=user_id)
        user_item.first_name=payload["first_name"]
        user_item.last_name=payload["last_name"]
        user_item.save()
        user = User.objects.get(user_id=user_id)
        serializer = UserSerializer(user)
        return JsonResponse({'user': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@csrf_exempt
def update_group(request,group_id):
    payload = json.loads(request.body)
    try:
        group_item=Group.objects.get(group_id=group_id)
        group_item.group_name=payload["group_name"]
        group_item.save()
        group = Group.objects.get(group_id=group_id)
        serializer = GroupSerializer(group)
        return JsonResponse({'group': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
@api_view(["DELETE"])
@csrf_exempt
def delete_user(request,user_id):
    try:
        user = User.objects.get(user_id=user_id)
        user.delete()
        return JsonResponse({'message': 'Deleted successfully'},safe=False,status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@csrf_exempt
def delete_group(request,group_id):
    try:
        group = Group.objects.get(group_id=group_id)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
