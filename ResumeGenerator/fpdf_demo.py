from fpdf import FPDF

# Create a PDF object
pdf = FPDF()

# Add a page to the PDF
pdf.add_page()

# Set font for the PDF
pdf.set_font('Arial', 'B', 16)

# Title
pdf.cell(200, 10, txt="Resume", ln=True, align='C')

# Set font for the content
pdf.set_font('arial', '', 10)

# Add Name
pdf.ln(10)  # Line break
pdf.cell(200, 10, txt="Name: John Doe", ln=True)

# Add Experience
pdf.cell(200, 10, txt="Experience:", ln=True)
pdf.multi_cell(0, 10, txt="Worked as a Software Engineer at XYZ Corp for 3 years. Involved in developing full-stack applications, managing databases, and optimizing code for better performance.")

# Add Education
pdf.cell(200, 10, txt="Education:", ln=True)
pdf.multi_cell(0, 10, txt="B.Tech in Computer Science, ABC University (2019-2023)")

# Add Skills
pdf.cell(200, 10, txt="Skills:", ln=True)
pdf.multi_cell(0, 10, txt="Python, Java, C++, Machine Learning, Data Analysis, Web Development, SQL")

# Save the PDF to a file
pdf.output('personal_information.pdf')

print("PDF created successfully.")
