from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import yagmail
import os
import sys
from twilio.rest import Client
from enum import Enum
import logging
from fake_useragent import UserAgent

BASEDIR = "/app"
logging.basicConfig(filename=f'{BASEDIR}/logs/log', level=logging.ERROR, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Outcome(Enum):
    NO_CRUISES = 0
    PRICE_EXCEEDS_MAX = 1
    GOOD_PRICE = 2
    DIDNT_WORK = 3
    DENIED_ACCESS = 4

def price_to_int(display_price):
    """
    Take display price of cruise and convert to int
    """
    price = display_price.replace("$", "").replace(",", "")
    return int(price)

def log_relevant_text(soup):
    logger.info(soup.body.text)
    return

def check_available_cruises(max_price):
    start_date = "2023-02-11"
    end_date = "2023-02-14"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-div-shm-usage')
    ua = UserAgent()
    options.add_argument(f'user-agent="{ua.random}"')
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.maximize_window()
    url = f"https://www.royalcaribbean.com/cruises?search=ship:WN|startDate:{start_date}~{end_date}"
    
    MAX_RETRIES = 5
    for i in range(MAX_RETRIES):
        try:
            driver.get(url)
            break
        except WebDriverException:
            pass
    if i >= MAX_RETRIES - 1:
        return Outcome.DIDNT_WORK, 0

    soup = BeautifulSoup(driver.page_source, "html.parser")
    cruise_results = soup.find(id="cruise-results-wrapper")
    log_relevant_text(soup)
    driver.quit()

    try:
        cruises = cruise_results.children
    except AttributeError:
        return Outcome.DENIED_ACCESS, 0

    if len(list(cruises)) == 0:
        return Outcome.NO_CRUISES, 0
    
    display_price = cruise_results.find("h2", class_="label-price")
    if display_price is None:
        return Outcome.NO_CRUISES, 0

    display_price = display_price.text
    price = price_to_int(display_price)
    if price > max_price:
        return Outcome.PRICE_EXCEEDS_MAX, price
    else:
        return Outcome.GOOD_PRICE, price

#SET ALL ENVS
# set -o allexport && source .env && set +o allexport
#SOURCE: https://stackoverflow.com/a/30969768
def send_mail(recipient, subject, message):
    sender = os.environ["SENDER_EMAIL"]
    app_password = os.environ["APP_PASSWORD"]

    yag = yagmail.SMTP(sender, app_password)
    yag.send(recipient, subject=subject, contents=message)

def send_text(recipient, message):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    sender = os.environ["SENDER_PHONE"]
    message = client.messages \
                    .create(
                        body=message,
                        from_=sender,
                        to=recipient
                    )

def first_element_meeting_condition(l, test):
    for i, element in enumerate(l):
        if test(element):
            return i

def update_environment_variables_file(key, value):
    with open(f"{BASEDIR}/.env") as f:
        lines = f.readlines()

    index_to_delete = first_element_meeting_condition(lines, lambda line: line.startswith(key))
    if index_to_delete is not None:
        del lines[index_to_delete]
    new_line = f"{key}={value}\n"
    lines.append(new_line)

    with open(f"{BASEDIR}/.env", "w") as f:
        for line in lines:
            f.write(line)

if __name__ == "__main__":
    emails = []
    phones = []
    max_price = int(os.environ["MAX_PRICE"])
    should_send = False
    for arg in sys.argv:
        if arg.startswith("email="):
            emails = arg.replace("email=", "").split(",")
        elif arg.startswith("phone="):
            phones = arg.replace("phone=", "").split(",")
        elif arg.startswith("max="):
            max_price = int(arg.replace("max=", ""))
        elif arg.startswith("should_send="):
            send = arg.replace("should_send=", "").lower()
            if send == "true":
                should_send = True

    logger.info("start job: emails: %s, phones: %s, max: %s, should_send: %s", emails, phones, max_price, should_send)

    outcome, price = check_available_cruises(max_price)
    if outcome == Outcome.GOOD_PRICE:
        update_environment_variables_file("MAX_PRICE", price)
        message = f"There is a spot available for ${price}."
        for email in emails:
            send_mail(email, subject="Spot available on cruise", message=message)
        for phone in phones:
            send_text(phone, message)
    elif should_send:
        send_mail(recipient=os.environ["SENDER_EMAIL"], subject="Update", message=f"{outcome}, {price}")
    
    logger.info("%s, PRICE: %d", outcome, price)
