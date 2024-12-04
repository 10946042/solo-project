from django import forms
#from .models import Message
#from .models import UserProfile

class MessageForm(forms.ModelForm):
    class Meta:
        #model = Message
        model = ""
        fields = ['content']  # 假设消息模型中有一个content字段

        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter your message...'}),
        }