from .page import Page


class GoalPage(Page):
    def __init__(self, pdf, width, height, goal_number):
        super().__init__(pdf, width, height)
        self._goal_number = goal_number

    def export(self, goal_meta: dict):
        self._add_header()
        global_analysis: str = goal_meta.get("page_content", self._get_random_text())
        global_analysis = self._get_random_text() if global_analysis == "" else global_analysis
        self._add_global_analysis(global_analysis)
        return

    def _add_header(self):
        self._add_goal_image(self._goal_number)
        title: str = f"Objectif {self._goal_number}"
        self._add_title(title)
        self._add_line()
        return
    
    def _add_global_analysis(self, global_analysis: str) -> None:
        self._pdf.setFont(self._font, self._font_size)
        y_position = self._text_section_y_position
        self._add_column_text(global_analysis, self._margin, y_position, 1)
        return