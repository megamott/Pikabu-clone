from django.urls import path, include

app_name = 'authentication'
urlpatterns = [
    path('', include('djoser.urls'), name='auth'),
    path('auth_token/', include('djoser.urls.authtoken'), name='auth-token'),
]
