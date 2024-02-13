from django.urls import path

from web_app.views import (main_view, registration_view, login_view,
                           logout_view, add_product_view, manage_product_view)

urlpatterns = [
    path('', main_view),
    path('registration', registration_view),
    path('login', login_view),
    path('logout', logout_view),
    path('product/new', add_product_view),
    path('product/<int:_id>/edit', manage_product_view)
]
