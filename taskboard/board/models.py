from django.contrib.auth.models import User
from django.db import models

class TaskList(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default="#ffffff")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasklists")
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks")
    def __str__(self):
        return self.title

class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name="custom_groups")
    task_lists = models.ManyToManyField(TaskList, related_name="groups")
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    def __str__(self):
        return self.user.username