from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Task
from .forms import UserRegisterForm, IndividualTaskForm, GroupTaskForm


User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_tasks')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user_username = request.POST.get('username')
        user_password = request.POST.get('password')

        user = authenticate(request, username=user_username, password=user_password)

        if user is not None:
            login(request, user)
            return redirect('my_tasks')
        else:
            messages.error(request, 'incorrect user or password')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required
def profile_view(request):
    return render(request, "profile.html" , {
        'user': request.user
    })

def user_list(request):
    users = User.objects.all().order_by('username')
    paginator = Paginator(users,25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_list.html',{
        'page_obj': page_obj
    })

@login_required
def create_individual_task(request):
    if request.method == 'POST':
        form = IndividualTaskForm(request.POST, initial={
            'user':request.user
        })
        if form.is_valid():
            form.save()
            return redirect('my_tasks')
    else:
        form = IndividualTaskForm(initial={
        'user':request.user
    })
        
    return render(request, 'task_form.html',{'form': form})

@login_required
def create_group_task(request):
    if request.method == 'POST':
        form = GroupTaskForm(request.POST, initial={
            'user':request.user
        })
        if form.is_valid():
            form.save()
            return redirect('my_tasks')
    else:
        form = GroupTaskForm(initial={
        'user':request.user
    })
    
    return render(request, 'task_form.html',{'form': form})
    
@login_required
def my_tasks(request):
    user = request.user

    tasks = Task.objects.filter(
        Q(created_by=user) |
        Q(assigned_to=user) |
        Q(group__members=user)
    ).distinct()

    return render(request, 'my_tasks.html', {'tasks': tasks})

@login_required
def tasks_to_validate(request):
    if not request.user.is_teacher():
        return redirect('my_tasks')
    
    tasks = Task.objects.filter(
        task_status=Task.STATUS_PENDING_REVIEW,
        task_type=Task.TYPE_EVALUABLE
    )

    return render(request, 'tasks_to_validate.html', {'tasks': tasks})