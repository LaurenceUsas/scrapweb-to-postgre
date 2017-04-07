from django.db import models

class UnitInformation(models.Model):
    construction_ref = models.CharField(primary_key=True, max_length=40)
    number = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    bedrooms = models.CharField(max_length=10)
    floor = models.CharField(max_length=20)
    area = models.FloatField()

    def __str__(self):
        return self.construction_ref

class UnitHistory(models.Model):
    date = models.DateField(auto_now=True)
    apartment = models.ForeignKey(UnitInformation, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    price = models.IntegerField()

    def __str__(self):
        return str(self.date) + ' - ' + self.apartment

class RawData(models.Model):
    date = models.DateField(auto_now=True)
    raw_data = models.CharField(max_length=100000)

    def __str__(self):
        return str(self.date)