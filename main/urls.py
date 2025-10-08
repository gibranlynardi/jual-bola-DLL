from django.urls import path
from main.views import (
    show_main, show_json, show_json_by_id, show_xml, show_xml_by_id,
    create_product, show_product, register, login_user, logout_user,
    edit_product, delete_product, add_product_ajax, delete_product_ajax, register_ajax, login_ajax, edit_product_ajax
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<uuid:id>/', show_product, name='show_product'),
    path('products/<uuid:id>/edit/', edit_product, name='edit_product'),
    path('products/<uuid:id>/delete/', delete_product, name='delete_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:product_id>/', show_json_by_id, name='show_json_by_id'),
    path('create-product-ajax/', add_product_ajax, name='add_product_ajax'),
    path('delete-product-ajax/<uuid:id>/', delete_product_ajax, name='delete_product_ajax'),
    path('edit-product-ajax/<uuid:id>/', edit_product_ajax, name='edit_product_ajax'), 
    path('register-ajax/', register_ajax, name='register_ajax'),
    path('login-ajax/', login_ajax, name='login_ajax'),
]