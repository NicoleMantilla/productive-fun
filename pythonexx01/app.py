import streamlit as st 
from fpdf import FPDF
import unicodedata

def clean_text(text):
    return unicodedata.normalize('NFKD', text).encode('latin-1', 'ignore').decode('latin-1')



# Clase personalizada para generar PDFs
class PDF(FPDF):
	def __init__(self, font_name):
		super().__init__()
		self.font_name = font_name

	def  header(self):
		if hasattr(self, 'document_title'):
			self.set_font(self.font_name, 'B', size=14)
			self.cell(w=0, h=20, txt=self.document_title, border=0, ln=1, align='C')
	
	def footer(self):
		self.set_y(-15)
		self.set_font(self.font_name, '', size=max(8, self.title_font_size - 4))
		self.cell(w=0, h=10, txt=f'Página {self.page_no()}', border=0, ln=0, align='C')
	
	def chapter_title(self, title, font='Arial', size=12):
		self.set_font(self.font_name, 'B', size=size)
		self.cell(w=0, h=10, txt=title, border=0, ln=1, align='L')
		self.ln(10)

	def chapter_body(self, body, font='Arial', size=12):
		self.set_font(self.font_name, '', size=size)
		self.multi_cell(w=0, h=10, txt=body)
		self.ln()
		
# Función para crear el PDF	
def create_pdf(filename, document_title, title_font_size, author, chapters, font_name, image_path=None):
	pdf = PDF(font_name)
	pdf.document_title = document_title
	pdf.title_font_size = title_font_size 
	pdf.add_page()

	if author:
		pdf.set_author(author)
	
	if image_path:
		pdf.image(image_path, x=10, y=24, w=pdf.w - 20)
		pdf.ln(120)

	for chapter in chapters:
		title, body, size = chapter
		pdf.chapter_title(title, size)
		pdf.chapter_body(body, size)

	pdf.output(filename)

# Interfaz Streamlit
def main():
	st.title("📝 Generador de PDF con Python")
	st.header("Configuración del Documento")

	fuentes_estandar = ['Arial', 'Courier', 'Times']

	fuente_seleccionada = st.selectbox("Selecciona la fuente para todo el documento", fuentes_estandar)

	document_title = st.text_input("Título del Documento", "Escribe aquí el título")
	title_font_size = st.slider("Tamaño fuente del título", 8, 48, 18)
	author = st.text_input("Autor", "")

	uploaded_image = st.file_uploader("Sube imagen (opcional)", type=["jpg", "png"])

	st.header("📚 Capítulos del Documento")
	chapters = []
	chapter_count = st.number_input("Número de capítulos", min_value=1, max_value=100, value=1)

	for i in range(chapter_count):
		st.subheader(f"Capítulo {i + 1}")
		title = st.text_input(f"Título del Capítulo  {i + 1}", 
							  f"Escribe aquí el título del Capítulo {i + 1} ")
		body = st.text_area(f"Contenido del capítulo {i +1}",
					   		 f"Escribe aquí el contenido de tu capítulo {i +1}")		
		size = st.slider(f"Tamaño de Fuente del Capítulo {i +1}", 8, 24, 12)
		chapters.append((title, body, size))
	
	if st.button("📤 Generar PDF"):
		image_path = uploaded_image.name if uploaded_image else None
		if image_path:
			with open(image_path, "wb") as f:
				f.write(uploaded_image.getbuffer())
			
		create_pdf(filename= "guion.pdf", document_title= document_title, author=author, title_font_size= title_font_size,
			 chapters=chapters, image_path=image_path, font_name=fuente_seleccionada)
		
		with open("guion.pdf", "rb") as pdf_file:
			PDFbyte = pdf_file.read()

		st.download_button(
			label="Descargar PDF 📥",
			data=PDFbyte,
			file_name="guion.pdf",
			mime='application/octet-stream'
		)

		st.success("PDF generado exitosamente ✅")


if __name__ == "__main__":
	main()
