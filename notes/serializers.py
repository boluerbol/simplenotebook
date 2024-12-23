from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # Add image_url as a custom field

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url  # This will return the URL of the image
        return None