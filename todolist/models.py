from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    #blank=True can be empty if needed
    memo = models.TextField(blank=True)
    #value is taken at the exact moment of instance creation
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    #stroes relationship between user and todoitem
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title