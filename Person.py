CONFIDENCE_THRESHOLD = 0.9

class Person:
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