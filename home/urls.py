from django.urls import path
from .views import index, import_data
from .views import import_data, ajax_view

app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    # path('base-details/<int:base_id>/', base_details, name='base_details'),
    path('import/', import_data, name='import_data'),
    path('ajax_view/', ajax_view, name='ajax_view'),
]
