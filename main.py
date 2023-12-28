import streamlit as st
import plotly.graph_objects as go #مكتبه للحصول على الرسومات البيانيه القراف
import calendar
from datetime import datetime
from streamlit_option_menu import option_menu


#----بدي قؤائم او مصفوفات للموقع
incomes =["salary","code","other incom"]
expenses =["food","home","saving","areen","other expenses","utilities"]
currency = "USD"

page_title ="Income and Expense Tracker"
page_icon = "💸"
layout = "centered"


st.set_page_config(page_title=page_title, page_icon=page_icon,layout=layout)
st.title(page_title+ " " + page_icon)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
           
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)




#---navigathion menu
selected = option_menu(
   
menu_title=None,
options=["data entry","data visualization"],
icons=["body-text","bar-chart-fill"],# https://icons.getbootstrap.com
orientation="horizontal",

)

if selected == "data entry":
   


#years = ["2023","2022"]
#months = ["jan","fep","march","........"]

  years = [datetime.today().year,datetime.today().year +1]
  months = list(calendar.month_name[1:])#اول موقع بكون في القائمه فاضي مان هيك بنبلش من واحد


  st.header(f"Data Entry in {currency}")#  من شان ادخل متغير سترنج جوى استرنج{}بستخدم 
  with st.form("entry_form", clear_on_submit=True):#هاي فورم بحط داخلها الاعمده#هاي االخانه تمحى لما نعمل سبمنت نضغط على الزر
#بدي اعمل عمودين
        col1,col2 =st.columns(2)
  #كل عامود بحط في سيليكت بوك
        col1.selectbox("select month:", months,key="month")#اعمل سيلكت بوكس واعطيتو القيم من القائمه
        col2.selectbox("select year:", years, key="year")#اعطيتو القيم من المصفوفه كلو واحد 
        "---"
  
        "---"#فاصل افقي خط
        with st.expander("Income"):
         for income in incomes:
          st.number_input(f"{income}:",min_value=0, format="%i", step=10,key=income)
        with st.expander("expenses"): 
         for expense in expenses:
          st.number_input(f"{expense}:", min_value=0, format ="%i",step=10,key=expense)
        with st.expander("comment"):
          comment = st.text_area("",placeholder="ادخل الملاحظه....")

        "---"
        submitted = st.form_submit_button("Save Data")#بعرف زر لتخزين المدخلات
        if submitted:#هاي متغير برجع ترو اذا الزر انضغط وانا معطي الزر لها المتغير
         period = str(st.session_state["year"])+ "_" + str(st.session_state["month"])
         incomes ={income: st.session_state[income] for income in incomes}
         expenses = {expense: st.session_state[expense] for expense in expenses}
          #------todo insert value in database
         st.write(f" # incomes: {incomes}")
         st.write(f"expenses: {expenses}")

         st.success("Data saved")

#----- plot rreriods
       
if selected == "data visualization":
    st.header("data visualization")
    with st.form("saved_periods"):
         #todo get periods from database
        period = st.selectbox("select period",["2022_march"])
        submitted = st.form_submit_button("plot period")
        if submitted:
           #TODO:get data from database

           comment ="ffffffffff"
           incomes ={'salary':1500,'code':500,'other incom':10}
           expenses ={'food':50,'home':50,
                      'saving':100,'areen':100,
                      'other expenses':200
                      ,'utilities':150}
           
           #create metrics#بدي اعمل كم عمليه حسابيه والمجموع وهيك شغلات
           total_income = sum(incomes.values())
           total_expense = sum(expenses.values())
           remaining_budget = total_income - total_expense
           col1, col2, col3 = st.columns(3)
           col1.metric("total income", f"{total_income}{currency}")
           col2.metric("total expense", f"{total_expense}{currency}")
           col3.metric("remaining budget", f"{remaining_budget}{currency}")
           st.text(f" ## comment:{comment}")


           #creat chart
           label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
           source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
           target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
           value = list(incomes.values()) + list(expenses.values())

           # Data to dict, dict to sankey
           link = dict(source=source, target=target, value=value)
           node = dict(label=label, pad=20, thickness=30, color="#E694FF")
           data = go.Sankey(link=link, node=node)

           # Plot it!
           fig = go.Figure(data)
           fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
           st.plotly_chart(fig, use_container_width=True) 



           