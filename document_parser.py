import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from secret import endpoint, key
import Student
import Parent

# formatting function
def format_address_value(address_value):
    return f"\n......House/building number: {address_value.house_number}\n......Road: {address_value.road}\n......City: {address_value.city}\n......State: {address_value.state}\n......Postal code: {address_value.postal_code}"


def analyze_tax_us_w2(person, _employer):
    #formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/w2.png"
    formUrl = "https://f.hubspotusercontent00.net/hubfs/342754/Sample_Form_W2_2020.pdf"
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Specify W2 form type
    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-tax.us.w2", formUrl
    )
    w2s = poller.result()

    for idx, w2 in enumerate(w2s.documents):
        # Form variant
        form_variant = w2.fields.get("W2FormVariant")
        
        # Tax year
        tax_year = w2.fields.get("TaxYear")
        
        w2_copy = w2.fields.get("W2Copy")
        employee = w2.fields.get("Employee")
        if employee:
            # Name
            employee_name = employee.value.get("Name")
            person.parseName(employee_name)

            # SSN
            employee_ssn = employee.value.get("SocialSecurityNumber")
            person.parseSSN(employee_ssn)

            # Address
            employee_address = employee.value.get("Address")
            person.parseAddress(employee_address)

            # Zipcode
            employee_zipcode = employee.value.get("ZipCode")
            person.parseZipCode(employee_zipcode)

        employer = w2.fields.get("Employer")
        if employer:
            # Employer name
            employer_name = employer.value.get("Name")
            _employer.parseName(employer_name)

            # Employer ID
            employer_id = employer.value.get("IdNumber")

            # Employer address
            employer_address = employer.value.get("Address")
            _employer.parseAddress(employer_address)
            
            # Employer zipcode
            employer_zipcode = employer.value.get("ZipCode")
            _employer.parseZipCode(employer_zipcode)
        
        # Wages, tips, and other compensation
        wages_tips = w2.fields.get("WagesTipsAndOtherCompensation")
        person.adjusted_gross_income = wages_tips.value

        # Federal income tax withheld
        fed_income_tax_withheld = w2.fields.get("FederalIncomeTaxWithheld")
        
        # Social security wages
        social_security_wages = w2.fields.get("SocialSecurityWages")
        
        # Social security tax withheld
        social_security_tax_withheld = w2.fields.get("SocialSecurityTaxWithheld")
        
        # Medicare wages and tips
        medicare_wages_tips = w2.fields.get("MedicareWagesAndTips")
        
        # Medicare tax withheld
        medicare_tax_withheld = w2.fields.get("MedicareTaxWithheld")
        
        # Social security tips
        social_security_tips = w2.fields.get("SocialSecurityTips")
        
        # Allocated tips
        allocated_tips = w2.fields.get("AllocatedTips")
        
        # Verification code
        verification_code = w2.fields.get("VerificationCode")
        
        # Dependent care benefits
        dependent_care_benefits = w2.fields.get("DependentCareBenefits")
        
        # Non-qualified plans
        non_qualified_plans = w2.fields.get("NonQualifiedPlans")
        
        # Additional information
        additional_info = w2.fields.get("AdditionalInfo")
        if additional_info:
            for item in additional_info.value:
                
                # Letter code
                letter_code = item.value.get("LetterCode")
                
                # Amount
                amount = item.value.get("Amount")

        # Statutory employee       
        is_statutory_employee = w2.fields.get("IsStatutoryEmployee")
        
        # Retirement plan
        is_retirement_plan = w2.fields.get("IsRetirementPlan")
        
        # Third-party sick pay
        third_party_sick_pay = w2.fields.get("IsThirdPartySickPay")
        
        # Other information
        other_info = w2.fields.get("Other")
        
        # State tax information
        state_tax_info = w2.fields.get("StateTaxInfos")
        if state_tax_info:
            for tax in state_tax_info.value:
                # State
                state = tax.value.get("State")
                
                # Employer state ID number
                employer_state_id_number = tax.value.get("EmployerStateIdNumber")
                
                # State wages, tips, etc
                state_wages_tips = tax.value.get("StateWagesTipsEtc")
                
                # State income tax
                state_income_tax = tax.value.get("StateIncomeTax")
        
        # Local tax information
        local_tax_info = w2.fields.get("LocalTaxInfos")
        if local_tax_info:
            for tax in local_tax_info.value:
                # Local wages, tips, etc
                local_wages_tips = tax.value.get("LocalWagesTipsEtc")
                
                # Local income tax
                local_income_tax = tax.value.get("LocalIncomeTax")
                
                # Locality name
                locality_name = tax.value.get("LocalityName")

if __name__ == "__main__":
    financial_info = Parent.Parent()
    student_info = Student.Student()
    analyze_tax_us_w2(student_info, financial_info)