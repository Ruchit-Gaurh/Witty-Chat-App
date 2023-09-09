from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile, Friend, ChatMessage
from .forms import ChatMessageForm
import json
import time

# Create your views here.
@login_required(login_url="/chats/login_page")
def index(request):
    user = request.user.profile
    friends = user.friends.all()
    context = {'user': user, 'friends':friends}
    return render(request, "mainchat/index.html", context)

def loginkr(request):
    return HttpResponse("<h2> jyada teez mt chl jo link bheji usse open kr")

def chat(request, idf):
    friend = Friend.objects.get(profile_id=idf)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.profile.id)
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msgsender=profile, msgreciver=user)
    rec_chats.update(seen=True)
    form = ChatMessageForm()
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_mssg = form.save(commit=False)
            chat_mssg.msgsender = user
            chat_mssg.msgreciver = profile
            chat_mssg.save()
            
            return redirect("/chats/" + str(friend.profile.id))
    context = {"friend": friend, "form": form, "user": user, "profile": profile, 'chats': chats, 'num': rec_chats.count()}
    return render(request, "mainchat/chat.html", context)


def login_page(request):
    context = {}
    return render(request, "mainchat/login.html", context)

def login_user(request):
    name = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=name, password= password)
    if user is not None:
        login(request, user)
        return redirect('/chats/')
    else:
        return HttpResponse("<h2>Kyu rakhte ho aaisa password jo yaad hi na rhe<h2>")

def register_page(request):
    context = {}
    return render (request, "mainchat/register.html", context)

def register(request):
    username= request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    User.objects.create_user(str(username), str(email), str(password))
    user = User.objects.get(username=username)
    fname = request.POST['name']
    url = request.POST['url']
    if url :
        purl = url
    else:
        purl = "https://cdn-icons-png.flaticon.com/512/666/666201.png"
    ch = Profile.objects.create(user=user, name=fname, pic=purl)
    r = Friend(profile=ch)
    r.save()
    return redirect("/chats/")

    
def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponse("<h2>paheli fursat me nikal<h2>")

def sentMessage(request, idf):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=idf)
    profile = Profile.objects.get(id=friend.profile.id)
    data= json.loads(request.body)
    new_chat = data["msg"]
    new_chat_msg = ChatMessage.objects.create(body=new_chat, msgsender=user, msgreciver=profile, seen=False)
    print(new_chat)
    return JsonResponse(new_chat_msg.body, safe=False)

def receiveMessages(request, idf):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=idf)
    profile = Profile.objects.get(id=friend.profile.id)
    arr=[]
    chats = ChatMessage.objects.filter(msgsender=profile, msgreciver=user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)

def sse_chat_view(request, idf):
    response = StreamingHttpResponse(event_stream(request, idf), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["Connectiobn"] = "keep-alive"
    response["X-Accel-Buffering"] = "no"

    return response

def event_stream(request , idf):
    friend = Friend.objects.get(profile_id=idf)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.profile.id)
    rec_chats = ChatMessage.objects.filter(msgsender=profile, msgreciver=user)
    cccc = rec_chats.count()
    while True:
        rec_chats = ChatMessage.objects.filter(msgsender=profile, msgreciver=user)
        if rec_chats.count() > cccc:
            yield f"data: test\n\n"
            cccc = rec_chats.count()
            time.sleep(2)
            

def search_users(request):
    search_query = request.GET.get('q', '')  # Get the search query from the request
    users = User.objects.filter(username__icontains=search_query)  # Filter users based on the search query
    user_list = [{'username': user.username, 'email': user.email, 'id': user.id} for user in users]  # Convert users to a list of dictionaries

    return JsonResponse({'users': user_list})


def add_friend(request, profile_id):
    try:
        friend_profile = Profile.objects.get(id=profile_id)

        current_user_friend, _ = Friend.objects.get_or_create(profile=request.user.profile)
        friend_instance, created = Friend.objects.get_or_create(profile=friend_profile)

        request.user.profile.friends.add(friend_instance)
        friend_profile.friends.add(current_user_friend)
        return JsonResponse({'success': True})
    except Profile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'})