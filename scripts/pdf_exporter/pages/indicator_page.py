from .page import Page
from .components.graph import Graph

class IndicatorPage(Page):
    def __init__(self, pdf, width, height, goal_number, indicator_number, indicator_name, quebec_issue, target, site_url):
        super(IndicatorPage, self).__init__(pdf, width, height)
        self._goal_number = goal_number
        self._indicator_number = indicator_number
        self._indicator_name = indicator_name
        self._quebec_issue = quebec_issue
        self._target = target
        self._site_url = site_url
        self._additional_page = False

    def export(self, indicator_meta: dict):
        self._add_header()
        self._add_data(self._indicator_number)
        x_position_text, y_position_text = self._set_initial_text_position()
        analysis = indicator_meta.get("analysis", self._get_random_text())
        x_position_text, y_position_text = self._add_section("Analyse", analysis, x_position_text, y_position_text)

        challenges = indicator_meta.get("community", self._get_random_text())
        x_position_text, y_position_text = self._add_section("Défis", challenges, x_position_text, y_position_text)

        initiatives = indicator_meta.get("initiatives", self._get_random_text())
        x_position_text, y_position_text = self._add_section("Initiatives", initiatives, x_position_text, y_position_text)
        return
        
    def _add_header(self):
        self._add_goal_image(self._goal_number)
        self._add_quebec_issue(self._quebec_issue)
        self._add_target(self._target)
        self._add_title(self._indicator_name)
        self._add_line()
        return
    
    def _add_quebec_issue(self, quebec_issue):
        distance_to_goal_image = 20
        position_x = self._margin + self._goal_image_size + distance_to_goal_image
        position_y = self._page_height - self._margin - self._title_font_size
        self._pdf.setFont(self._font, self._title_font_size)
        self._pdf.drawString(position_x, position_y, quebec_issue)
        return
    
    def _add_target(self, target: str) -> None:
        distance_to_goal_image = 20
        position_x = self._margin + self._goal_image_size + distance_to_goal_image
        position_y = self._page_height - self._margin - self._goal_image_size/2
        self._pdf.setFont(self._title_font, self._subtitle_font_size)
        self._pdf.drawString(position_x, position_y, target)
        return
    
    def _add_data(self, indicator):
        print("Waiting for graph to be generated...")
        graph = Graph(self._graph_width, self._graph_height, indicator, self._site_url)
        graph_path:str = graph.get_graph_path()
        if not graph_path:
            self._pdf.setFont(self._title_font, 16)
            self._pdf.drawString(self._margin, self._text_section_y_position, "Pas de graphique disponible")
            print("No graph available")
        else:
            y_position = self._text_section_y_position - self._graph_height
            self._pdf.drawImage(graph_path, self._margin, y_position, width=self._graph_width, height=self._graph_height, preserveAspectRatio=True)
            print("graph added")
        return
    
    def _set_initial_text_position(self):
        distance_to_graph: int = (self._graph_height % self._font_size) + self._font_size*2
        x_position: int = self._margin
        y_position: int = self._text_section_y_position - self._graph_height - distance_to_graph
        return x_position, y_position
    
    def _add_section(self, title, text, x_position, y_position):
        text = f"{title}:\n\n{text}\n\n"
        self._pdf.setFont(self._font, self._font_size)
        y_position = 0 if y_position < self._margin + self._font_size*5 else y_position
        x_position, y_position = self._adjust_column_position(x_position, y_position)
        x_position, y_position = self._add_column_text(text, x_position, y_position)
        return x_position, y_position
