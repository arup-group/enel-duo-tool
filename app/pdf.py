# generate PDF report

from fpdf import FPDF
import analysis

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        # Custom logo and positioning
        self.image('https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Enel_Group_logo.svg/1200px-Enel_Group_logo.svg.png', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'DUO AgroPV Report', 0, 0, 'R')
        self.ln(20)
        
    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
        self.cell(0, 10, "Arup", 0, 0, 'L')

    def page_body(self):
        # Determine how many plots there are per page and set positions
        # and margins accordingly
        self.cell(0, 0, analysis.Analysis().rec(), 1, 1, "L")
            
    def print_page(self):
        # Generates the report
        self.add_page()
        self.page_body()