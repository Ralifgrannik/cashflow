from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_list, name='record_list'),
    path('record/new/', views.record_create, name='record_create'),
    path('record/<int:pk>/edit/', views.record_update, name='record_update'),
    path('record/<int:pk>/delete/', views.record_delete, name='record_delete'),

    path('statuses/', views.manage_statuses, name='manage_statuses'),
    path('statuses/<int:pk>/edit/', views.edit_status, name='edit_status'),
    path('statuses/<int:pk>/delete/', views.delete_status, name='delete_status'),

    path('types/', views.manage_types, name='manage_types'),
    path('types/<int:pk>/edit/', views.edit_type, name='edit_type'),
    path('types/<int:pk>/delete/', views.delete_type, name='delete_type'),

    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),

    path('subcategories/', views.manage_subcategories, name='manage_subcategories'),
    path('subcategories/<int:pk>/edit/', views.edit_subcategory, name='edit_subcategory'),
    path('subcategories/<int:pk>/delete/', views.delete_subcategory, name='delete_subcategory'),
    path('ajax/categories/', views.ajax_load_categories, name='ajax_load_categories'),
    path('ajax/subcategories/', views.ajax_load_subcategories, name='ajax_load_subcategories'),
]
