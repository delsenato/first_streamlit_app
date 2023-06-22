
# created the main python file

import streamlit
import pandas
import requests


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

streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/kiwi")
#streamlit.text(fruityvice_response.json())

# This code creates a formatted table with headings.
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains :")
#streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

#Allow the user  to add fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write('The user entered ', add_my_fruit)
import requests
my_cur1 = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_cur1.execute("insert into PUBLIC.FRUIT_LOAD_LIST values ('" + add_my_fruit  "')")
#my_cur1.execute("insert into PUBLIC.FRUIT_LOAD_LIST values ('parrot')")
my_cur1.execute("insert into PUBLIC.FRUIT_LOAD_LIST values ('" add_my_fruit '")")
my_cur3 = my_cnx.cursor()
my_cur3.execute("SELECT * from fruit_load_list")


#insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST
#values ('banana')
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

