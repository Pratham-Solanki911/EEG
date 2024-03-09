import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from keras.utils import to_categorical 
from keras.models import load_model
import requests

input_file = r'emotions.csv'
data = pd.read_csv(input_file)
scaler = StandardScaler()
label_mapping = {'NEGATIVE': 0, 'NEUTRAL': 1, 'POSITIVE': 2}
data['label'] = data['label'].replace(label_mapping)
X = data.drop('label', axis=1)
y = data['label'].copy()
scaler.fit(X)
X = scaler.transform(X) 
y = to_categorical(y)




st.set_page_config(
    page_title="LNN Project",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': "https://www.linkedin.com/in/pratham-solanki01/",
        'About'   : "here is a paper link for the project"
    }
)
with st.sidebar: 
    # st.image('https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png')
    st.image('Loading_Neural_Brains.gif')
    st.title('Emotion detection')
    st.info('This Application demonstrates an efficint DL model for EEG devices')
   
st.title('EEG based Emotion Detection using Liquid Neural Networks') 
selected_row = st.slider('Select Row', 0, len(X)-1, 0)

with st.spinner('Loading...'):
    import time
    time.sleep(5) 
fig, ax = plt.subplots(figsize=(5,1))
ax.plot(X[selected_row])
ax.set_xlabel('Time(s)')
ax.set_ylabel('Value')
ax.set_title('Time Series Data - Row {}'.format(selected_row), fontsize = 7)
ax.axis('off')
st.pyplot(fig, use_container_width = True)

st.info('This is the output of the machine learning model as tokens')
def get_prediction(selected_index):
    # Send selected index to model server for prediction
    response = requests.get(f'http://localhost:5001/predict/{selected_index}')
    return response.json()
# In replace the model (which is present in the main function) with the following code
prediction_result = get_prediction(selected_row)
        
# Display prediction result
st.write('Prediction:', prediction_result['predicted_class'])
st.write('Message:', prediction_result['predicted_label'])