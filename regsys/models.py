from django.db import models
from django.db.models import F, Q
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

class Event(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Номер")
    event_name = models.CharField(max_length=200, verbose_name="Название")
    start_date = models.DateField(verbose_name="Первый день")
    end_date = models.DateField(verbose_name="Последний день")
    place = models.CharField(max_length=100, verbose_name="Место")
    annotation = models.CharField(max_length=1000, verbose_name="Аннотация")
    
    def __str__(self):
        return self.event_name
        
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("Последний день мероприятия не может идти раньше первого")
        
    
    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        constraints = [
            models.UniqueConstraint(fields=['event_name'], name='unique name')
    ]


class Timetable(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Номер")
    timetable_name = models.CharField(max_length=200, verbose_name="Название")
    category = models.CharField(max_length=100, verbose_name="Категория")
    date = models.DateField(verbose_name="Дата")
    place = models.CharField(max_length=100, verbose_name="Место")
    host = models.CharField(max_length=100, verbose_name="Ведущий")
    annotation = models.CharField(max_length=1000, verbose_name="Аннотация")
    repeating = models.BooleanField(verbose_name="Повтор?")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Событие")
    seats = models.IntegerField(default=-1, verbose_name="Свободных мест")
    
    def __str__(self):
        return self.timetable_name
        
    def clean(self):
        if self.date < self.event.start_date or self.date > self.event.end_date:
            raise ValidationError("Дата не должна выходить за рамки события")
    
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"
        
        
class Guest(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, verbose_name="Номер")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    firstname = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество")
    school = models.CharField(max_length=100, verbose_name="Место обучения")
    phone = models.CharField(max_length=100, verbose_name="Номер телефона")
    telegram = models.CharField(max_length=100, verbose_name="Телеграм")
    
    def __str__(self):
        return self.user.username
            
    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        
        
class Registration(models.Model):
    class Status(models.TextChoices):
        AFF = "AFF", "Подтверждено"
        INT = "INT", "Пересекается"
        WAI = "WAI", "Очередь"
        VIS = "VIS", "Посещено"
        MIS = "MIS", "Пропущено"
        
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name="Событие")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="Участник")
    status = models.CharField(choices=Status.choices, default=Status.AFF, verbose_name="Статус")
    
    def __str__(self):
        return str(self.timetable) + " / " + str(self.guest)
    
    def is_past(self):
        return self.status in {self.Status.VIS, self.Status.MIS}
        
    def is_seated(self):
        return self.status in {self.Status.AFF, self.Status.VIS, self.Status.MIS}
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
   
     
class Label(models.Model):
    class Type(models.TextChoices):
        TAR = "TAR", "Аудитория"
        FIE = "FIE", "Направление"
        CON = "CON", "Подтверждение"
        
    id = models.AutoField(primary_key=True, verbose_name="Номер")
    label_name = models.CharField(max_length=50, verbose_name="Название")
    type = models.CharField(choices=Type.choices, verbose_name="Тип")
    
    def __str__(self):
        return self.label_name
    
    class Meta:
        verbose_name = "Лейбл"
        verbose_name_plural = "Лейблы"


class Labelmap(models.Model):  
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Событие")
    label = models.ForeignKey(Label, on_delete=models.CASCADE, verbose_name="Лейбл")
    
    def __str__(self):
        return str(self.event) + " / " + str(self.label)
    
    class Meta:
        verbose_name = "Лейблмап"
        verbose_name_plural = "Лейблмап"

@receiver(pre_save, sender=Registration)
def minus_seat(sender, instance, **kwargs):
    if instance.id is None:
        if instance.is_seated:
            t = instance.timetable
            if t.seats > 0:
                t.seats -= 1
                t.save()
    else:
        previous = Registration.objects.get(id=instance.id)
        t = instance.timetable
        if not previous.is_seated and instance.is_seated:
            if t.seats > 0:
                t.seats -= 1
                t.save()
        if previous.is_seated and not instance.is_seated:
            if t.seats > -1:
                t.seats += 1
                t.save()
                
@receiver(pre_delete, sender=Registration)
def plus_seat(sender, instance, **kwargs):
    if instance.is_seated:
        t = instance.timetable
        if t.seats > -1:
            t.seats += 1
            t.save()
        