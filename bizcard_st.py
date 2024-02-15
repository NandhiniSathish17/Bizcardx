import streamlit as st
import easyocr
import pymysql
import pandas as pd 
import base64

import cv2

import re
# myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='yourpwd',database='bizcardx')
# cur = myconnection.cursor()

# table_create_sql = '''CREATE TABLE IF NOT EXISTS mytable (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                                                          Name TEXT,Designation TEXT,
#                                                         Company_name TEXT,
#                                                         Address TEXT,
#                                                         Contact_number TEXT,
#                                                         Mail_id TEXT,
#                                                         Website_link TEXT,
#                                                         Image BLOB);'''
# cur.execute(table_create_sql)

##-------------------Code for Background image------------------------##
st.set_page_config(layout='wide')
def sidebar_bg(side_bg):
   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file) 
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

sidebar_bg(r"/Users/sathish/Desktop/sidebar1.jpeg")
set_png_as_page_bg("/Users/sathish/Desktop/image2.webp")

##---------------------------------Streamlit application------------------------------------#

from streamlit_option_menu import option_menu
with st.sidebar:
    st.title(":white[Contents]")
   
    selected =option_menu( menu_title= "Overview",
          options=["Home","Uploading","Extracting data","Modify"],
          icons=["house-door","bi bi-cloud-arrow-up-fill","eraser-fill"],
          menu_icon="book-fill",
          default_index=0,styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#14CFCC"}})
         


t1,c1,c2,c4=st.columns([1,1,1,11])
with t1:
    title_html = '''
    <h1 style="text-align: center; font:Helvetica; color: green;">
        <a  style="text-decoration: none; color: #14CFCC;">
           BizCardX - Extracting Business Card Data 
        </a>
    
    </h1><br>

    
'''

st.markdown(title_html, unsafe_allow_html=True)
import easyocr
import cv2


##------------------Code for Tab Selection----------------##

if selected=="Home":
     st.write("The project 'BizCardX: Extracting Business Card Data with OCR ' likely involves the development of a system or software application that utilizes Optical Character Recognition (OCR) technology to extract information from business cards.Here's a potential short description:BizCardX is a project focused on automating the extraction of data from business cards using Optical Character Recognition (OCR) technology. By leveraging advanced algorithms, BizCardX can swiftly and accurately capture key information such as contact details, company names, addresses, and other pertinent data from scanned or photographed business cards. This streamlined process simplifies data entry and enhances efficiency in managing contact information.")
filename=None



#Function for data extraction from uploaded image
def extracted_data(image):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image, paragraph=True, decoder='wordbeamsearch')
    img = cv2.imread(image)
    for detection in result:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        text = detection[1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.rectangle(img, top_left, bottom_right, (204, 0, 34), 5)
        img = cv2.putText(img, text, top_left, font, 0.8,
                          (0, 0, 255), 2, cv2.LINE_AA)

    
    return img

##--------------------------------------------Funtion for uploading in to database---------------------------------

def upload_database(image):
    # ----------------------------------------Getting data from image using easyocr------------------------------------------------------
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image, paragraph=True, decoder='wordbeamsearch')
    # -----------------------------------------converting  data to single string------------------------------------------------------
    data = []
    j = 0
    for i in result:
        data.append(result[j][1])
        j += 1
    data
    org_reg = " ".join(data)
    reg = " ".join(data)
    # ------------------------------------------Separating EMAIL---------------------------------------------------------------------------
    email_regex = re.compile(r'''(
	[a-zA-z0-9]+
	@
	[a-zA-z0-9]+
	\.[a-zA-Z]{2,10}
	)''', re.VERBOSE)
    email = ''
    for i in email_regex.findall(reg):
        email += i
        reg = reg.replace(i, '')
    # ------------------------------------------Separating phone number---------------------------------------------------------------------------
    phoneNumber_regex = re.compile(r'\+*\d{2,3}-\d{3,10}-\d{3,10}')
    phone_no = ''
    for numbers in phoneNumber_regex.findall(reg):
        phone_no = phone_no + ' ' + numbers
        reg = reg.replace(numbers, '')
    # ------------------------------------------Separating Address---------------------------------------------------------------------------
    address_regex = re.compile(r'\d{2,4}.+\d{6}')
    address = ''
    for addr in address_regex.findall(reg):
        address += addr
        reg = reg.replace(addr, '')
    # ------------------------------------------Separating website link---------------------------------------------------------------------------
    link_regex = re.compile(r'www.?[\w.]+', re.IGNORECASE)
    link = ''
    for lin in link_regex.findall(reg):
        link += lin
        reg = reg.replace(lin, '')
    # ------------------------------------------Separating Designation ----------------------------------------
    desig_list = ['DATA MANAGER', 'CEO & FOUNDER',
                  'General Manager', 'Marketing Executive', 'Technical Manager']
    designation = ''
    for i in desig_list:
        if re.search(i, reg):
            designation += i
            reg = reg.replace(i, '')
    # ------------------------------------------Separating Company name (only suitable for this dataset)--------------------------------------
    # ----------------------------------to overcome this combine all the three datas to single column ----------------------------------------
    comp_name_list = ['selva digitals', 'GLOBAL INSURANCE',
                      'BORCELLE AIRLINES', 'Family Restaurant', 'Sun Electricals']
    company_name = ''
    for i in comp_name_list:
        if re.search(i, reg, flags=re.IGNORECASE):
            company_name += i
            reg = reg.replace(i, '')
    name = reg.strip()

    # ------------------------------------reading and getting byte values of image-----------------------------------------------------------
    with open(image, 'rb') as file:
        blobimg = file.read()
    #  
    myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='yourpwd',database='bizcard')
    cur = myconnection.cursor()
    # -----------------------------------------inserting data into table---------------------------------------------------------------------
    image_insert = '''INSERT INTO bizcardx (Name, Designation, Company_name,
                    Address, Contact_number,Mail_id,
                    Website_link,Image) 
                    values(%s,%s,%s,%s,%s,%s,%s,%s)'''
    
    values = (name, designation, company_name,
                   address, phone_no, email, link, blobimg)
              
    cur.execute(image_insert,values)
    myconnection.commit()
def show_database():
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='your pwd',database='bizcard')
        cur = myconnection.cursor()
        new_df = pd.read_sql("SELECT * FROM bizcardx", con=myconnection)
        return new_df

df = show_database()

if selected=="Uploading":
    st.title("Business Card Information Extractor")
    uploaded_image = st.file_uploader("Upload a business card image", type=["jpg", "png"])
    
    if uploaded_image is not None:
             
            filename=uploaded_image.name
            print(filename)    
            image = uploaded_image.read()
            with open(f'{filename}.png', 'wb') as f:
               f.write(uploaded_image.getvalue())
            st.image(uploaded_image,caption="Uploadved Image", use_column_width=True)
            st.balloons()


            st.subheader(':violet[Image view of Data]')
            on=st.toggle("Extract Data from Image")
            if on:
            # if st.button('Extract Data from Image'):
                extracted = extracted_data(f'{filename}.png')

                st.image(extracted)
                flattened_data = extracted.flatten()
                df = pd.DataFrame({'Pixel_Value': flattened_data})

                # Display the DataFrame
                print(df)
              
            st.subheader(':violet[Upload extracted to Database]')
            if st.button('Upload data'):
                upload_database(f'{filename}.png')
                st.success('Data uploaded to Database successfully!', icon="✅")
       


if selected=="Extracting data":
    st.title(':blue[All Data in Database]')
    if st.button('Show All'):
            st.dataframe(df)
    st.subheader(':blue[Search Data by Column]')
    column = str(st.radio(':blue[Select column to search]', ('Name', 'Designation',
                    'Company_name', 'Address', 'Contact_number', 'Mail_id', 'Website_link'), horizontal=True))
    value = str(st.selectbox(':blue[Please select value to search]', df[column]))


    if st.button('Search Data'):
            st.dataframe(df[df[column] == value])

if selected == "Modify":
    st.subheader(':blue[You can Edit or Delete the extracted data here]')
    select = option_menu(None,
                         options=["ALTER", "DELETE"],
                         icons=["pencil-fill","trash3-fill"],
                         default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                 "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                 "nav-link-selected": {"background-color": "#6495ED"}})

    if select == "ALTER":
            st.markdown(":blue[Alter the data here]")
            myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='yourpwd',database='bizcard')
            cur = myconnection.cursor()
            cur.execute("SELECT name FROM bizcardx")
            result = cur.fetchall()
            business_cards = {} 
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                st.markdown("#### Update or modify any data below")
                cur.execute(
                "select company_name,name,designation,contact_number,mail_id,website_link,address from bizcardx WHERE name=%s",
                (selected_card,))
                result = cur.fetchone()

                # DISPLAYING ALL THE INFORMATIONS
                company_name = st.text_input("Company_Name", result[0])
                name = st.text_input("Card_Holder", result[1])
                designation = st.text_input("Designation", result[2])
                mobile_number = st.text_input("Mobile_Number", result[3])
                email = st.text_input("Email", result[4])
                website = st.text_input("Website", result[5])
                address=st.text_input("Address", result[6])

                if st.button(":blue[Commit changes to DB]"):


                   # Update the information for the selected business card in the database
                    cur.execute("""UPDATE bizcardx SET company_name=%s,name=%s,designation=%s,contact_number=%s,mail_id=%s,website_link=%s,
                                    address=%s
                                    WHERE name=%s""", (company_name, name , designation, mobile_number, email, website, address,
                    selected_card))
                    myconnection.commit()
                    st.success("Information updated in database successfully.")

            if st.button(":blue[View updated data]"):
                cur.execute(
                    "select company_name,name,designation,contact_number,mail_id,website_link,address from bizcardx")
                updated_df = pd.DataFrame(cur.fetchall(),
                                          columns=["Company_Name", "Name", "Designation", "Contact_number",
                                                   "Mail_id",
                                                   "Website_link", "Address"])
                st.write(updated_df)
        

        # try:


        # except:
        #     st.warning("There is no data available in the database")

    if select == "DELETE":
            st.subheader(":blue[Delete the data]")
        # try:
            myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='yourpwd',database='bizcard')
            cur = myconnection.cursor()
            cur.execute("SELECT name FROM bizcardx")
            result = cur.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                st.write(f"### You have selected :orange[**{selected_card}'s**] card to delete")
                st.write("#### Proceed to delete this card?")
                if st.button("Yes Delete Business Card"):
                    cur.execute(f"DELETE FROM bizcardx WHERE name='{selected_card}'")
                    myconnection.commit()
                    st.success("Business card information deleted from database.")

            if st.button(":blue[View updated data]"):
                cur.execute(
                    "select company_name,name,designation,contact_number,mail_id,website_link,address from bizcardx")
                updated_df = pd.DataFrame(cur.fetchall(),
                                          columns=["Company_Name", "Name", "Designation", "Mobile_Number",
                                                   "Email",
                                                   "Website", "Address"])
                st.write(updated_df)
    
        # except:
        #     st.warning("There is no data available in the database")











