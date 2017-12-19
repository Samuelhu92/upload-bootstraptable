from django.conf.urls import url,include
from fund import views
import fund

urlpatterns = [
    url(r'^fund/(\d+)$',views.fundinfo,name='fund_info'),
    url(r'^tree/$',views.fundtree,name='fund_tree'),
    url(r'^parent/$',views.fundparent,name='fund_parent'),
    url(r'^child/(\d+)$',views.fundchild,name='fund_child'),
    url(r'^show/$',views.show,name='fund_show'),
    url(r'^upload/$',views.upload,name='trade_upload'),
    url(r'^process/$',views.FileFieldView,name='upload_process')

]