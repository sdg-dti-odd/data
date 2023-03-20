import os
import json
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdf_exporter.pages.indicator_page import IndicatorPage
from pdf_exporter.pages.goal_page import GoalPage
from pdf_exporter.pages.first_page import FirstPage

class ExportPdf:

    def __init__(self, directory, file_name, site_url, municipalité):
        self.__directory = directory
        self.__file_name = file_name
        self.__site_url = site_url
        self.__municipalité = municipalité
        self.__export_file_path = f"{self.__directory}/{self.__file_name}"
        self.__pdf = canvas.Canvas(self.__export_file_path, pagesize=letter)
        self.__page_width, self.__page_height = letter

    def export_pdf(self):
        try:
            os.mkdir('charts')
        except FileExistsError:
            shutil.rmtree('charts')
            os.mkdir('charts')
        indicators= self.__get_all_indicators()
        indicators_by_goal: dict[str, list[str]] = self.__sort_indicators_by_goal(indicators)
        
        first_page = FirstPage(self.__pdf, self.__page_width, self.__page_height, self.__municipalité, self.__site_url)
        first_page.export()

        for goal_number, indicators in indicators_by_goal.items():
            try:
                goal_meta = json.load(open(f"{self.__directory}/meta/{goal_number}-a-1.json"))
            except FileNotFoundError:
                goal_meta = {}
            goal_page = GoalPage(self.__pdf, self.__page_width, self.__page_height, goal_number)
            goal_page.export(goal_meta)
            self.__pdf.showPage()
            self.__add_indicators(indicators, goal_number)

        self.__pdf.save()
        print(f"PDF exported to {self.__export_file_path}")
        shutil.rmtree('charts')
        return
        
    def __get_all_indicators(self):
        data_folder = "%s/%s" % (self.__directory, "data")
        all_data_file_names = os.listdir(data_folder)
        indicators = []
        for file_name in all_data_file_names:
            if self.__file_is_suitable(file_name):
                if "a" in file_name or "b" in file_name:
                    continue
                indicators.append(file_name.replace(".json", ""))
        sorted_indicators = sorted(indicators, key=lambda x: tuple(map(int, x.split('-'))))
        return sorted_indicators
    
    def __file_is_suitable(self, file_name):
        return self.__file_is_json(file_name) and self.__indicator_is_complete(file_name)
    
    def __file_is_json(self, file_name):
        return file_name.endswith(".json")
    
    def __indicator_is_complete(self, file_name):
        file_path = "%s/data/%s" % (self.__directory, file_name)
        json_file = open(file_path)
        indicator_data = json.load(json_file)
        return indicator_data != []
    
    def __sort_indicators_by_goal(self, indicators):
        indicators_by_goal = {}
        for indicator in indicators:
            goal_number = indicator.split('-')[0]
            if goal_number not in indicators_by_goal:
                indicators_by_goal[goal_number] = []
            indicators_by_goal[goal_number].append(indicator)
        return indicators_by_goal
    
    def __add_indicators(self, indicators: list[str], goal_number: str) -> None:
        for indicator in indicators:
            print(f"Processing {indicator}...")
            meta: dict = json.load(open(f"{self.__directory}/meta/{indicator}.json"))

            indicator_name = meta["indicator_name"]
            quebec_issue = meta.get("quebec_issue", "ENJEU QUÉBÉCOIS À DÉFINIR")
            target = meta.get("target_name", "Cible à définir")

            indicator_page = IndicatorPage(self.__pdf, self.__page_width, self.__page_height, goal_number, indicator, indicator_name, quebec_issue, target, self.__site_url)
            indicator_page.export(meta)

            self.__pdf.showPage()
