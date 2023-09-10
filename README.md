# Witty Chat App

Witty Chat App is a real-time chat application built using Django that allows users to chat with friends in real-time. This project uses SSE for instant messaging and includes user authentication, friend requests, and chat message history.

Demo:- https://witty.up.railway.app/

## Features

- User registration and authentication.
- Add friends by searching for their usernames.
- Real-time chat using SSE.
(Note: After deploying the code on web, SSE was slowing down the web app and was not functioning properly so I removed it from javascript If you wish you can still use it all models and logic are intact you just have to eventSource in Javacript)
- Chat message history.
- User-friendly and responsive UI.
- Built-in profile pictures and customizable profiles.

## Getting Started

To get started with the Witty Chat App on your local machine, follow these steps:

### Installation

1. Clone the repository:
   
   ```bash
   git clone https://github.com/Ruchit-Gaurh/Witty-Chat-App.git

2. Change to the project directory:
   
    ```bash
    cd rchatapp

3. Install Python dependencies:

     ```bash
     pip install -r requirements.txt

4. Apply database migrations:

     ```bash
     python manage.py migrate

5. Create a superuser account (admin):

     ```bash
     python manage.py createsuperuser

6. Start the development server:

     ```bash
     python manage.py runserver

7. Access the app in your web browser at http://127.0.0.1:8000/chats/.
