import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import facebook
from monsterapi import client
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.chrome.options import Options
import requests
import os
import chromedriver_autoinstaller



def install_ff():
    os.system('sbase install geckobrowser')
    os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/browsers/geckobrowser /home/appuser/venv/bin/geckobrowser')

install_ff()


if 'button1_clicked' not in st.session_state:
    st.session_state.button1_clicked = False

if 'button2_clicked' not in st.session_state:
    st.session_state.button2_clicked = False

if 'show_number1' not in st.session_state:
    st.session_state.show_number1 = 0
if 'selected_image_index' not in st.session_state:
    st.session_state.selected_image_index = 0

if 'selected_image_url' not in st.session_state:
    st.session_state.selected_image_url = ""


def main_page():
    st.title("Welcome To Dashboard")


#facebook login automation
def user_login_facebook(username, password):
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    #prefs = {"profile.default_content_setting_values.notifications": 2}
    #chrome_options.add_experimental_option("prefs", prefs)

    # chrome driver
    
    #chrome_driver_path = 'C:\\Users\\srija\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'
    #service = Service(chrome_driver_path)
    #service = Service()
    #browser = webdriver.Chrome(service=service, options=chrome_options)
    #browser = webdriver.Chrome()


    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)


    browser.get("http://www.facebook.com")
    #browser.maximize_window()
    username_elem = browser.find_element(By.ID, "email")
    password_elem = browser.find_element(By.ID, "pass")
    button = browser.find_element(By.CSS_SELECTOR, 'button[data-testid="royal_login_button"]')
    username_elem.send_keys(username)
    password_elem.send_keys(password)
    button.click()
    st.success("Login successful!")
    #input_text=st.text_input("Enter content key words ")




#user login function frontend
# user login function frontend
def user_login():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    run_button_clicked = st.checkbox("Login")
    if run_button_clicked:
        if username and password:
            st.info("Logging in...")
            user_login_facebook(username, password)
        else:
            st.warning("Please enter both username and password.")

    input_text = st.text_input("Enter content key words ")
    run_button_clicked = st.checkbox("Run button")

    if run_button_clicked:
        st.text("Generating images")

        api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZkN2M2ZGI3NWUxZTRjODViYTg0NzdiNWYzMWU4MTM2IiwiY3JlYXRlZF9hdCI6IjIwMjMtMTItMTNUMTQ6NTQ6MTYuMDM0Mzc3In0.mE2K3F3RlvaQD4PHZ6tb_37ACu4-wLR-FUTZZCDH0Ro'  # Your API key here
        monster_client = client(api_key)
        model = 'sdxl-base'
        prompt = input_text
        input_data = {
            'prompt': prompt,
            'negprompt': 'unreal, fake, meme, joke, disfigured, poor quality, bad, ugly, text, letters, numbers, humans',
            'samples': 2,
            'steps': 50,
            'aspect_ratio': 'square',
            'guidance_scale': 7.5,
            'seed': 2414,
        }
        result = monster_client.generate(model, input_data)

        image_urls = result['output']

        # Display all images with buttons
        for i, image_url in enumerate(image_urls):
            st.image(image_url, caption=f'Image {i + 1}', use_column_width=True, width=200)

        # Allow user to input the image index they want to choose
        selected_image_index = st.text_input("Enter the image index you want to choose (e.g., 1)")


        #select the caption
        api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZkN2M2ZGI3NWUxZTRjODViYTg0NzdiNWYzMWU4MTM2IiwiY3JlYXRlZF9hdCI6IjIwMjMtMTItMTNUMTQ6NTQ6MTYuMDM0Mzc3In0.mE2K3F3RlvaQD4PHZ6tb_37ACu4-wLR-FUTZZCDH0Ro'  # Your API key here
        monster_client = client(api_key)
        model = 'falcon-7b-instruct'
        input_data = {
            'prompt': prompt,
            'top_k': 15,
            'top_p': 0.5,
            'temp': 0.99,
            'max_length': 256,
            'beam_size': 1,
            'system_prompt': "The follwoing is a marketing lead and creates marketing contnent for facebook pages as per user needs and do not give give placeholders",
                    }
        result = monster_client.generate(model, input_data)
          
        print(result['text'])

        message = result['text']
        print(message[9:])


        
        

        # Provide button to choose the specified image
        if st.checkbox("Choose Image"):
            if 1 <= int(selected_image_index) <= len(image_urls):
                st.session_state.selected_image_index = int(selected_image_index) - 1
                st.session_state.selected_image_url = image_urls[int(selected_image_index) - 1]
                st.text(f"Selected Image {selected_image_index}")
                st.text('Posting')
                access_token = 'EAAVaJXTNldsBOZCmiIci3al49LfjcFOZAKwkWubwMoFhs36HBYLnFkiLVAfZCEtzMYZAYDw96HvaASFpfy2WaCTY0hbfK7xmRSoh0CVK40GrDaARJbCo7WUsMtKdDMOYuZBYb5GEA52bWnRoEHOKtxNbTrUYP2NMvcraATdkPnZClCw63rFt6hg5LnV1ZAf5Lz6g3xZCPs4ZD'  # Your Facebook access token here
                page_id = '179897971873271'  # Your Facebook page ID here
                message = message

                # Uncomment the line below if you need to post the image to Facebook
                post_to_facebook_demo(access_token, page_id, message, st.session_state.selected_image_url)
            else:
                st.warning(f"Invalid image index. Please enter a number between 1 and {len(image_urls)}.")



#admin login frontend sample
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    if st.checkbox("Login"):
        if username and password:
            st.info("Logging in...")
            # browser = login_to_facebook(username, password)

        # Wait for user to press Enter before closing the browser
        # close = input("Press Enter to close the browser...")
        # if close == '':
        #     browser.quit()
        else:
            st.warning("Please enter both username and password.")




#facebook posting automation hard coded main
def post_to_facebook(access_token, page_id, message, image_path):
    graph = facebook.GraphAPI('EAAVaJXTNldsBOZCmiIci3al49LfjcFOZAKwkWubwMoFhs36HBYLnFkiLVAfZCEtzMYZAYDw96HvaASFpfy2WaCTY0hbfK7xmRSoh0CVK40GrDaARJbCo7WUsMtKdDMOYuZBYb5GEA52bWnRoEHOKtxNbTrUYP2NMvcraATdkPnZClCw63rFt6hg5LnV1ZAf5Lz6g3xZCPs4ZD')
    print(page_id)

    # Post to the user's feed or page with the attached media
    graph.put_photo(parent_object='me', image=open(image_path, 'rb'), message=message)
    st.text('Posted content to Facebook Page')

#facebook posting automation hard coded demo
def post_to_facebook_demo(access_token, page_id, message, image_path):
    image_url = image_path
    image_response = requests.get(image_url)
    graph = facebook.GraphAPI(access_token)
    print(page_id)

    # Check if the request was successful (status code 200)
    if image_response.status_code == 200:
    # Open the image file in binary mode
        with open('local_image.png', 'wb') as file:
            # Write the content of the response to the file
            file.write(image_response.content)

            # Now you can use 'local_image.png' as the image path in your code
        graph.put_photo(parent_object='me', image=open('local_image.png', 'rb'), message=message)
        st.text ("Posted")

    else:
        print(f"Failed to download image. Status code: {image_response.status_code}")




def main():
    # Sidebar
    st.sidebar.header("Navigation")
    #Mainpage = st.sidebar.button("Main Page")

    user_selection = st.sidebar.selectbox("Select User", ["", "admin", "user"])
    if user_selection == "user":
        user_login()
    elif user_selection == "admin":
        admin_login()
    #elif Mainpage:
    #    main_page()
    else:
        main_page()

if __name__ == "__main__":
    main()
