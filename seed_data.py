import json
from app import app, db
from models import Category, Question

def seed_questions():
    """Seed the database with sample questions"""
    
    with app.app_context():
        # Clear existing data
        Question.query.delete()
        Category.query.delete()
        db.session.commit()
        
        # Create categories
        categories = [
            {"name": "Governance & Accountability", "description": "Questions about organizational governance, policies, and accountability measures for data protection compliance.", "order_num": 1},
            {"name": "Awareness & Training", "description": "Assessment of staff awareness and training programs related to data protection and privacy.", "order_num": 2},
            {"name": "Data Processing and Sharing", "description": "Evaluation of data processing activities, sharing practices, and compliance with data protection principles.", "order_num": 3},
            {"name": "Administration", "description": "Review of administrative procedures and digital management of data protection processes.", "order_num": 4},
            {"name": "Capturing", "description": "Assessment of data collection and acquisition processes, ensuring secure and compliant data capturing methods.", "order_num": 5},
            {"name": "Actions On Security", "description": "Evaluation of security measures, access controls, and data protection safeguards.", "order_num": 6}
        ]
        
        for cat_data in categories:
            category = Category(**cat_data)
            db.session.add(category)
        
        # Create questions
        questions = [
            # Governance & Accountability
            {
                "category": "Governance & Accountability",
                "question_text": "Is your top-management aware of the Nigeria Data Protection Act (NDPA) and the potential implications on your organization?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 1
            },
            {
                "category": "Governance & Accountability",
                "question_text": "Have you implemented any information security standard in your organization before? If YES, specify and upload evidence if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 2
            },
            {
                "category": "Governance & Accountability",
                "question_text": "Do you have a documented data breach incident management procedure? Upload the procedure if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 3
            },
            {
                "category": "Governance & Accountability",
                "question_text": "Have you conducted a detailed audit of your privacy and data protection practices before this assessment?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 4
            },
            {
                "category": "Governance & Accountability",
                "question_text": "Do you have a designated Data Protection Officer (DPO) or equivalent role in your organization?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "No", "In Process of Appointing"]),
                "order_num": 5
            },
            
            # Awareness & Training
            {
                "category": "Awareness & Training",
                "question_text": "Have you organized any NDPA awareness seminar for your members of staff or suppliers?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 6
            },
            {
                "category": "Awareness & Training",
                "question_text": "Do your employees receive regular training on data protection and privacy matters? Upload training materials if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes, Regularly", "Occasionally", "No"]),
                "order_num": 7
            },
            {
                "category": "Awareness & Training",
                "question_text": "Are employees aware of their roles and responsibilities regarding data protection compliance?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Fully Aware", "Partially Aware", "Not Aware"]),
                "order_num": 8
            },
            {
                "category": "Awareness & Training",
                "question_text": "Do you have documented training records for data protection awareness programs? Upload records if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 9
            },
            
            # Data Processing and Sharing
            {
                "category": "Data Processing and Sharing",
                "question_text": "Do you collect and process personal information through digital mediums?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 10
            },
            {
                "category": "Data Processing and Sharing",
                "question_text": "Do you have documented procedures for lawful data processing activities? Upload procedures if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 11
            },
            {
                "category": "Data Processing and Sharing",
                "question_text": "Do you obtain appropriate consent before processing personal data where required?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Always", "Sometimes", "Never"]),
                "order_num": 12
            },
            {
                "category": "Data Processing and Sharing",
                "question_text": "Do you share personal data with third parties? If yes, do you have data sharing agreements in place? Upload agreements if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes, with agreements", "Yes, without agreements", "No sharing"]),
                "order_num": 13
            },
            {
                "category": "Data Processing and Sharing",
                "question_text": "Do you have mechanisms to ensure data accuracy and keep personal data up-to-date?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 14
            },
            
            # Administration
            {
                "category": "Administration",
                "question_text": "Do you maintain records of processing activities as required by NDPA? Upload records if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 15
            },
            {
                "category": "Administration",
                "question_text": "Do you have digital systems in place to manage data subject requests (access, rectification, erasure)?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Fully Implemented", "Partially Implemented", "Not Implemented"]),
                "order_num": 16
            },
            {
                "category": "Administration",
                "question_text": "Are your data protection policies and procedures regularly reviewed and updated? Upload current policies if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes, Regularly", "Occasionally", "No"]),
                "order_num": 17
            },
            {
                "category": "Administration",
                "question_text": "Do you have processes for data retention and disposal in accordance with NDPA requirements?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 18
            },
            
            # Capturing
            {
                "category": "Capturing",
                "question_text": "Do you have secure methods for collecting personal data from various sources?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 19
            },
            {
                "category": "Capturing",
                "question_text": "Are data collection forms and processes designed with privacy considerations in mind? Upload sample forms if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 20
            },
            {
                "category": "Capturing",
                "question_text": "Do you validate the source and accuracy of personal data during collection?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Always", "Sometimes", "Never"]),
                "order_num": 21
            },
            {
                "category": "Capturing",
                "question_text": "Do you inform data subjects about the purpose of data collection at the point of collection?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Always", "Sometimes", "Never"]),
                "order_num": 22
            },
            
            # Actions On Security
            {
                "category": "Actions On Security",
                "question_text": "Do you have technical and organizational measures to secure personal data against unauthorized access?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Comprehensive measures", "Basic measures", "No measures"]),
                "order_num": 23
            },
            {
                "category": "Actions On Security",
                "question_text": "Are access controls implemented to ensure only authorized personnel can access personal data? Upload access control policy if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "Partially", "No"]),
                "order_num": 24
            },
            {
                "category": "Actions On Security",
                "question_text": "Do you have incident response procedures for data security breaches?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes", "In Development", "No"]),
                "order_num": 25
            },
            {
                "category": "Actions On Security",
                "question_text": "Are personal data transmissions encrypted and secure?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Always", "Sometimes", "Never"]),
                "order_num": 26
            },
            {
                "category": "Actions On Security",
                "question_text": "Do you conduct regular security assessments and penetration testing? Upload recent assessment reports if available.",
                "question_type": "multiple_choice",
                "options": json.dumps(["Yes, Regularly", "Occasionally", "No"]),
                "order_num": 27
            }
        ]
        
        for q_data in questions:
            question = Question(**q_data)
            db.session.add(question)
        
        db.session.commit()
        print(f"Successfully seeded {len(categories)} categories and {len(questions)} questions!")

if __name__ == "__main__":
    seed_questions()