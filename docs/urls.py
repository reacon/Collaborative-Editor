from django.urls import path
from . import views

urlpatterns = [
    path('', views.documents_list, name='documents_list'),
    path('add',views.add_document,name='add_document'),
    path('<slug:slug>', views.document_view, name='document_view'),
    path('<slug:slug>/delete', views.delete_document, name='delete_document'),

]