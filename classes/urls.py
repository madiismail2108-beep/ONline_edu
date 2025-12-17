from django.urls import path
from . import views
from .views import topic_list, topic_detail, topic_create, topic_update, topic_delete

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('module/', views.module_list, name='module_list'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),
    path('lesson/', views.lesson_list, name='lesson_list'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('create-course/', views.create_course, name='create_course'),
    path('create-module/<int:course_id>/', views.create_module, name='create_module'),
    path('create-lesson/<int:module_id>/', views.create_lesson, name='create_lesson'),

    path('<int:pk>/', views.course_detail, name='courses_detail'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:course_id>/topics/', topic_list, name='topic_list'),
    path('topic/<int:pk>/', topic_detail, name='topic_detail'),
    path('topic/add/', topic_create, name='topic_add'),
    path('topic/<int:pk>/edit/', topic_update, name='topic_edit'),
    path('topic/<int:pk>/delete/', topic_delete, name='topic_delete'),
]
