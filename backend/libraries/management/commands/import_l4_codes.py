import csv
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from libraries.models import L3Code, L4Code  # Adjust as per your actual models
from django.db import transaction
from constants.models import Unit
from libraries.models import ActivityType,ActivityTypeDetail

class Command(BaseCommand):
    help = 'Import L2 Code from a text file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the data file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Create a dictionary of L1 Codes for lookup
            l3_code_dict = {l3_code.l2_code.l1_code.l1_code + "-" + l3_code.l2_code.l2_code + "-" + l3_code.l3_code   : str(l3_code.id) for l3_code in L3Code.objects.all()}
            # print(l3_code_dict)
            unit_dict = {unit.unit: str(unit.id) for unit in Unit.objects.all()}
            # print(unit_dict)
            actiivty_type_dict = {activity.description: str(activity.id) for activity in ActivityType.objects.all()}
            activity_type_detail_dict = {activity_detail.description: str(activity_detail.id) for activity_detail in ActivityTypeDetail.objects.all()}

            # print(activity_dict )

            with open(file_path, 'r', encoding='utf-8') as file:
                print("opening file")

                reader = csv.reader(file, delimiter='!')
                k = 1
                with transaction.atomic():  # Ensure atomic transaction
                    L4Code.objects.all().delete()

                    
                    for line in reader:
                        fields = line
                        # print(k)
                        l4_code_code = fields[0].upper()
                        # print(fields[1].upper()+"-"+fields[2].upper()+"-"+fields[3].upper())
                        l3_code_id = l3_code_dict.get(fields[1].upper()+"-"+fields[2].upper()+"-"+fields[3].upper())
                        l4_code_description = fields[4].upper()
                        unit_id = unit_dict.get(fields[5].lower())
                        mtc_dgs_nkt = fields[6]
                        nak_ote = fields[7]
                        l4_ref = fields[8]
                        l4_hkds = fields[9].upper() == 'TRUE'
                        l4_calc_method = fields[10]
                        l4_bf_dg = fields[11] if fields[11] else None
                        l4_mk_ks = fields[12] if fields[12] else None
                        tax = fields[13].upper() == 'TRUE'
                        activity_type = actiivty_type_dict.get(fields[14].upper())
                        activity_type_detail = activity_type_detail_dict.get(fields[15].upper())
                        created_by_id = '12f4aa11-b6fc-482f-894d-0962ad5f4313'

                        if l3_code_id:
                            # Create the L2Code instance
                            L4Code.objects.create(
                                l3_code_id=l3_code_id,
                                l4_code=l4_code_code,
                                description=l4_code_description,
                                unit_id=unit_id,
                                mtc_dgs_nkt=mtc_dgs_nkt,
                                nak_ote=nak_ote,
                                l4_ref=l4_ref,
                                l4_hkds=l4_hkds,
                                l4_calc_method=l4_calc_method,
                                l4_bf_dg=l4_bf_dg,
                                l4_mk_ks=l4_mk_ks,
                                tax=tax,
                                activity_type_id=activity_type,
                                activity_detail_id=activity_type_detail,

                                created_by_id=created_by_id,
                                updated_by_id=created_by_id
                            )
                        else:
                            raise CommandError(f'L4-L3-L2-L1 Code {fields[1]+"-"+fields[2].upper() + "-" +fields[3].upper()+ "-" +fields[0].upper()+ "-" + str(k)} not found.')
                        k += 1


                self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            raise CommandError(f'File not found at {file_path}')
        except Exception as e:
            raise CommandError(f'Error: {str(e)+"-"+str(k)}')
