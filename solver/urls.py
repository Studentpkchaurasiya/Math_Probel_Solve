from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('create-new-account/', views.create_new_account, name='create_new_account'),
    path('login/', views.login_user, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('logout/',views.logout_user, name='logout'),
    path('dashboard/problems/', views.problems, name='problems'),
    path('problems/', views.problem_page, name='problems'),
    path('check-answer/', views.check_answer, name='check_answer'),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
