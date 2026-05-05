from rest_framework import serializers
from v1.models import Materials,Brand,SubCategory,Category,Enquiry


class MaterialSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    def get_image(self,obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    class Meta:
        model = Materials
        fields = ['id', 'name', 'description', 'count', 'price', 
                  'product_code', 'image', 'industry','attachment_1','attachment_2','attachment_3','attachment_4']
        
class SubCategorySerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['name', 'materials']


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'sub_category']
        
class BrandSerializer(serializers.ModelSerializer):
    
    materials = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'materials']
        
        
class EnquirySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Enquiry
        fields = '__all__'