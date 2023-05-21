CONFIDENCE_THRESHOLD = 0.9

# Information for first section of the FAFSA (Student Information)
class StudentInformation:
    lastName = ""
    firstName = ""
    middleInitial = ""
    address = ""
    city = ""
    state = ""
    zipCode = ""
    social_security_number = ""
    date_of_birth = ""
    telephone_number = ""
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

    def parseSSN(self, ssn):
        if ssn.confidence > CONFIDENCE_THRESHOLD:
          self.social_security_number = ssn.value

    def parseName(self, name):
        if name.confidence > CONFIDENCE_THRESHOLD:
          name = (name.value).split(" ")
          self.firstName = name[0]
          self.lastName = name[1]
    
    def parseAddress(self, address):
        if address.confidence > CONFIDENCE_THRESHOLD:
          self.address = address.value
    
    def parseZipCode(self, zipCode):
        if zipCode.confidence > CONFIDENCE_THRESHOLD:
          self.zipCode = zipCode.value

    def to_string(self):
      return self.firstName + " " + self.lastName


    
