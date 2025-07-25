from django.urls import path, include
from . import views
from .views import export_qualification_excel,export_teaching_excel,export_contract_excel,export_organizational_excel,export_remarks_excel,export_research_excel,export_scientific_excel,export_publications_excel,export_social_excel,teacher_dashboard
from main.views import teacher_load_view

# urlpatterns = [
#     path('', views.dashboard, name='dashboard'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),  # <-- теперь корень ведёт в index
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('export/qualification/', export_qualification_excel, name='export_qualification_excel'),
    path('export/teaching/', export_teaching_excel, name='export_teaching_excel'),
    path('export/organizational/', export_organizational_excel, name='export_organizational_excel'),
    path('export/research/', export_research_excel, name='export_research_excel'),
    path('export/contract/', export_contract_excel, name='export_contract_excel'),
    path('export/scientific/', export_scientific_excel, name='export_scientific_excel'),
    path('export/publications/', export_publications_excel, name='export_publications_excel'),
    path('export/social/', export_social_excel, name='export_social_excel'),
    path('export/remarks/', export_remarks_excel, name='export_remarks_excel'),
    path('export/full/', views.export_full_teacher_excel, name='export_full_teacher_excel'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('teacher/<int:teacher_id>/load/', views.teacher_load_view, name='teacher_load'),
    
]