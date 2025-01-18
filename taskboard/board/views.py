from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskList, Group
from .forms import LoginForm, TaskForm, TaskListForm, GroupInviteForm, EditProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def task_list(request):
    sort = request.GET.get('sort', 'title')
    if sort not in ['title', 'due_date', 'is_completed']:
        sort = 'title'
    tasks = Task.objects.filter(user=request.user).order_by(sort)
    return render(request, 'board/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'board/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'board/task_form.html', {'form': form})

@login_required
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

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('board/task_list')
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

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('task_list')  
#             else:
#                 form.add_error(None, "Invalid username or password")
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('task_list')

def create_task_list(request):
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

def calendar_view(request):
    tasks = Task.objects.filter(user=request.user, event_date__gte=now()).order_by('event_date')
    return render(request, 'board/calendar.html', {'tasks': tasks})