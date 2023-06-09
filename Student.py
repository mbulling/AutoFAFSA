import Person

# Student Information
class Student(Person.Person):
    super().__init__()
    driver_license_number = ""
    driver_license_state = ""
    email_address = ""
    citizenship_status = ""
    alien_registration_number = ""
    marital_status = ""
    marital_date = ""
    legal_resident_state = ""
    legal_resident_before_2018 = True
    legal_resident_date = ""
    parent_1_education_level = ""
    parent_2_education_level = ""
    did_complete_high_school = True
    high_school_name = ""
    high_school_city = ""
    high_school_state = ""
    bachelor_degree_before_2023 = False
    grade_in_college = ""
    degree_type = ""
    born_before_jan_1_2000 = False
    married = False
    working_on_master_or_doctorate = False
    on_active_duty_in_armed_forces = False
    is_veteran = False
    support_other_children = False
    support_other_dependents = False
    in_foster_care = False
    emancipated_minor = False
    in_legal_guardianship = False
    homeless_or_unaccompanied_youth = False
    household_size = 0
    number_in_college = 0
    received_medicaid = False
    received_snap = False
    received_free_lunch = False
    received_tanf = False
    received_wic = False
    dislocated_worker = False

