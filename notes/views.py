from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

# Получить все заметки для всех пользователей (если нужно для API)
@api_view(['GET'])
def get_all_notes(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

# Отображение всех заметок для текущего пользователя на главной странице
def home_view(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)  # Фильтруем заметки по текущему пользователю
    else:
        notes = []  # Для неаутентифицированных пользователей заметки пустые
    return render(request, 'home.html', {'notes': notes})

# Создание заметки (доступно только авторизованным пользователям)
@login_required
def create_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # Get the uploaded image

        if title and content:
            Note.objects.create(
                user=request.user, 
                title=title, 
                content=content,
                image=image)
            return redirect('home')  # После создания заметки перенаправляем на главную страницу
    return render(request, 'notes/create_note.html')  # Отображаем форму для создания заметки

# Обновление заметки (доступно только авторизованным пользователям)
@login_required
def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Проверяем, что пользователь является владельцем заметки
    if note.user != request.user:
        return redirect('home')  # Перенаправляем, если пользователь пытается изменить чужую заметку

    if request.method == "POST":
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        # Update image if provided
        if 'image' in request.FILES:
            note.image = request.FILES['image']
        note.save()
        return redirect('home')  # Перенаправляем на главную страницу после обновления
    return render(request, 'notes/update_note.html', {'note': note})

# Удаление заметки (доступно только авторизованным пользователям)
@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Проверяем, что пользователь является владельцем заметки
    if note.user != request.user:
        return redirect('home')  # Перенаправляем, если пользователь пытается удалить чужую заметку

    if request.method == "POST":
        note.delete()
        return redirect('home')  # Перенаправляем на главную страницу после удаления
    return render(request, 'notes/delete_note.html', {'note': note})

def index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})
