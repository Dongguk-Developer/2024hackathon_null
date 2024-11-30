from django.urls import path
from .views import *

app_name='null'
urlpatterns = [
    path('upload/', upload_image, name='detect' ),
    path('detect/', line_detection, name='detect' ),
    path('home/', home, name='home' ),
    path('reservation/', reservation, name='reservation' ),
    path('send_mail/<int:reser_id>', send_mail, name='send_mail' ),
    path('show_cube/', show_cube, name='show_cube' ),
    path('check_code/', check_code, name='check_code' ),
    path('make_code/<int:reser_id>', make_code, name='make_code' ),
]

