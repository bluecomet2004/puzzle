import uuid
import jwt
import datetime
from django.db import models
from typing import Dict, Any


class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        ordering = ['createdAt']
        
        def __str__(self) -> str:
            return self.email
        

class GameHistoryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    score = models.FloatField()
    difficulty = models.CharField(max_length=128)
    matrixSize = models.IntegerField()
    limitTime = models.IntegerField()
    overTime = models.IntegerField()
    finishedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'game_history'
        ordering = ['-finishedAt']

        def __str__(self) -> str:
            return self.finishedAt
        

def generate_token(user: UserModel, secret_key: str, duration: int) -> str:
    payload: Dict[str, Any] = {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

def get_user_from_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get("id")
        return UserModel.objects.get(id=user_id)
    except (jwt.InvalidTokenError, UserModel.DoesNotExist):
        return None