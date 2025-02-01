from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('filter-grid/', views.course_filter_grid, name='course_filter_grid'),
    path('<slug:slug>/', views.course_single, name='course_single'),
    path('<slug:slug>/<int:section_id>/', views.course_single, name='course_single_section'),
    path('<slug:slug>/test/<int:test_id>/', views.course_test, name='course_test'),
    path('<slug:slug>/test/<int:test_id>/result/', views.course_test_result, name='course_test_result'),
    path('<slug:slug>/quiz/<int:quiz_id>/', views.quiz_view, name='quiz_view'),
    path('<int:section_id>/complete/', views.complete_section, name='complete_section'),
    path('not-found/', views.not_found, name='course_not_found'),

]
