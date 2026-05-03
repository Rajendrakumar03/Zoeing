from django.shortcuts import render
from v1.models import Materials,SubCategory,Brand,Category
from rest_framework import viewsets
from rest_framework.response import Response
from v1.serializers.material_serializer import BrandSerializer,CategorySerializer,EnquirySerializer
from v1.utils import send_email
from v1.constants import INTERNAL_MAIL_SUBJECT,INTERNAL_BODY,SENDER,PASSWORD,INTERNAL_RECIPIENTS,USER_MAIL_SUBJECT,USER_BODY


class EnquiryView(viewsets.ViewSet):
        
    def post(self,request):
        # import pdb;pdb.set_trace()
        data = request.data
        print(data['email'])
        mail = data['email']
        
        serializer = EnquirySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            material_list = data['materials']
            formatted_list = '\n'.join([
                f" - {item['name']} : {item['quantity']}"
                for item in material_list
            ])
            send_email(subject=INTERNAL_MAIL_SUBJECT,body=INTERNAL_BODY.format(mail=data['email'],materials=formatted_list),sender=SENDER,recipients=INTERNAL_RECIPIENTS,password=PASSWORD)
            send_email(subject=USER_MAIL_SUBJECT,body=USER_BODY.format(materials=formatted_list),sender=SENDER,recipients=[mail],password=PASSWORD)
            
            return Response("Saved Successfully")
        
        return Response("Not Saved")
        
class MaterialView(viewsets.ViewSet):  
    def get(self,request):
                
        products = Category.objects.prefetch_related('sub_category__materials').all()
        serializer = CategorySerializer(products,many=True,context={'request':request})
    
        if serializer:
            return Response(serializer.data)
        return Response("No data Available")
    
    
    def brand_list(self,request):
        
        brands = Brand.objects.prefetch_related('materials').all()
        
        serializer = BrandSerializer(brands,many=True,context={'request': request})
        
        if serializer:
            return Response (serializer.data)
        
        return Response("No data Aaailable")
    
    
    def all_materials(self,request):
        pass
    
    
    
        