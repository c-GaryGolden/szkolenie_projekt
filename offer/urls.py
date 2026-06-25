from django.urls import path
from . import views

urlpatterns = [
    # =========================================================================
    # 1. WARSTWA FUNKCJONALNA / PREZENTACJI (Dla człowieka w przeglądarce - HTML)
    # =========================================================================
    # Strona główna - lista wszystkich dostępnych kategorii
    path('kategorie/', views.kategorie_lista, name='kategorie_lista'),
    
    # Szczegóły kategorii / opis powiązany z daną kategorią (używa istniejącego widoku)
    path('kategorie/<int:kategoria>/', views.szkolenie_opis, name='szkolenia_kategoria'),
    
    # Szczegółowy opis konkretnego szkolenia w danej kategorii
    path('kategorie/<int:kateg>/course/<int:id>/', views.szkolenie_opis, name='szkolenie_opis'),
    
    # Formularze użytkownika
    path('register/', views.rejestracja_form, name='register'),
    path('issues/', views.zgloszenie_problemu, name='zgloszenie_problemu'),

    # Panel Managera (Zarządzanie)
    path('offer-mng/', views.panel_glowny, name='panel_glowny'),
    path('offer-mng/categ-lst/', views.categ_lst, name='categ_lst'),
    path('offer-mng/course-lst/', views.course_lst, name='course_lst'),
    path('offer-mng/categ-add/', views.categ_add, name='categ_add'),
    path('offer-mng/course-add/', views.course_add, name='course_add'),


    # =========================================================================
    # 2. WARSTWA TECHNICZNA / INTERFEJSY DANYCH (Dla skryptów i systemów - JSON)
    # =========================================================================
    path('api/formTemplates/', views.api_form_templates, name='api_form_templates'),
    path('api/messageTemplates/', views.api_message_templates, name='api_message_templates'),
    
    path('api/categories/', views.api_categories_hardcoded, name='api_categories_hardcoded'),
    path('api/courses/', views.api_courses, name='api_courses'),
    
    path('api/registers/', views.api_registers, name='api_registers'),
    path('api/register/', views.api_register_detail, name='api_register_detail'),
    
    path('api/problemReport/', views.api_problem_report_save, name='api_problem_report_save'),
    path('api/problems/', views.api_problems_list, name='api_problems_list'),
]
