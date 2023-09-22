from django import forms
from django.forms import ModelForm
from .models import ChatMessage

class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "chat-input", "id":"message", "rows":1, "placeholder":"Type your message and press Enter..."}))
    class Meta:
        model = ChatMessage
        fields = ["body"]