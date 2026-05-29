import os
from openai import OpenAI
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables (expecting OPENAI_API_KEY in the root directory's .env)
load_dotenv(dotenv_path="../.env")

# Initialize OpenAI client
client = OpenAI()

class ResumePDF(FPDF):
    def header(self):
        # We don't need a specific header for all pages, but we can customize if needed
        pass

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def generate_resume_content(name, contact_info, job_title, experience, skills):
    prompt = f"""
    You are an expert resume writer. Create a professional resume for the following individual.
    
    Name: {name}
    Contact Information: {contact_info}
    Target Job Title: {job_title}
    Experience Summary: {experience}
    Key Skills: {skills}
    
    Structure the resume with the following sections clearly labeled with ALL CAPS (e.g., SUMMARY, PROFESSIONAL EXPERIENCE, SKILLS, EDUCATION):
    - SUMMARY: A brief, compelling professional summary.
    - PROFESSIONAL EXPERIENCE: Elaborate on the experience provided, making it sound professional and impactful. Use bullet points starting with a dash (-).
    - SKILLS: A formatted list of skills.
    
    Do not use markdown like asterisks (**) or hashes (#). Use plain text formatting. Ensure the tone is highly professional.
    """
    
    try:
        print("\nGenerating resume content with AI... Please wait.")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume writer and career coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating content from OpenAI: {e}")
        print("\n[Falling back to mock resume template due to API error]")
        return f"""SUMMARY
An accomplished and dedicated {job_title} with a strong background. Proven ability to deliver high-quality results and contribute effectively to team goals.

PROFESSIONAL EXPERIENCE
- {experience}
- Successfully managed projects from conception to completion.
- Collaborated with cross-functional teams to improve processes and efficiency.
- Consistently met and exceeded performance targets.

SKILLS
- {skills}
- Leadership, Problem Solving, Communication
"""

def create_pdf(name, content, output_filename="resume.pdf"):
    pdf = ResumePDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Title (Name)
    pdf.set_font('Arial', 'B', 18)
    # Encode correctly for FPDF latin-1
    safe_name = name.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 10, safe_name.upper(), ln=True, align='C')
    pdf.ln(5)
    
    # Content
    pdf.set_font('Arial', '', 11)
    
    # Replacing common unicode chars that FPDF might choke on
    content = content.replace('\u2013', '-').replace('\u2014', '-').replace('\u2018', "'").replace('\u2019', "'").replace('\u2022', '-')
    
    # Process line by line to handle bolding (capitalized headers)
    for line in content.split('\n'):
        # If line is entirely uppercase (ignoring non-alpha) and somewhat short, treat as header
        alpha_chars = [c for c in line if c.isalpha()]
        if len(alpha_chars) > 0 and all(c.isupper() for c in alpha_chars) and len(line) < 40 and not line.strip().startswith('-'):
            pdf.ln(4)
            pdf.set_font('Arial', 'B', 12)
            safe_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(0, 8, safe_line, ln=True)
            pdf.set_font('Arial', '', 11)
        else:
            safe_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 6, safe_line)
            
    pdf.output(output_filename)
    print(f"\nSuccess! Resume saved to {output_filename}")

def main():
    print("=== AI Resume Builder ===")
    print("Please provide some basic details to generate your professional resume.\n")
    
    name = input("Enter your full name: ")
    contact_info = input("Enter your contact info (e.g., Phone, Email, LinkedIn): ")
    job_title = input("Enter your target job title: ")
    experience = input("Briefly describe your experience (e.g., 3 years in sales at XYZ): ")
    skills = input("Enter your key skills (comma separated): ")
    
    content = generate_resume_content(name, contact_info, job_title, experience, skills)
    
    if content:
        print("\n--- Generated Content Preview ---\n")
        print(content)
        print("\n---------------------------------")
        
        filename = f"{name.replace(' ', '_').lower()}_resume.pdf"
        # ensure no empty names just in case
        if not filename.strip("_resume.pdf"):
            filename = "generated_resume.pdf"
            
        create_pdf(name, content, filename)

if __name__ == "__main__":
    main()
