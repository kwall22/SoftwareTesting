from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@given('I navigate to "{url}"')
def step_navigate_to_url(context, url):
    context.browser.get(url)

@when('I am on the main Washington County branch page')
def step_check_main_branch_page(context):
    expected_url = "https://library.washco.utah.gov/"
    actual_url = context.browser.current_url
    assert actual_url == expected_url

@then('I should see the address')
def step_verify_address(context):
    expected_address = "88 West 100 South"
    address_element = context.browser.find_element(By.CSS_SELECTOR, "#second .textwidget")
    actual_address = address_element.text.strip()
    assert expected_address in actual_address

@when('I navigate to the St. George branch')
def step_navigate_to_st_george(context):
    branch_menu_item = context.browser.find_element(By.ID, "menu-item-1380")
    actions = ActionChains(context.browser)
    actions.move_to_element(branch_menu_item).perform()

    st_george_link = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1387"))
    )
    st_george_link.click()

@then('I should see the branch manager')
def step_verify_branch_manager(context):
    expected_manager = "Alan Anderson"
    manager_element = context.browser.find_element(By.XPATH, "//article[@id='post-4']//strong")
    actual_manager = manager_element.text.strip()
    assert actual_manager == expected_manager

@when('I click on the "Renew/Pay Fines" tab')
def step_click_pay_fines_tab(context):
    renew_tab = context.browser.find_element(By.LINK_TEXT, "Renew/Pay Fines")
    renew_tab.click()

@then('I should see a login page')
def step_see_login_page(context):
    login_div = context.browser.find_element(By.XPATH, '/html/body/div/div[2]')
    assert login_div.is_displayed()

@when('I click on the Library Programs link in the Book A Room drop down menu')
def step_click_on_lib_program(context):
    book_a_room_tab = context.browser.find_element(By.ID, "menu-item-1496")
    ActionChains(context.browser).move_to_element(book_a_room_tab).perform()
    library_programs_link = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1497"))
    )
    library_programs_link.click()

@then('I should be on the book a room page')
def step_verify_room_page(context):
    context.browser.switch_to.window(context.browser.window_handles[-1])
    current_url = context.browser.current_url
    expected_url = "https://washco.libcal.com/"
    assert expected_url == current_url

@when('I click on the Monthly Newsletters link in the Whats New drop down menu')
def step_click_on_newsletters_page(context):
    whats_new_tab = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1383"))
    )
    ActionChains(context.browser).move_to_element(whats_new_tab).perform()
    monthly_newsletter_link = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1535"))
    )
    monthly_newsletter_link.click()

@then('I should see the newsletters headline')
def step_verify_newsletter_headline(context):
    header_element = WebDriverWait(context.browser, 35).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='main']/header/h1/span"))
    )
    header_text = header_element.text
    assert header_text == "Newsletters"

@when('I click on the Search The Online Catalog link in the Catalog drop down menu')
def step_click_on_catalog_page(context):
    catalog_tab = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1381"))
    )
    ActionChains(context.browser).move_to_element(catalog_tab).perform()
    online_catalog_link = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1396"))
    )
    online_catalog_link.click()

@then('I should be on the online catalog page')
def step_verify_online_catalog_page(context):
    current_url = context.browser.current_url
    expected_url = "https://catalog.library.washco.utah.gov/"
    assert expected_url in current_url

@when('I search the catalog for Twilight')
def step_search_catalog_for_twilight(context):
    search_form = WebDriverWait(context.browser, 35).until(
        EC.presence_of_element_located((By.ID, "searchForm"))
    )
    search_input = search_form.find_element(By.ID, "q")
    search_input.clear()
    search_input.send_keys("Twilight")
    search_form.submit()
@then('Twilight should be in the search results')
def step_find_twilight_in_results(context):
    search_results = WebDriverWait(context.browser, 35).until(
        EC.presence_of_element_located((By.ID, "detailLink2"))
    )
    result_title = search_results.get_attribute("title")
    assert result_title == "Twilight"

@when('I click on the Mission & History link in the More drop down menu')
def step_click_on_mission_page(context):
    more_tab = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1386"))
    )
    ActionChains(context.browser).move_to_element(more_tab).perform()
    mission_page_link = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1465"))
    )
    mission_page_link.click()

@then('I should see the Mission & History header')
def step_verify_mission_header(context):
    header_element = WebDriverWait(context.browser, 35).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="post-1330"]/div/header/h1'))
    )
    header_text = header_element.text
    assert header_text == "Mission & History"

@when('I click the Page Turners Club link in the Saint George Community drop down menu')
def step_click_book_club_link(context):
    community_tab = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1384"))
    )
    ActionChains(context.browser).move_to_element(community_tab).perform()
    saint_george_tab = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1426"))
    )
    ActionChains(context.browser).move_to_element(saint_george_tab).perform()
    book_club_link = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1437"))
    )
    book_club_link.click()

@then('I should see the book club page header')
def step_verify_book_club_header(context):
    header_element = WebDriverWait(context.browser, 35).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="post-125"]/div/header/h1'))
    )
    header_text = header_element.text
    assert header_text == "Page Turners Book Club"

@when('I click the Board of Directors link in the More drop down menu')
def step_click_directors_link(context):
    more_tab = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1386"))
    )
    ActionChains(context.browser).move_to_element(more_tab).perform()
    directors_page_link = WebDriverWait(context.browser, 35).until(
        EC.element_to_be_clickable((By.ID, "menu-item-1466"))
    )
    directors_page_link.click()

@then('I should see the contact information for the board of directors')
def step_find_directors_contact_information(context):
    p_element = WebDriverWait(context.browser, 35).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="post-18"]/div/div/p[2]/strong'))
    )
    p_text = p_element.text
    assert p_text == "Contact Information:"

def after_scenario(context, scenario):
    context.browser.quit()