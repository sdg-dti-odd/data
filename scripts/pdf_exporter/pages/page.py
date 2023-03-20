import textwrap
from lorem_text import lorem
import random
from reportlab.lib.utils import ImageReader
from abc import ABC, abstractmethod
from reportlab.pdfbase import pdfmetrics


class Page(ABC):
    def __init__(self, pdf, width, height):
        self._pdf = pdf
        self._page_width = width
        self._page_height = height
        self._title_font = "Times-Bold"
        self._title_font_size = 14
        self._subtitle_font_size = 12
        self._first_title_font_size = 24
        self._font = "Times-Roman"
        self._font_size = 10
        self._margin_inch = 1
        self._margin = self._margin_inch * 72
        self._column_number = 3
        self._column_width = (self._page_width - (self._margin * 2)) / self._column_number
        self._column_margin = 10
        self._goal_image_size = 80
        self._logo_size = 400
        self._text_section_y_position = self._page_height - self._margin - self._goal_image_size - 50
        self._graph_width = self._column_width * 2 - self._column_margin
        self._graph_height = self._graph_width * 0.875

    def _add_column_text(self, text, x_position, y_position, column_number = None) -> tuple[int, int]:
        text_width_in_points = self._pdf.stringWidth(text, self._font, self._font_size)
        if text_width_in_points == 0:
            return x_position, y_position
        
        text_width: int = (self._page_width - (self._margin * 2)) 
        column_width = self._column_width if column_number is None else text_width / column_number
        
        line_width_in_points = column_width - self._column_margin*2
        line_width_in_caracters = int(line_width_in_points/text_width_in_points * len(text))
        lines = text.split("\n")

        for line in lines:  
            wrapped_text = " " if len(line)==0 else textwrap.wrap(line, width=line_width_in_caracters, replace_whitespace=False)
            for wrapped_line in wrapped_text:
                self._pdf.drawString(x_position, y_position, wrapped_line)
                y_position -= self._font_size
                x_position, y_position = self._adjust_column_position(x_position, y_position, column_width)

        return x_position, y_position
    
    def _adjust_column_position(self, x_position, y_position, column_width = None) -> tuple[int, int]:
        column_width = self._column_width if column_width is None else column_width
        distance_to_graph = (self._graph_height % self._font_size) + self._font_size*2
        if x_position == self._margin and y_position <= self._margin:
            x_position = self._margin + column_width
            y_position = self._text_section_y_position - self._graph_height - distance_to_graph if not self._additional_page else self._text_section_y_position
        elif x_position == self._margin + column_width and y_position <= self._margin:
            x_position = self._margin + self._column_width*2
            y_position = self._text_section_y_position 
        elif x_position == self._margin + column_width*2 and y_position <= self._margin:
            x_position = self._margin
            y_position = self._text_section_y_position
            self._pdf.showPage()
            self._add_header()
            self._pdf.setFont(self._font, self._font_size)
            self._additional_page = True
        return x_position, y_position
    
    def _get_random_text(self):
        words_number = random.randint(50, 300)
        return lorem.words(words_number)
    
    def _add_goal_image(self, goal_number):
        goal_image = ImageReader(f"https://open-sdg.org/sdg-translations/assets/img/goals/fr/{goal_number}.png")
        position_bottom_left_y = self._page_height - self._margin - self._goal_image_size
        self._pdf.drawImage(goal_image, x=self._margin, y=position_bottom_left_y, width=self._goal_image_size, height=self._goal_image_size, preserveAspectRatio=True)
        return
    
    def _add_title(self, title):
        distance_to_goal_image = 20
        position_x = self._margin + self._goal_image_size + distance_to_goal_image
        position_y = self._page_height - self._margin - self._goal_image_size/2 - self._subtitle_font_size*1.2

        max_line_width_in_points = self._page_width - position_x - self._margin
        title_width_in_points = pdfmetrics.stringWidth(title, self._font, self._subtitle_font_size)
        line_width_in_caracters = int(max_line_width_in_points/title_width_in_points * len(title))
        title = textwrap.wrap(title, width=line_width_in_caracters)
        
        writter = self._pdf.beginText(position_x, position_y)
        writter.setFont(self._font, self._subtitle_font_size)
        writter.textLines(title)
        self._pdf.drawText(writter)
    
    def _add_line(self):
        line_width = 0.5
        self._pdf.setLineWidth(line_width)
        distance_to_header = 20
        x1 = self._margin
        x2 = self._page_width - self._margin
        y = self._page_height - self._margin - self._goal_image_size - distance_to_header
        self._pdf.line(x1, y, x2, y)
        return
    
    @abstractmethod
    def _add_header(self):
        pass
