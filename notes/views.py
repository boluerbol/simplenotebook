from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



# Home view for authenticated users to view all their notes (not really needed for API)
def home_view(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)
    else:
        notes = []  # Empty list for unauthenticated users
    return render(request, 'home.html', {'notes': notes})

# Create a new note (available only for authenticated users)
class CreateNoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        image = request.FILES.get('image')

        if not title or not content:
            return Response({"error": "Title and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate title
        if Note.objects.filter(user=request.user, title=title).exists():
            return Response({"error": "A note with this title already exists."}, status=status.HTTP_400_BAD_REQUEST)

        note = Note.objects.create(
            user=request.user,
            title=title,
            content=content,
            image=image
        )
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Update an existing note (available only for authenticated users)
class UpdateNoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)

        if note.user != request.user:
            return Response({"error": "You do not have permission to update this note."}, status=status.HTTP_403_FORBIDDEN)

        new_title = request.data.get('title', note.title)
        content = request.data.get('content', note.content)
        image = request.FILES.get('image')

        # Check for duplicate title (excluding the current note)
        if Note.objects.filter(user=request.user, title=new_title).exclude(id=note.id).exists():
            return Response({"error": "A note with this title already exists."}, status=status.HTTP_400_BAD_REQUEST)

        note.title = new_title
        note.content = content
        if image:
            note.image = image
        note.save()

        serializer = NoteSerializer(note)
        return Response(serializer.data)


# Delete a note (available only for authenticated users)
class DeleteNoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)

        if note.user != request.user:
            return Response({"error": "You do not have permission to delete this note."}, status=status.HTTP_403_FORBIDDEN)

        note.delete()
        return Response({"message": "Note deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class UserNotesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Filter notes by the logged-in user
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    
