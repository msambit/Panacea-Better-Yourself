import os
import os.path
import io
import subprocess
import time
import re
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import json5
import altair as alt
from streamlit.scriptrunner.script_run_context import get_script_run_ctx
from streamlit.server.server import Server
from streamlit_url_fragment import get_fragment
import boto3
client = boto3.client('cognito-idp','us-east-1')

API_URL = "https://api-inference.huggingface.co/models/Nakul24/RoBERTa-Goemotions-6"
headers = {"Authorization": "Bearer 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"}

ak_url = "https://7888th4wcl.execute-api.us-east-1.amazonaws.com/v1/predict"


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def fetch(session, url,headers1):
        try:
            result = session.get(url,headers=headers1)
            return result.json()
        except Exception:
            return {}

def main():  
    st.set_page_config(layout="wide",page_title="Mental Health")

    st.image('https://panacea.s3.amazonaws.com/Picture1.png',width=100)
    st.write('AI to Predict mental status of a person')
    

    #st.write("AI to Predict mental status of a person")

    headers = get_fragment()
    if headers == "" or headers == None:
        st.markdown(
        """[Log In](https://ccprojectdomain.auth.us-east-1.amazoncognito.com/login?client_id=47mogrgfkjucdcol48qp7fsmi5&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https://ec2-3-89-99-74.compute-1.amazonaws.com:8501)"""
        )
        components.html("""
        <script src="https://apps.elfsight.com/p/platform.js" defer></script>
        <div class="elfsight-app-4c045bce-f323-4061-899e-f47ed67adf87"></div>
        """,height=650)
    else:
        header_list = headers.split("&")
        token = header_list[1].split("=") 
        #st.write(token[1])

    if headers != "" and headers != None:
        response = client.get_user(AccessToken= token[1])
        hello = "Hi " + response["Username"]
        st.subheader(hello)
        

        session = requests.Session()
        #test = fetch(session,"https://panacea-app.auth.us-east-1.amazoncognito.com/login?client_id=2b5dqcl0go20lksgia833dl182&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https://share.streamlit.io/nakul24-1/mental-health-cloud/main/main.py")
        #st.text(test)
        with st.form("my_form"):
            st.header("Questions")
            st.subheader("Q1) How have you been feeling lately?")
            input_q1 = st.text_area("Type out all your feelings here")
            st.markdown("***")
            st.subheader("Q2) Why do you think you feel like this?")
            input_q2 = st.text_area("Please describe what caused your feelings")
            st.markdown("***")
            st.subheader("Q3) Since when are you feeling like this?")
            input_q3 = st.text_area("Please inform us about the timeframe of your current feeling")
            submitted = st.form_submit_button("Submit")
            
            #input_text = re.sub("\s+", " ", st.text_input("Enter text"))
            #index = st.number_input("ID", min_value=0, max_value=100, key="index")

        if submitted:   
            st.header("Result")
            st.markdown("***")
            answers = input_q1 + " " + input_q2 + " " + input_q3
            #out = query({"inputs": answers,})
            
            #st.text(pd.DataFrame.from_records(out[0]))

            #st.bar_chart(pd.DataFrame.from_records(out[0]))
            url = 'https://7fhrcwqoqh.execute-api.us-east-1.amazonaws.com/FirstStage/panacea'
            
            myobj = {
            "messages": answers
            }
            headers1 = {"authToken" : token[1]}

            json_object = json.dumps(myobj, indent = 4)
            
            x = requests.post(url,headers = headers1, data = json_object)
            out =  json.loads(x.text)

            #st.text(out)
            #st.text(x.text)
            #st.text(x.status_code)
            c = alt.Chart(pd.DataFrame.from_records(out)).mark_bar().encode(
                y='label',
                x='score').properties(width=200,height=350)
            
            st.altair_chart(c,use_container_width=True)
            st.markdown("***")
            
            # ADD Video in columns , add suggestions/resources based on current mood
            col1, col2 = st.columns(2)

            with col1:
                st.header("Your Current mood is")
                max_key = maxPricedItem = max(out, key=lambda x:x['score'])
                st.subheader(max_key['label'])
                if max_key['label'] == 'anxiety':

                    st.markdown("""<h3>Try these activities :</h3>
                                        <ul>
                                        <li>We would suggest to limit alcohol and caffeine, which can aggravate anxiety and trigger panic attacks.</li>
                                        <li>Exercise daily to help you feel good and maintain your health</li>
                                        <li>Take deep breaths. Inhale and exhale slowly.</li>
                                        </ul>""",unsafe_allow_html=True)

                    
                elif max_key['label'] == 'depression':
                    #st.write("We would suggest you to try the following tasks :")
                    st.markdown("""<h3>We would suggest you to try the following tasks :</h3>
                                        <ul>
                                        <li>Walking for thirty minutes</li>
                                        <li>Socialize with Friends and Family</li>
                                        <li>Eat a Healthy Diet</li>
                                        </ul>
                                        <h2>If you feel the need to talk to someone right now contact -</h2>
                                        <ul>
                                        <li>NYU Helpline</li>
                                        <li>USA Suicide Prevention</li>
                                        </ul>""",unsafe_allow_html=True)
                    
                elif max_key['label'] == 'anger':
                    st.markdown("""<h3>Try these activities :</h3>
                                        <ul>
                                        <li>Get some exercise as physical activity can help reduce stress that can cause you to become angry.</li>
                                        <li>Try some deep breathing techniques or listening to music.</li>
                                        <li>Exercise daily to help you feel calmer.</li>
                                        <li>If you harmed someone, apologise. If you hurt yourself, apologise to yourself</li>
                                        <li>Talk about how you are feeling. Parents or carers and other family members, such as grandparents, may be good listeners.</li>
                                        </ul>""",unsafe_allow_html=True)
                
                elif max_key['label'] == 'disgust':
                    st.markdown("""<h3>Feeling disgusted is a normal response, Here are a few ways to manage feelings of disgust:</h3>
                                        <ul>
                                        <li>Don't let your feelings control your thinking. </li>
                                        <li>Rather than spending time imagining what other people are doing and thinking, become more mindful of your own wants, needs, and feelings.</li>
                                        <li>Talk to someone you trust about your feelings.Parents and other family members, such as grandparents, may be good listeners. </li>
                                        <li>Don't bad mouth the person you felt upset with.</li>
                                        </ul>""",unsafe_allow_html=True)
                    
                   
                elif max_key['label'] == 'joy':
                    st.markdown("""<h3>It's great you're feeling joyful, here are a few things we suggest you to do :</h3>
                                        <ul>
                                        <li>Maintain your joy by focusing on keeping composure.</li>
                                        <li>Use your positive mindframe to do something productive</li>
                                        <li>Celebrate , throw a party, meet friends and/or family.</li>
                                        <li>Spend Time in Nature, explore and enjoy the beauty of the world around you</li>
                                        </ul>""",unsafe_allow_html=True)
                    

                elif max_key['label'] == 'surprise':

                    st.markdown("""<h3>You seem surprised, here is how you can cope up with suprise and unexpected events :</h3>
                                        <ul>
                                        <li>Acknowledge the fact, and learn to accept that surprises and unexpected events are part of life and are unavoidable.</li>
                                        <li>In the future, when making a plan, always have an alternate plan, in case the first plans fail.</li>
                                        <li>Celebrate , throw a party, meet friends and/or family.</li>
                                        <li>Wait for a few moments, before blurting out when confronting unexpected or unpleasant turns of fate.</li>
                                        <li>Think constructively where you are going from there. You need to think how to adjust to the new situation and either fix it, improve it, or make the most of it.</li>
                                        </ul>""",unsafe_allow_html=True)

            with col2:
                if max_key['label'] == 'anxiety':
                    st.video('https://youtu.be/embed/ybBxDWir8-8') 
        
                elif max_key['label'] == 'depression':
                    st.video('https://youtu.be/embed/c_gqTkwiGys') 
                    
                elif max_key['label'] == 'anger':
                    st.video('https://youtu.be/embed/mQ2FJBJBRc') 

                elif max_key['label'] == 'disgust':
                    st.video('https://youtu.be/embed/74Z6WrQiu5k') 
                    
                elif max_key['label'] == 'joy':
                    st.video('https://youtu.be/embed/KFtELA58wEE') 

                elif max_key['label'] == 'surprise':
                    st.video('https://youtu.be/embed/va1XMhEFsb0') 
            
            
            #if st.button("View History"):
        
        
            data = fetch(session, f"https://7fhrcwqoqh.execute-api.us-east-1.amazonaws.com/FirstStage/panacea",headers1)
            if data:
                #st.text(data)
                df = pd.DataFrame.from_records(data)
                #st.text(df)
                df1 = pd.DataFrame.from_records(json5.loads(df.loc['labels'][0][0]))
                df1['Time'] = df.loc['times'][0][0]

                for x in range(1,len(df.loc['times'][0])):
                  df2 = pd.DataFrame.from_records(json5.loads(df.loc['labels'][0][x]))
                  df2['Time'] = df.loc['times'][0][x]
                  df1 = pd.concat([df1, df2])
                  
                df1['Time'] = pd.to_datetime(df1['Time'],unit='s')
                df1['Time'] = df1['Time'].dt.strftime('%d-%m %H:%M')
                st.markdown("***")
                st.header("Mental Health History")
                st.markdown("***")


                
                c2 = alt.Chart(df1).mark_bar().encode(
                x=alt.X('sum(score)', stack="normalize"),
                y='Time',
                color='label'
                ).properties(height = 600)
                
                st.altair_chart(c2,use_container_width=True)
            else:
                st.error("Error")


            #History = st.form_submit_button("View History") # Chart code in comment below
            '''
                


            '''

    
    components.html("""
    <script src="https://apps.elfsight.com/p/platform.js" defer></script>
    <div class="elfsight-app-b996a8bc-edc2-4dc8-9b70-e462d9601b13"></div>
    """)

if __name__ == '__main__':
    main()






