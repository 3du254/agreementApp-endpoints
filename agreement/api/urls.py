from django.urls import path
from agreement.api import views
app_name='agreement'
urlpatterns = [
    path('pdf/<int:id>', views.generateAgreementPDF, name='create_pdf'),
    #path('create', views.api_create_agreement_detail, name='agreement_buyer_detail'),
    path('list', views.AgreementListView.as_view(), name='list_agreement'),
    path('list/<int:pk>', views.AgreementRetrieveAPIView.as_view(), name='list_one_agreement'),
    path('create', views.AgreementCreateApiView.as_view(), name='create_agreement'),
    path('update/<int:pk>', views.AgreementUpdateAPIView.as_view(), name='update_agreement'),
    path('delete/<int:pk>', views.AgreementDestroyAPIView.as_view(), name='update_agreement')
]