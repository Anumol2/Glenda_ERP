from django.urls import path

from vendor_app import views

urlpatterns = [
    path('vender_register_view', views.vender_register_view, name='vender_register_view'),
    path('view_vendor_list', views.view_vendor_list, name='view_vendor_list'),
    path('create_vendor_details/<int:id>', views.create_vendor_details, name='create_vendor_details'),
    path('view_vendor_profile/<int:id>', views.view_vendor_profile, name='view_vendor_profile'),
    path('export_vendor_profile_pdf/<int:id>', views.vendor_details_pdf, name='export_vendor_profile_pdf'),
    path('export_vendor_list_csv', views.vendor_list_csv, name='export_vendor_list_csv'),

    # path('vendor_search',views.vendor_search,name='vendor_search'),
    path('edit_vender/<int:id>', views.edit_vender, name='edit_vender'),
    path('delete_vender_view/<int:id>', views.delete_vender_view, name='delete_vender_view'),
    # vendor front page
    path('login', views.vendor_login, name='login'),
    path('vendor_search_and_export',views.vendor_search_and_export,name='vendor_search_and_export'),
    path('vendor_signup', views.vendor_signup, name='vendor_signup')

]
