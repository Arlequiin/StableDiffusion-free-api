from selenium import webdriver;from selenium.webdriver.chrome.options import Options;from selenium.webdriver.support.ui import WebDriverWait;from selenium.webdriver.support import expected_conditions as EC;from selenium.webdriver.common.by import By;import time;from flask import Flask, request, jsonify, render_template;from flask_cors import CORS;import os

app = Flask(__name__)
CORS(app)
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    driver = webdriver.Chrome(options=options)
    width = 553
    height = 795
    driver.set_window_size(width, height)
    url = os.getenv("MODEL")
    driver.get(url)
    prompt = request.form.get('prompt')
    print(prompt)

    search_input = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.NAME, 'prompt')))
    search_input.send_keys(prompt)
    search_input.submit()
    driver.execute_script("document.title = ''")
    time.sleep(4)
    images = driver.find_elements(By.CSS_SELECTOR, 'img')
    while len(images)==0:
      time.sleep(2)
      images = driver.find_elements(By.CSS_SELECTOR, 'img')
    image_sources = [image.get_attribute('src') for image in images[:8]]
    driver.quit()
    return jsonify(image_sources)

  return render_template('index.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
