import streamlit as st 
from fpdf import FPDF 

class PDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font("Helvetica", style='B', size=12)
            self.cell(0, 10, txt=self.document_title, border=0, ln=1, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", style='I', size=8)
        self.cell(0, 10, txt="Pagina " + str(self.page_no()) + "/{nb}", border=0, ln=0, align='C')

    def chapter_title(self, title, font='Helvetica', size=12):
        self.set_font(font, style='B', size=size)
        self.cell(0, 10, txt=title, border=0, ln=1, align='L')
        self.ln(10)

    def chapter_body(self, text, font='Helvetica', size=12):
        self.set_font(font, size=size)
        self.multi_cell(0, 10, txt=text)
        self.ln()
        
def create_pdf(filename, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)

    if image_path:
        pdf.image(image_path, x=10, y=25, w=pdf.w - 20)
        pdf.ln(120)

    for chapter in chapters:
        title, body, font, size = chapter
        pdf.chapter_title(title, font, size)
        pdf.chapter_body(body, font, size)

    pdf.output(filename)

def main():
    st.title("Generador de PDF's")
    st.header('Configuracion del Documento ')
    document_title = st.text_input("Titulo del documento", "Titulo del documento")
    author = st.text_input("Autor del documento", "")
    uploaded_image = st.file_uploader("Cargar imagen", type=['jpg', 'png', 'jpeg', 'gif', 'svg'])

    st.header('Capitulos del documento')
    chapters = []
    num_chapters = st.number_input("Numero de capitulos", min_value=1, max_value=10, value=1)

    for i in range (num_chapters):
        st.subheader(f'Capitulo {i+1}')
        title = st.text_input(f'Titulo del capitulo {i+1}', f'Titulo del capitulo {i+1}')
        body = st.text_area(f'Cuerpo del capitulo {i+1}', f'Contenido del capitulo {i+1}')
        font = st.selectbox(f'Fuente del capitulo {i+1}', ['Times', 'Courier'])
        size = st.slider(f'Tamaño de fuente del capitulo {i+1}', 8, 24, 12)
        chapters.append((title, body, font, size))
    if st.button('Generar PDF'):
        image_path = uploaded_image.name if uploaded_image else None
        if image_path:
            with open(image_path, 'wb') as f:
                f.write(uploaded_image.getbuffer())

        create_pdf('historia.pdf', document_title, author, chapters, image_path)

        with open('historia.pdf', 'rb') as pdf_file:
            PDFByte = pdf_file.read()

        st.download_button(
            label='Descargar pdf'
            , data=PDFByte
            , file_name='historia.pdf'
            , mime='application/octet-stream'

        )

        st.success('Pdf generado exitosamente!!!')

if __name__ == "__main__":
    main()


