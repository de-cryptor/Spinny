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
from datetime import timedelta,datetime
from django.utils import timezone
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist

@method_decorator(csrf_exempt, name='dispatch')
class AuthTokenInterface(View):


    '''
    API to give authentication token for furthur API on successful Login.
    '''
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
                auth.auth_token = get_random_string(64)
                auth.save()
                result['auth-token'] = auth.auth_token
                result['message'] = "User Logged in Successfully"
                result['status'] = status

            else :
                raise Exception("Please provide correct credentials")

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

    '''
    Check Conditions to maintain Box Database Integrity.
    '''
    @staticmethod
    def check_validity(user):
        if Box.objects.all().count() == 0 :
            return True

        area = Box.objects.all().aggregate(Avg('area'))
        if area['area__avg'] > A1 :
            return False

        volume =  Box.objects.all().aggregate(Avg('volume'))
        if volume['volume__avg'] > V1 :
            return False

        datetime_one_week_ago = timezone.now().date() - timedelta(days=7)

        boxes_last_week = Box.objects.filter(created_on__gt=datetime_one_week_ago).count()
        if boxes_last_week > L1 :
            return False
        
        boxes_last_week_by_user = Box.objects.filter(created_by=user,created_on__gt=datetime_one_week_ago).count()
        if boxes_last_week_by_user > L2 :
            return False
        
        return True

    '''
    Check for User Logged in .
    '''
    @staticmethod
    def login_check(auth_token):

        try:
            auth = UserAuthentication.objects.get(auth_token=auth_token)
            return auth.user
        
        except:
            raise LoginRequiredException("Login Required")
        

    '''
    Box List API for various filter
    '''
    def get(self,request):
        
        result = dict()
        status = 200

        try:
            # Authentication
            auth_token = request.META["HTTP_AUTHENTICATION_TOKEN"]
            user = self.login_check(auth_token)

            box_queryset = Box.objects.all()

            #Django Custom Filter
            box_objs = BoxFilter(request.GET,queryset=box_queryset).qs

            #My List of Boxes
            if 'created_by' in request.GET and request.GET['created_by'] == user.username :
                if user.is_staff :
                    box_objs = box_objs.filter(created_by=user)
                else :
                    raise PermissionDeniedException("You dont have permission to list your boxes , You must be a staff user.")

            #Box Serialzer Data
            boxes = [box.custom_serializer() for box in box_objs]
            if not user.is_staff :
                for box in boxes :
                    box.pop('created_by')
                    box.pop('created_on')
            result['boxes'] = boxes
            result['result'] = "Box list loaded successfully"
            result['status'] = status

        except Exception as e:
            status = 500
            result['message'] = "Error in loading Box List"
            result['error_reason'] = str(e)
            result['status'] = status

        return JsonResponse(result,status = result['status'])


    '''
    API to create new box.
    '''
    def post(self,request):

        result = dict()
        status = 200

        
        try :
            auth_token = request.META["HTTP_AUTHENTICATION_TOKEN"]
            #Login Check
            user = self.login_check(auth_token)
            #Request Body
            post_data = json.loads(request.body)
            length = post_data['length']
            width = post_data['width']
            height = post_data['height']
            #Input Check
            if not self.check_validity(user):
                raise InvalidInputException("Invalid Input , Box Database integrity does not allow this input")

            if not user.is_staff:
                raise PermissionDeniedException("You dont have permission to create the box , You must be a staff user.")

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

    '''
    API to delete the box.
    '''
    def delete(self,request):
        result = dict()
        status = 200
        try:
            auth_token = request.META["HTTP_AUTHENTICATION_TOKEN"]
            #Login Check
            user = self.login_check(auth_token)
            #Request Body
            post_data = json.loads(request.body)
            box_id = post_data['id']
            try :
                box = Box.objects.get(id=box_id)
            except :
                raise ObjectDoesNotExist("Box Does not Exist with provided id")

            if not box.created_by == user :
                raise Exception("You can not delete the box, You must be creater of the box")
            
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


    '''
    API to update the Box.
    '''
    def put(self,request):
        result = dict()
        status = 200
        try:
            auth_token = request.META["HTTP_AUTHENTICATION_TOKEN"]
            #Login Check
            user = self.login_check(auth_token)
            #Request Body
            post_data = json.loads(request.body)
            box_id = post_data['id']
            length = post_data['length']
            width = post_data['width']
            height = post_data['height']

            #Input Check
            if not self.check_validity(user):
                raise InvalidInputException("Invalid Input , Box Database integrity does not allow this input")

            if not user.is_staff:
                raise PermissionDeniedException("You dont have permission to update the box , You must be a staff user.")

            try :
                box = Box.objects.get(id=box_id)
            except :
                raise ObjectDoesNotExist("Box Does not Exist with provided id")

            box.length = length
            box.width = width
            box.height = height
            box.area = box.get_area()
            box.volume = box.get_volume()
            box.updated_on = datetime.now()
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





