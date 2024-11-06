from django.urls import path
from hr_app import views
urlpatterns = [
    path('Employee_list',views.Employee_list,name='Employee_list'),
    path('AddDetails/<int:id>',views.AddDetails,name='AddDetails'),
    path('view_employee_profile/<int:id>',views.view_employee_profile,name='view_employee_profile'),
    path('update_employee_details/<int:id>',views.update_employee_details,name='update_employee_details'),
    path('delete_employee_details/<int:id>',views.delete_employee_details,name='delete_employee_details'),
    path('employee_search_and_export',views.employee_search_and_export,name='employee_search_and_export'),
    path('view_leave_list',views.view_leave_list,name='view_leave_list'),
    path('approve_leave_request/', views.approve_leave_request, name='approve_leave_request'),
    path('reject_leave_request/', views.reject_leave_request, name='reject_leave_request'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('request_leave', views.leave_request_form, name='leave_request_form'),
    path('search_approved_leave_requests',views.search_approved_leave_requests,name='search_approved_leave_requests'),
    path('employee/', views.employee_detail, name='employee_detail'),
    path('leave_history/<int:id>',views.leave_history,name='leave_history'),
    path('create_payroll/<int:id>',views.create_payroll,name='create_payroll'),
    path('payroll_summary/<int:id>',views.payroll_summary,name='payroll_summary'),
    path('payroll-by-month/', views.payroll_by_month, name='payroll_by_month'),
]