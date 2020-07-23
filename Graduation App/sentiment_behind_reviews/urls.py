from django.urls import path, include
from . import views
# from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('products/', views.products, name="products"),
    path('signup/', views.signup_form, name="signup_form"),
    path('login/', views.login_form, name="login_form"),
    path('logout/', views.logout_form, name="logout_form"),
    path('contact_us/', views.contact_form, name="contact_form"),
    path('products/reviews/<int:id>/', views.product_reviews, name='product_reviews'),
    # path('products/' + str(id), Dashviews.public_profile_view, name='public_profile_view'),
    # path("logout/", LogoutView.as_view(), name="logout"),

]