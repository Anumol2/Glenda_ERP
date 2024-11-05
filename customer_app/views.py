from django.shortcuts import render, redirect

# Create your views here.
import csv
from lib2to3.pgen2.driver import Driver
from django.http import HttpResponse, JsonResponse

from customer_app.forms import RegistrationForm
from customer_app.models import customer_registration


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_customeruser')  # Redirect to a success page or another appropriate page
    else:
        form = RegistrationForm()

    return render(request, 'customer/registration.html', {'form': form, 'menus': menus})


def view_customeruser(request):
    view = customer_registration.objects.all()
    return render(request, 'customer/viewcustomer.html', {'menus': menus, 'view': view})


def customer_search(request):
    customer_list = customer_registration.objects.all()  # Default to all vendors

    if request.method == 'GET':
        search_query = request.GET.get('search_query', '').strip()

        if search_query:
            # Build filters
            filters = Q()

        if search_query.isdigit():
            filters &= Q(phone_number__icontains=search_query)  # Filter by user name

        else:
            filters &= Q(name__icontains=search_query)  # Filter by vendor phone number

        # Apply filters if any were provided
    if filters:
        customer_list = customer_registration.objects.filter(filters)

    context = {
        'view': customer_list,  # This will be used in the template
    }

    return render(request, 'customer/viewcustomer.html', context)


def view_customer_profile(request, id):

    view = customer_registration.objects.filter(user_id=id)

    return render(request, 'customer/search_profile.html', {'view': view, 'menus': menus})


def customer_list_csv(request):
    view = customer_registration.objects.all()

    context = {'view': view, }
    response = HttpResponse(content_type='application/csv')
    response['Content-Disposition'] = f'attachment; filename="customer_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone Number'])

    customers = customer_registration.objects.all()

    for customer in customers:
        writer.writerow([customer.name, customer.phone_number])

    return response


def customer_exportsearch(request):
    # Prefetch menus for rendering in the template
    export_format = request.GET.get('export', '')
    search_query = request.GET.get('search_query', '').strip()  # Search by name or phone number

    # Initialize the filters
    filters = Q()

    # Initialize the export list based on the search query
    if search_query:
        # Check if the search query is a digit (indicating a phone number)
        if search_query.isdigit():
            filters &= Q(phone_number__icontains=search_query)
        else:
            filters &= Q(name__icontains=search_query)

    # Fetch the filtered list based on the constructed filters
    searchexport_list = customer_registration.objects.filter(filters)

    # If 'export' parameter is found, handle CSV export
    if export_format == 'excel':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Customer_searchexport_List.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['Name', 'Address', 'State', 'District', 'Pincode', 'Email', 'GST Number', 'PAN Number', 'Phone Number'])

        for customer in searchexport_list:
            writer.writerow([
                customer.name,
                customer.address,
                customer.state,
                customer.district,
                customer.pincode,
                customer.email,
                customer.GST_number,
                customer.PAN_number,
                customer.phone_number
            ])

        return response  # Return CSV response for download

    # Prepare the context to render in the template
    context = {
        'view': searchexport_list,  # Filtered customer list for display
           # Menus for navigation
        'search_query': search_query,  # Keep search query in the context for display in form
    }

    # Render the combined view template
    return render(request, 'customer/viewcustomer.html', context)