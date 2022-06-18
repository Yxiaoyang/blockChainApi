from django.urls import path
from xdai import views
from django.views.generic import TemplateView

urlpatterns = [
    path('transfer/', views.transfer),
    path('get_block/', views.get_block),
    path('get_balance/', views.get_balance),
    path('get_nonce/', views.get_nonce),
    path('get_erc20_blance/', views.get_erc20_blance),
    path('erc20_transfer/', views.erc20_transfer),
    path('get_latest_blkNum/', views.get_latest_blkNum),
    path('get_transcation/', views.get_transcation),
    path('replace_transfer/', views.replace_transfer),
    path('create_addr/', views.create_addr),
    path('get_gas/', views.get_gas),
]