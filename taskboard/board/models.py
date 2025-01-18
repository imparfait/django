from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class TaskList(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default="#ffffff")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_lists")
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.list:
            default_list, created = TaskList.objects.get_or_create(user=self.user, name="To Do List")
            self.list = default_list
        super(Task, self).save(*args, **kwargs)

class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name="custom_groups")
    task_lists = models.ManyToManyField(TaskList, related_name="groups")
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    def __str__(self):
        return self.user.username
