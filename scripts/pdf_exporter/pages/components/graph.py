from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import time


class Graph:
    def __init__(self, width, height, indicator_number, site_url):
        self._width = width
        self._height = height
        self._indicator_number = indicator_number
        self._site_url = site_url
        
    def get_graph_path(self) -> str | None:
        try:
            self._get_graph_element(self._indicator_number)
        except (TimeoutException, WebDriverException) as e:
            return None
        graph_path = self._get_path(self._indicator_number)
        return graph_path
    
    def _get_graph_element(self, indicator: str) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')

        # Start up the browser
        driver = webdriver.Chrome(options=options)

        # Load the HTML containing the canvas element
        driver.get(f"{self._site_url}/{indicator}/index.html")

        time.sleep(30)

        canvas = driver.find_element(By.ID, "selectionsChart")
        chart_screenshot = canvas.screenshot_as_png
        with open(f"charts/{indicator}.png", "wb") as f:
            f.write(chart_screenshot)
        return 
    
    def _get_path(self, indicator: str) -> str:
        image_path = f"charts/{indicator}.png"
        image = Image.open(image_path)
        cropped_image = ImageOps.crop(image, (0, 0, 0, 85))
        image.close()
        cropped_image.save(image_path)
        return image_path
    