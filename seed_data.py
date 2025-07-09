
import json
from app import app, db
from models import Category, Question

def seed_questions():
    """Seed the database with the complete audit questionnaire"""
    
    with app.app_context():
        # Clear existing data
        Question.query.delete()
        Category.query.delete()
        db.session.commit()
        
        # Create categories with descriptions
        categories = [
            {
                "name": "Accountability and Governance", 
                "description": "This section evaluates your organization's governance framework, management awareness, policies, and accountability measures for data protection compliance under the Nigeria Data Protection Act (NDPA).",
                "order_num": 1
            },
            {
                "name": "Data Protection Officer / Compliance Organisation", 
                "description": "This section assesses the appointment, training, certification, and effectiveness of your Data Protection Officer (DPO) or Data Protection Compliance Organisation (DPCO) in ensuring NDPA compliance.",
                "order_num": 2
            },
            {
                "name": "Data Inventory and Mapping", 
                "description": "This section examines how your organization identifies, documents, and maintains an inventory of personal data, including data sources, usage, and storage locations.",
                "order_num": 3
            },
            {
                "name": "Data Classification Assessment", 
                "description": "This section evaluates your organization's approach to classifying personal data based on sensitivity and risk levels to ensure appropriate protection measures.",
                "order_num": 4
            },
            {
                "name": "Administration", 
                "description": "This section reviews the administrative and technological processes your organization uses for data governance, access control, and automated data management systems.",
                "order_num": 5
            },
            {
                "name": "Capturing", 
                "description": "This section assesses your organization's data collection methods, validation processes, backup procedures, and disaster recovery capabilities.",
                "order_num": 6
            },
            {
                "name": "Actions & Security", 
                "description": "This section evaluates the technical and organizational security measures implemented to protect personal data throughout its lifecycle, including encryption, access controls, and incident response.",
                "order_num": 7
            }
        ]
        
        for cat_data in categories:
            category = Category(**cat_data)
            db.session.add(category)
        
        # Create all questions with proper numbering
        questions = [
            # ACCOUNTABILITY AND GOVERNANCE (Questions 1-29)
            {
                "category": "Accountability and Governance",
                "question_text": "Did you process the personal data of: a) More than 1,000 Data Subjects in the last 6 months OR b) More than 2,000 Data Subjects in the last 12 months?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 1
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Is your top-management aware of the Nigeria Data Protection Act (NDPA) and the potential implication on your organisation?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 2
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Have you implemented any information security standard in your organisation before? If Yes, specify standard and upload supporting document.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 3
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Do you have a documented data breach incident management procedure? Please upload the document if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 4
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Do you collect and process personal information through digital mediums?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 5
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Have you organised any NDPA awareness seminar for staff or suppliers? Please upload training evidence if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 6
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Have you conducted a detailed audit of your privacy and data protection practices? Please upload audit report if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 7
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Have you defined management support for data protection compliance through policy frameworks? Please upload policy document if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 8
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Do you have a data protection compliance and review mechanism?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 9
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Have you developed a capacity building plan for staff on data protection compliance? Please upload the plan if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 10
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Do you know the types of personal data you hold?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 11
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Do you know the sources of the personal data you hold?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 12
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Who do you share personal data with? Please provide details in the comments section.",
                "question_type": "multiple_choice",
                "options": json.dumps(["We share data", "We don't share data", "Not sure"]),
                "order_num": 13
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Have you reviewed your HR policy to ensure employee data is NDPA compliant? Please upload HR policy if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 14
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Have you assessed whether you are a Data Controller or Processor?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Controller", "Processor", "Both", "Not Sure"]),
                "order_num": 15
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Have appropriate technical and organisational measures been implemented for data protection? Please upload supporting documents if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 16
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Do you have a DPIA policy for assessing privacy impact in new/existing projects? Please upload DPIA policy if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 17
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Does your DPIA policy address: a) Description of processing operations, b) Purpose of processing, c) Legitimate interest pursued, d) Assessment of necessity and proportionality, e) Risk to rights and freedoms, f) Mitigation measures?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes, all items", "Yes, some items", "No"]),
                "order_num": 18
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Who is responsible for data protection compliance in your organisation? Please provide details in the comments section.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Designated person/team", "Multiple people", "Not clearly defined"]),
                "order_num": 19
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Are your service providers/merchants compliant with the NDPR? If yes, please upload audit trust documents. If no, have you mandated them to be compliant?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No", "Some"]),
                "order_num": 20
            },
            {
                "category": "Accountability and Governance",
                "question_text": "What training programs are in place for employee data privacy and security awareness? Please upload training materials or summary if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Comprehensive programs", "Basic programs", "None"]),
                "order_num": 21
            },
            {
                "category": "Accountability and Governance",
                "question_text": "How often are employees updated on changes in privacy regulations?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Quarterly", "Bi-annually", "Annually", "Not at all"]),
                "order_num": 22
            },
            {
                "category": "Accountability and Governance",
                "question_text": "What accountability measures exist for processing activities? Please provide details in the comments section.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Strong measures", "Basic measures", "None"]),
                "order_num": 23
            },
            {
                "category": "Accountability and Governance",
                "question_text": "What strategies support embedding privacy culture in the organisation? Please provide details in the comments section.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Comprehensive strategies", "Basic strategies", "None"]),
                "order_num": 24
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Have workshops been conducted to educate stakeholders about privacy obligations? Please upload workshop evidence if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 25
            },
            {
                "category": "Accountability and Governance",
                "question_text": "How do you ensure all individuals understand their data protection responsibilities? Please provide details in the comments section.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Clear processes", "Basic processes", "No processes"]),
                "order_num": 26
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Is privacy awareness promoted at all levels of the organisation?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 27
            },
            {
                "category": "Accountability and Governance",
                "question_text": "Are there training programs/resources on privacy best practices?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 28
            },
            {
                "category": "Accountability and Governance",
                "question_text": "How are staff held accountable for privacy policy adherence? Please provide details in the comments section.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Clear accountability measures", "Basic measures", "No measures"]),
                "order_num": 29
            },
            
            # DATA PROTECTION OFFICER / COMPLIANCE ORGANISATION (Questions 30-78)
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Does your DPCO also perform the role of your DPO?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 30
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Has a DPO been appointed for NDPA compliance oversight? Please upload appointment letter if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 31
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Do you use the same DPCO for compliance implementation and audit?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 32
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Has your DPO been trained in the last year? Please upload training certificate if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 33
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Does your DPO hold a valid data privacy certification? Please upload certification proof if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 34
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Does the DPO have sufficient access, support, and budget?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 35
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Has conflict of interest been evaluated if the DPO holds multiple roles?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No", "Not Applicable"]),
                "order_num": 36
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Does the DPO have expertise to: a) Advise business and third parties, b) Monitor NDPA compliance, c) Raise awareness and assign responsibilities, d) Provide DPIA-related advice?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes, all areas", "Yes, some areas", "No"]),
                "order_num": 37
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Is there a channel (e.g. webpage) for data subjects to reach your organisation? Please provide webpage link in comments.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 38
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Are there checks to ensure individual rights are preserved under NDPA?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 39
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Is there a public-facing mechanism for Data Subject inquiries (e.g., webpage)? Please upload webpage link or screenshot if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 40
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Are all staff trained to recognise Subject Access Requests (SARs)?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 41
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Do you have procedures for handling SARs from third parties?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 42
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Have you implemented breach detection, reporting and investigation protocols?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 43
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Do you notify affected individuals of breaches that pose high risk to their rights?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 44
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Have all staff handling personal data been trained on their responsibilities?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 45
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Are these responsibilities documented in job descriptions?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 46
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Do you use third-party data processors? If Yes, are contracts NDPA-compliant? Please upload contract sample if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes, with compliant contracts", "Yes, without compliant contracts", "No"]),
                "order_num": 47
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Do you review contracts regularly for NDPA compliance?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 48
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Do you transfer personal data outside Nigeria? If Yes, please upload data transfer policy and provide details in comments about countries, data types, purpose, and legal basis.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 49
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "How do you assess adequacy of protection in recipient countries? Please provide details in comments.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Comprehensive assessment", "Basic assessment", "No assessment"]),
                "order_num": 50
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "What technical and organisational measures are in place (e.g., encryption, access control)? Please provide details in comments.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Comprehensive measures", "Basic measures", "Limited measures"]),
                "order_num": 51
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Do you inform Data Subjects about international transfers and rights?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 52
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "How do you respond to SARs for internationally transferred data? Please provide details in comments.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Established procedures", "Basic procedures", "No procedures"]),
                "order_num": 53
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Do you meet ISO/IEC 27001 standards or similar for securing personal data? Please upload certification or summary of controls if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 54
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Are staff aware that unauthorised access to personal data is prohibited?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 55
            },
            {
                "category": "Data Protection Officer / Compliance Organisation",
                "question_text": "Are staff informed that data confidentiality continues after employment ends?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 56
            },
            
            # DATA INVENTORY AND MAPPING (Questions 57-62)
            {
                "category": "Data Inventory and Mapping",
                "question_text": "Have you developed a data inventory/map identifying data usage and location? Please upload sample if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 57
            },
            {
                "category": "Data Inventory and Mapping",
                "question_text": "How frequently is the data inventory updated?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Quarterly", "Annually", "As needed", "Not updated"]),
                "order_num": 58
            },
            {
                "category": "Data Inventory and Mapping",
                "question_text": "Are specific individuals/teams responsible for data inventory accuracy?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 59
            },
            {
                "category": "Data Inventory and Mapping",
                "question_text": "Who maintains the data inventory, and how is cross-departmental input managed? Please provide details in comments.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Centralized management", "Distributed management", "No clear management"]),
                "order_num": 60
            },
            {
                "category": "Data Inventory and Mapping",
                "question_text": "What tools/technologies support your data inventory process? Please provide details in comments.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Specialized tools", "Basic tools", "Manual processes"]),
                "order_num": 61
            },
            {
                "category": "Data Inventory and Mapping",
                "question_text": "Do you use third-party tools/services for inventory automation or accuracy?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 62
            },
            
            # DATA CLASSIFICATION ASSESSMENT (Questions 63-67)
            {
                "category": "Data Classification Assessment",
                "question_text": "Do you have a data classification policy for risk-based categorisation? Please upload policy if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 63
            },
            {
                "category": "Data Classification Assessment",
                "question_text": "How are classification categories defined? Please provide details in comments.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Well-defined categories", "Basic categories", "No defined categories"]),
                "order_num": 64
            },
            {
                "category": "Data Classification Assessment",
                "question_text": "Do you have procedures to identify/classify personal data in your systems?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 65
            },
            {
                "category": "Data Classification Assessment",
                "question_text": "What classification levels are used (e.g., Public, Confidential, Restricted)? Please provide details in comments.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Multiple levels", "Basic levels", "No classification"]),
                "order_num": 66
            },
            {
                "category": "Data Classification Assessment",
                "question_text": "Provide examples of data classification in your organization. Please provide details in comments.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Clear examples available", "Some examples available", "No examples"]),
                "order_num": 67
            },
            
            # ADMINISTRATION (Questions 68-73)
            {
                "category": "Administration",
                "question_text": "Do you use technology/an automated process to handle data?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 68
            },
            {
                "category": "Administration",
                "question_text": "Is there a documented data governance policy in place? Does it align with the way you process data on the system?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No", "Partially"]),
                "order_num": 69
            },
            {
                "category": "Administration",
                "question_text": "Are there procedures for data access control and user permissions?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No", "Partially"]),
                "order_num": 70
            },
            {
                "category": "Administration",
                "question_text": "Do you use technology or automated processes to manage the collection, storage, use, and processing of data?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 71
            },
            {
                "category": "Administration",
                "question_text": "Does the technology/automated process in place comply with industry and regulatory standards?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No", "Not Sure"]),
                "order_num": 72
            },
            {
                "category": "Administration",
                "question_text": "Are security awareness training sessions conducted to educate employees about physical and environmental security measures?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No", "Sometimes"]),
                "order_num": 73
            },
            
            # CAPTURING (Questions 74-102)
            {
                "category": "Capturing",
                "question_text": "Do you use technology or automated processes for data collection?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 74
            },
            {
                "category": "Capturing",
                "question_text": "What methods or tools are used for data collection within the organization? Please upload documentation if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Multiple methods", "Basic methods", "Manual methods"]),
                "order_num": 75
            },
            {
                "category": "Capturing",
                "question_text": "Are data collection processes standardized and documented?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 76
            },
            {
                "category": "Capturing",
                "question_text": "Are there mechanisms to verify the accuracy and completeness of collected data?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 77
            },
            {
                "category": "Capturing",
                "question_text": "Are there any tech or automated processes used in collecting and processing data?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 78
            },
            {
                "category": "Capturing",
                "question_text": "What are the primary sources of data for the organization? Please upload documentation if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Multiple sources", "Few sources", "Single source"]),
                "order_num": 79
            },
            {
                "category": "Capturing",
                "question_text": "How is data from different sources processed and used? Please upload documentation if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Integrated processing", "Basic processing", "Manual processing"]),
                "order_num": 80
            },
            {
                "category": "Capturing",
                "question_text": "Are there procedures for validating and cleansing incoming data?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 81
            },
            {
                "category": "Capturing",
                "question_text": "Are there procedures for obtaining consent and permissions for data collection and processing, especially sensitive data?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 82
            },
            {
                "category": "Capturing",
                "question_text": "What methods are used for processing and analysing data within the organization? Please upload documentation if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Advanced methods", "Basic methods", "Manual methods"]),
                "order_num": 83
            },
            {
                "category": "Capturing",
                "question_text": "Are there controls in place to prevent unauthorized access or modification of data during processing?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 84
            },
            {
                "category": "Capturing",
                "question_text": "How do you store/backup data?",
                "question_type": "multiple_choice",
                "options": json.dumps(["On Premises", "Cloud", "Both"]),
                "order_num": 85
            },
            {
                "category": "Capturing",
                "question_text": "How frequently is data backed up, and what methods are employed for backups? Please upload documentation if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Daily", "Weekly", "Monthly", "Irregular"]),
                "order_num": 86
            },
            {
                "category": "Capturing",
                "question_text": "Do you have a disaster recovery plan? Is there a procedure for activating and carrying out the plan in the event of a calamity?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes, comprehensive plan", "Yes, basic plan", "No"]),
                "order_num": 87
            },
            {
                "category": "Capturing",
                "question_text": "Do employees receive training on the disaster recovery plan?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 88
            },
            {
                "category": "Capturing",
                "question_text": "Is your on-premises/cloud storage accessible to anyone?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 89
            },
            {
                "category": "Capturing",
                "question_text": "Do you have measures in place to ensure the security of your premises/cloud infrastructure?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 90
            },
            {
                "category": "Capturing",
                "question_text": "Do you have measures to authenticate and authorize access to your premises/cloud services?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 91
            },
            {
                "category": "Capturing",
                "question_text": "Does the technology record and manage access to data?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 92
            },
            {
                "category": "Capturing",
                "question_text": "Do you train employees on cloud security best practices? (Only for those who require access)",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 93
            },
            {
                "category": "Capturing",
                "question_text": "How is data quality monitored and maintained throughout its lifecycle? Please upload documentation if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Comprehensive monitoring", "Basic monitoring", "No monitoring"]),
                "order_num": 94
            },
            {
                "category": "Capturing",
                "question_text": "Does a backup policy exist, and is it routinely tested?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 95
            },
            {
                "category": "Capturing",
                "question_text": "Are backups kept in a safe, off-site place?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 96
            },
            {
                "category": "Capturing",
                "question_text": "Does the disaster recovery plan undergo routine testing?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 97
            },
            
            # ACTIONS & SECURITY (Questions 98-153)
            {
                "category": "Actions & Security",
                "question_text": "Do you apply technology or automated processes to protect data?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 98
            },
            {
                "category": "Actions & Security",
                "question_text": "Does the process protect data while in transit and at rest?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 99
            },
            {
                "category": "Actions & Security",
                "question_text": "Do you use any encryption method?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 100
            },
            {
                "category": "Actions & Security",
                "question_text": "Does the organization have an information security policy, and is it communicated to all employees?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 101
            },
            {
                "category": "Actions & Security",
                "question_text": "Are access controls and authentication mechanisms in place?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 102
            },
            {
                "category": "Actions & Security",
                "question_text": "How are security incidents and breaches detected, reported, and mitigated? Please upload documentation if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Comprehensive procedures", "Basic procedures", "No procedures"]),
                "order_num": 103
            },
            {
                "category": "Actions & Security",
                "question_text": "Do you authorize and verify user identities for your applications?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 104
            },
            {
                "category": "Actions & Security",
                "question_text": "Do you have safeguards against unwanted access to your applications?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 105
            },
            {
                "category": "Actions & Security",
                "question_text": "Do you update software regularly?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 106
            },
            {
                "category": "Actions & Security",
                "question_text": "Do you ensure the security of third-party components in your applications?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 107
            },
            {
                "category": "Actions & Security",
                "question_text": "Is the security of mobile applications ensured?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No", "Not Applicable"]),
                "order_num": 108
            },
            {
                "category": "Actions & Security",
                "question_text": "Are best practices for application security taught to employees?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 109
            },
            {
                "category": "Actions & Security",
                "question_text": "Do you implement cybersecurity practices to secure the network?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 110
            },
            {
                "category": "Actions & Security",
                "question_text": "Are firewalls and IDS/IPS in place?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 111
            },
            {
                "category": "Actions & Security",
                "question_text": "Are network devices configured securely?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 112
            },
            {
                "category": "Actions & Security",
                "question_text": "Are unnecessary network ports/protocols blocked?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 113
            },
            {
                "category": "Actions & Security",
                "question_text": "Is there a process for monitoring network traffic?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 114
            },
            {
                "category": "Actions & Security",
                "question_text": "Do you have staff that work from home?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 115
            },
            {
                "category": "Actions & Security",
                "question_text": "Do they connect to the organisation network for tasks?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 116
            },
            {
                "category": "Actions & Security",
                "question_text": "Do you provide secure connection technologies (e.g., VPN, tunneling)?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 117
            },
            {
                "category": "Actions & Security",
                "question_text": "Are mechanisms provided to secure data during communication with clients?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 118
            },
            {
                "category": "Actions & Security",
                "question_text": "Are physical controls (locks, alarms, CCTV) used?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 119
            },
            {
                "category": "Actions & Security",
                "question_text": "What measures protect against physical threats? Please upload documentation if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Comprehensive measures", "Basic measures", "Limited measures"]),
                "order_num": 120
            },
            {
                "category": "Actions & Security",
                "question_text": "Are systems and software updated frequently?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 121
            },
            {
                "category": "Actions & Security",
                "question_text": "Is there a procedure to track system activities and detect irregularities?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 122
            },
            {
                "category": "Actions & Security",
                "question_text": "Is there a documented data disposal plan for paper and electronic waste?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No"]),
                "order_num": 123
            },
            {
                "category": "Actions & Security",
                "question_text": "How is personal data destroyed before disposal? Is it NIST-compliant? Please upload documentation if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["NIST-compliant", "Compliant with other standards", "Basic destruction", "No documented process"]),
                "order_num": 124
            }
        ]
        
        for q_data in questions:
            question = Question(**q_data)
            db.session.add(question)
        
        db.session.commit()
        print(f"Successfully seeded {len(categories)} categories and {len(questions)} questions!")

if __name__ == "__main__":
    seed_questions()
