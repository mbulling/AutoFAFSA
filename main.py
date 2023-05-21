import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from secret import endpoint, key
import student_information as student
import parent_financials as parent

# formatting function
def format_address_value(address_value):
    return f"\n......House/building number: {address_value.house_number}\n......Road: {address_value.road}\n......City: {address_value.city}\n......State: {address_value.state}\n......Postal code: {address_value.postal_code}"


def analyze_tax_us_w2(person, financial):
    # sample form document
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
        form_variant = w2.fields.get("W2FormVariant")
        if form_variant:
            print(
                "Form variant: {} has confidence: {}".format(
                    form_variant.value, form_variant.confidence
                )
            )
        tax_year = w2.fields.get("TaxYear")
        if tax_year:
            print(
                "Tax year: {} has confidence: {}".format(
                    tax_year.value, tax_year.confidence
                )
            )
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
            print("Employer data:")
            employer_name = employer.value.get("Name")
            if employer_name:
                print(
                    "...Name: {} has confidence: {}".format(
                        employer_name.value, employer_name.confidence
                    )
                )
            employer_id = employer.value.get("IdNumber")
            if employer_id:
                print(
                    "...ID Number: {} has confidence: {}".format(
                        employer_id.value, employer_id.confidence
                    )
                )
            employer_address = employer.value.get("Address")
            if employer_address:
                print(
                    "...Address: {}\n......has confidence: {}".format(
                        format_address_value(employer_address.value),
                        employer_address.confidence,
                    )
                )
            employer_zipcode = employer.value.get("ZipCode")
            if employer_zipcode:
                print(
                    "...Zipcode: {} has confidence: {}".format(
                        employer_zipcode.value, employer_zipcode.confidence
                    )
                )
        wages_tips = w2.fields.get("WagesTipsAndOtherCompensation")
        if wages_tips:
            print(
                "Wages, tips, and other compensation: {} has confidence: {}".format(
                    wages_tips.value,
                    wages_tips.confidence,
                )
            )
        fed_income_tax_withheld = w2.fields.get("FederalIncomeTaxWithheld")
        if fed_income_tax_withheld:
            print(
                "Federal income tax withheld: {} has confidence: {}".format(
                    fed_income_tax_withheld.value, fed_income_tax_withheld.confidence
                )
            )
        social_security_wages = w2.fields.get("SocialSecurityWages")
        if social_security_wages:
            print(
                "Social Security wages: {} has confidence: {}".format(
                    social_security_wages.value, social_security_wages.confidence
                )
            )
        social_security_tax_withheld = w2.fields.get("SocialSecurityTaxWithheld")
        if social_security_tax_withheld:
            print(
                "Social Security tax withheld: {} has confidence: {}".format(
                    social_security_tax_withheld.value,
                    social_security_tax_withheld.confidence,
                )
            )
        medicare_wages_tips = w2.fields.get("MedicareWagesAndTips")
        if medicare_wages_tips:
            print(
                "Medicare wages and tips: {} has confidence: {}".format(
                    medicare_wages_tips.value, medicare_wages_tips.confidence
                )
            )
        medicare_tax_withheld = w2.fields.get("MedicareTaxWithheld")
        if medicare_tax_withheld:
            print(
                "Medicare tax withheld: {} has confidence: {}".format(
                    medicare_tax_withheld.value, medicare_tax_withheld.confidence
                )
            )
        social_security_tips = w2.fields.get("SocialSecurityTips")
        if social_security_tips:
            print(
                "Social Security tips: {} has confidence: {}".format(
                    social_security_tips.value, social_security_tips.confidence
                )
            )
        allocated_tips = w2.fields.get("AllocatedTips")
        if allocated_tips:
            print(
                "Allocated tips: {} has confidence: {}".format(
                    allocated_tips.value,
                    allocated_tips.confidence,
                )
            )
        verification_code = w2.fields.get("VerificationCode")
        if verification_code:
            print(
                "Verification code: {} has confidence: {}".format(
                    verification_code.value, verification_code.confidence
                )
            )
        dependent_care_benefits = w2.fields.get("DependentCareBenefits")
        if dependent_care_benefits:
            print(
                "Dependent care benefits: {} has confidence: {}".format(
                    dependent_care_benefits.value,
                    dependent_care_benefits.confidence,
                )
            )
        non_qualified_plans = w2.fields.get("NonQualifiedPlans")
        if non_qualified_plans:
            print(
                "Non-qualified plans: {} has confidence: {}".format(
                    non_qualified_plans.value,
                    non_qualified_plans.confidence,
                )
            )
        additional_info = w2.fields.get("AdditionalInfo")
        if additional_info:
            print("Additional information:")
            for item in additional_info.value:
                letter_code = item.value.get("LetterCode")
                if letter_code:
                    print(
                        "...Letter code: {} has confidence: {}".format(
                            letter_code.value, letter_code.confidence
                        )
                    )
                amount = item.value.get("Amount")
                if amount:
                    print(
                        "...Amount: {} has confidence: {}".format(
                            amount.value, amount.confidence
                        )
                    )
        is_statutory_employee = w2.fields.get("IsStatutoryEmployee")
        if is_statutory_employee:
            print(
                "Is statutory employee: {} has confidence: {}".format(
                    is_statutory_employee.value, is_statutory_employee.confidence
                )
            )
        is_retirement_plan = w2.fields.get("IsRetirementPlan")
        if is_retirement_plan:
            print(
                "Is retirement plan: {} has confidence: {}".format(
                    is_retirement_plan.value, is_retirement_plan.confidence
                )
            )
        third_party_sick_pay = w2.fields.get("IsThirdPartySickPay")
        if third_party_sick_pay:
            print(
                "Is third party sick pay: {} has confidence: {}".format(
                    third_party_sick_pay.value, third_party_sick_pay.confidence
                )
            )
        other_info = w2.fields.get("Other")
        if other_info:
            print(
                "Other information: {} has confidence: {}".format(
                    other_info.value,
                    other_info.confidence,
                )
            )
        state_tax_info = w2.fields.get("StateTaxInfos")
        if state_tax_info:
            print("State Tax info:")
            for tax in state_tax_info.value:
                state = tax.value.get("State")
                if state:
                    print(
                        "...State: {} has confidence: {}".format(
                            state.value, state.confidence
                        )
                    )
                employer_state_id_number = tax.value.get("EmployerStateIdNumber")
                if employer_state_id_number:
                    print(
                        "...Employer state ID number: {} has confidence: {}".format(
                            employer_state_id_number.value,
                            employer_state_id_number.confidence,
                        )
                    )
                state_wages_tips = tax.value.get("StateWagesTipsEtc")
                if state_wages_tips:
                    print(
                        "...State wages, tips, etc: {} has confidence: {}".format(
                            state_wages_tips.value, state_wages_tips.confidence
                        )
                    )
                state_income_tax = tax.value.get("StateIncomeTax")
                if state_income_tax:
                    print(
                        "...State income tax: {} has confidence: {}".format(
                            state_income_tax.value, state_income_tax.confidence
                        )
                    )
        local_tax_info = w2.fields.get("LocalTaxInfos")
        if local_tax_info:
            print("Local Tax info:")
            for tax in local_tax_info.value:
                local_wages_tips = tax.value.get("LocalWagesTipsEtc")
                if local_wages_tips:
                    print(
                        "...Local wages, tips, etc: {} has confidence: {}".format(
                            local_wages_tips.value, local_wages_tips.confidence
                        )
                    )
                local_income_tax = tax.value.get("LocalIncomeTax")
                if local_income_tax:
                    print(
                        "...Local income tax: {} has confidence: {}".format(
                            local_income_tax.value, local_income_tax.confidence
                        )
                    )
                locality_name = tax.value.get("LocalityName")
                if locality_name:
                    print(
                        "...Locality name: {} has confidence: {}".format(
                            locality_name.value, locality_name.confidence
                        )
                    )

                print("----------------------------------------")
    print(person.to_string())


if __name__ == "__main__":
    financial_info = parent.ParentFinancials()
    student_info = student.StudentInformation()
    analyze_tax_us_w2(student_info, financial_info)