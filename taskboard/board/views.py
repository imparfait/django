from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Task, TaskGroup, TaskImage, TaskList
from .forms import AddMemberForm, TaskForm, TaskGroupForm, TaskListForm, EditProfileForm
from django.db.models import Prefetch
from django.contrib.auth import logout
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def task_list(request):
    sort = request.GET.get('sort', 'title') 
    order = request.GET.get('order', 'asc') 
    if sort not in ['title', 'due_date', 'is_completed']:
        sort = 'title'
    if order not in ['asc', 'desc']:
        order = 'asc'
    if order == 'desc':
        sort = f'-{sort}'
    task_lists = TaskList.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'tasks',
            queryset=Task.objects.filter(user=request.user).order_by(sort),
            to_attr='sorted_tasks'
        )
    )
    return render(request, 'board/task_list.html',{'task_lists': task_lists, 'sort': sort, 'order': order})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'board/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == "POST":
        task_form  = TaskForm( user=request.user, data=request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user
            task.save()
            images = request.FILES.getlist('images[]')
            for image in images:
                TaskImage.objects.create(task=task, image=image)
            return redirect('task_list')
    else:
        task_form =  TaskForm(user=request.user)
    return render(request, 'board/task_form.html', {'task_form': task_form,})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images[]')
            for image in images:
                TaskImage.objects.create(task=task, image=image)
            return redirect("task_detail", pk=task.id)
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, "board/task_form.html", {"task_form": form, "task": task})

def delete_task_image(request, image_id):
    image = get_object_or_404(TaskImage, id=image_id)
    if image.task.user == request.user: 
        image.delete()
    return redirect('task_edit', pk=image.task.pk)

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'board/task_confirm_delete.html', {'task': task})

@login_required
def profile(request):
    return render(request, 'board/profile.html')

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save() 
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)  
    return render(request, 'board/edit_profile.html', {'form': form})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = TaskGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            form.save_m2m()  
            return redirect('groups_list') 
    else:
        form = TaskGroupForm()
    return render(request, 'board/create_group.html', {'form': form})

@login_required
def edit_group(request, pk):
    group = get_object_or_404(TaskGroup, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = TaskGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('groups_list')
    else:
        form = TaskGroupForm(instance=group)
    return render(request, 'board/create_group.html', {'form': form})

@login_required
def groups_list(request):
    groups = TaskGroup.objects.filter(members=request.user)
    return render(request, 'board/groups_list.html', {'groups': groups})

@login_required
def group_detail(request, pk):
    group = get_object_or_404(TaskGroup, pk=pk)
    if request.method == "POST":
        form = AddMemberForm(request.POST)
        if form.is_valid():
            user_to_add = form.cleaned_data['user']
            if user_to_add != request.user:  
                group.members.add(user_to_add)
                return redirect('group_detail', pk=group.pk)
    else:
        form = AddMemberForm()
    return render(request, 'board/group_detail.html', {
        'group': group,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'board/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('task_list')

def task_list_create(request):
    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.user = request.user  
            task_list.save()
            return redirect('task_list')
    else:
        form = TaskListForm()
    return render(request, 'board/task_list_form.html', {'form': form})

@login_required
def calendar_data(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    tasks = Task.objects.filter(user=request.user,event_date__year=year, event_date__month=month) 
    tasks_data = {}
    for task in tasks:
        task_day = task.event_date.day
        if task_day not in tasks_data:
            tasks_data[task_day] = []
        tasks_data[task_day].append({
            'title': task.title,
            'url': reverse('task_detail', args=[task.pk]),
            'event_date': task.event_date.strftime('%Y-%m-%d')
        })
    return JsonResponse(tasks_data)

def task_toggle(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user) 
    if request.method == 'POST':
        task.is_completed = not task.is_completed
        task.save()
    return redirect('task_list')

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'board/user_profile.html', {'profile_user': user})