from django.urls import path
from . import views
from .views import export_qualification_excel,export_teaching_excel,export_contract_excel,export_organizational_excel,export_remarks_excel,export_research_excel,export_scientific_excel,export_social_excel

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
from django.urls import path
from . import views

urlpatterns = [
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
path('export/social/', export_social_excel, name='export_social_excel'),
path('export/remarks/', export_remarks_excel, name='export_remarks_excel'),
    
]