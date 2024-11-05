

from django.urls import path,include

from Glenda_App import views
from Glenda_App.views import raw_materials_data

urlpatterns = [
    path('', views.customer_index, name='customer_index'),
    path('admin_home',views.index,name='admin_home'),
    path('create_menu', views.create_menu, name='create_menu'),
    path('create_submenu', views.create_submenu, name='create_submenu'),
    path('calendar', views.calendar, name='calendar'),
    # path('pie-chart/', views.pie_chart_view, name='pie_chart'),
    path('api/raw-materials/', raw_materials_data, name='raw_materials_data'),  # API endpoint
    # path('stock-data/', stock_data, name='stock_data'),
    # path('chat',views.user_list, name='user_list'),
    # path('chat/users/<int:user_id>/',views.chat_with_user, name='chat_with_user'),
    # path('chat/send_message/', views.send_message, name='send_message'),  # API endpoint for sending message

]
