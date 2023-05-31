import uuid
from django.db import models

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
            return self.name
        

class GameHistoryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    score = models.FloatField()
    limitTime = models.IntegerField()
    overTime = models.IntegerField()
    finishedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'game_history'
        ordering = ['-finishedAt']

        def __str__(self) -> str:
            return self.finishedAt