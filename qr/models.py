from django.db import models

class Muster(models.Model):
    employee_id = models.CharField(max_length=20)
    item = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_id} - {self.item}"

    class Meta:
        db_table = 'muster'


MEAL_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
]

class MealSlot(models.Model):
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.meal_type} ({self.start_time} - {self.end_time})"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"
    
class MenuImage(models.Model):
    image = models.ImageField(upload_to='menu_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Menu uploaded on {self.uploaded_at}"

class UserHistory(models.Model):
    user_id = models.CharField(max_length=50)  # Name/ID
    date = models.DateField()
    time = models.TimeField()
    meal = models.CharField(max_length=50)  # Breakfast, Lunch, etc.
    qty = models.IntegerField()

    def __str__(self):
        return f"{self.user_id} - {self.meal} ({self.date})"
    
class UserMealHistory(models.Model):
    user_id = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    meal = models.CharField(max_length=50)
    qty = models.IntegerField()

    def __str__(self):
        return f"{self.user_id} - {self.meal} on {self.date} at {self.time}"
    
class Company(models.Model):
    name = models.CharField(max_length=255)

class Department(models.Model):
    name = models.CharField(max_length=255)
    
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employee')

class QrData(models.Model):
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        null=True,      # database madhe null allow karte
        blank=True      # forms madhe blank allow karte
    )
    name_id = models.CharField(max_length=100)  # हे Name/ID साठी
    date = models.DateField()
    time = models.TimeField()
    meal = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name_id
