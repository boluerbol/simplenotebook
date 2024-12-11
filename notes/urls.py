from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_note, name='create_note'),
    path('update/<int:note_id>/', views.update_note, name='update_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('api/notes/', views.get_all_notes, name='get_all_notes'),

]
