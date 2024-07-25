from langchain.document_loaders import PyPDFLoader
from loguru import logger
from fpdf import FPDF

class CreatePDF(FPDF):
    def header(self):
        # Select Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Framed title
        self.cell(30, 10, 'Summary', 1, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')


class PDFHandler:
    logger.info("Iniciando PDF Handler")

    def read_pdf(self, file_path) -> list:
        """Realiza a leitura do PDF passado na inicializacao da classe

        Returns:
            list: Lista de objetos "Page" do documento
        """
        logger.info(f"Leitura do PDF: {file_path}")

        return PyPDFLoader(file_path).load_and_split()


    def create_pdf(self, text, output_path):
        """Realiza a criacao de um documento PDF

        Args:
            text (str): Texto do documento
            output_path (str): caminho de criacao do documento
        """
        logger.info(f"Criando PDF em: {output_path}")

        new_pdf = CreatePDF()
        new_pdf.add_page()
        new_pdf.set_font("Arial", size=12)

        new_pdf.multi_cell(0, 10, text)

        new_pdf.output(output_path)
