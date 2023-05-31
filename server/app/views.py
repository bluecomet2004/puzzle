import math
from datetime import datetime
from django.contrib.auth.hashers import make_password
from app.models import UserModel, GameHistoryModel
from app.serializers import UserSerializer, GameHistorySerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
                "message": "Cannot find the user"
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
        pk = request.GET.get('id')
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
            }, status=status.HTTP_204_NO_CONTENT)
        

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = UserModel

    def get_user_by_email(self, email):
        try:
            return UserModel.objects.get(email=email)
        except:
            return None
    
    def post(self, request):
        loginData = request.data
        user = self.get_user_by_email(email=loginData["email"])

        if user == None:
            return Response({
                "success": False,
                "message": "Cannot find the user."
            }, status=status.HTTP_404_NOT_FOUND)
        # else:
            # auth = JSONWebTokenAuthentication()


class GameHistoryView(generics.GenericAPIView):
    serializer_class = GameHistorySerializer
    queryset = GameHistoryModel

    def get(self, request):
        page_param = request.GET.get('page', 1)
        limit_param = request.GET.get('limit', 10)
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
            serializer.save()
            return Response({
                "success": True,
                "message": "Successfully created"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        pk = request.GET.get('id')
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
            }, status=status.HTTP_204_NO_CONTENT)     