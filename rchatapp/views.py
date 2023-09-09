from django.shortcuts import render, HttpResponse, redirect

def mred(request):
    return redirect("/chats/")