from .models import Box
from .filters import BoxFilter
from django.core.exceptions import ObjectDoesNotExist
from .serializers import BoxSerializer,AdminBoxSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes , authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .Validation import check_validity

'''
Create new Box api
'''
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def create_box(request):
    box = Box(created_by=request.user)
    data = JSONParser().parse(request)
    serializer = AdminBoxSerializer(box, data=data,partial=True)
    if serializer.is_valid() and check_validity(request.user):
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
List All box api
'''
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def list_box(request):
    box_queryset = Box.objects.all()
    boxes = BoxFilter(request.GET,queryset=box_queryset).qs
    serializer = BoxSerializer(boxes, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


'''
List my boxes api 
'''
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def my_list_box(request):
    box_queryset = Box.objects.filter(created_by=request.user)
    boxes = BoxFilter(request.GET,queryset=box_queryset).qs
    serializer = AdminBoxSerializer(boxes, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

'''
Update box with given id
'''
@api_view(['PUT'])
@permission_classes([IsAdminUser])
@authentication_classes([TokenAuthentication])
def update_box(request,pk):
    try:
        box = Box.objects.get(pk=pk)
    except Box.DoesNotExist:
        data = dict()
        data["reason"] = "Box does not Exist"
        return Response(data,status=status.HTTP_404_NOT_FOUND)

    data = JSONParser().parse(request)
    serializer = AdminBoxSerializer(box, data=data,partial=True)
    if serializer.is_valid() and check_validity(request.user):
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
Delete box with given id
'''
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@authentication_classes([TokenAuthentication])
def delete_box(request,pk):
    try:
        box = Box.objects.get(pk=pk)
        if request.user == box.created_by :
            box.delete()
        else:
            data = dict()
            data['reason'] = "You must be creator of the Box."
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    except Box.DoesNotExist:
        data = dict()
        data["reason"] = "Box does not Exist"
        return Response(data,status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




