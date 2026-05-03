
from django.urls import path
from v1.views.material_views import EnquiryView,MaterialView
from django.conf import settings
from django.conf.urls.static import static


material_urlpatterns = [
    path('materials',MaterialView.as_view({'get':'get'}),name='materials'),
    path('brand_materials',MaterialView.as_view({'get':'brand_list'}),name='brand_materials'),
    path('enquiry',EnquiryView.as_view({'post':'post'}),name='enquiry'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)