from django.contrib.auth.models import User
from django.db import models

class TaskList(models.Model):
    COLOR_CHOICES = [
        ("#FF5733", "Red"),
        ("#33FF57", "Green"),
        ("#3357FF", "Blue"),
        ("#FFFF33", "Yellow"),
        ("#FF33FF", "Pink"),
        ("#800080", "Purple"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default="#000000")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_lists")
    def __str__(self):
        return self.name
    
class TaskGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name="task_groups", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_group")
    def __str__(self):
        return self.name
    
class Task(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    list = models.ForeignKey(
        TaskList, 
        on_delete=models.CASCADE, 
        related_name="tasks", 
        null=False, 
        default=1  
    )    
    group = models.ForeignKey(TaskGroup, on_delete=models.SET_NULL, related_name="tasks", null=True, blank=True) 
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.list:
            default_list, created = TaskList.objects.get_or_create(user=self.user, name="To Do List")
            self.list = default_list
        super(Task, self).save(*args, **kwargs)

class TaskImage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='task_images/')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    def __str__(self):
        return self.user.username
