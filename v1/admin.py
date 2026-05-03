# from django.contrib import admin
# from v1.models import Category,Brand,Materials,Enquery,SubProduct,User
# from django.utils.html import format_html,mark_safe
# from django.shortcuts import render, redirect
# from django.urls import path
# from django.contrib import messages
# from django.utils.html import format_html
# import pandas as pd
# import io


# # class FileUploadAdmin(admin.ModelAdmin):
# #     """Base admin with file upload capability"""
# #     change_list_template = "admin/file_upload.html"

# #     def get_urls(self):
# #         urls = super().get_urls()
# #         custom_urls = [
# #             path('upload/', self.admin_site.admin_view(self.upload_file), name='upload-file'),
# #         ]
# #         return custom_urls + urls

# #     def upload_file(self, request):
# #         if request.method == 'POST':
# #             file = request.FILES.get('upload_file')

# #             if not file:
# #                 messages.error(request, 'Please select a file.')
# #                 return redirect('..')

# #             # validate extension
# #             ext = file.name.split('.')[-1].lower()
# #             if ext not in ['xlsx', 'csv']:
# #                 messages.error(request, 'Only .xlsx and .csv files are allowed.')
# #                 return redirect('..')

# #             try:
# #                 # read file
# #                 if ext == 'xlsx':
# #                     df = pd.read_excel(io.BytesIO(file.read()))
# #                 else:
# #                     df = pd.read_csv(io.BytesIO(file.read()))

# #                 # normalize column names
# #                 df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# #                 # validate required columns
# #                 required_columns = {'category', 'sub_product', 'material_name'}
# #                 missing = required_columns - set(df.columns)
# #                 if missing:
# #                     messages.error(request, f'Missing required columns: {", ".join(missing)}')
# #                     return redirect('..')

# #                 # drop rows where mandatory fields are empty
# #                 df = df.dropna(subset=['category', 'sub_product', 'material_name'])

# #                 if df.empty:
# #                     messages.error(request, 'No valid rows found in file.')
# #                     return redirect('..')

# #                 created_counts = self.process_file(df)
# #                 messages.success(
# #                     request,
# #                     f"Import successful — "
# #                     f"{created_counts['categories']} categories, "
# #                     f"{created_counts['sub_products']} sub-products, "
# #                     f"{created_counts['materials']} materials created."
# #                 )

# #             except Exception as e:
# #                 messages.error(request, f'Error processing file: {str(e)}')

# #             return redirect('..')

# #         return render(request, 'admin/file_upload.html', {
# #             'title': 'Upload File',
# #             'opts': self.model._meta,
# #         })

# #     def process_file(self, df):
# #         counts = {'categories': 0, 'sub_products': 0, 'materials': 0}

# #         for _, row in df.iterrows():
# #             # ── Category ──────────────────────────────────────
# #             category, cat_created = Category.objects.get_or_create(
# #                 name=str(row['category']).strip()
# #             )
# #             if cat_created:
# #                 counts['categories'] += 1

# #             # ── SubProduct ────────────────────────────────────
# #             sub_product, sub_created = SubProduct.objects.get_or_create(
# #                 name=str(row['sub_product']).strip(),
# #                 product=category,
# #             )
# #             if sub_created:
# #                 counts['sub_products'] += 1

# #             # ── Brand (optional) ──────────────────────────────
# #             brand = None
# #             brand_name = row.get('brand', None)
# #             if pd.notna(brand_name) and str(brand_name).strip():
# #                 brand, _ = Brand.objects.get_or_create(
# #                     name=str(brand_name).strip()
# #                 )

# #             # ── Material ──────────────────────────────────────
# #             Materials.objects.create(
# #                 name=str(row['material_name']).strip(),
# #                 description=row.get('description', None) if pd.notna(row.get('description')) else None,
# #                 count=int(row['count']) if pd.notna(row.get('count')) else 0,
# #                 price=float(row['price']) if pd.notna(row.get('price')) else None,
# #                 product_code=str(row['product_code']).strip() if pd.notna(row.get('product_code')) else None,
# #                 industry=str(row['industry']).strip() if pd.notna(row.get('industry')) else None,
# #                 product=category,
# #                 sub_product=sub_product,
# #                 brand=brand,
# #             )
# #             counts['materials'] += 1

# #         return counts





# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['email']
#     list_per_page = 20
#     search_fields = ['email']
    
    
#     def has_view_permission(self, request, obj = None):
#         return True

# @admin.register(Category)
# class ProductAdmin(admin.ModelAdmin):
    
#     change_list_template = "admin/file_upload.html" 
#     list_display = ['name']
#     list_per_page = 20
#     search_fields = ['name']
    
#     def has_add_permission(self, request):
#         return True
    
#     def has_view_permission(self, request,obj=None):
#         return True
    
#     def has_delete_permission(self, request,obj=None):
#         return True
    

# @admin.register(SubProduct)
# class SubProductAdmin(admin.ModelAdmin):
    
#     list_display = ['name','product']
#     list_per_page = 20
#     search_fields = ['name']
    
#     def has_add_permission(self, request):
#         return True
    
#     def has_view_permission(self, request,obj=None):
#         return True
    
#     def has_delete_permission(self, request,obj=None):
#         return True
    
    

# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
    
    
#     list_display = ['name']
#     list_per_page = 20
#     search_fields = ['name']
    
#     def has_add_permission(self, request):
#         return True
    
#     def has_view_permission(self, request,obj=None):
#         return True
    
#     def has_delete_permission(self, request,obj=None):
#         return True
    

# @admin.register(Materials)
# class MaterialsAdmin(admin.ModelAdmin):
    
    
#     list_display = ['name','count','price','product_code','brand','product','sub_product']
#     list_per_page = 20
#     search_fields = ['name']
    
#     def has_add_permission(self, request):
#         return True
    
#     def has_view_permission(self, request,obj=None):
#         return True
    
#     def has_delete_permission(self, request,obj=None):
#         return True


# @admin.register(Enquery)
# class EnqueryAdmin(admin.ModelAdmin):
    
    
#     list_display = ['email','phone_number','created_at']
#     list_per_page = 20
#     search_fields = ['email']
#     readonly_fields = ['formatted_materials']
    
#     fields = ['email', 'phone_number', 'formatted_materials']
    
#     def formatted_materials(self, obj):
#         if not obj.materials:
#             return '-'
        
#         rows = ''.join([
#             f"""
#             <tr>
#                 <td style="padding: 8px; border: 1px solid #ddd;">{item.get('name', '-')}</td>
#                 <td style="padding: 8px; border: 1px solid #ddd;">{item.get('count', '-')}</td>
#             </tr>
#             """
#             for item in obj.materials
#         ])
        
#         html = f"""
#             <table style="border-collapse: collapse; width: 50%;">
#                 <thead>
#                     <tr style="background-color: #417690; color: white;">
#                         <th style="padding: 8px; border: 1px solid #ddd;">Material Name</th>
#                         <th style="padding: 8px; border: 1px solid #ddd;">Count</th>
#                     </tr>
#                 </thead>
#                 <tbody>
#                     {rows}
#                 </tbody>
#             </table>
#         """
#         return mark_safe(html) 


#     formatted_materials.short_description = 'Materials'  # field label
    
    
#     def has_add_permission(self, request):
#         return False
    
#     def has_view_permission(self, request,obj=None):
#         return True
    
#     def has_delete_permission(self, request,obj=None):
#         return False
    
#     def has_change_permission(self, request, obj = None):
#         return False


from django.contrib import admin
from v1.models import Category, Brand, Materials, Enquiry, SubCategory, User
from django.utils.html import format_html, mark_safe
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages
import pandas as pd
import io


class FileUploadMixin:

    def get_urls(self):
        urls = super().get_urls()
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        custom_urls = [
            path(
                'upload/',
                self.admin_site.admin_view(self.upload_file),
                name=f'{app_label}_{model_name}_upload',  # ← unique per model
            ),
        ]
        return custom_urls + urls

    # def upload_file(self, request):
    #     if request.method == 'POST':
    #         file = request.FILES.get('upload_file')

    #         if not file:
    #             messages.error(request, 'Please select a file.')
    #             return redirect('../')

    #         ext = file.name.split('.')[-1].lower()
    #         if ext not in ['xlsx', 'csv']:
    #             messages.error(request, 'Only .xlsx and .csv files are allowed.')
    #             return redirect('../')

    #         try:
    #             if ext == 'xlsx':
    #                 df = pd.read_excel(io.BytesIO(file.read()))
    #             else:
    #                 df = pd.read_csv(io.BytesIO(file.read()))

    #             df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    #             required_columns = {'category', 'sub_product', 'material_name'}
    #             missing = required_columns - set(df.columns)
    #             if missing:
    #                 messages.error(request, f'Missing required columns: {", ".join(missing)}')
    #                 return redirect('../')

    #             df = df.dropna(subset=['category', 'sub_product', 'material_name'])

    #             if df.empty:
    #                 messages.error(request, 'No valid rows found in file.')
    #                 return redirect('../')

    #             counts = self.process_file(df)
    #             messages.success(
    #                 request,
    #                 f"Import successful — "
    #                 f"{counts['categories']} categories, "
    #                 f"{counts['sub_products']} sub-products, "
    #                 f"{counts['materials']} materials created."
    #             )

    #         except Exception as e:
    #             messages.error(request, f'Error processing file: {str(e)}')

    #     return redirect('../')
    def upload_file(self, request):
        if request.method == 'POST':
            file = request.FILES.get('upload_file')

            if not file:
                messages.error(request, 'Please select a file.')
                return redirect('../')

            ext = file.name.split('.')[-1].lower()

            if ext not in ['xlsx', 'csv']:
                messages.error(request, 'Only .xlsx and .csv files are allowed.')
                return redirect('../')

            try:
                if ext == 'xlsx':
                    df = pd.read_excel(io.BytesIO(file.read()))
                else:
                    df = pd.read_csv(io.BytesIO(file.read()))


                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

                required_columns = {'category', 'sub_category', 'material_name','product_code'}
                missing = required_columns - set(df.columns)

                if missing:
                    messages.error(request, f'Missing required columns: {", ".join(missing)}')
                    return redirect('../')

                df = df.dropna(subset=['category', 'sub_category', 'material_name'])

                if df.empty:
                    messages.error(request, 'No valid rows found in file.')
                    return redirect('../')
                
                missing_product_code_rows = []
                for idx, row in df.iterrows():
                    product_code = row.get('product_code', None)
                    if pd.isna(product_code) or str(product_code).strip() == '':
                        row_number = idx + 2  # +2 because idx is 0-based and row 1 is header
                        missing_product_code_rows.append(row_number)

                if missing_product_code_rows:
                    row_list = ', '.join(str(r) for r in missing_product_code_rows)
                    messages.error(
                        request,
                        f'Product code is missing in row(s): {row_list}. Please fix and re-upload.'
                    )
                    return redirect('../')
                
                duplicate_in_file = df[df.duplicated(subset=['product_code'], keep=False)]
                if not duplicate_in_file.empty:
                    duplicates = []
                    for idx, row in duplicate_in_file.iterrows():
                        duplicates.append(f"'{str(row['product_code']).strip()}' in row {idx + 2}")
                    messages.error(
                        request,
                        f'Duplicate product codes found in file: {", ".join(duplicates)}. Please fix and re-upload.'
                    )
                    return redirect('../')
                
                # existing_codes = []
                # for idx, row in df.iterrows():
                #     product_code = str(row['product_code']).strip()
                #     if Materials.objects.filter(product_code=product_code).exists():
                #         existing_codes.append(f"'{product_code}' in row {idx + 2}")
                        

                # if existing_codes:
                #     messages.error(
                #         request,
                #         f'Product code already exists in database: {", ".join(existing_codes)}. Please fix and re-upload.'
                #     )
                #     return redirect('../')

                counts = self.process_file(df)
                
                total_rows = len(df)
                skipped_rows = total_rows - counts['materials']

                messages.success(
                    request,
                    f"File saved successfully!"
                    f"{counts['category']} categories, "
                    f"{counts['sub_category']} sub-category, "
                    f"{counts['materials']} materials created."
                    f"{skipped_rows} rows skipped (already exists in database)"
                )

            except Exception as e:
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error processing file: {str(e)}')

        else:
            print("=== NOT A POST REQUEST, method:", request.method)

        return redirect('../')

    def process_file(self, df):
        # import pdb;pdb.set_trace()
        counts = {'category': 0, 'sub_category': 0, 'materials': 0,'skipped_rows':0}

        for _, row in df.iterrows():
            # print("Processing row:", row.to_dict())  # ← see each row

            try:
                category, cat_created = Category.objects.get_or_create(
                    name=str(row['category']).strip()
                )
                if cat_created:
                    counts['category'] +=1
                    
                sub_category, sub_created = SubCategory.objects.get_or_create(
                    name=str(row['sub_category']).strip(),
                    category=category,
                )
                
                if sub_created:
                    counts['sub_category']+=1

                brand = None
                brand_name = row.get('brand', None)
                if pd.notna(brand_name) and str(brand_name).strip():
                    brand, _ = Brand.objects.get_or_create(name=str(brand_name).strip())
                    
                raw_code = row.get('product_code')
                
                if isinstance(raw_code, float) and raw_code.is_integer():
                    product_code = str(int(raw_code)).strip()
                else:
                    product_code = str(raw_code).strip()
                    
                if Materials.objects.filter(product_code=product_code).exists():
                    counts['skipped'] += 1
                    continue

                name         = str(row['material_name']).strip() if pd.notna(row.get('material_name')) else None
                description  = str(row['description']).strip() if pd.notna(row.get('description')) else None
                product_code = str(row['product_code']).strip() if pd.notna(row.get('product_code')) else None
                count        = int(row['count']) if pd.notna(row.get('count')) else 0
                price        = float(row['price']) if pd.notna(row.get('price')) else None
                industry     = str(row['industry']).strip() if pd.notna(row.get('industry')) else None
                

                
                Materials.objects.create(
                    name=name,
                    description=description,
                    product_code=product_code,
                    count=count,
                    price=price,
                    industry=industry,
                    category=category,
                    sub_category=sub_category,
                    brand=brand,
                )
                
                counts['materials'] += 1

            except Exception as e:
                print(f"ERROR on row: {e}")  # ← see exact error
                import traceback
                traceback.print_exc()

        return counts

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['upload_form_html'] = mark_safe(self.get_upload_form_html(request))
        return super().changelist_view(request, extra_context=extra_context)

    def get_upload_form_html(self,request):
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        print("CSRF Token:",csrf_token)
        
        # upload_url = request.path.rstrip('/') + '/upload/'
        upload_url = '/admin/v1/category/upload/'
        print("Upload URL:", upload_url)       # ← confirm in terminal
        print("CSRF Token:", csrf_token[:20]) 
        
        return f"""
        <br>
        <div style="margin-top:30px;">
            <h2 style="font-size:16px; font-weight:600; color:#333; border-bottom:2px solid #417690; padding-bottom:8px; margin-bottom:16px;">
                File Upload — Import Categories, Sub-Category &amp; Materials
            </h2>
            <div style="background:#fff; border:1px solid #ddd; border-radius:6px; padding:24px; max-width:700px;">
                <form method="post" enctype="multipart/form-data" action="{upload_url}">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                    <div style="margin-bottom:16px;">
                        <label style="display:block; font-weight:600; margin-bottom:8px;">
                            Select File <span style="color:red">*</span>
                        </label>
                        <input type="file" name="upload_file" accept=".xlsx,.csv" required
                            style="display:block; width:100%; padding:10px; border:2px dashed #ccc; border-radius:4px; cursor:pointer; box-sizing:border-box;" />
                        <small style="color:#666; margin-top:6px; display:block;">Accepted: .xlsx, .csv</small>
                    </div>
                    <div style="background:#f0f4ff; border:1px solid #c5d0f5; border-radius:4px; padding:12px 16px; margin-bottom:16px; font-size:13px;">
                        <strong>Required columns:</strong> category, sub_category, material_name<br>
                        <strong>Optional columns:</strong> description, count, price, product_code, industry, brand
                    </div>
                    <button type="submit"
                        style="background:#417690; color:white; border:none; padding:10px 24px; border-radius:4px; font-size:14px; cursor:pointer; font-weight:600;">
                        Upload &amp; Import
                    </button>
                </form>
            </div>
            <div style="margin-top:20px; max-width:700px;">
                <p style="font-size:13px; font-weight:600; margin-bottom:8px;">Sample Format:</p>
                <table style="border-collapse:collapse; font-size:12px; width:100%;">
                    <tr style="background:#f5f5f5; font-weight:600;">
                        <td style="border:1px solid #ddd; padding:6px 10px;">category</td>
                        <td style="border:1px solid #ddd; padding:6px 10px;">description</td>                        
                        <td style="border:1px solid #ddd; padding:6px 10px;">sub_category</td>
                        <td style="border:1px solid #ddd; padding:6px 10px;">material_name</td>
                        <td style="border:1px solid #ddd; padding:6px 10px;">count</td>
                    </tr>
                    <tr>
                        <td style="border:1px solid #ddd; padding:6px 10px;">Electronics</td>
                        <td style="border:1px solid #ddd; padding:6px 10px;">Description for the Product</td>                        
                        <td style="border:1px solid #ddd; padding:6px 10px;">Phones</td>
                        <td style="border:1px solid #ddd; padding:6px 10px;">iPhone 15</td>
                        <td style="border:1px solid #ddd; padding:6px 10px;">10</td>
                    </tr>
                </table>
            </div>
        </div>
        """  # ← properly closed


# ── User ──────────────────────────────────────────────────────────────────────
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_per_page = 20
    search_fields = ['email']

    def has_view_permission(self, request, obj=None):
        return True


# ── Category ──────────────────────────────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(FileUploadMixin, admin.ModelAdmin):  # ← removed change_list_template
    list_display = ['name']
    list_per_page = 20
    search_fields = ['name']

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# ── SubProduct ────────────────────────────────────────────────────────────────
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_per_page = 20
    search_fields = ['name']

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# ── Brand ─────────────────────────────────────────────────────────────────────
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 20
    search_fields = ['name']

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# ── Materials ─────────────────────────────────────────────────────────────────
@admin.register(Materials)
class MaterialsAdmin(FileUploadMixin, admin.ModelAdmin):
    list_display = ['name', 'count', 'price', 'product_code', 'brand', 'category', 'sub_category']
    list_per_page = 20
    search_fields = ['name']

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# ── Enquery ───────────────────────────────────────────────────────────────────
@admin.register(Enquiry)
class EnqueryAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number', 'created_at']
    list_per_page = 20
    search_fields = ['email']
    readonly_fields = ['formatted_materials']
    fields = ['email', 'phone_number', 'formatted_materials']

    def formatted_materials(self, obj):
        if not obj.materials:
            return '-'

        rows = ''.join([
            f"""
            <tr>
                <td style="padding:8px; border:1px solid #ddd;">{item.get('name', '-')}</td>
                <td style="padding:8px; border:1px solid #ddd;">{item.get('count', '-')}</td>
            </tr>
            """
            for item in obj.materials
        ])

        html = f"""
            <table style="border-collapse:collapse; width:50%;">
                <thead>
                    <tr style="background-color:#417690; color:white;">
                        <th style="padding:8px; border:1px solid #ddd;">Material Name</th>
                        <th style="padding:8px; border:1px solid #ddd;">Count</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        """
        return mark_safe(html)

    formatted_materials.short_description = 'Materials'

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
