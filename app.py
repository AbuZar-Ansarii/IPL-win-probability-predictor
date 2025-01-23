import pickle
import streamlit as st
import pandas as pd
from select import error

model = pickle.load(open("ipl_model.pkl","rb"))

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities =['Mohali', 'Jaipur', 'Indore', 'Johannesburg', 'Chandigarh',
       'Mumbai', 'Hyderabad', 'Pune', 'Bangalore', 'Chennai', 'Kolkata',
       'Dharamsala', 'Ahmedabad', 'Cuttack', 'Delhi', 'Port Elizabeth',
       'Visakhapatnam', 'Centurion', 'Cape Town', 'Bengaluru', 'Durban',
       'Ranchi', 'Kimberley', 'East London', 'Bloemfontein', 'Nagpur',
       'Abu Dhabi', 'Sharjah', 'Raipur']


st.title("IPL PROBABILITY PREDICTOR")


col1,col2 = st.columns(2)
with col1:
    batting_team = st.selectbox("Select Batting Team",sorted(teams))
with col2:
    bowling_team = st.selectbox("Select Bowling Team",sorted(teams))

selected_city = st.selectbox("Select City",sorted(cities))

target = st.number_input("Target",min_value=0,max_value=350)

col3,col4,col5 = st.columns(3)
with col3:
    score = st.number_input("Score",min_value=0,max_value=130)
with col4:
    overs = st.number_input("Overs Completed",min_value=0,max_value=20)
with col5:
    wickets = st.number_input("Wickets Out",min_value=0,max_value=10)


if st.button("Predict Probability"):
    if batting_team == bowling_team:
        st.header("Please Select Different Teams")
    else:
        if target == 0 :
            st.header("Please Set Valid Target")
        else:
            if overs == 0 :
                st.header("Please Predict After Some Balls")
            else:
                if wickets == 10:
                    st.header(f"{batting_team} Won The Match")
                else:
                    runs_left = target - score
                    balls_left = 120 - (overs*6)
                    wickets = 10 - wickets
                    crr = score/overs
                    rrr = (runs_left*6)/balls_left
                    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],
                                                 'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],
                                                 'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})
                    result = model.predict_proba(input_df)
                    loss = result[0][0]
                    win = result[0][1]

                    st.header(bowling_team + " -  " + str(round(win*100)) + "%")
                    st.header(batting_team + " -  " + str(round(loss*100)) + "%")
