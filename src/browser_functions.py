import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from src.chess_functions import chess_notation_to_pixel
from src.js_scripts import generate_arrow_script, remove_arrow_script

def iniate_browser(chrome_dir):
    '''
    Iniate Browser
    '''
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("detach", True)
    if os.name == "nt":
        print("OS is windows")
        if chrome_dir:
            options.add_argument(f"user-data-dir={chrome_dir}") #Path to your chrome profile
        driver = webdriver.Chrome(options=options)
    else:
        print("Only windows is supported, exiting.")
        return False
    # Go to website
    driver.get("https://lichess.org/")
    return driver

def locate_and_click_element(driver, xpath:str):
    """
    Locate an element by XPath and perform a click using pyautogui.
    """
    try:
        # Locate element
        element = driver.find_element(By.XPATH, xpath)
        # print(f"Element located: {xpath}")
        action = ActionChains(driver)
        action.move_to_element(element).click().perform()
        return

    except Exception as e:
        print(f"Error locating or clicking element: {xpath}, Error: {e}")


def move_to_coordinates_and_click(driver, move:str, width:int, height:int, areBlack:bool):
    """
    Convert a move like 'h4h6' to pixels and click the relevant squares.
    """
    start_x, start_y, end_x, end_y = chess_notation_to_pixel(move, width, height, areBlack)

    # Generate XPath for start and end positions
    start_xpath = f"//*[contains(@style, 'transform: translate({start_x}px, {start_y}px)')]"
    end_xpath = f"//*[contains(@style, 'transform: translate({end_x}px, {end_y}px)')]"

    try:
        # Locate and click the start square
        element = driver.find_element(By.XPATH, start_xpath)
        action = ActionChains(driver)
        action.move_to_element(element).click().perform()

        # Locate and click the destination square
        driver.find_element(By.XPATH, end_xpath).click()

        # print(f"Moved piece from {move[:2]} to {move[2:]}")
    except Exception as e:
        print(f"Error with move {move}: {e}")

def draw_arrow(driver, width:str, height:str, move:str, areBlack):
    # Remove old arrow if exists
    elm = driver.find_elements(By.CLASS_NAME, "cg-shapes")
    if elm:
        script = remove_arrow_script(width, height, str(move))
        driver.execute_script(script, elm)
    # Draw arrow
    script = generate_arrow_script(width, height, str(move), areBlack)
    driver.execute_script(script, elm)