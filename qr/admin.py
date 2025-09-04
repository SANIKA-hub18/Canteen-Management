from django.contrib import admin
from .models import UserHistory

# Register your models here.
from django.contrib import admin
from .models import MealSlot

class MealSlotAdmin(admin.ModelAdmin):
    list_display = ('meal_type', 'start_time', 'end_time')

admin.site.register(MealSlot, MealSlotAdmin)

@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'time', 'meal', 'qty')