from .page import Page
from reportlab.lib.utils import ImageReader 


class FirstPage(Page):
    def __init__(self, pdf, width, height, municipalité: str, site_url: str):
        super().__init__(pdf, width, height)
        self._municipalité = municipalité
        self._site_url = site_url
    
    def export(self):
        self._pdf.setFont(self._title_font, self._first_title_font_size)
        title: str = f"Examen local volontaire partiel: {self._municipalité}"
        title_width = self._pdf.stringWidth(title, self._title_font, self._first_title_font_size)
        self._pdf.drawString(self._page_width/2 - title_width/2, self._page_height/2, title)
        self._add_logo()
        self._pdf.setFont(self._font, self._font_size)
        text: str = "Ce document est un export de données du portail des indicateurs de développement durable du Québec."
        text_width = self._pdf.stringWidth(text, self._font, self._font_size)
        self._pdf.drawString(self._page_width/2 - text_width/2, self._page_height/2 - self._title_font_size*1.2, text)
        text: str = "Il a été généré automatiquement à partir des données disponibles sur le site."
        text_width = self._pdf.stringWidth(text, self._font, self._font_size)
        self._pdf.drawString(self._page_width/2 - text_width/2, self._page_height/2 - self._title_font_size*1.2*2, text)
        self._pdf.showPage()
        return

    def _add_logo(self):
        logo = ImageReader(f"{self._site_url}/assets/img/SDG_logo.png")
        position_bottom_left_x = int(self._page_width/2 - self._logo_size/2)
        position_bottom_left_y = self._page_height - self._margin - self._logo_size
        self._pdf.drawImage(logo, x=position_bottom_left_x, y=position_bottom_left_y, width=self._logo_size, height=self._logo_size, preserveAspectRatio=True)
        self._pdf.setFont(self._title_font, self._title_font_size)
        temp_text: str = "IMAGE PERSONNALISÉE DE LA MUNICIPALITÉ"
        temp_text_width = self._pdf.stringWidth(temp_text, self._title_font, self._title_font_size)
        self._pdf.drawString(self._page_width/2 - temp_text_width/2, position_bottom_left_y + self._logo_size/2, temp_text)
        return
    
    def _add_header(self):
        return