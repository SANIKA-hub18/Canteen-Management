from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
app_name = 'qr'
urlpatterns = [
    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard
    path("meal-slots/", views.dashboard_view, name="dashboard"),  # ✅ dashboard.html मुख्य
    path("dashboard/", views.dashboard_view, name="dashboard_alt"),  # alternative URL

    # QR Code
    path("qrpage/", views.QrCodeView.as_view(), name="qr_code_view"),
    path("scan/", views.QrCodeScan.as_view(), name="qrscan"),
    path("scanner/", views.qrscanner_view, name="qrscanner"),

    # Menu Items
    path("add-item/", views.add_item_view, name="add_item"),
    path("manage-menu-items/", views.manage_menu_items, name="manage_menu_items"),
    path("save-item/", views.save_item, name="save_item"),
    path("delete-item/", views.delete_item, name="delete_item"),
    path("view-items/", views.view_items, name="view_items"),
    path("upload-menu/", views.upload_menu, name="upload_menu"),
    path("delete-menu-image/<int:image_id>/", views.delete_menu_image, name="delete_menu_image"),
    
    # Menu Items API (for AJAX calls)
    path("api/menu-items/", views.api_get_menu_items, name="api_get_menu_items"),

    # Reports & Slots
    path("time-slots/", views.time_slots, name="time_slots"),
    path("reports/", views.view_reports, name="view_reports"),
    path("save_qr_data/", views.save_qr_data, name="save_qr_data"),
    path("employee/<int:employee_id>/report/", views.employee_report, name="employee_report"),

    # Company
    path("settings/company/", views.set_company, name="set_company"),
    path("settings/company/add/", views.add_company, name="add_company"),
    path("settings/company/<int:company_id>/delete/", views.delete_company, name="delete_company"),
    path("settings/company/<int:company_id>/", views.company_employees, name="company_employees"),
    path("settings/company/<int:company_id>/add_employee/", views.add_employee, name="add_employee"),
    path("settings/company/<int:company_id>/edit/<int:employee_id>/", views.edit_employee, name="edit_employee"),
    path("settings/company/<int:company_id>/delete/<int:employee_id>/", views.delete_employee, name="delete_employee"),

    # Department
    path("settings/department/", views.set_department, name="set_department"),
    path("settings/department/add/", views.add_department, name="add_department"),
    path("settings/department/<int:dept_id>/edit/", views.edit_department, name="edit_department"),
    path("settings/department/<int:dept_id>/delete/", views.delete_department, name="delete_department"),
    path("department/<int:dept_id>/employees/", views.department_employees, name="department_employees"),

    # Forgot Password URLs
    # Step 1: Request reset
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            success_url=reverse_lazy('qr:password_reset_done')  # ✅ Done page वर redirect
        ),
        name='password_reset'
    ),

    # Step 2: Reset done
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name='password_reset_done'
    ),

    # Step 3: Password reset confirm
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy('qr:password_reset_complete')  # ✅ Reset complete page
        ),
        name='password_reset_confirm'
    ),

    # Step 4: Reset complete
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name='password_reset_complete'
    ),

    path("api/chart-data/", views.api_chart_last_5_days, name="api_chart_last_5_days"),

]
