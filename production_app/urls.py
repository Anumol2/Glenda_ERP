from django.urls import path

from production_app import views

urlpatterns = [
    path('addwater_category', views.addwater_category, name='addwater_category'),
    path('create_water', views.create_water, name='create_water'),
    path('view_finished_water_good', views.view_finished_water_good, name='view_finished_water_good'),
    path('update_finished_goods/<int:id>', views.update_finished_goods, name='update_finished_goods'),
    path('delete_goods/<int:id>', views.delete_goods, name='delete_goods'),
    path('Add_damagedgoods', views.add_damagedgoods, name='Add_damagedgoods'),
    path('damaged_goods', views.damaged_goods, name='damaged_goods'),
    path('add_damaged_good_category',views.add_damaged_good_category, name='add_damaged_good_category'),
    path('damage_delete/<int:id>',views.damage_delete, name='damage_delete'),
    path('update_damage/<int:id>',views.update_damage, name='update_damage'),
    path('request_messages',views.request_messages, name='request_messages'),
    path('request_messages_detail/<int:id>',views.request_messages_detail, name='request_messages_detail'),
    path('search',views.search,name='search'),
    path('finishedgoods_production_search',views.finishedgoods_production_search,name='finishedgoods_production_search'),
    path('update_finished_goods_stocks/<int:id>', views.update_finished_goods_stocks, name='update_finished_goods_stocks'),
    path('finishedgoods_production_stock_history/<int:id>', views.finishedgoods_production_stock_history, name='finishedgoods_production_stock_history'),
    path('finished_goods_production_history_pdf/<int:id>', views.finished_goods_production_history_pdf, name='finished_goods_production_history_pdf'),
    path('finished_goods_production_history_excel/<int:id>', views.finished_goods_production_history_excel, name='finished_goods_production_history_excel'),
    path('update_damaged_goods_stocks/<int:id>', views.update_damaged_goods_stocks, name='update_damaged_goods_stocks'),
    path('damagedgoods_production_stock_history/<int:id>',views.damagedgoods_production_stock_history,name='damagedgoods_production_stock_history'),
    path('damaged_goods_production_history_pdf/<int:id>', views.damaged_goods_production_history_pdf, name='damaged_goods_production_history_pdf'),
    path('damaged_goods_production_history_excel/<int:id>', views.damaged_goods_production_history_excel, name='damaged_goods_production_history_excel'),
    path('finishedgoods_message_request_history', views.finishedgoods_message_request_history, name='finishedgoods_message_request_history'),
    path('finished_goods_message_history_pdf', views.finished_goods_message_history_pdf, name='finished_goods_message_history_pdf'),
    path('finished_goods_message_history_excel', views.finished_goods_message_history_excel, name='finished_goods_message_history_excel')
]