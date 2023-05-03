from django.db import models

class Event(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Номер")
    name = models.CharField(max_length=200, verbose_name="Название")
    date = models.CharField(max_length=100, verbose_name="Даты")
    place = models.CharField(max_length=100, verbose_name="Место")
    annotation = models.CharField(max_length=1000, verbose_name="Аннотация")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"


class Timetable(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Номер")
    name = models.CharField(max_length=200, verbose_name="Название")
    category = models.CharField(max_length=100, verbose_name="Категория")
    date = models.DateField(verbose_name="Дата")
    place = models.CharField(max_length=100, verbose_name="Место")
    host = models.CharField(max_length=100, verbose_name="Ведущий")
    annotation = models.CharField(max_length=1000, verbose_name="Аннотация")
    repeating = models.BooleanField(verbose_name="Повтор?")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Событие")
    seats = models.IntegerField(default=-1, verbose_name="Свободных мест")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"
        
        
class Guest(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Номер")
    name = models.CharField(max_length=200, verbose_name="Название")
    school = models.CharField(max_length=100, verbose_name="Место обучения")
    email = models.EmailField(max_length=100, verbose_name="Почта")
    phone = models.CharField(max_length=100, verbose_name="Телефон")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        
        
class Registration(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name="Событие")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name="Участник")
    
    def __str__(self):
        return str(self.timetable) + " / " + str(self.guest)
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"