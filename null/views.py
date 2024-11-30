from io import BytesIO
from django.core.files.base import ContentFile
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import uuid
import re
import random
from .models import *
import cv2
import numpy as np
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

import sqlite3

from .models import Reservation
# Create your views here.
def home(request):
    return render(request, 'null/home.html')



def reservation(request): #예약 하는 곳
    if request.method == "POST":
        name = request.POST['name']
        gender = request.POST['gender']
        age = request.POST['age']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        date = request.POST['date']

        reser = Reservation(name=name, phone_number=phone_number, email=email, date=date, gender=gender, age=age)
        reser.save()
        return redirect(reverse('null:make_code', args=[reser.id])) #make_code로 가기
    else:
        return render(request, 'null/reser.html')#reser.html로 가기

def make_code(request, reser_id):
    def generate_unique_reservation_code():
        while True:
            # 6자리 랜덤 숫자 코드 생성
            code = f"RSV-{random.randint(100000, 999999)}"

            # Reservation 모델에서 코드 중복 여부 확인
            if not Reservation.objects.filter(reser_code=code).exists():
                return code
    reser_code = generate_unique_reservation_code()
    personal_imform = Reservation.objects.get(id=reser_id)
    personal_imform.reser_code = reser_code #예약 코드 개인에게 저장
    personal_imform.save()
    return redirect(reverse('null:send_mail', args=[reser_id]))


# 이메일 전송 함수
def send_mail(request, reser_id):
    smtp_server = "smtp.naver.com"
    smtp_port = 587
    reser = Reservation.objects.get(id=reser_id)
    sender_email = "rest753321@naver.com"
    sender_password = "wodbs123"
    receiver_email = reser.email

    subject = "체험형 공방 예약 완료 안내"
    body = (
        f"안녕하세요, {reser.name}님.\n\n"
        f"체험형 공방 예약이 완료되었습니다.\n"
        f"예약 날짜: {reser.date.year}년 {reser.date.month}월 {reser.date.day}일\n"
        f"예약 시간: {reser.date.hour}시 {reser.date.minute}분 \n"
        f"예약 코드: {reser.reser_code}\n\n"
        f"예약해주셔서 감사합니다!"
    )
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류가 발생했습니다: {e}")
    return redirect(reverse('null:home'))

def upload_image(request):
    if request.method == "POST":
        form = ImageFileForm(request.POST, request.FILES)

        if form.is_valid():
            ImageFile.objects.all().delete()
            form.save()

            return redirect(reverse("null:detect"))
    else:
        form = ImageFileForm()
        return render(request, 'null/detect.html', {'form': form})

def line_detection(request):
    def empty(pos):
        pass

    uploaded_img = ImageFile.objects.last()
    img = cv2.imread(uploaded_img.image.path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (300, 400))

    #가우시안 블러링 - 노이즈 제거하는 거!
    gaus_img = cv2.GaussianBlur(img, (5, 5), 0.3)

    #cv2.imshow('view', img)
    #canny = cv2.Canny(img, 150, 200)
    #cv2.imshow("Canny", canny)
    #cv2.waitKey(10000)
    #cv2.destroyAllWindows()
    #canny 방법


    sobel_x = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)


    gradient_magnitude = cv2.magnitude(sobel_x, sobel_y)
    gradient_magnitude = np.clip(gradient_magnitude,180, 255).astype(np.uint8)

    image_rgba = cv2.cvtColor(gradient_magnitude, cv2.COLOR_BGR2BGRA)

    black_pixels = (image_rgba[:, :, :3] == [180,180,180]).all(axis=2)

    image_rgba[black_pixels, :3] = [255,255,255]
    image_rgba[black_pixels, 3] = 100

    is_success, buffer = cv2.imencode(".png", image_rgba)
    if not is_success:
        raise Exception("이미지 인코딩 실패")
    io_stream = BytesIO(buffer)
    io_stream.seek(0)
    cube_image = ImageFile.objects.last()
    cube_image.image.save("processed_image.png", ContentFile(io_stream.read()))


    return redirect(reverse('null:show_cube'))

def show_cube(request):
    image = ImageFile.objects.last()
    return render(request, 'null/show_cube.html', {'image': image})

def check_code(request):
    if request.method == "POST":
        reser_code = request.POST['reser_code']
        place = request.POST['place'] #관광 장소
        personal_inform = Reservation.objects.get(reser_code=reser_code)
        personal_inform.activity_set.create(activity_name=place)
        return redirect(reverse('null:check_code'))
    else:
        return render(request, 'null/check_code.html')
