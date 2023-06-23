
# created the main python file

import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favourites') 
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocker Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.text('')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)



#Create New fuction here
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized



#New section to display fruityvice api response.
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
        
except URLError as e:
    streamlit.error()

#
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized)





#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)



streamlit.header("The fruit load list contains :")
#Snowflake related functions
def get_fruit_load_list():
        with my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * from fruit_load_list")
            return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.header("The fruit load list contains :")
    streamlit.dataframe(my_data_rows)

#Allow the user  to add fruit to the list
#add_my_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
#streamlit.write('The user entered ', add_my_fruit)
#import requests
#my_cur1 = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_cur1.execute("insert into PUBLIC.FRUIT_LOAD_LIST values ('" + add_my_fruit  "')")
#my_cur1.execute("insert into PUBLIC.FRUIT_LOAD_LIST values ('parrot')")
#my_cur1.execute("insert into PUBLIC.FRUIT_LOAD_LIST values" + f"('{add_my_fruit}')") 
#my_cur3 = my_cnx.cursor()
#my_cur3.execute("SELECT * from fruit_load_list")


#Allow the end user to add a fruit to the table
def insert_row_snowflake(new_fruit):
        with my_cnx.cursor() as my_cur:
            #my_cur.execute("Insert into fruit_load_list values ('from streamlit')")
            my_cur.execute("Insert into fruit_load_list values" + f"('{add_my_fruit}')") 
            return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function) 




#insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST
#values ('banana')
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

streamlit.stop()
