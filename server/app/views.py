import math
from datetime import datetime
from django.core import serializers
from django.contrib.auth.hashers import make_password
from app.models import UserModel, GameHistoryModel, generate_token, get_user_from_token
from app.serializers.adminSerializer import UserSerializer, GameHistorySerializer
from app.serializers.userSerializer import RegisterSerializer, LoginSerializer
from rest_framework import status, generics
from rest_framework.response import Response


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_account = serializer.save()
            user = serializers.serialize('python', [user_account])[0]['fields']
            return Response({
                "success": True,
                "message": "Successfully registered",
                "user": user
            }, status=status.HTTP_201_CREATED)
        else:   
            return Response({
                "success": False,
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            checked_user = serializer.check_user()
            token = generate_token(checked_user, "puzzle", 3600)
            user = serializers.serialize('python', [checked_user])[0]['fields']
            return Response({
                "success": True,
                "message": "Welcome back!",
                "user": user,
                "token": token
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

class TokenView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        header = request.META.get("HTTP_AUTHORIZATION")
        token = header.split()[1] if header else None
        decoded_user = get_user_from_token(token, "puzzle")

        if decoded_user == None:
            return Response({
                "success": False,
                "message": "The token has expired."
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = UserModel.objects.filter(email=decoded_user.email)
            user_data = serializers.serialize('python', [decoded_user])[0]['fields']
            if user.exists() == True:
                return Response({
                    "success": True,
                    "message": "Token is valid.",
                    "user": {
                        "name": user_data["name"],
                        "email": user_data["email"],
                        "createdAt": user_data["createdAt"]
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "message": "The token has expired."
                }, status=status.HTTP_401_UNAUTHORIZED)
        

class UserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def get_user_by_email(self, email):
        try:
            return UserModel.objects.get(email=email)
        except:
            return None
        
    def get_user_by_pk(self, pk):
        try:
            return UserModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request):
        page_param = int(request.GET.get('page', 1))
        limit_param = int(request.GET.get('limit', 10))
        search_param = request.GET.get('search')
        start_num = (page_param - 1) * limit_param
        end_num = page_param * limit_param
        users = UserModel.objects.all()
        total_users = users.count()

        if search_param:
            users = users.filter(name__icontains=search_param)
        serializer = self.serializer_class(users[start_num:end_num], many=True)

        return Response({
            "success": True,
            "total": total_users,
            "current_page": page_param,
            "last_page": math.ceil(total_users / limit_param),
            "list": serializer.data
        })

    def post(self, request):
        userData = request.data
        exist = self.get_user_by_email(userData["email"])

        if exist != None:
            return Response({
                "success": False,
                "message": "User already exists."
            }, status=status.HTTP_403_FORBIDDEN)
        else:
            newUser = {
                "name": userData["name"],
                "email": userData["email"],
                "password": make_password(userData["password"])
            }
            serializer = self.serializer_class(data=newUser)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Successfully registered.",
                    "user": serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "success": False,
                    "message": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request):
        pk = request.GET.get('id')
        userData = request.data
        user = self.get_user_by_pk(pk=pk)

        if user == None:
            return Response({
                "success": False,
                "message": "Cannot find the user."
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(user, data=userData, partial=True)
            if serializer.is_valid():
                serializer.validated_data["updatedAt"] = datetime.now()
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Successfully updated.",
                    "user": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "message": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request):
        pk = request.GET.get('id', 'all')

        if pk == 'all':
            user = UserModel.objects.all()
            user.delete()
            return Response({
                "success": True,
                "users": user
            }, status=status.HTTP_200_OK)
        else:
            user = self.get_user_by_pk(pk=pk)

            if user == None:
                return Response({
                    "success": False,
                    "message": "Cannot find the user."
                }, status=status.HTTP_404_NOT_FOUND)
            else:
                user.delete()
                return Response({
                    "success": True,
                    "message": "Deleted successfully."
                }, status=status.HTTP_200_OK)


class GameHistoryView(generics.GenericAPIView):
    serializer_class = GameHistorySerializer
    queryset = GameHistoryModel

    def get_history_by_pk(self, pk):
        try:
            return GameHistoryModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request):
        page_param = int(request.GET.get('page', 1))
        limit_param = int(request.GET.get('limit', 10))
        search_param = request.GET.get('search')
        start_num = (page_param - 1) * limit_param
        end_num = page_param * limit_param
        histories = GameHistoryModel.objects.all()
        total_history = histories.count()

        if search_param:
            histories = histories.filter(name__icontains=search_param)
        serializer = self.serializer_class(histories[start_num:end_num], many=True)

        return Response({
            "success": True,
            "total": total_history,
            "current_page": page_param,
            "last_page": math.ceil(total_history / limit_param),
            "list": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        historyData = request.data
        serializer = self.serializer_class(data=historyData)
        if serializer.is_valid():
            history = serializer.save()
            json_history = serializers.serialize('python', [history])[0]['fields']
            return Response({
                "success": True,
                "message": "Successfully created",
                "history": json_history
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        pk = request.GET.get('id', 'all')

        if pk == 'all':
            history = GameHistoryModel.objects.all()
            history.delete()
            return Response({
                "success": True,
                "history": history
            }, status=status.HTTP_200_OK)
        else:
            history = self.get_history_by_pk(pk=pk)

            if history == None:
                return Response({
                    "success": False,
                    "message": "Cannot find the history."
                }, status=status.HTTP_404_NOT_FOUND)
            else:
                history.delete()
                return Response({
                    "success": True,
                    "message": "Deleted successfully."
                }, status=status.HTTP_200_OK)     