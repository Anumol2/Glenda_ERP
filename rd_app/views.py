from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from inventory_app.models import RawMaterialsStock
from purchase_app.models import RawMaterials
from rd_app.forms import RD_approvalForm
from Glenda_App.models import Menu
from rd_app.models import RD_stock,RD_Unapproved_Stock

from register_app.models import CustomUser, MenuPermissions
from django.core.paginator import Paginator

# Create your views here.

def raw_material_stock_approve(request):
    # Fetch menus and counts
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)


    raw_materials_stock = RawMaterialsStock.objects.all().order_by('-date')

    # Pagination logic
    paginator = Paginator(raw_materials_stock, 5)  # Show 5 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'rd/raw_material_stock_approval_list.html', {'allocated_menus': allocated_menus,'raw_materials_stock':page_obj})





def raw_material_stock_approve_review(request, id):
    # Fetch menus and counts
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)

    request_data = get_object_or_404(RawMaterialsStock, id=id)

    # Handle POST request for approval action only
    if request.method == 'POST':
        print(request.POST)  # Debugging: Print the POST data

        # Approval process
        if 'approve' in request.POST:
            try:
                # Get approved stock and reason from form data
                approved_stock = int(request.POST.get('approved_stock', 0))
                reason = request.POST.get('response', '').strip()  # Optional reason if not all stock approved
            except ValueError:
                error_message = "Invalid number for approved stock."
                return render(request, 'rd/raw_material_stock_approval_view.html', {
                    'data': request_data,
                    'allocated_menus': allocated_menus,
                    'error_message': error_message
                })

            # Check if approved stock exceeds the available stock
            if approved_stock > request_data.stock:
                error_message = "Approved stock cannot exceed the arrived stock quantity."
                return render(request, 'rd/raw_material_stock_approval_view.html', {
                    'data': request_data,
                    'allocated_menus': allocated_menus,
                    'error_message': error_message
                })

            # Require a reason if not all stock is approved
            if approved_stock < request_data.stock and not reason:
                error_message = "Please provide a reason if not all stocks are approved."
                return render(request, 'rd/raw_material_stock_approval_view.html', {
                    'data': request_data,
                    'allocated_menus': allocated_menus,
                    'error_message': error_message
                })

            # Update stock status, response, and total stock
            request_data.status = 'Reviewed'
            request_data.response = reason  # Store reason if provided
            raw_material = request_data.raw_materials
            raw_material.total_stock += approved_stock  # Add only approved stock to total stock
            raw_material.save()
            request_data.save()

            # Calculate unapproved stock
            unapproved_stock = request_data.stock - approved_stock

            # Record approved and unapproved stocks in RD_stock
            RD_stock.objects.create(
                raw_materials=request_data,
                approved_stock=approved_stock,
                unapproved_stock=unapproved_stock
            )

            # Update or create the RD_Unapproved_Stock entry for the category
            category = raw_material.category
            unapproved_stock_entry, created = RD_Unapproved_Stock.objects.get_or_create(
                raw_materials__category=category,
                raw_materials=raw_material,
                defaults={'total_unapproved_stock': unapproved_stock}
            )

            if not created:
                # If an entry exists, update its total_unapproved_stock
                unapproved_stock_entry.total_unapproved_stock += unapproved_stock
                unapproved_stock_entry.save()

            # Redirect after successful approval
            return redirect('raw_material_stock_approve')

    # Render the page initially or if an error occurs
    return render(request, 'rd/raw_material_stock_approval_view.html', {
        'data': request_data,
        'allocated_menus': allocated_menus
    })

def stock_approval_history(request,id):
    # Fetch menus and counts
    use = request.user  # Get the current user

    # Get user's permissions
    user_permissions = MenuPermissions.objects.filter(user=use).select_related('menu', 'sub_menu')

    # Create a dictionary to hold menus and their allocated submenus
    allocated_menus = {}
    for perm in user_permissions:
        if perm.menu not in allocated_menus:
            allocated_menus[perm.menu] = []
        allocated_menus[perm.menu].append(perm.sub_menu)


    rd_stock = RD_stock.objects.get(id = id)

    context = {
        'allocated_menus': allocated_menus,
        'data':rd_stock
    }

    return render(request,'rd/history_raw_material_stock_approval_view.html',context)

