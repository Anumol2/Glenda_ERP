from django.urls import path
from logistics_app import views

urlpatterns = [

        path('Add_driver',views.Add_driver,name='Add_driver'),
        path('Add_vehicle',views.Add_vehicle,name='Add_vehicle'),
        path('create_route',views.create_route,name='create_route'),
        path('Add_routeplan',views.Add_routeplan,name='Add_routeplan'),
        path('view_driver',views.view_driver,name='view_driver'),
        path('update_driver/<int:id>',views.update_driver,name='update_driver'),
        path('delete_driver/<int:id>',views.delete_driver,name='delete_driver'),
        path('view_vehicle',views.view_vehicle,name='view_vehicle'),
        path('update_vehicle/<int:id>',views.update_vehicle,name='update_vehicle'),
        path('delete_vehicle/<int:id>',views.delete_vehicle,name='delete_vehicle'),
        path('view_route',views.view_route,name='view_route'),
        path('update_route/<int:id>',views.update_route,name='update_route'),
        path('delete_route/<int:id>',views.delete_route,name='delete_route'),
        path('view_routeplan',views.view_routeplan,name='view_routeplan'),
        path('update_routeplan/<int:id>',views.update_routeplan,name='update_routeplan'),
        path('delete_routeplan/<int:id>',views.delete_routeplan,name='delete_routeplan'),
        path('get-route-details/', views.get_route_details, name='get_route_details'),
        path('driver_search_and_export',views.driver_search_and_export,name='driver_search_and_export'),
        path('route_search_and_export',views.route_search_and_export,name='route_search_and_export'),
        path('vehicle_search_and_export',views.vehicle_search_and_export,name='vehicle_search_and_export'),
        path('route_plan_search_and_export',views.route_plan_search_and_export,name='route_plan_search_and_export'),
        path('Maintenanace',views.VehicleMaintenanace,name='Maintenanace'),
        path('view_vmaintenance',views.view_vmaintenance,name='view_vmaintenance'),
        path('update_vmaintenance/<int:id>',views.update_vmaintenance,name='update_vmaintenance'),
        path('delete_vmaintenance/<int:id>',views.delete_vmaintenance,name='delete_vmaintenance'),
        path('vmaintenance_search',views.vmaintenance_search,name='vmaintenance_search'),
        path('vehicle_maintenance_search_and_export',views.vehicle_maintenance_search_and_export,name='vehicle_maintenance_search_and_export'),

]