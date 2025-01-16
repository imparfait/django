from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskList, Group
from .forms import TaskForm, TaskListForm, GroupInviteForm, EditProfileForm
from django.contrib.auth import update_session_auth_hash
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'board/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'board/task_detail.html', {'task': task})

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'board/task_form.html', {'form': form})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'board/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')

@login_required
def profile(request):
    return render(request, 'board/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
                update_session_auth_hash(request, user) 
            user.save() 
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)  
    return render(request, 'board/edit_profile.html', {'form': form})

def group_invite(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = GroupInviteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                group.members.add(user)
                messages.success(request, f"User {user.username} added to group.")
            else:
                messages.error(request, "User with this email does not exist.")
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupInviteForm()
    return render(request, 'board/group_invite.html', {'form': form, 'group': group})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'board/group_detail.html', {'group': group})

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
