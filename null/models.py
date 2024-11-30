from django.db import models
from django.contrib.postgres.fields import ArrayField

class Time(models.Model):
    possible_time = models.DateTimeField() # 예약 시간대들.
    # 날짜 마다 가능한 시간들 저장하기
    isvalid = models.BooleanField(default="TRUE") #예약 가능한지? 혹시 몰라서 넣은것들
    possible_team = models.IntegerField(default=4) #예약 가능한 팀

class Reservation(models.Model): # 예약자 팀 정보
    name = models.CharField(default="", max_length=50) #예약자명

    phone_number = models.CharField(default="", max_length=50)

    email = models.EmailField(default="")

    date = models.DateTimeField() #예약 지정일

    reser_code = models.CharField(default="", max_length=50) #예약 코드

    gender = models.CharField(default="", max_length=10)
    age = models.IntegerField(default=0)

class activity(models.Model):
    reservation_fk = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    activity_name = models.CharField(default="", max_length=50)

class ImageFile(models.Model):
    image = models.ImageField() # 이미지 받기

    def __str__(self):
        return f"파일명 : {self.image}"




