
from django.db import models

class Calender(models.Model): # 아래 Time에 foreignkey를 주기 위한 용도임.
    day = models.DateField()
    # 그냥 밑에 Time에 짱박아도 되긴 하는데 그럼 데이터가 지저분하니까..

class Time(models.Model):
    day_fk = models.ForeignKey(Calender, on_delete=models.CASCADE)
    possible_time = models.DateTimeField() # 예약 시간대들.
    # 날짜 마다 가능한 시간들 저장하기
    isvalid = models.BooleanField(default="TRUE") #예약 가능한지? 혹시 몰라서 넣은것들
    possible_team = models.IntegerField(default=1) #예약 가능한 팀

class Reservation(models.Model):
    name = models.CharField(default="", max_length=50) #예약자명

    Number_first = models.CharField(default="", max_length=3) #010
    Number_second = models.CharField(default="", max_length=4) #0000
    Number_third = models.CharField(default="", max_length=4) #0000

    email = models.EmailField()

    count_people = models.IntegerField(default=0) #참여 인원수

    activation =models.CharField(default="", max_length=100) #활동

    date = models.DateTimeField() #예약 지정일

    reser_number = models.IntegerField(default=0) #예약번호


class ImageFile(models.Model):
    title = models.CharField(default="", max_length=100)
    image = models.ImageField() # 이미지 받기

    def __str__(self):
        return f"제목 : {self.title} 파일명 : {self.image}"




