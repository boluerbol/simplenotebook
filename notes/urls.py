from django.urls import path
from . import views
from .views import (
    CreateNoteAPIView, 
    UpdateNoteAPIView, 
    DeleteNoteAPIView,
    UserNotesView, 
)

urlpatterns = [
    # Traditional home view - change if you're making it purely API-based
    # path('', views.home_view, name='home'), 

    # API paths for notes
    path('getUserNotes/', UserNotesView.as_view(), name='api_get_all_notes'),  # Endpoint to get all notes (if needed)
    path('create/', CreateNoteAPIView.as_view(), name='api_create_note'),  # Create a new note
    path('update/<int:note_id>/', UpdateNoteAPIView.as_view(), name='api_update_note'),  # Update an existing note
    path('delete/<int:note_id>/', DeleteNoteAPIView.as_view(), name='api_delete_note'),  # Delete a note
]
