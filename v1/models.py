from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager





class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

        
        
class User(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = "user"
        db_table = "user"
    
    def __str__(self):
        return self.email

        

class Category(TimeStampMixin):
    name = models.CharField(max_length=255,blank=True,null=True)
    # material = models.ForeignKey(Materials,on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "category"
        db_table = "category"
        
    
    def __str__(self):
        return self.name
    
class SubCategory(TimeStampMixin):
    name = models.CharField(max_length=255,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_category')
    
    class Meta:
        verbose_name = 'sub_category'
        db_table = 'sub_category'
        
        
    
    def __str__(self):
        return self.name
    
    
class Brand(TimeStampMixin):
    name = models.CharField(max_length=255,blank=True,null=True)
    # material = models.ForeignKey(Materials,on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "brand"
        db_table = "brand"
        
    
    def __str__(self):
        return self.name
    

class Materials(TimeStampMixin):
    name = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    count = models.IntegerField(blank=True,null=True)
    price = models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=2)
    product_code = models.CharField(max_length=255,blank=True,null=True,unique=True)
    image = models.ImageField(upload_to='materials/',blank=True,null=True)
    industry = models.CharField(max_length=255,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='materials')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True,related_name='materials')
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='materials')
    class Meta:
        verbose_name = "materials"
        db_table = "materials"
        
    
    def __str__(self):
        return self.name
        
    
class Enquiry(TimeStampMixin):
    user_name = models.CharField(max_length=150,blank=False,null=False)
    email= models.EmailField(blank=False,null=False)
    materials = models.JSONField(blank=False,null=False)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    company_name = models.CharField(max_length=150,blank=True,null=True)
    class Meta:
        verbose_name = "enquiry"
        db_table = "enquiry"
        
    
    def __str__(self):
        return self.email
    