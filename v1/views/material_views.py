from django.shortcuts import render
from v1.models import Materials,SubCategory,Brand,Category
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from v1.serializers.material_serializer import BrandSerializer,CategorySerializer,EnquirySerializer
from v1.utils import send_email
from v1.constants import INTERNAL_MAIL_SUBJECT,INTERNAL_BODY,SENDER,PASSWORD,INTERNAL_RECIPIENTS,USER_MAIL_SUBJECT,USER_BODY
from rest_framework import status



class EnquiryView(viewsets.ViewSet):
        
    def post(self,request):
        
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
    
    
    def get_all_materials(self,request):
                
        all_materials = Materials.objects.select_related('category', 'brand', 'sub_category').all()
        
        response = []
        
        for material in all_materials:
            
            attachments = []

            for i in range(1, 5):
                file_field = getattr(material, f'attachment_{i}', None)

                if file_field:
                    file_url = request.build_absolute_uri(file_field.url)
                    file_name = file_field.name.split('/')[-1]

                    attachments.append({
                        'name' :file_name,
                        'file':file_url
                    })
            
            data = {
                'id': material.id,
                'name':material.name,
                'description' :material.description,
                'count': material.count,
                'price': material.price,
                'zo_material_code':material.zo_material_code,
                'product_code': material.product_code,
                'image': request.build_absolute_uri(material.image.url) if material.image else None,
                'industry': material.industry,
                'category': material.category.name if material.category else None,
                'brand': material.brand.name if material.brand else None,
                'sub_category': material.sub_category.name if material.sub_category else None,
                'attachment' :  attachments  
                                      
            }
            response.append(data)
            
        if response:
            return Response({"message":"Successfully Fetched","materials": response},status=status.HTTP_200_OK)
        
        return Response({"message":"No materials found"},status=status.HTTP_404_NOT_FOUND)
        
    
    
    
        