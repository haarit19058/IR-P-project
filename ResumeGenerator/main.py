import json
import os
from fpdf import FPDF
import argparse
from langchain_groq.chat_models import ChatGroq
import secure
Groq_Token = secure.key


def rephrase(skills,education,experience,other_details):

    prompt = f'''
            Rephrase the following text into a formal and polished format, suitable for a resume:
            skills : {skills}
            education : {education}
            experience : {experience}
            other_details : {other_details}
            Return the output as a tuple of three strings in the format: (skills, education,experience,other_details)
            Do not give anything other than the tuple in response
            Do not include ':' in response

    '''
    model_name = 'llama3-70b-8192'
    llm = ChatGroq(model=model_name, api_key=Groq_Token, temperature=0)
    answer = llm.invoke(prompt)
    # print(answer.content)


    return [j.strip() for j in [i.split(":")[1] for i in eval(answer.content)]]

def convertColor(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6 or not all(char in '0123456789abcdefABCDEF' for char in hex_color):
        raise ValueError("Invalid hexadecimal color code")
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def saveCurrent(args, name, contact_no, email_id, address, skills, education, experience, other_details):
    data = {
        'font_size': args.font_size,
        'font_color': args.font_color,
        'background_color': args.background_color,
        'name': name,
        'contact_no': contact_no,
        'email_id': email_id,
        'address': address,
        'skills': skills,
        'education': education,
        'experience': experience,
        'other_details': other_details
    }
    with open('resume_config.json', 'w') as f:
        json.dump(data, f, indent=4)

def loadPrevious():
    if os.path.exists('resume_config.json'):
        with open('resume_config.json', 'r') as f:
            return json.load(f)
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description='Resume Generator')
    parser.add_argument('--font-size', type=int, default=12, help='Font size')
    parser.add_argument('--font-color', type=str, default='#000000', help='Font color (hex code or color name)')
    parser.add_argument('--background-color', type=str, default='#FFFFFF', help='Background color (hex code or color name)')
    parser.add_argument('--regenerate', action='store_true', help='Regenerate the resume with previous values')
    parser.add_argument('--rephrase', action='store_true', help='Use llama 3.0 to rephrase and enhance your text')
    args = parser.parse_args()

    # print(rephrase("","",""))
    
    if args.regenerate:
        variables = loadPrevious()
        if variables is not None:
            name = variables['name']
            contact_no = variables['contact_no']
            email_id = variables['email_id']
            address = variables['address']
            skills = variables['skills']
            education = variables['education']
            experience = variables['experience']
            other_details = variables['other_details']
            args.font_size = variables['font_size']
            args.font_color = variables['font_color']
            args.background_color = variables['background_color']
            print("Regenerated the recent build.")
        else:
            print("No previous values found. Please run the script without --regenerate to create a new resume.")
            return
    else:
        name = input("Enter your name: ")
        contact_no = input("Enter your contact number: ")
        email_id = input("Enter your email ID: ")
        address = input("Enter your address: ")
        skills = input("Enter your skills (comma-separated): ")
        education = input("Enter your education details: ")
        experience = input("Enter your experience details: ")
        other_details = input("Enter any other details you'd like to include: ")
        saveCurrent(args, name, contact_no, email_id, address, skills, education, experience, other_details)

    if args.rephrase:
        [skills,education,experience,other_details] = rephrase(skills,education,experience,other_details)
        saveCurrent(args, name, contact_no, email_id, address, skills, education, experience, other_details)

    pdf = FPDF()
    pdf.add_page()

    # BackGround Color
    pdf.set_fill_color(*convertColor(args.background_color))
    pdf.rect(0, 0, 210, 297, 'F') 

    pdf.set_font('Arial', 'B', args.font_size + 4)
    pdf.set_text_color(*convertColor(args.font_color))
    pdf.cell(0, 15, txt=name, ln=True, align='C')

    # Contact
    pdf.set_font('Arial', '', args.font_size)
    pdf.set_text_color(*convertColor(args.font_color))
    pdf.x = 10
    pdf.cell(190, 5, txt=f"Contact No.: {contact_no}", ln=True, align='L')
    pdf.cell(190, 10, txt=f"Email ID: {email_id}", ln=True, align='L')
    pdf.cell(190, 10, txt=f"Address: {address}", ln=True, align='L')

    pdf.set_font('Arial', 'B', args.font_size+2)
    pdf.set_text_color(*convertColor(args.font_color))
    # Skills
    pdf.ln(10)  # Line break
    pdf.cell(200, 10, txt="Skills:", ln=True)
    pdf.set_font('Arial', '', args.font_size)
    pdf.set_text_color(*convertColor(args.font_color))
    pdf.multi_cell(0, 10, txt=skills, fill=True)

    # Education
    pdf.ln(10) 
    pdf.set_font('Arial', 'B', args.font_size+2)
    pdf.set_text_color(*convertColor(args.font_color))
    pdf.cell(200, 10, txt="Education:", ln=True)
    pdf.set_font('Arial', '', args.font_size)
    pdf.set_text_color(*convertColor(args.font_color))
    pdf.multi_cell(0, 10, txt=education, fill=True)

    # Experience
    pdf.ln(10)  # Line break
    pdf.set_font('Arial', 'B', args.font_size+2)
    pdf.set_text_color(*convertColor(args.font_color))
    pdf.cell(200, 10, txt="Experience:", ln=True)
    pdf.set_font('Arial', '', args.font_size)
    pdf.set_text_color(*convertColor(args.font_color))
    pdf.multi_cell(0, 10, txt=experience, fill=True)

    # Other details
    if(len(other_details)>0):
        pdf.ln(10)  # Line break
        pdf.set_font('Arial', 'B', args.font_size+2)
        pdf.set_text_color(*convertColor(args.font_color))
        pdf.cell(200, 10, txt="Other Details:", ln=True)
        pdf.set_font('Arial', '', args.font_size)
        pdf.set_text_color(*convertColor(args.font_color))
        pdf.multi_cell(0, 10, txt=other_details, fill=True)
    
    pdf.output('Resume.pdf')
    print("File saved as Resume.pdf")


if __name__=="__main__":
    main()