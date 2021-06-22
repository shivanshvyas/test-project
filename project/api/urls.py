from django.conf.urls import url 
from api import views 
 
urlpatterns = [ 
    url('product/', views.ProductList.as_view()),
    url('product/<int:pk>/', views.ProductDetail.as_view()),

]