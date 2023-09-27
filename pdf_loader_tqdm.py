from  PyPDF2 import PdfReader
from fpdf import FPDF
from tqdm import tqdm


def extract_text(file): #Extract text from PDF file
    reader = PdfReader(file)
    str = ""
    
    # Use tqdm to monitor the progress through a for loop
    for i in tqdm(range(len(reader.pages)), desc="Extracting text"):
        str += reader.pages[i].extract_text()
        
    with open("output_text.txt", "w", encoding="utf-8") as f:
        f.write(str)
        


def convert_text_to_pdf(input_file, output_file): #Convert the output.txt file to PDF
    # Read the content of the text file
    with open(input_file, 'r', encoding="utf-8") as file:
        text = file.read()

    # Create an instance of the FPDF class and add a page
    pdf = FPDF()
    pdf.add_font('DejaVuSans', '', 'dejavu-sans/DejaVuSans.ttf', uni=True) #I had to use this font to overcome the unicode problem
    pdf.add_page()

    # Set font and font size
    pdf.set_font("DejaVuSans", size=12)

    # Add the text content to the PDF
    # Use tqdm to monitor the progress through a for loop
    lines = text.split("\n")
    for line in tqdm(lines, desc="Converting to PDF"):
        pdf.multi_cell(0, 10, line)

    # Save the PDF to a file
    pdf.output(output_file)




if __name__ == "__main__":
    
    extract_text("data/input_pdf/Marc Mentat_2022.3-Users_Guide.pdf")
    
    convert_text_to_pdf('output_text.txt', 'data/output_pdf/output.pdf')

