from enum import Enum


class GeneralEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def choices_v2v(cls):
        return tuple((i.value, i.value) for i in cls)

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class UserGroupsEnum(GeneralEnum):
    Admin = "Admin"
    User = "User"


class UserGroupsEnum(GeneralEnum):
    JV_Admin = "JV Admin"
    Company_User = "Company User"
    Integration_User = "Integration User"
    Read_Only_User = "Read-Only User"
    Security_User = "Security User"


class StatusEnum(GeneralEnum):
    YES = "Evet"
    NO = "Hayır"


class FileCheckMessageEnum(GeneralEnum):
    file_format_message = "Dosya xls veya xlsx formatında olmalıdır!"
    incorrect_excel_column_message = "Excel sütun başlıkları doğru değil!"
    excel_column_order = "Excel sütun sıralaması yanlış. Excel sütun listesi aşağıdaki gibi olmalıdır!!"


class AlreadyMessageEnum(GeneralEnum):
    already_tckn_message = "TC kimlik numarası zaten kayıtlı!"
    not_already_tckn_message = "TC kimlik numarası kayıtlı değil!"
    already_passport_message = "Pasaport numarası zaten kayıtlı!"
    not_already_passport_message = "Pasaport numarası kayıtlı değil!"
    already_email_message = "Email adresi zaten kayıtlı!"


class NotAlreadyMessageEnum(GeneralEnum):
    not_already_sgk_info_message = "sgk işe giriş kodu,"
    not_already_department_message = "departman,"
    not_already_nationality_message = "uyruk,"
    not_already_grade_message = "derece,"
    not_already_title_message = "unvan,"
    not_already_position_message = "pozisyon,"
    not_already_card_type_message = "kart tipi,"
    not_already_duty_message = "görev,"
    not_already_formen_message = "Formen TC kimlik numarası bulunamadı!"
    not_already_team_leader_message = "Takım Lideri TC kimlik numarası bulunamadı!"


class DateMessageEnum(GeneralEnum):
    birth_date_message = "doğum tarihi,"
    start_date_of_work_message = "işe başlama tarihi"
    start_date_of_work_check_message = "İşe başlama tarihi bugünün tarihinden iler de olamaz!"


class NewRecordMessageEnum(GeneralEnum):
    new_record_message = "Eklemek ister misiniz?"


class IsIntegerMessageEnum(GeneralEnum):
    is_not_integer_message = "Sütun alanının değerleri sayı olmalıdır!"


class LengthMessageEnum(GeneralEnum):
    tckn_length_message = "TC kimlik numrası 11 hane olmalıdır!"
    phone_length_message = "Telefon numarası 10 hane olmalıdır!"


class CheckValueMessageEnum(GeneralEnum):
    tckn_passport_empty_message = "Aşağıdaki satırlar da TC kimlik ve pasaport numarası boş,birlikte boş olamaz!"
    tckn_passport_not_empty_message = "TC kimlik ve pasaport numarası birlikte dolu olamaz!"
    confirm_reject_empty_message = "Aşağıdaki satırlar da onayla ve reddet boş,birlikte boş olamaz!"
    confirm_reject_value_message = "Aşağıdaki satırlar da onayla ve reddet 1 veya 0 olmalıdır!"
    confirm_reject_not_empty_message = "Aşağıdaki satırlar da onayla ve reddet dolu,birlikte dolu olamaz!"
    grade_empty_message = "Aşağıdaki satırlar da derece kodu ve derece birlikte dolu veya boş olmalıdır!"
    action_date_not_valid_message = "Ret/Onay tarihi formatı yanlıştır!"
    start_date_not_valid_message = "Başlangıç tarihi formatı yanlıştır!"
    start_date_lesshan_action_date_message = "Başlangıç tarihi Ret/Onay tarihinden küçük olamaz!"
    check_birth_place_type_message = "Doğum yeri metin olmalıdır!"
    country_code = "+9"


class PhaseMessageEnum(GeneralEnum):
    phase_confirm_message = "Güvenlik Soruşturması Onaylandı"
    phase_reject_message = "Güvenlik Soruşturması Reddedildi"
    phase_start_message = "Güvenlik Soruşturması Başlatıldı"


class FileImportExportStatusEnum(GeneralEnum):
    loading = "loading"
    completed = "completed"
    failed = "failed"


class FileTypeEnum(GeneralEnum):
    work_design = "work_design"
    ppr_design = "ppr_design"
    daily_report = "daily_report"
    material_management = "material_management"
    thematic_plan = "thematic_plan"
    work_permit = "work_permit"
    site_obstacles = "site_obstacles"
    work_type = "work_type" 
    unit = "unit"
    cmdd = 'current_month_daily_distribution'
    smeta_analysis = 'smeta_analysis'
    cmdd_static = 'current_month_daily_distribution_static'
    daily_report_management_static = 'daily_report_management_static'
    manpowercomparison_static = 'manpowercomparison_static'
    manpoweronsite_static = 'manpoweronsite_static'
    sd_report_static = 'sd_report_static'
    employee_data = 'employee_data'
    employee_tracking = 'employee_tracking'
    pm_smu_crew_region_area = 'pm_smu_crew_region_area'
    generate_employee_data = 'generate_employee_data'
    
class FileProcessTypeEnum(GeneralEnum):
    work_design_import = "work_design_import"
    work_design_export = "work_design_export"
    ppr_design_import = "ppr_design_import"
    ppr_design_export = "ppr_design_export"
    daily_report_import = "daily_report_import"
    material_management_import = "material_management_import"
    material_management_export = "material_management_export"
    thematic_plan_import = "thematic_plan_import"
    thematic_plan_export = "thematic_plan_export"
    smeta_analysis_import = "smeta_analysis_import" 
    site_obstacles_export = "site_obstacles_export"
    work_type_import = "work_type_import"  
    unit_import = "unit_import"
    cmdd_import = "current_month_daily_distribution_import"
    cmdd_static_import = "current_month_daily_distribution_static_import"
    cmdd_static_export = "current_month_daily_distribution_static_export"
    daily_report_management_static_import = "daily_report_management_static_import"
    manpowercomparison_static_import = "manpowercomparison_static_import"
    manpoweronsite_static_import = "manpoweronsite_static_import"
    sd_report_static_import = "sd_report_static_import"   
    employee_data_import = "employee_data_import"
    