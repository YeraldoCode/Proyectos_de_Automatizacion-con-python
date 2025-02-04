import streamlit as st 
from fpdf import FPDF 

class PDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font("Arial", 'B', size = 12)
            self.cell(0, 10, txt=self.document_title, border=0,  ln=1, align='C')