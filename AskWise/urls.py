"""
URL configuration for AskWise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from AskWise import settings
from app import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    # path('ask', views.ask, name='ask'),
    # path('hot', views.hot, name='hot'),
    # path('question/<int:question_id>', views.question, name='question'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('settings', views.settings, name='settings'),
    path('signup', views.signup, name='signup'),
    path('cart', views.cart, name='cart'),
    path('orders', views.orders, name='orders'),
    path('add_to_cart_index/<int:store_item_id>/', views.add_to_cart_index, name='add_to_cart_index'),
    path('remove_from_cart_index/<int:store_item_id>', views.remove_from_cart_index, name='remove_from_cart_index'),
    path('add_to_cart/<int:order_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:order_item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('buy', views.buy, name='buy'),

    # path('tag/<str:tag_name>', views.tag, name='tag'),
    # path('vote/', views.vote_question, name='vote_question'),

    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
