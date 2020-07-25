from django.shortcuts import render
from django.views import View
from .models import Box,UserAuthentication
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import decimal 
from .filters import BoxFilter
from django.db.models import Avg
from spinny_project.settings import A1 , V1 , L1 , L2 , InvalidInputException , LoginRequiredException, PermissionDeniedException
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist

@method_decorator(csrf_exempt, name='dispatch')
class AuthTokenInterface(View):

    def post(self,request):
        result = dict()
        status = 200

        
        try :
            post_data = json.loads(request.body)
            username = post_data['username']
            password = post_data['password']
            user = authenticate(username=username,password=password)
            if user :
                auth, created = UserAuthentication.objects.get_or_create(user=user)
                auth.auth_token = get_random_string(32)
                auth.save()
                result['auth-token'] = auth.auth_token
                result['message'] = "User Logged in Successfully"
                result['status'] = status

        except KeyError as ke:
            status = 500
            result['message'] = "User Login Failed"
            result['error_reason'] = "Required Fields Missing"
            result['status'] = status

        except Exception as e:
            status = 500
            result['message'] = "User Login Failed"
            result['error_reason'] = str(e)
            result['status'] = status

        return JsonResponse(result,status = result['status'])



@method_decorator(csrf_exempt, name='dispatch')
class BoxView(View):

    @staticmethod
    def check_validity(user):
        if Box.objects.all().count() == 0 :
            return True

        area = Box.objects.all().aggregate(Avg('area'))
        print(area)
        if area['area__avg'] > A1 :
            return False

        volume =  Box.objects.all().aggregate(Avg('volume'))
        print(volume)
        if volume['volume__avg'] > V1 :
            return False

        datetime_one_week_ago = timezone.now().date() - timedelta(days=7)

        boxes_last_week = Box.objects.filter(created_on__gt=datetime_one_week_ago).count()
        print(boxes_last_week)
        if boxes_last_week > L1 :
            return False
        
        boxes_last_week_by_user = Box.objects.filter(created_by=user,created_on__gt=datetime_one_week_ago).count()
        print(boxes_last_week_by_user)
        if boxes_last_week_by_user > L2 :
            return False
        
        return True

    @staticmethod
    def login_check(auth_token):

        try:
            auth = UserAuthentication.objects.get(auth_token=auth_token)
            return auth.user
        
        except:
            raise LoginRequiredException("Login Required")
        


    def get(self,request):
        
        result = dict()
        status = 200

        try:
            auth_token = request.META["HTTP_AUTHENTICATION_TOKEN"]
            user = self.login_check(auth_token)
            box_queryset = Box.objects.filter()
            box_objs = BoxFilter(request.GET,queryset=box_queryset).qs
            boxes = [box.custom_serializer() for box in box_objs]
            for box in boxes :
                box.pop('created_by')
                box.pop('updated_on')
            result['boxes'] = boxes
            result['result'] = "Box list loaded successfully"
            result['status'] = status

        except Exception as e:
            status = 500
            result['message'] = "Error in loading boxes"
            result['error_reason'] = str(e)
            result['status'] = status

        return JsonResponse(result,status = result['status'])


    def post(self,request):

        result = dict()
        status = 200

        
        try :
            auth_token = request.META["HTTP_AUTHENTICATION_TOKEN"]
            user = self.login_check(auth_token)
            post_data = json.loads(request.body)
            length = post_data['length']
            width = post_data['width']
            height = post_data['height']
            if not self.check_validity(user):
                raise InvalidInputException("Invalid Input , Please input values in Range")
            box = Box.objects.create(length=length,width=width,height=height,created_by=user)
            box.area = box.get_area()
            box.volume = box.get_volume()
            box.save()
            result['message'] = "Box Created Successfully"
            result['status'] = status

        except KeyError as ke:
            status = 500
            result['message'] = "Box creation Failed"
            result['error_reason'] = "Required Fields Missing"
            result['status'] = status

        except Exception as e:
            status = 500
            result['message'] = "Box creation Failed"
            result['error_reason'] = str(e)
            result['status'] = status

        return JsonResponse(result,status = result['status'])

    def delete(self,request):
        result = dict()
        status = 200
        try:
            auth_token = request.META["HTTP_AUTHENTICATION_TOKEN"]
            print(auth_token)
            user = self.login_check(auth_token)
            post_data = json.loads(request.body)
            box_id = post_data['id']
            box = Box.objects.filter(id=box_id)
            box.delete()
            result['message'] = "Box Deleted Successfully"
            result['status'] = status

        except KeyError as ke:
            status = 500
            result['message'] = "Box Deletion Failed"
            result['error_reason'] = "Required Fields Missing"
            result['status'] = status

        except Exception as e:
            status = 500
            result['message'] = "Box Deletion Failed"
            result['error_reason'] = str(e)
            result['status'] = status 
        
        return JsonResponse(result,status = result['status'])



    def put(self,request):
        result = dict()
        status = 200
        try:
            auth_token = request.META["HTTP_AUTHENTICATION_TOKEN"]

            #Login Check
            user = self.login_check(auth_token)
            post_data = json.loads(request.body)
            box_id = post_data['id']
            length = post_data['length']
            width = post_data['width']
            height = post_data['height']

            #Input Check
            if not self.check_validity(user):
                raise InvalidInputException("Invalid Input , Please input values in Range")

            try :
                box = Box.objects.get(id=box_id)
            
            except :
                raise ObjectDoesNotExist("Box Does not Exist with provided id")

            box.length = length
            box.width = width
            box.height = height
            box.area = box.get_area()
            box.volume = box.get_volume()
            box.save()
            result['message'] = "Box Updated Successfully"
            result['status'] = status

        except KeyError as ke:
            status = 500
            result['message'] = "Box Updation Failed"
            result['error_reason'] = "Required Fields Missing"
            result['status'] = status

        except Exception as e:
            status = 500
            result['message'] = "Box Updation Failed"
            result['error_reason'] = str(e)
            result['status'] = status 
        
        return JsonResponse(result,status = result['status'])





