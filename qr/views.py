from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.timezone import now
from django.utils import timezone
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
import json
import csv
from datetime import datetime
from qr.models import QrData,MealSlot
from django.db.models import Count
from django.utils.timezone import now
from io import BytesIO
import pandas as pd
import csv
from django.utils.timezone import now, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.utils.timezone import localdate
# PDF support
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .models import (
    MenuItem,
    MenuImage,
    UserHistory,
    Company,
    Employee,
    Department,
    Muster,
    MealSlot
    
)
from qr.models import QrData
from .forms import MenuImageForm

import qrcode
import qrcode.image.svg
from io import BytesIO
import base64
import numpy as np
import cv2
from PIL import Image

# ---------------- Dashboard & QR ----------------

@login_required(login_url="qr:login")
def dashboard_view(request):
    today = timezone.now().date()
    slots = MealSlot.objects.all().order_by('start_time')

    # आजचे counts
    today_data = QrData.objects.filter(date=today)
    tea_count = today_data.filter(meal='Tea').aggregate(total=Sum('quantity'))['total'] or 0
    coffee_count = today_data.filter(meal='Coffee').aggregate(total=Sum('quantity'))['total'] or 0
    snacks_count = today_data.filter(meal='Snacks').aggregate(total=Sum('quantity'))['total'] or 0
    breakfast_count = today_data.filter(meal='Breakfast').aggregate(total=Sum('quantity'))['total'] or 0
    lunch_count = today_data.filter(meal='Lunch').aggregate(total=Sum('quantity'))['total'] or 0
    dinner_count = today_data.filter(meal='Dinner').aggregate(total=Sum('quantity'))['total'] or 0

    # Recent 5 meals
    latest_meals = QrData.objects.all().order_by('-date', '-time')[:5]

    context = {
        'slots': slots,
        'tea_count': tea_count,
        'coffee_count': coffee_count,
        'snacks_count': snacks_count,
        'breakfast_count': breakfast_count,
        'lunch_count': lunch_count,
        'dinner_count': dinner_count,
        'current_date': today.strftime('%B %d, %Y'),
        'latest_meals': latest_meals,
    }
    return render(request, "dashboard.html", context)


def qrscanner_view(request):
    return render(request, 'qrscanner.html')

def qrcode_generate(request):
    template_name = 'qr.html'
    qrcode_img = get_qrcode_svg('{}&{}'.format('This is the qrcode data guys.', 'bip-zip'))
    return render(request, template_name, {'qrcode': qrcode_img})

def get_qrcode_svg(text):
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(text, image_factory=factory, box_size=30)
    stream = BytesIO()
    img.save(stream)
    base64_image = base64.b64encode(stream.getvalue()).decode()
    return 'data:image/svg+xml;utf8;base64,' + base64_image

@csrf_exempt
def qrscanner_api(request):
    if request.method == 'POST':
        try:
            data_json = json.loads(request.body)
            image_data = data_json.get('image')
            if not image_data:
                return JsonResponse({'status': 'fail', 'message': 'No image found'}, status=400)

            image_bytes = base64.b64decode(image_data.split(',')[1])
            img = BytesIO(image_bytes)
            qr_text = qrcodeReader(img)

            if qr_text:
                try:
                    employee_id, item = qr_text.split('-', 1)
                    muster_obj = Muster.objects.create(employee_id=employee_id, item=item)
                    return JsonResponse({'status': 'success', 'data': qr_text, 'id': muster_obj.id})
                except Exception:
                    return JsonResponse({'status': 'fail', 'message': 'Invalid QR code format'}, status=400)
            else:
                return JsonResponse({'status': 'fail', 'message': 'No QR code detected'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': f'Exception occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=405)

def qrcodeReader(img):
    try:
        image = Image.open(img).convert('RGB')
        np_image = np.array(image)
        bgr_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(bgr_image)
        return data if data else None
    except Exception as e:
        print("Error in QR decode:", str(e))
        return None

class QrCodeView(View):
    def get(self, request):
        return render(request, 'qr.html')

class QrCodeScan(View):
    def get(self, request):
        return render(request, 'qrscanner.html')

# ---------------- Meal Slot Dashboard ----------------

def meal_slot_dashboard(request):
    slots = MealSlot.objects.all().order_by('start_time')
    current_year = timezone.now().year
    today = timezone.now().date()

    # ----- Monthly data -----
    tea_monthly = [0] * 12
    coffee_monthly = [0] * 12
    snacks_monthly = [0] * 12
    breakfast_monthly = [0] * 12
    lunch_monthly = [0] * 12
    dinner_monthly = [0] * 12

    monthly_counts = QrData.objects.filter(date__year=current_year) \
    .annotate(month=ExtractMonth('date')) \
    .values('month', 'meal') \
    .annotate(count=Count('id'))

    for entry in monthly_counts:
        month_idx = entry['month'] - 1
        item = entry['meal']
        count = entry['count']

        if item == 'Tea':
            tea_monthly[month_idx] = count
        elif item == 'Coffee':
            coffee_monthly[month_idx] = count
        elif item == 'Snacks':
            snacks_monthly[month_idx] = count
        elif item == 'Breakfast':
            breakfast_monthly[month_idx] = count
        elif item == 'Lunch':
            lunch_monthly[month_idx] = count
        elif item == 'Dinner':
            dinner_monthly[month_idx] = count

    # ----- Today's summary -----
    today_data = QrData.objects.filter(date=today)
    tea_count = today_data.filter(meal='Tea').aggregate(total=Sum('quantity'))['total'] or 0
    coffee_count = today_data.filter(meal='Coffee').aggregate(total=Sum('quantity'))['total'] or 0
    snacks_count = today_data.filter(meal='Snacks').aggregate(total=Sum('quantity'))['total'] or 0
    breakfast_count = today_data.filter(meal='Breakfast').aggregate(total=Sum('quantity'))['total'] or 0
    lunch_count = today_data.filter(meal='Lunch').aggregate(total=Sum('quantity'))['total'] or 0
    dinner_count = today_data.filter(meal='Dinner').aggregate(total=Sum('quantity'))['total'] or 0
     # ✅ Recent 5 meals
    latest_meals = QrData.objects.all().order_by('-date', '-time')[:5]
    context = {
        'slots': slots,
        'tea_data': json.dumps(tea_monthly),
        'coffee_data': json.dumps(coffee_monthly),
        'snacks_data': json.dumps(snacks_monthly),
        'breakfast_data': json.dumps(breakfast_monthly),
        'lunch_data': json.dumps(lunch_monthly),
        'dinner_data': json.dumps(dinner_monthly),
        'tea_count': tea_count,
        'coffee_count': coffee_count,
        'snacks_count': snacks_count,
        'breakfast_count': breakfast_count,
        'lunch_count': lunch_count,
        'dinner_count': dinner_count,
        'current_date': today.strftime('%B %d, %Y'),
        'latest_meals': latest_meals,
    }

    return render(request, 'dashboard.html', context)
# ---------------- Menu Item Management ----------------

def add_item_view(request):
    return render(request, 'qr/add_item.html')

def manage_menu_items(request):
    items = MenuItem.objects.all()
    return render(request, 'qr/manage_menu_items.html', {'menu_items': items})

@csrf_exempt
def save_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('id')
        name = data.get('name')
        price = data.get('price')

        if item_id:
            item = get_object_or_404(MenuItem, id=item_id)
            item.name = name
            item.price = price
            item.save()
            return JsonResponse({'message': 'Item updated'})
        else:
            MenuItem.objects.create(name=name, price=price)
            return JsonResponse({'message': 'Item added'})

    return JsonResponse({'error': 'Invalid method'}, status=400)

def delete_item(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get("id")
            item = MenuItem.objects.get(id=item_id)
            item.delete()
            return JsonResponse({'message': 'Item deleted successfully'})
        except MenuItem.DoesNotExist:
            return JsonResponse({'message': 'Item not found'}, status=404)
    return JsonResponse({'message': 'Invalid request'}, status=400)

# ---------------- Menu HTML Views ----------------

def add_item(request):
    return render(request, 'qr/add_item.html')

def view_items(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'qr/view_items.html', {'menu_items': menu_items})

def upload_menu(request):
    if request.method == 'POST':
        form = MenuImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('qr:upload_menu')
    else:
        form = MenuImageForm()

    images = MenuImage.objects.order_by('-uploaded_at')
    return render(request, 'qr/upload_menu.html', {'form': form, 'images': images})

@require_POST
def delete_menu_image(request, image_id):
    img = get_object_or_404(MenuImage, id=image_id)
    img.image.delete()
    img.delete()
    return redirect('qr:upload_menu')

def time_slots(request):
    slots = MealSlot.objects.all()

    if request.method == "POST":
        for slot in slots:
            start_time = request.POST.get(f"start_time_{slot.id}")
            end_time = request.POST.get(f"end_time_{slot.id}")
            if start_time and end_time:
                slot.start_time = start_time
                slot.end_time = end_time
                slot.save()
        messages.success(request, "Meal slot timings updated successfully!")
        return redirect('qr:time_slots')

    return render(request, 'time_slots.html', {"slots": slots})

def view_reports(request):
    company     = request.GET.get('company')
    department  = request.GET.get('department')
    date_from   = request.GET.get('date_from')
    date_to     = request.GET.get('date_to')

    # base queryset (QrData direct use karu)
    queryset = QrData.objects.all().order_by('-date', '-time')

    # ----- Apply filters -----
    if company:
        queryset = queryset.filter(employee__company__id=company)
    if department:
        queryset = queryset.filter(employee__department__id=department)
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)

    # ----- CSV DOWNLOAD -----
    if request.GET.get('download') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="meal_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name/ID', 'Date', 'Time', 'Meal', 'Qty'])
        for r in queryset:
            writer.writerow([r.employee.name, r.date, r.time, r.meal, r.quantity])
        return response

    # ----- EXCEL DOWNLOAD -----
    if request.GET.get('download') == 'excel':
        df = pd.DataFrame(queryset.values(
            'employee__name', 'date', 'time', 'meal', 'quantity'
        ))
        with BytesIO() as b:
            writer = pd.ExcelWriter(b, engine='openpyxl')
            df.to_excel(writer, index=False, sheet_name='Meal Report')
            writer.close()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="meal_report.xlsx"'
            return response

    # ----- PDF DOWNLOAD -----
    if request.GET.get('download') == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="meal_report.pdf"'
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        data = [['Name/ID','Date','Time','Meal','Qty']]
        for r in queryset:
            data.append([r.employee.name, str(r.date), str(r.time), r.meal, r.quantity])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
            ('GRID',(0,0),(-1,-1),1,colors.black),
        ]))
        doc.build([table])
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    # Render HTML report page
    context = {
    'records': queryset,
    'companies': Company.objects.all(),
    'departments': Department.objects.all(),
    'selected_company': company,
    'selected_department': department,
    'date_from': date_from,
    'date_to': date_to,
   }
    return render(request, 'view_reports.html', context)



def dashboard(request):
    recent_history = UserHistory.objects.all().order_by('-date', '-time')[:5]
    return render(request, 'dashboard.html', {'recent_history': recent_history})

def set_company(request):
    companies = Company.objects.all()
    return render(request, 'qr/set_company.html', {'companies': companies})

@require_POST
def add_company(request):
    name = request.POST.get('name')
    if name:
        Company.objects.create(name=name)
    return redirect('qr:set_company')

@require_POST
def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.delete()
    return redirect('qr:set_company')

# --- Employee Management ---

@require_http_methods(["GET", "POST"])
def add_employee(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        dept_id = request.POST.get("department")
        department = Department.objects.get(id=dept_id) if dept_id else None

        Employee.objects.create(company=company, name=name, email=email, department=department)
        return redirect('qr:company_employees', company_id=company.id)

    else:
        departments = Department.objects.all()
        context = {
            "company": company,
            "departments": departments,
        }
        return render(request, 'qr/add_employee.html', context)

def company_employees(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    employees = company.employees.all()
    departments = Department.objects.all()  # Departments add करा

    context = {
        'company': company,
        'employees': employees,
        'departments': departments,   # Template साठी
    }
    return render(request, 'qr/company_employees.html', context)


@require_http_methods(["GET", "POST"])
@require_http_methods(["GET", "POST"])
def edit_employee(request, company_id, employee_id):
    employee = get_object_or_404(Employee, id=employee_id, company_id=company_id)
    if request.method == "POST":
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')

        # 👇 Department compulsory ठेवणे
        dept_id = request.POST.get("department")
        if not dept_id:
            messages.error(request, "Department is required!")
            return redirect(request.path)

        employee.department = Department.objects.get(id=dept_id)
        employee.save()
        return redirect('qr:company_employees', company_id=company_id)

    departments = Department.objects.all()
    return render(request, 'qr/edit_employee.html', {'employee': employee, 'departments': departments})


@require_POST
def delete_employee(request, company_id, employee_id):
    employee = get_object_or_404(Employee, id=employee_id, company_id=company_id)
    employee.delete()
    return redirect('qr:company_employees', company_id=company_id)

# --- Department Management ---

def set_department(request):
    companies = Company.objects.all()
    selected_company_id = request.GET.get('company')

    if selected_company_id:
        
        departments = Department.objects.filter(employee__company_id=selected_company_id).distinct()
    else:
        departments = Department.objects.none()

    context = {
        'companies': companies,
        'departments': departments,
        'selected_company_id': selected_company_id,
    }
    return render(request, 'qr/set_department.html', context)


@require_POST
def add_department(request):
    name = request.POST.get('name')
    if name:
        Department.objects.create(name=name)
    return redirect('qr:set_department')

@require_http_methods(["GET", "POST"])
def edit_department(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)
    if request.method == "POST":
        department.name = request.POST.get('name')
        department.save()
        return redirect('qr:set_department')
    return render(request, 'qr/edit_department.html', {'department': department})

@require_POST
def delete_department(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)
    department.delete()
    return redirect('qr:set_department')

def api_get_menu_items(request):
    items = MenuItem.objects.all().values('id', 'name', 'price')
    return JsonResponse({'menu_items': list(items)})

def department_employees(request, dept_id):
    selected_company_id = request.GET.get('company')
    department = get_object_or_404(Department, id=dept_id)
    employees = Employee.objects.filter(department=department)

    if selected_company_id:
        employees = employees.filter(company_id=selected_company_id)

    context = {
        'department': department,
        'employees': employees,
        'selected_company_id': selected_company_id,
    }
    return render(request, 'qr/department_employees.html', context)

@csrf_exempt
def save_qr_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            meal = data.get('meal')
            qty  = data.get('qty')

            if not name or not meal or qty is None:
                return JsonResponse({'status': 'fail', 'message': 'Missing QR data'}, status=400)

            today = datetime.now().date()
            current_time = datetime.now().time()

            # Fetch employee object
            employee_obj = Employee.objects.filter(name=name).first()
            if not employee_obj:
                return JsonResponse({'status': 'fail', 'message': 'Employee not found'}, status=404)

            # Save QR data
            QrData.objects.create(
                employee=employee_obj,
                name_id=name,
                date=today,
                time=current_time,
                meal=meal,
                quantity=int(qty)
            )

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=405)

def employee_report(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    # Current month
    today = now().date()
    start_of_month = today.replace(day=1)

    records = QrData.objects.filter(
        employee=employee,
        date__range=[start_of_month, today]
    ).order_by('-date', '-time')

    # ----- CSV download -----
    if request.GET.get('download') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{employee.name}_monthly_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date','Time','Meal','Qty'])
        for r in records:
            writer.writerow([r.date, r.time, r.meal, r.quantity])
        return response

    # ----- Excel download -----
    if request.GET.get('download') == 'excel':
        df = pd.DataFrame(records.values('date','time','meal','quantity'))
        with BytesIO() as b:
            with pd.ExcelWriter(b, engine='openpyxl') as writer:  
             df.to_excel(writer, index=False, sheet_name='Monthly Report')
            response = HttpResponse(b.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="monthly_report.xlsx"'
            return response


    # ----- PDF download -----
    if request.GET.get('download') == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{employee.name}_monthly_report.pdf"'
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        data = [['Date','Time','Meal','Qty']]
        for r in records:
            data.append([str(r.date), str(r.time), r.meal, r.quantity])
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
            ('GRID',(0,0),(-1,-1),1,colors.black),
        ]))
        doc.build([table])
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    # Render HTML page
    context = {
        'employee': employee,
        'records': records,
        'date_from': start_of_month,
        'date_to': today,
    }
    return render(request, "employee_report.html", context)



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("qr:dashboard")   
        else:
            messages.error(request, "❌ Invalid username or password")
    return render(request, "login.html")   


def logout_view(request):
    logout(request)
    return redirect("qr:login")

@require_GET
def api_chart_last_5_days(_request):
    today = localdate()
    last_5_dates = [today - timedelta(days=i) for i in reversed(range(5))]

    labels = []
    tea_counts = []
    snacks_counts = []
    coffee_counts = []
    breakfast_counts = []
    lunch_counts = []

    for d in last_5_dates:
        labels.append(d.strftime("%b %d"))
        day_data = QrData.objects.filter(date=d)
        tea_counts.append(day_data.filter(meal="Tea").aggregate(total=Sum("quantity"))['total'] or 0)
        snacks_counts.append(day_data.filter(meal="Snacks").aggregate(total=Sum("quantity"))['total'] or 0)
        coffee_counts.append(day_data.filter(meal="Coffee").aggregate(total=Sum("quantity"))['total'] or 0)
        breakfast_counts.append(day_data.filter(meal="Breakfast").aggregate(total=Sum("quantity"))['total'] or 0)
        lunch_counts.append(day_data.filter(meal="Lunch").aggregate(total=Sum("quantity"))['total'] or 0)

    return JsonResponse({
        "labels": labels,
        "tea": tea_counts,
        "snack": snacks_counts,
        "coffee": coffee_counts,
        "breakfast": breakfast_counts,
        "lunch": lunch_counts
    })
