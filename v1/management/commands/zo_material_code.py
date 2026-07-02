from django.core.management.base import BaseCommand
from v1.models import Materials
import configs as cfg

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--zo_material_code',
            default=False,
            choices=["true","false"],
            help="Material process"
            
        )
        
        
    def zo_materials(self):
        
        materials = Materials.objects.all()
        
        for mat in materials:
            # import pdb;pdb.set_trace()
            
            id = mat.id
            
            material_code = cfg.MATERIAL_CODE + '_' + str(id)
            
            table_update = Materials.objects.filter(id=id).update(zo_material_code=material_code)
            
            
    def handle(self, *args, **options):
        if options['zo_material_code'] == 'true':
            self.zo_materials()
            
            