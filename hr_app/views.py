from django.shortcuts import render,redirect,get_object_or_404,reverse
from register_app.models import CustomUser
from hr_app.models import EmployeeDetails,RequestLeave,Payroll
from Glenda_App.models import Menu
from .forms import EmployeeDetailsForm,LeaveRequestForm,PayrollForm
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa
from openpyxl import Workbook
from openpyxl.styles import Font,Alignment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import csv
from decimal import Decimal  # For setting a default fallback value of zero
def Employee_list(request):
    # Fetch all users with is_staff=True
    users = CustomUser.objects.filter(is_staff=True,is_superuser=False)

    for user in users:

        user.details_added = EmployeeDetails.objects.filter(user=user).exists()
    paginator = Paginator(users,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the filtered HR employee details and menus to the context
    context = {
        'page_obj':page_obj
    }

    return render(request, 'hr/Employee_list.html', context)

def AddDetails(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()

    if request.method == 'POST':
        form = EmployeeDetailsForm(request.POST, request.FILES)

        emergency_contact_number = request.POST.get('emergency_contact_number')
        aadhar_no = request.POST.get('aadhar_no')
        employee_esi_no = request.POST.get('employee_esi_no')
        pf_no = request.POST.get('pf_no')

        # Validation checks
        if len(str(emergency_contact_number)) != 10:
            messages.warning(request, 'Contact number must be exactly 10 digits.')

        if len(str(aadhar_no)) != 12:
            messages.warning(request, 'Aadhar number must be exactly 12 digits.')

        if len(str(employee_esi_no)) != 20:
            messages.warning(request, 'ESI number must be exactly 20 digits.')

        if len(str(pf_no)) != 17:
            messages.warning(request, 'PF number must be exactly 17 digits.')

        if EmployeeDetails.objects.filter(aadhar_no=aadhar_no).exists():
            messages.warning(request, 'Aadhar number already exists.')
            return render(request, 'hr/add_employee_details.html', {'form': form, 'menus': menus})

        if EmployeeDetails.objects.filter(emergency_contact_number=emergency_contact_number).exists():
            messages.warning(request, 'Phone number already exists.')
            return render(request, 'hr/add_employee_details.html', {'form': form, 'menus': menus})

        if EmployeeDetails.objects.filter(employee_esi_no=employee_esi_no).exists():
            messages.warning(request, 'ESI Number already exists.')
            return render(request, 'hr/add_employee_details.html', {'form': form, 'menus': menus})

        if EmployeeDetails.objects.filter(pf_no=pf_no).exists():
            messages.warning(request, 'PF number already exists.')
            return render(request, 'hr/add_employee_details.html', {'form': form, 'menus': menus})

        if form.is_valid():
            employee = form.save(commit=False)  # Do not save yet
            employee.user_id = id  # Associate the user
            employee.save()  # Now save it

            return redirect('Employee_list')  # Redirect to employee list after successful submission
    else:
        form = EmployeeDetailsForm()

    return render(request, 'hr/add_employee_details.html', {'form': form, 'menus': menus})

def view_employee_profile(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()

    view = get_object_or_404(EmployeeDetails,user_id=id)

    return render(request,'hr/view_employee_profile.html',{'view':view,'menus':menus})

def update_employee_details(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()
    view = get_object_or_404(EmployeeDetails, user_id=id)

    if request.method == 'POST':
        form = EmployeeDetailsForm(request.POST,instance=view)

        if form.is_valid():
            form.save()
            return redirect('Employee_list')

    else:
        form = EmployeeDetailsForm(request.POST, instance=view)
    return render(request, 'hr/update_employee_details.html', {'view':view, 'menus': menus,'form':form})

def delete_employee_details(request, id):
    menus = Menu.objects.prefetch_related('submenus').all()

    # Fetch the object or return a 404 error if not found
    dtl = get_object_or_404(EmployeeDetails, id=id)

    if request.method == "POST":
        dtl.delete()
        return redirect('Employee_list')

    # Render the confirmation page for GET requests
    return render(request, 'hr/delete_employee_details.html', {'dtl': dtl,'menus':menus})


def employee_search_and_export(request):
    menus = Menu.objects.prefetch_related('submenus').all()

    # Start with an empty query to show all staff members by default
    employee_list = CustomUser.objects.filter(is_staff=True, is_superuser=False)

    search_query = request.GET.get('search_query', '').strip()
    export_format = request.GET.get('export', '')

    if search_query:
        filters = Q(is_staff=True, is_superuser=False)
        if search_query.isdigit():
            filters &= Q(phone_number__icontains=search_query)
        else:
            filters &= Q(name__icontains=search_query)

        employee_list = CustomUser.objects.filter(filters)

    # Check for export format (either 'csv' or 'pdf')
    if export_format == 'excel':
        wb = Workbook()
        ws = wb.active
        ws.title = 'Employee List'
        ws.merge_cells('A1:D1')
        ws['A1'] = 'Employee List'
        headline_font = Font(bold=True, size=14)
        ws['A1'].font = headline_font
        ws['A1'].alignment = Alignment(horizontal='center')

        headers = ['Name', 'Email', 'Phone Number']
        ws.append(headers)

        header_font = Font(bold=True)
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=2, column=col_num)
            cell.font = header_font

        for employee in employee_list:
            ws.append([employee.name, employee.email, employee.phone_number])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="employee_list.xlsx"'

        wb.save(response)
        return response

    elif export_format == 'pdf':
        # PDF export
        template = get_template('hr/employee_details_pdf.html')  # A separate template for PDF
        context = {'users': employee_list, 'menus': menus}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="employee_list.pdf"'

        pdf_status = pisa.CreatePDF(html, dest=response)

        if pdf_status.err:
            return HttpResponse('Error generating PDF', status=500)

        return response

    # Normal page rendering (with search functionality)

    for user in employee_list:

        user.details_added = EmployeeDetails.objects.filter(user=user).exists()

    context = {
        'users': employee_list,  # Filtered employees list
        'menus': menus,
    }

    return render(request, 'hr/Employee_list.html', context)

def view_leave_list(request):
    # Fetch all employees
    employees = EmployeeDetails.objects.all()

    # Prepare a list to hold employee leave requests
    leave_requests = []

    for employee in employees:
        # Get all leave requests for each employee
        requests = RequestLeave.objects.filter(employee=employee)
        leave_requests.append({
            'employee': employee,
            'requests': requests  # This will be a QuerySet of leave requests
        })

    # Apply pagination to leave_requests list
    paginator = Paginator(leave_requests, 10)  # Show 10 employees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    menus = Menu.objects.prefetch_related('submenus').all()

    # Pass the paginated leave_requests and menus to the context
    context = {
        'menus': menus,
        'page_obj': page_obj  # Include the page object in the context
    }

    return render(request, 'hr/leave_list.html', context)


@csrf_exempt
def approve_leave_request(request):
    if request.method == 'POST':
        user_id = request.POST.get('employee_user_id')
        try:
            leave_request = RequestLeave.objects.get(id=user_id)
            leave_request.approval_status = 'APPROVED'  # Update status to 'approved'
            leave_request.save()
            return JsonResponse({'success': True})
        except RequestLeave.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Leave request not found'})

@csrf_exempt
def reject_leave_request(request):
    if request.method == 'POST':
        user_id = request.POST.get('employee_user_id')
        rejection_reason = request.POST.get('rejection_reason')
        try:
            leave_request = RequestLeave.objects.get(id=user_id)
            leave_request.approval_status = 'REJECTED'  # Update status to 'rejected'
            leave_request.rejection_reason = rejection_reason
            leave_request.save()
            return JsonResponse({'success': True})
        except RequestLeave.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Leave request not found'})



def my_profile(request):
    user = request.user
    leave_requests = RequestLeave.objects.filter(employee__user=user).order_by('-start_date')  # Order by date
    menus = Menu.objects.prefetch_related('submenus').all()

    # Pagination logic
    paginator = Paginator(leave_requests, 5)  # Show 5 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'hr/my_leave_request.html', {
        'user': user,
        'leave_requests': page_obj,
        'menus': menus,
    })


def leave_request_form(request):
    menus = Menu.objects.prefetch_related('submenus').all()
    user = request.user
    emp=EmployeeDetails.objects.get(user_id=user)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            # Set the employee based on the logged-in user
            leave_request.employee_id =emp.id
            leave_request.save()
            return redirect('my_profile')  # Redirect after saving
    else:
        form = LeaveRequestForm()

    return render(request, 'hr/leave_request_form.html', {'form': form, 'menus': menus})


def search_approved_leave_requests(request):
    # Fetch all employees
    employees = EmployeeDetails.objects.all()

    # Prepare a list to hold employee leave requests
    leave_requests = []

    # Get search query from request
    search_query = request.GET.get('search_query', '').strip()

    for employee in employees:
        # Get all approved leave requests for each employee
        requests = RequestLeave.objects.filter(employee=employee, approval_status='Approved')

        print(requests)

        # If there is a search query, filter by employee name
        if search_query and search_query.lower() not in employee.user.name.lower():
            continue  # Skip this employee if the name does not match the search query

        leave_requests.append({
            'employee': employee,
            'requests': requests  # This will be a QuerySet of leave requests
        })

    # Apply pagination to leave_requests list
    paginator = Paginator(leave_requests, 10)  # Show 10 employees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    menus = Menu.objects.prefetch_related('submenus').all()

    # Pass the paginated leave_requests and menus to the context
    context = {
        'menus': menus,
        'page_obj': page_obj,  # Include the page object in the context
        'search_query': search_query,  # Include search query for form repopulation
    }

    return render(request, 'hr/leave_list.html', context)

def employee_detail(request):
    menus = Menu.objects.prefetch_related('submenus').all()

    # Get initial queryset for finished goods based on the provided ID
    Employee = EmployeeDetails.objects.all()

    # Get filter type and query date from the request
    filter_type = request.GET.get('filter')
    query_date = request.GET.get('query')  # Expected format: YYYY-MM-DD
    is_filtered = False

    # Apply filtering if filter type is 'date' and query_date is provided
    if filter_type == 'date' and query_date:
        employee_list = Employee.filter(date=query_date)
        is_filtered = True  # Flag to indicate that a filter has been applied

    # Prepare context for rendering template
    context = {
        'data': Employee,
        'menus': menus,
        'filter_type': filter_type,
        'query_date': query_date,
        'is_filtered': is_filtered  # Pass flag to template
    }

    return render(request, 'hr/employee_detail.html', context)

def leave_history(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()

    leave_request = RequestLeave.objects.filter(employee__user_id=id).order_by('-start_date')

    # Get filter type and query date from the request
    filter_type = request.GET.get('filter')
    query_date = request.GET.get('query')  # Expected format: YYYY-MM-DD
    is_filtered = False

    # Apply filtering if filter type is 'date' and query_date is provided
    if filter_type == 'date' and query_date:
        finished_good = leave_request.filter(date=query_date)
        is_filtered = True  # Flag to indicate that a filter has been applied

    # Prepare context for rendering template
    context = {
        'data': leave_request,
        'menus': menus,
        'filter_type': filter_type,
        'query_date': query_date,
        'is_filtered': is_filtered  # Pass flag to template
    }

    return render(request, 'hr/leave_history.html', context)


def create_payroll(request, id):
    # Retrieve the employee instance based on the given user ID
    employee = get_object_or_404(EmployeeDetails, user_id=id)
    basic_salary = employee.basic or Decimal('0.00')  # Ensure fallback to 0 if basic salary is null

    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():

            payroll_date = form.cleaned_data['pay_date']

            # Check if a payroll entry already exists for the same employee in the same month and year
            existing_payroll = Payroll.objects.filter(
                employee=employee,
                pay_date__year=payroll_date.year,
                pay_date__month=payroll_date.month
            ).exists()

            if existing_payroll:
                messages.warning(request,f"A payroll entry for {employee.user.name} already exists for {payroll_date.strftime('%B %Y')}.")
                return render(request, 'hr/payroll_form.html',{'form': form, 'employee': employee, 'basic_salary': basic_salary})

            payroll = form.save(commit=False)
            payroll.employee = employee  # Set the employee field for Payroll

            # Calculate gross earnings
            gross_earnings = (
                    basic_salary +
                    form.cleaned_data.get('hra', Decimal('0.00')) +
                    form.cleaned_data.get('da', Decimal('0.00')) +
                    form.cleaned_data.get('ot', Decimal('0.00')) +
                    form.cleaned_data.get('bonuses', Decimal('0.00'))+
                    form.cleaned_data.get('medical',Decimal('0.00'))+
                    form.cleaned_data.get('insurance',Decimal('0.00'))+
                    form.cleaned_data.get('ta', Decimal('0.00'))+
                    form.cleaned_data.get('food_allowance', Decimal('0.00'))
            )

            # Calculate total deductions
            total_deductions = (
                    form.cleaned_data.get('canteen_expense', Decimal('0.00')) +
                    form.cleaned_data.get('pf', Decimal('0.00')) +
                    form.cleaned_data.get('esi', Decimal('0.00')) +
                    form.cleaned_data.get('leave_plus', Decimal('0.00'))
            )

            # Calculate net pay and set it on the payroll instance
            payroll.net_pay = gross_earnings - total_deductions

            # Save the payroll instance with the calculated net pay
            payroll.save()

            # Redirect to the desired page after successful save
            return redirect('Employee_list')
    else:
        # Provide the basic salary to the form if needed
        form = PayrollForm()

    # Render the form along with basic salary and employee information
    return render(request, 'hr/payroll_form.html', {'form': form, 'employee': employee, 'basic_salary': basic_salary})

def payroll_summary(request,id):
    menus = Menu.objects.prefetch_related('submenus').all()

    payroll = Payroll.objects.filter(employee__user_id=id).order_by('-pay_date')

    # Get filter type and query date from the request
    filter_type = request.GET.get('filter')
    query_date = request.GET.get('query')  # Expected format: YYYY-MM-DD
    is_filtered = False

    # Apply filtering if filter type is 'date' and query_date is provided
    if filter_type == 'date' and query_date:
        finished_good = payroll.filter(date=query_date)
        is_filtered = True  # Flag to indicate that a filter has been applied

    # Prepare context for rendering template
    context = {
        'data': payroll,
        'menus': menus,
        'filter_type': filter_type,
        'query_date': query_date,
        'is_filtered': is_filtered  # Pass flag to template
    }

    return render(request, 'hr/payroll_summary.html', context)