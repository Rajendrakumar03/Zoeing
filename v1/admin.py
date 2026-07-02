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
from v1.models import Category, Brand, Materials, Enquiry, SubCategory, User,SoldStock,InvoiceUpload
from django.utils.html import format_html, mark_safe
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages
import pandas as pd
import io
from django.utils import timezone
from django.db.models import Sum
from django.middleware.csrf import get_token
from .utils import parse_sold_invoice_pdf



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
    
    def clean_description(self, text):
        if not text:
            return None
        
        # normalize line endings (Excel uses \r\n sometimes)
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # split into lines
        lines = text.split('\n')
        
        while lines and lines[-1].strip() == '':
            lines.pop()
        
        # remove empty lines at start and end
        # lines = [line for line in lines]
        
        # join paragraphs with double newline for spacing
        paragraphs = [line for line in lines if line.strip() != '']
        # current = []
        
        # for line in lines:
        #     if line.strip() == '':
        #         if current:
        #             paragraphs.append('\n'.join(current))
        #             current = []
        #     else:
        #         current.append(line)
        
        # if current:
        #     paragraphs.append('\n'.join(current))
        
        # join paragraphs with double newline = blank line between them
        return '\n\n'.join(paragraphs)

    def process_file(self, df):
        
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
                
                raw_description  = str(row['description']) if pd.notna(row.get('description')) else None
                description = self.clean_description(raw_description)

                name         = str(row['material_name']).strip() if pd.notna(row.get('material_name')) else None
                # description  = str(row['description']) if pd.notna(row.get('description')) else None
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
        
        csrf_token = get_token(request)
        print("CSRF Token:",csrf_token)
        
        # upload_url = request.path.rstrip('/') + '/upload/'
        # upload_url = '/admin/v1/category/upload/'
        upload_url=request.path.rstrip('/') + '/upload/'
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
    list_display = ['id','email','company_name','user_role']
    list_per_page = 20
    search_fields = ['email']
    

    def has_view_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj = None):
        return False


# ── Category ──────────────────────────────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(FileUploadMixin, admin.ModelAdmin):  # ← removed change_list_template
    list_display = ['id','name']
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
    list_display = ['id','name', 'category']
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
    list_display = ['id','name']
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
    list_display = ['id','name', 'count', 'price','zo_material_code', 'product_code', 'brand', 'category', 'sub_category','attachment_1','attachment_2','attachment_3','attachment_4']
    list_per_page = 20
    search_fields = ['name','id']

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# ── Enquery ───────────────────────────────────────────────────────────────────
@admin.register(Enquiry)
class EnqueryAdmin(admin.ModelAdmin):
    list_display = ['id','email', 'phone_number', 'created_at']
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
    
    
@admin.register(SoldStock)
class SoldStockAdmin(admin.ModelAdmin):
    list_display = ['material', 'quantity_sold', 'unit_price', 'total_price']
    # list_filter  = ['sold_date', 'customer_name']
    search_fields = ['material__name', 'invoice_number', 'customer_name']
    readonly_fields = ['material', 'quantity_sold', 'unit_price', 'total_price', 'created_at']

    def has_add_permission(self, request):
        return False  # only via PDF upload

    def has_change_permission(self, request, obj=None):
        return False  # readonly — can't edit sold records

    def has_delete_permission(self, request, obj=None):
        return False  # can't delete sold records
    
    

@admin.register(InvoiceUpload)
class InvoiceUploadAdmin(admin.ModelAdmin):
    change_list_template = 'admin/v1/invoiceupload/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        return [
            path('upload-sold/', self.admin_site.admin_view(self.upload_sold_invoice), name='invoice-upload-sold'),
            path('upload-stock/', self.admin_site.admin_view(self.upload_stock), name='invoice-upload-stock'),
        ] + urls

    def upload_sold_invoice(self, request):
        import pdb;pdb.set_trace()
        if request.method == 'POST':
            pdf_file = request.FILES.get('invoice_pdf')
            if not pdf_file:
                messages.error(request, 'Please select a PDF invoice.')
                return redirect('../')

            try:
                parsed = parse_sold_invoice_pdf(pdf_file)

                if not parsed['items']:
                    messages.error(request, 'No line items found in PDF.')
                    return redirect('../')

                success, failed, not_found = [], [], []
                pdf_file.seek(0)

                for item in parsed['items']:
                    material_code = item['material_code']
                    quantity     = item['quantity']

                    try:
                        material = Materials.objects.get(zo_material_code=material_code)

                        if material.count < quantity:
                            failed.append(f"'{material_code}' — only {material.count} in stock, invoice says {quantity}")
                            continue

                        SoldStock.objects.create(
                            material       = material,
                            invoice = parsed['invoice_number'],
                            customer_name  = parsed['customer_name'],
                            quantity_sold  = quantity,
                            unit_price     = item['unit_price'],
                            total_price    = item['total_price'],
                            invoice_file   = pdf_file,
                            sold_date      = parsed['sold_date'],
                        )

                        material.count -= quantity
                        material.save()
                        success.append(f"{material_code} (qty: {quantity})")

                    except Materials.DoesNotExist:
                        not_found.append(material_code)

                if success:
                    messages.success(request, f"✅ Invoice {parsed['invoice_number']} processed! Updated: {', '.join(success)}")
                if failed:
                    messages.error(request, f"❌ Stock insufficient: {' | '.join(failed)}")
                if not_found:
                    messages.warning(request, f"⚠️ Product codes not found: {', '.join(not_found)}")

            except Exception as e:
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error reading PDF: {str(e)}')

        return redirect('../')

    def upload_stock(self, request):
        import pdb;pdb.set_trace()
        """Admin manually increases stock count"""
        if request.method == 'POST':
            product_code = request.POST.get('product_code', '').strip()
            quantity     = request.POST.get('quantity', 0)
            note         = request.POST.get('note', '')

            if not product_code or not quantity:
                messages.error(request, 'Product code and quantity are required.')
                return redirect('../')

            try:
                material = Materials.objects.get(product_code=product_code)
                material.count += int(quantity)
                material.save()
                messages.success(
                    request,
                    f"✅ Stock updated! {product_code} — new count: {material.count}"
                )
            except Materials.DoesNotExist:
                messages.error(request, f"Product code '{product_code}' not found.")

        return redirect('../')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['sold_invoice_html'] = mark_safe(self.get_sold_invoice_html(request))
        extra_context['add_stock_html']    = mark_safe(self.get_add_stock_html(request))
        return super().changelist_view(request, extra_context=extra_context)

    def get_sold_invoice_html(self, request):
        csrf_token = get_token(request)
        upload_url = request.path.rstrip('/') + '/upload-sold/'
        return f"""
        <div style="margin-top:20px;">
            <h2 style="font-size:16px; font-weight:600; color:#c0392b; border-bottom:2px solid #c0392b; padding-bottom:8px; margin-bottom:16px;">
                📤 Upload Sales Invoice PDF — Reduce Stock
            </h2>
            <div style="background:#fff; border:1px solid #ddd; border-radius:6px; padding:24px; max-width:700px;">
                <form method="post" enctype="multipart/form-data" action="{upload_url}">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                    <div style="margin-bottom:16px;">
                        <label style="display:block; font-weight:600; margin-bottom:8px;">
                            Invoice PDF <span style="color:red">*</span>
                        </label>
                        <input type="file" name="invoice_pdf" accept=".pdf" required
                            style="display:block; width:100%; padding:10px; border:2px dashed #e74c3c; border-radius:4px; cursor:pointer; box-sizing:border-box;" />
                        <small style="color:#666; margin-top:6px; display:block;">
                            System auto-reads: invoice number, date, customer, product codes, quantities, prices
                        </small>
                    </div>
                    <div style="background:#fff5f5; border:1px solid #f5c6cb; border-radius:4px; padding:12px 16px; margin-bottom:16px; font-size:13px;">
                        ⚠️ Product codes in PDF must match exactly with product codes in Materials table.
                    </div>
                    <button type="submit" style="background:#c0392b; color:white; border:none; padding:10px 24px; border-radius:4px; font-size:14px; cursor:pointer; font-weight:600;">
                        Upload & Process Invoice
                    </button>
                </form>
            </div>
        </div>
        """

    def get_add_stock_html(self, request):
        csrf_token = get_token(request)
        upload_url = request.path.rstrip('/') + '/upload-stock/'
        return f"""
        <div style="margin-top:40px;">
            <h2 style="font-size:16px; font-weight:600; color:#27ae60; border-bottom:2px solid #27ae60; padding-bottom:8px; margin-bottom:16px;">
                📥 Add New Stock — Increase Count
            </h2>
            <div style="background:#fff; border:1px solid #ddd; border-radius:6px; padding:24px; max-width:700px;">
                <form method="post" action="{upload_url}">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                    <div style="margin-bottom:16px;">
                        <label style="display:block; font-weight:600; margin-bottom:8px;">
                            Product Code <span style="color:red">*</span>
                        </label>
                        <input type="text" name="product_code" required placeholder="e.g. APL-001"
                            style="display:block; width:100%; padding:10px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" />
                    </div>
                    <div style="margin-bottom:16px;">
                        <label style="display:block; font-weight:600; margin-bottom:8px;">
                            Quantity to Add <span style="color:red">*</span>
                        </label>
                        <input type="number" name="quantity" required min="1" placeholder="e.g. 50"
                            style="display:block; width:100%; padding:10px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" />
                    </div>
                    <div style="margin-bottom:16px;">
                        <label style="display:block; font-weight:600; margin-bottom:8px;">Note (optional)</label>
                        <input type="text" name="note" placeholder="e.g. New stock from supplier"
                            style="display:block; width:100%; padding:10px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" />
                    </div>
                    <button type="submit" style="background:#27ae60; color:white; border:none; padding:10px 24px; border-radius:4px; font-size:14px; cursor:pointer; font-weight:600;">
                        Add Stock
                    </button>
                </form>
            </div>
        </div>
        """

    # hide default list actions — this page is only for uploads
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# class InvoiceUploadAdmin(admin.ModelAdmin):
#     list_display  = ['invoice_number', 'customer_name', 'invoice_date', 'get_user', 'sold_items_count', 'created_at']
#     list_per_page = 20
#     search_fields = ['invoice_number', 'customer_name', 'user__email']
#     list_filter   = ['invoice_date']
#     readonly_fields = ['invoice_number', 'customer_name', 'invoice_date', 'user', 'invoice', 'created_at', 'updated_at', 'sold_items_count', 'view_sold_items']

#     fields = ['invoice_number', 'customer_name', 'invoice_date', 'user', 'invoice', 'sold_items_count', 'view_sold_items', 'created_at']

#     def get_urls(self):
#         urls = super().get_urls()
#         return [
#             path('upload-sold/', self.admin_site.admin_view(self.upload_sold_invoice), name='invoice-upload-sold'),
#             path('upload-stock/', self.admin_site.admin_view(self.upload_stock), name='invoice-upload-stock'),
#         ] + urls

#     # ── list display helpers ───────────────────────────────────
#     def get_user(self, obj):
#         return obj.user.email if obj.user else '❌ No user matched'
#     get_user.short_description = 'Customer Email'

#     def sold_items_count(self, obj):
#         return obj.sold_stocks.count()
#     sold_items_count.short_description = 'Items Sold'

#     def view_sold_items(self, obj):
#         if not obj.pk:
#             return '-'
#         rows = ''.join([
#             f"""
#             <tr>
#                 <td style="padding:8px; border:1px solid #ddd;">{stock.material.name}</td>
#                 <td style="padding:8px; border:1px solid #ddd;">{stock.material.product_code}</td>
#                 <td style="padding:8px; border:1px solid #ddd;">{stock.quantity_sold}</td>
#                 <td style="padding:8px; border:1px solid #ddd;">{stock.unit_price}</td>
#                 <td style="padding:8px; border:1px solid #ddd;">{stock.total_price}</td>
#             </tr>
#             """
#             for stock in obj.sold_stocks.all()
#         ])
#         if not rows:
#             return '-'
#         return mark_safe(f"""
#             <table style="border-collapse:collapse; width:100%;">
#                 <thead>
#                     <tr style="background:#417690; color:white;">
#                         <th style="padding:8px; border:1px solid #ddd;">Material</th>
#                         <th style="padding:8px; border:1px solid #ddd;">Product Code</th>
#                         <th style="padding:8px; border:1px solid #ddd;">Qty Sold</th>
#                         <th style="padding:8px; border:1px solid #ddd;">Unit Price</th>
#                         <th style="padding:8px; border:1px solid #ddd;">Total Price</th>
#                     </tr>
#                 </thead>
#                 <tbody>{rows}</tbody>
#             </table>
#         """)
#     view_sold_items.short_description = 'Sold Items'

#     # ── upload sold invoice ────────────────────────────────────
#     def upload_sold_invoice(self, request):
#         if request.method == 'POST':
#             pdf_file = request.FILES.get('invoice_pdf')
#             if not pdf_file:
#                 messages.error(request, 'Please select a PDF invoice.')
#                 return redirect('../')

#             if not pdf_file.name.lower().endswith('.pdf'):
#                 messages.error(request, 'Only PDF files are allowed.')
#                 return redirect('../')

#             try:
#                 from .utils import parse_sold_invoice_pdf
#                 from django.contrib.auth import get_user_model
#                 User = get_user_model()

#                 parsed = parse_sold_invoice_pdf(pdf_file)
#                 print("Parsed invoice:", parsed)

#                 if not parsed['items']:
#                     messages.error(request, 'No line items found in PDF. Check product codes match.')
#                     return redirect('../')

#                 if not parsed['invoice_number']:
#                     messages.error(request, 'Could not extract invoice number from PDF.')
#                     return redirect('../')

#                 pdf_file.seek(0)

#                 # ── match user from invoice email ──────────────
#                 user           = None
#                 customer_email = parsed.get('customer_email')

#                 if customer_email:
#                     try:
#                         user = User.objects.get(email=customer_email)
#                         print(f"Matched user: {user.email}")
#                     except User.DoesNotExist:
#                         print(f"No user found for email: {customer_email}")

#                 # ── create invoice record ──────────────────────
#                 invoice = InvoiceUpload.objects.create(
#                     user           = user,
#                     invoice_number = parsed['invoice_number'],
#                     customer_name  = parsed['customer_name'],
#                     invoice        = pdf_file,
#                     invoice_date   = parsed['sold_date'],
#                 )

#                 success, failed, not_found = [], [], []

#                 for item in parsed['items']:
#                     product_code = item['product_code']
#                     quantity     = item['quantity']

#                     try:
#                         material = Materials.objects.get(product_code=product_code)

#                         # ── check stock ────────────────────────
#                         if material.count < quantity:
#                             failed.append(
#                                 f"'{product_code}' — only {material.count} in stock, "
#                                 f"invoice says {quantity}"
#                             )
#                             continue

#                         # ── create sold record ─────────────────
#                         SoldStock.objects.create(
#                             material      = material,
#                             invoice       = invoice,
#                             quantity_sold = quantity,
#                             unit_price    = item['unit_price'],
#                             total_price   = item['total_price'],
#                             sold_date     = parsed['sold_date'],
#                         )

#                         # ── reduce stock ───────────────────────
#                         material.count -= quantity
#                         material.save()

#                         success.append(f"{product_code} (qty: {quantity})")

#                     except Materials.DoesNotExist:
#                         not_found.append(product_code)

#                 # ── build result message ───────────────────────
#                 if success:
#                     messages.success(
#                         request,
#                         f"✅ Invoice {parsed['invoice_number']} processed! "
#                         f"Customer: {parsed['customer_name']} | "
#                         f"User: {user.email if user else '⚠️ Not matched'} | "
#                         f"Updated: {', '.join(success)}"
#                     )
#                 if not user:
#                     messages.warning(
#                         request,
#                         f"⚠️ No registered user found for '{customer_email}'. "
#                         f"Invoice saved without user link."
#                     )
#                 if failed:
#                     messages.error(request, f"❌ Stock insufficient: {' | '.join(failed)}")
#                 if not_found:
#                     messages.warning(request, f"⚠️ Product codes not found in DB: {', '.join(not_found)}")

#             except Exception as e:
#                 import traceback
#                 traceback.print_exc()
#                 messages.error(request, f'Error reading PDF: {str(e)}')

#         return redirect('../')

#     # ── add stock manually ─────────────────────────────────────
#     def upload_stock(self, request):
#         if request.method == 'POST':
#             product_code = request.POST.get('product_code', '').strip()
#             quantity     = request.POST.get('quantity', 0)
#             note         = request.POST.get('note', '').strip()

#             if not product_code or not quantity:
#                 messages.error(request, 'Product code and quantity are required.')
#                 return redirect('../')

#             try:
#                 material  = Materials.objects.get(product_code=product_code)
#                 old_count = material.count
#                 material.count += int(quantity)
#                 material.save()
#                 messages.success(
#                     request,
#                     f"✅ Stock updated! {material.name} ({product_code}) — "
#                     f"previous: {old_count} | added: {quantity} | new count: {material.count}"
#                     + (f" | note: {note}" if note else "")
#                 )
#             except Materials.DoesNotExist:
#                 messages.error(request, f"❌ Product code '{product_code}' not found in Materials.")

#         return redirect('../')

#     # ── inject forms below list ────────────────────────────────
#     def changelist_view(self, request, extra_context=None):
#         extra_context = extra_context or {}
#         extra_context['sold_invoice_html'] = mark_safe(self.get_sold_invoice_html(request))
#         extra_context['add_stock_html']    = mark_safe(self.get_add_stock_html(request))
#         return super().changelist_view(request, extra_context=extra_context)

#     def get_sold_invoice_html(self, request):
#         csrf_token = get_token(request)
#         upload_url = request.path.rstrip('/') + '/upload-sold/'
#         return f"""
#         <div style="margin-top:30px;">
#             <h2 style="font-size:16px; font-weight:600; color:#c0392b; border-bottom:2px solid #c0392b; padding-bottom:8px; margin-bottom:16px;">
#                 📤 Upload Sales Invoice PDF — Reduce Stock
#             </h2>
#             <div style="background:#fff; border:1px solid #ddd; border-radius:6px; padding:24px; max-width:700px;">
#                 <form method="post" enctype="multipart/form-data" action="{upload_url}">
#                     <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
#                     <div style="margin-bottom:16px;">
#                         <label style="display:block; font-weight:600; margin-bottom:8px;">
#                             Invoice PDF <span style="color:red">*</span>
#                         </label>
#                         <input type="file" name="invoice_pdf" accept=".pdf" required
#                             style="display:block; width:100%; padding:10px; border:2px dashed #e74c3c; border-radius:4px; cursor:pointer; box-sizing:border-box;" />
#                         <small style="color:#666; margin-top:6px; display:block;">
#                             System auto-reads: invoice number, date, customer email, product codes, quantities, prices
#                         </small>
#                     </div>
#                     <div style="background:#fff5f5; border:1px solid #f5c6cb; border-radius:4px; padding:12px 16px; margin-bottom:16px; font-size:13px;">
#                         <strong>System will auto-extract:</strong><br>
#                         ✅ Invoice number &nbsp;
#                         ✅ Invoice date &nbsp;
#                         ✅ Customer name &nbsp;
#                         ✅ Customer email (matched to user) &nbsp;
#                         ✅ Product codes &nbsp;
#                         ✅ Quantities &nbsp;
#                         ✅ Prices<br><br>
#                         <strong>⚠️ Note:</strong> Product codes in PDF must match exactly with product codes in Materials table.
#                     </div>
#                     <button type="submit"
#                         style="background:#c0392b; color:white; border:none; padding:10px 24px; border-radius:4px; font-size:14px; cursor:pointer; font-weight:600;">
#                         Upload & Process Invoice
#                     </button>
#                 </form>
#             </div>
#         </div>
#         """

#     def get_add_stock_html(self, request):
#         csrf_token = get_token(request)
#         upload_url = request.path.rstrip('/') + '/upload-stock/'
#         return f"""
#         <div style="margin-top:40px; margin-bottom:40px;">
#             <h2 style="font-size:16px; font-weight:600; color:#27ae60; border-bottom:2px solid #27ae60; padding-bottom:8px; margin-bottom:16px;">
#                 📥 Add New Stock — Increase Count
#             </h2>
#             <div style="background:#fff; border:1px solid #ddd; border-radius:6px; padding:24px; max-width:700px;">
#                 <form method="post" action="{upload_url}">
#                     <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
#                     <div style="margin-bottom:16px;">
#                         <label style="display:block; font-weight:600; margin-bottom:8px;">
#                             Product Code <span style="color:red">*</span>
#                         </label>
#                         <input type="text" name="product_code" required placeholder="e.g. APL-001"
#                             style="display:block; width:100%; padding:10px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" />
#                     </div>
#                     <div style="margin-bottom:16px;">
#                         <label style="display:block; font-weight:600; margin-bottom:8px;">
#                             Quantity to Add <span style="color:red">*</span>
#                         </label>
#                         <input type="number" name="quantity" required min="1" placeholder="e.g. 50"
#                             style="display:block; width:100%; padding:10px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" />
#                     </div>
#                     <div style="margin-bottom:16px;">
#                         <label style="display:block; font-weight:600; margin-bottom:8px;">
#                             Note (optional)
#                         </label>
#                         <input type="text" name="note" placeholder="e.g. New stock from supplier ABC"
#                             style="display:block; width:100%; padding:10px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box;" />
#                     </div>
#                     <button type="submit"
#                         style="background:#27ae60; color:white; border:none; padding:10px 24px; border-radius:4px; font-size:14px; cursor:pointer; font-weight:600;">
#                         Add Stock
#                     </button>
#                 </form>
#             </div>
#         </div>
#         """

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False
