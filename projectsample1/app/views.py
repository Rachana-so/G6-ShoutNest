from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt
from .models import User

from app.models import User,Shouts,Friends,Reports
from app.serializers import UserSerializer,ShoutSerializer,FriendsSerializer,ReportsSerializer,UserShoutsSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage
import jwt, datetime

result_token:any


class RegisterView(APIView):
   
    @method_decorator(csrf_exempt)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request,format=None):
        print(request)
        userName = request.data['userName']
        print(userName)
        password = request.data['password']

        user = User.objects.filter(userName=userName,password=password).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

      

        payload = {
            'id': user.userId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
       
        result_token=token
        response = Response()
       
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'userId':user.userId,
            'password':user.password,
            'emailId':user.emailId,
            'userName':user.userName

        }
        return response

@csrf_exempt
def getUserbyId(request, UserId=0):
    print("Request",UserId)
    if request.method == 'GET':
        if UserId != 0:
            user=User.objects.filter(userId=UserId); """ user=User.objects.get(UserId=UserId) """
            
            user_serializers = UserSerializer(user,many=True)
            final_user=user_serializers.data
        return JsonResponse(final_user,safe=False)
    return JsonResponse("user not found..",safe=False)



# ***method for settings profile pic****
class ProfileView(APIView):
    @method_decorator(csrf_exempt)
    def put(self, request,format=None):
      
        userId = request.data['userId']
        profilePic=request.data['profilePic']
       
        user=User.objects.get(userId=userId)
        print("Request data ",request.data)
        print("USer data  ",user)
        serializer = UserSerializer(user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        print(profilePic)
        return JsonResponse("Profile added",safe=False)


 


@csrf_exempt
def UserApi(request,id=0):
    if request.method=='GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)

    elif request.method=='POST':
        user_data=JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        user_data = JSONParser().parse(request)
        user=User.objects.get(userId=user_data['userId'])
        print("USer  ",user.password)
        user_serializer=UserSerializer(user,data=user_data)
        print("USer serialize ",user_serializer)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        user=User.objects.get(userId=id)
        user.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)


@csrf_exempt
def SaveFile(request):
    file=request.FILES['uploadedFile']
    file_name = default_storage.save(file.name,file)
    

    return JsonResponse(file_name,safe=False)

@csrf_exempt
def ShoutsApi(request,id=0):
    if request.method=='GET':
        shouts = Shouts.objects.all()
        shouts_serializer = ShoutSerializer(shouts, many=True)
        return JsonResponse(shouts_serializer.data, safe=False)

    elif request.method=='POST':
        shouts_data=JSONParser().parse(request)
        shouts_serializer = ShoutSerializer(data=shouts_data)
        print(shouts_serializer)
        if shouts_serializer.is_valid():
            shouts_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        shouts_data = JSONParser().parse(request)
        shouts=Shouts.objects.get(shoutId=shouts_data['shoutId'])
        shouts_serializer=ShoutSerializer(shouts,data=shouts_data)
        if shouts_serializer.is_valid():
            shouts_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        shouts=Shouts.objects.get(shoutId=id)
        shouts.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)


@csrf_exempt
def FriendsApi(request,id=0):
    if request.method=='GET':
        friends = Friends.objects.all()
        friends_serializer = FriendsSerializer(friends, many=True)
        return JsonResponse(friends_serializer.data, safe=False)

    elif request.method=='POST':
        friends_data=JSONParser().parse(request)
        friends_serializer = FriendsSerializer(data=friends_data)
        if friends_serializer.is_valid():
            friends_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        friends_data = JSONParser().parse(request)
        user=Friends.objects.all().filter(userId=friends_data['userId'],friendId=friends_data['friendId']).first()
      
        user_serializer=FriendsSerializer(user,data=friends_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

        

    elif request.method=='DELETE':
        row1=Friends.objects.get(id=id)
        row1.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)





@csrf_exempt
def ReportsApi(request,id=0):
    if request.method=='GET':
        reports = Reports.objects.all()
        reports_serializer = ReportsSerializer(reports, many=True)
        return JsonResponse(reports_serializer.data, safe=False)

    elif request.method=='POST':
        reports_data=JSONParser().parse(request)
        reports_serializer = ReportsSerializer(data=reports_data)
        if reports_serializer.is_valid():
            reports_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        reports_data = JSONParser().parse(request)
        reports=Reports.objects.get(shoutId=reports_data['reportId'])
        reports_serializer=ReportsSerializer(reports,data=reports_data)
        if reports_serializer.is_valid():
             reports_serializer.save()
             return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        reports=Reports.objects.get(reportId=id)
        reports.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)


@csrf_exempt
def UserShoutsApi(request,UserId=0):
    if request.method == 'GET':
        if UserId != 0:
            friends=Friends.objects.filter(userId=UserId) | Friends.objects.filter(friendId=UserId)
            friends_serializers = FriendsSerializer(friends,many=True)
            friend_list=friends_serializers.data
            print('friendlist',friend_list)
            friends_set=set()
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['friendId'])
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['userId'])
            print('friendset',friends_set)

            usershouts_list = list()

            for i in friends_set:
                print("hello")
               
                user11=User.objects.get(userId=i)
             
                uname=user11.userName
                print("UserName",uname)
                newuser={'userId':i,'userName':uname}
                # User('userId'=i,u)
                print("hello1",user11)
                usershouts_serializer = UserShoutsSerializer(instance=newuser,many=True)
                print("hello3",usershouts_serializer.data)
                # UserShoutSerializer(shouts,many=True)
                usershouts_list.append(usershouts_serializer.data)
                
                print("hello4")
            print('USer shoutlist',usershouts_list)
            final_usershouts_list=list()
            for i in usershouts_list:
                for j in i:
                    final_usershouts_list.append(j)
            print('final',final_usershouts_list)

                  


        return JsonResponse(final_usershouts_list,safe=False)
    return JsonResponse("Shouts not found..",safe=False)


@csrf_exempt
def friendShoutsApi(request, UserId=0):
    if request.method == 'GET':
        if UserId != 0:
            friends=Friends.objects.filter(userId=UserId) | Friends.objects.filter(friendId=UserId)
            friends_serializers = FriendsSerializer(friends,many=True)
            friend_list=friends_serializers.data
            print('friendlist',friend_list)
            friends_set=set()
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['friendId'])
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['userId'])
            print('friendset',friends_set)

            
            user_shout_list=[]
            
            for i in friends_set:
                shouts=Shouts.objects.filter(userId=i)
                ssff=Shouts.objects.filter(userId=i).values('caption','photoFileName','userId__userName','shoutId','userId','type','uploadDate','path','userId__profilePic')
                for s in ssff:
                    user_shout_list.append(s)
                
            return JsonResponse(user_shout_list,safe=False)
    return JsonResponse("Shouts not found..",safe=False)


@csrf_exempt
def DetailsOfFriendsApi(request, UserId=0):
    if request.method == 'GET':
        if UserId != 0:
            friends=Friends.objects.filter(userId=UserId) | Friends.objects.filter(friendId=UserId)
            friends_serializers = FriendsSerializer(friends,many=True)
            friend_list=friends_serializers.data
            print('friendlist',friend_list)
            friends_set=set()
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['friendId'])
            for i in friend_list:
                if i['status']==3:
                    friends_set.add(i['userId'])
            print('friendset',friends_set)

            user_list = list()

            for i in friends_set:
                fuser=User.objects.filter(userId=i)
                user_serializer = UserSerializer(fuser,many=True)
                user_list.append(user_serializer.data)
                print(' user',fuser)

            
            


        return JsonResponse(user_list,safe=False)
    return JsonResponse(" not found..",safe=False)





