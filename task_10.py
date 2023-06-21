import re

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    # wd = webdriver.Firefox()
    # wd = webdriver.Safari()
    wd.implicitly_wait(1)
    request.addfinalizer(wd.quit)
    return wd


def test_correct_page(driver):
    # main page
    driver.get("http://localhost/litecart/en/")

    box = driver.find_element(By.CSS_SELECTOR, "#box-campaigns > div > ul > li:first-child > a.link")
    main_text = box.find_element(By.CSS_SELECTOR, "div.name").text
    print(f"\nMain page:\ntext: {main_text}")

    regular_price = box.find_element(By.CSS_SELECTOR, "s.regular-price").text
    campaign_price = box.find_element(By.CSS_SELECTOR, "strong.campaign-price").text
    print(f"regular_price: {regular_price}\ncampaign_price: {campaign_price}")

    color_regular = box.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("color")
    r_g_b_regular = re.search(r'[rgba?]\((\d+),\s*(\d+),\s*(\d+)', color_regular).groups()
    strike_regular = box.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("text-decoration-line")
    print(f"color_regular: {color_regular}\nstrike_regular: {strike_regular}")

    weight_campaign = box.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-weight")
    color_campaign = box.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("color")
    print(f"weight_campaign: {weight_campaign}\ncolor_campaign: {color_campaign}")
    r_g_b_campaign = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color_campaign).groups()

    regular_font = box.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("font-size")
    campaign_font = box.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-size")
    print(f"regular_font: {regular_font}\ncampaign_font: {campaign_font}")

    # product page
    product_link = box.get_attribute("href")
    driver.get(product_link)
    box = driver.find_element(By.CSS_SELECTOR, "#box-product")

    product_text = box.find_element(By.CSS_SELECTOR, "h1.title").text
    print(f"\nProduct page:text: {product_text}")

    regular_price_pr = box.find_element(By.CSS_SELECTOR, "s.regular-price").text
    campaign_price_pr = box.find_element(By.CSS_SELECTOR, "strong.campaign-price").text
    print(f"regular_price_pr: {regular_price_pr}\ncampaign_price_pr: {campaign_price_pr}")

    color_regular_pr = box.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("color")
    r_g_b_reg_pr = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color_regular_pr).groups()
    strike_reg_pr = box.find_element(
        By.CSS_SELECTOR, "s.regular-price").value_of_css_property("text-decoration-line")
    print(f"color_regular_pr: {color_regular_pr}\nstrike_reg_pr: {strike_reg_pr}")

    weight_campaign_pr = box.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-weight")
    color_campaign_pr = box.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("color")
    print(f"weight_campaign_pr: {weight_campaign_pr}\ncolor_campaign_pr: {color_campaign_pr}")
    r_g_b_campaign_pr = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color_campaign_pr).groups()

    regular_font_pr = box.find_element(By.CSS_SELECTOR, "s.regular-price").value_of_css_property("font-size")
    campaign_font_pr = box.find_element(By.CSS_SELECTOR, "strong.campaign-price").value_of_css_property("font-size")
    print(f"regular_font_pr: {regular_font_pr}\ncampaign_font_pr: {campaign_font_pr}\n")

    # assertion section
    assert main_text == product_text, "The product title is different on the main page vs. the product one"

    assert regular_price == regular_price_pr, "The regular price is different on the main page vs. the product one"

    assert r_g_b_regular[0] == r_g_b_regular[1] == r_g_b_regular[2], "Main page: the regular price color is not grey"
    assert strike_regular == "line-through", "Main page: the regular price is not struck through on the Main page"
    assert r_g_b_reg_pr[0] == r_g_b_reg_pr[1] == r_g_b_reg_pr[2], "Product page: the regular price color is not grey"
    assert strike_reg_pr == "line-through", "Product page: the regular price is not struck through on the Main page"

    assert int(weight_campaign) >= 700, "Main page: the campaign price is not in bold"
    assert r_g_b_campaign[1] == r_g_b_campaign[2], "Main page: the campaign price color is not red"
    assert int(weight_campaign_pr) >= 700, "Product page: the campaign price is not in bold"
    assert r_g_b_campaign_pr[1] == r_g_b_campaign_pr[2], "Product page: the campaign price color is not red"

    assert float(regular_font.rstrip("px")) < float(campaign_font.rstrip("px")), \
        "Main page: the regular price is not smaller than the campaign one"
    assert float(regular_font_pr.rstrip("px")) < float(campaign_font_pr.rstrip("px")), \
        "Product page: the regular price is not smaller than the campaign one"
