from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .form import Account_creation_form
from .models import All_account
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from .midlewares import auth, guest
from django.contrib import messages
from django.http import JsonResponse
from .models import Problem, UserProblemStatus
from django.views.decorators.cache import never_cache


@guest
def home(request):
    return render(request, 'home.html')

@guest
def create_new_account(request):
    if request.method=='POST':
        form = Account_creation_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "🎉 Welcome aboard! Your account has been created. You can now explore your dashboard.")
            return render(request, 'login.html')
    else:
        initial_data = {
            'mobile_number':'',
            'email':'',
            'username':'',
            'password1':'',
            'password2':'',
            'name' : '',
            'address': '',
            'standard' : ''
        }
        form = Account_creation_form(initial=initial_data)
    return render(request, 'create_new_account.html', {'form':form})

@never_cache
@guest
def login_user(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data={
            'username':'',
            'password':''
        }
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'login.html', {'form':form})

@never_cache
@auth
def dashboard(request):
    profile=request.user.all_account
    
    total = Problem.objects.filter(standard=profile.standard).count()
    solved = UserProblemStatus.objects.filter(user=request.user, is_solved=True).count()
    stars = solved // 3  # simple rule: 1 star per 3 correct
    level = "Beginner" if solved < 5 else "Intermediate" if solved < 10 else "Advanced"
    if total>0:
        progress = ((solved)*100)/(total)
    else:
        progress = 0

    return render(request, 'dashboard.html', {
        'total': total,
        'solved': solved,
        'stars': stars,
        'level': level,
        'progress': progress,
        'profile':profile
    })
    
@never_cache
@auth
def profile(request):
    profile=request.user.all_account
    return render(request, 'profile.html', {'profile':profile})

@never_cache
@auth
def logout_user(request):
    logout(request)
    return redirect('login')

@never_cache    
@auth
def problems(request):
    return render(request, 'problems.html')

@never_cache
@auth
def problem_page(request):
    profile = request.user.all_account
    problem_list = []
    for p in Problem.objects.filter(standard=profile.standard).order_by('id'):
        problem_list.append({
            'id': p.id, # type: ignore
            'title': p.title,
            'body': p.body,
            'options': p.options,
        })
    
    statuses = {
        s.problem.id: s.is_solved for s in UserProblemStatus.objects.filter(user=request.user) # type: ignore
    }
    return render(request, 'problems.html', {
        'problems': problem_list,
        'statuses': statuses,
        'profile' : profile
    })

@never_cache
@auth
def check_answer(request):
    if request.method == 'POST':
        problem_id = request.POST['problem_id']
        selected = int(request.POST['selected'])

        problem = get_object_or_404(Problem, id=problem_id)
        correct = selected == problem.correct_option

        if correct:
            UserProblemStatus.objects.update_or_create(
                user=request.user, problem=problem,
                defaults={'is_solved': True}
            )

        return JsonResponse({'correct': correct})
    return HttpResponse("check answer")


