


from django.urls import path

from purchase_app import views

urlpatterns = [
    path('add_category',views.add_category,name='add_category'),
    path('create_raw_material',views.create_raw_material,name='create_raw_material'),
    path('view_rawmaterials',views.view_rawmaterials,name='view_rawmaterials'),
    path('update_rawmaterials/<int:id>', views.update_rawmaterials, name='update_rawmaterials'),
    path('delete_raw/<int:id>', views.delete_rawmaterils, name='delete_raw'),
    path('message_requests', views.message_request, name='message_requests'),
    path('message_response/<int:id>', views.message_response, name='message_response'),
    path('raw_material_purchase_search', views.raw_material_purchase_search, name='raw_material_purchase_search'),
    path('add_stocks/<int:id>', views.add_stocks, name='add_stocks'),
    path('rawmaterials_stock_history/<int:id>', views.rawmaterials_stock_history, name='rawmaterials_stock_history'),
    path('message_request_list_history', views.message_request_list_history, name='message_request_list_history'),
    path('raw_message_request_list_history_pdf', views.raw_message_request_list_history_pdf, name='raw_message_request_list_history_pdf'),
    path('raw_message_request_list_history_excel', views.raw_message_request_list_history_excel,name='raw_message_request_list_history_excel'),

]