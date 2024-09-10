from django.db import models
from django.contrib.auth.models import User
import openai
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUserManager, User, Teacher, Student
from profiles.form import MessageForm
from django.conf import settings
#from profiles.models import UserProfile

openai.api_key = settings.OPENAI_API_KEY
def chatbox(request):
    user_profile = UserProfile.objects.get(user=request.user)
    messages = Message.objects.all().order_by('-timestamp')
    response = None
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.save()
            
            # 与OpenAI ChatGPT交互
            response = get_chatgpt_response(new_message.content)
            
            return redirect('chatbox')
    else:
        form = MessageForm()
    
    context = {
        'user_profile': user_profile,
        'messages': messages,
        'form': form,
        'response': response,
    }
    return render(request, 'calculator/chatbox.html', context)

def get_chatgpt_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)