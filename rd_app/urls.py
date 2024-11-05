from django.urls import path

from rd_app import views

urlpatterns = [
    path('raw_material_stock_approve', views.raw_material_stock_approve, name='raw_material_stock_approve'),
    path('raw_material_stock_approve_review/<int:id>', views.raw_material_stock_approve_review, name='raw_material_stock_approve_review'),
    path('stock_approval_history/<int:id>', views.stock_approval_history,name='stock_approval_history'),

]
