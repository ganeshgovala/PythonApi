from flask import Flask, jsonify, request #type: ignore
from flask_cors import CORS # type: ignore
import os

from selenium import webdriver #type: ignore
from selenium.webdriver.chrome.service import Service #type: ignore
from selenium.webdriver.support.ui import WebDriverWait #type: ignore
from selenium.webdriver.support import expected_conditions as EC #type: ignore
from selenium.webdriver.common.by import By #type: ignore
from selenium.webdriver.support.ui import Select #type: ignore
from selenium.webdriver.chrome.options import Options #type: ignore
from datetime import datetime
import time


app = Flask(__name__)
CORS(app)

def openWebsite() :
    path = 'C:\\Users\\srira\\Downloads\\chromedriver-2\\chromedriver-win64\\chromedriver.exe'
    website = 'https://vishnu.ac.in/Default.aspx?ReturnUrl=%2f'
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service = service)
    driver.get(website)
    return driver

def login(driver, username, password) :
    wait = WebDriverWait(driver, 10)
    input_field = wait.until(EC.visibility_of_element_located((By.ID, 'txtId2')))
    password_field = wait.until(EC.visibility_of_element_located((By.ID, 'txtPwd2')))
    login_btn = wait.until(EC.visibility_of_element_located((By.ID, 'imgBtn2')))
    input_field.send_keys(username)
    password_field.send_keys(password)
    login_btn.click()
    return wait


@app.route('/thisMonthSubWise', methods=['POST'])
def this_month_subwise() :
    driver = openWebsite()
    data = request.json
    username = data.get('username')
    password = data.get('password')
    wait = login(driver, username, password)

    print("login done")

    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    attendance_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@href="Academics/StudentAttendance.aspx?showtype=SA"]')))
    attendance_btn.click()

    iframe = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe')))
    driver.switch_to.frame(iframe)

    this_month_btn = wait.until(EC.visibility_of_element_located((By.ID, 'radMonthly')))
    this_month_btn.click()

    current_time = datetime.now()
    current_month = current_time.month
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    month = months[current_month - 1]
    year = current_time.year

    month_drop_down_element = driver.find_element(By.ID, 'ctl00_CapPlaceHolder_ddlMonth')
    month_drop_down = Select(month_drop_down_element)
    month_drop_down.select_by_visible_text(month)

    year_drop_down_element = driver.find_element(By.ID, 'ctl00_CapPlaceHolder_ddlYear')
    year_drop_down = Select(year_drop_down_element)
    year_drop_down.select_by_visible_text(str(year))

    show_btn = wait.until(EC.visibility_of_element_located((By.ID, 'btnShow')))
    show_btn.click()

    table_rows = driver.find_elements(By.CLASS_NAME, 'reportData1')
    changed_arr = table_rows[1:]
    data = []
    for i in changed_arr :
        arr = i
        li = arr.text.split(" ")
        data.append(li[1:])

    for i in data :
        if len(i) == 5 :
            i[0] = i[0]+i[1]
            i.remove("LAB")
    return data


@app.route('/tillNowSubWise', methods=['POST'])
def sub_wise_till_now() :
    driver = openWebsite()
    data = request.json
    username = data.get('username')
    password = data.get('password')
    wait = login(driver, username, password)

    print("login done")

    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    attendance_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@href="Academics/StudentAttendance.aspx?showtype=SA"]')))
    attendance_btn.click()

    iframe = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe')))
    driver.switch_to.frame(iframe)

    tillNow_btn = wait.until(EC.visibility_of_element_located((By.ID, 'radTillNow')))
    tillNow_btn.click()

    show_btn = wait.until(EC.visibility_of_element_located((By.ID, 'btnShow')))
    show_btn.click()

    table_rows = driver.find_elements(By.CLASS_NAME, 'reportData1')
    changed_arr = table_rows[1:]
    data = []
    for i in changed_arr :
        arr = i
        li = arr.text.split(" ")
        data.append(li[1:])

    for i in data :
        if len(i) == 5 :
            i[0] = i[0] + i[1]
            i.remove("LAB")
    return data


@app.route('/updateData', methods=['POST'])
def updateData() :
    driver = openWebsite()
    data = request.json
    username = data.get('username')
    password = data.get('password')
    wait = login(driver, username, password)

    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    return common(wait, driver)


@app.route('/getAttendance', methods=['POST'])
def getAttendanceTillNow() :
    driver = openWebsite()
    data = request.json
    username = data.get('username')
    password = data.get('password')
    wait = login(driver, username, password)
    time.sleep(3)

    try :
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        dashboard = wait.until(EC.visibility_of_element_located((By.ID, 'imgHead')))
        return common(wait, driver)
    except :
        try :
            error = EC.visibility_of_element_located((By.ID, 'lblError1'))
            print("Invalid Email");
            return jsonify(message = "Invalid")
        except :
            return jsonify(message = "Error")

def common(wait, driver) :
    print("Called")
    username_element = wait.until(EC.visibility_of_element_located((By.ID, 'lblUser')))
    username = username_element.text

    attendance_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@href="Academics/StudentAttendance.aspx?showtype=SA"]')))
    attendance_btn.click()

    iframe = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe')))
    driver.switch_to.frame(iframe)

    tillNow_btn = wait.until(EC.visibility_of_element_located((By.ID, 'radTillNow')))
    tillNow_btn.click()

    show_btn = wait.until(EC.visibility_of_element_located((By.ID, 'btnShow')))
    show_btn.click()

    till_now_table_rows = driver.find_elements(By.CLASS_NAME, 'reportHeading2WithBackground')
    till_now_data = till_now_table_rows[1].text.split(' ')

    this_month_btn = wait.until(EC.visibility_of_element_located((By.ID, 'radMonthly')))
    this_month_btn.click()

    current_time = datetime.now()
    current_month = current_time.month
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    month = months[current_month - 1]
    year = current_time.year

    month_drop_down_element = driver.find_element(By.ID, 'ctl00_CapPlaceHolder_ddlMonth')
    month_drop_down = Select(month_drop_down_element)
    month_drop_down.select_by_visible_text(month)

    year_drop_down_element = driver.find_element(By.ID, 'ctl00_CapPlaceHolder_ddlYear')
    year_drop_down = Select(year_drop_down_element)
    year_drop_down.select_by_visible_text(str(year))

    show_btn = wait.until(EC.visibility_of_element_located((By.ID, 'btnShow')))
    show_btn.click()

    this_month_table_rows = driver.find_elements(By.CLASS_NAME, 'reportHeading2WithBackground')
    this_month_data = this_month_table_rows[1].text.split(' ')

    driver.quit()
    result = {
        "name" : username[5:],
        "till_now" : str(till_now_data[3]),
        "till_now_attended" : str(till_now_data[2]) + " / " + str(till_now_data[1]),
        "this_month" : str(this_month_data[3]),
        "this_month_attended" : str(this_month_data[2]) + " / " + str(this_month_data[1])
    }
    return jsonify(message = result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))