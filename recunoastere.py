import numpy as np
import pandas as pd
import cv2
import redis #pt database
from insightface.app import FaceAnalysis #pt model insightface
from sklearn.metrics import pairwise #pt cosine similarity
from datetime import date
import os



# Conectare la Redis Client
hostname = 'redis-10109.c232.us-east-1-2.ec2.redns.redis-cloud.com'
portnumber = 10109
password = 'sFiLLF3c4juFoPxMqjjRE8tv3aOXgbR7'

r = redis.StrictRedis(host=hostname, port=portnumber, password=password)

#Iau date din DB
def culegere_date(name):
    retrieve_dict = r.hgetall(name)
    if not retrieve_dict:
        # Handle the case when the dictionary is empty
        return pd.DataFrame(columns=['Nume', 'Functie', 'Trasaturi'])

    retrieve_series = pd.Series(retrieve_dict)
    retrieve_series = retrieve_series.apply(lambda x: np.frombuffer(x, dtype=np.float32))
    index = retrieve_series.index
    index = list(map(lambda x: x.decode(), index))
    retrieve_series.index = index
    retrieve_df = retrieve_series.to_frame().reset_index()
    retrieve_df.columns = ['ID_persoana', 'Trasaturi']
    retrieve_df[['Nume', 'Functie']] = retrieve_df['ID_persoana'].apply(lambda x: x.split('@')).apply(pd.Series)
    return retrieve_df[['Nume', 'Functie', 'Trasaturi']]



# Aducem modelul de pe insightface
    #bufallo_l numit appl, root=path(numele folderului in care se afla buffalo_l)
aplicatie = FaceAnalysis(name='buffalo_l', root='model_insightface', providers=['CPUExecutionProvider'])
    #providers=['CUDAExecutionProvider', 'CPUExecutionProvider']) fara CUDA, folosesc doar CPU
aplicatie.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.5)

# ALgoritm Machine Learning  - cu metoda similitudintea cosinusului
def algoritm_ml(dataframe, coloana_trasaturi, valoare_cu_care_compar,nume_functie=['Nume','Functie'], punct_detectie = 0.5):
     #cu cosine similarity
    #pasul 1- iau colectia de date din dataframe
    dataframe = dataframe.copy()
    #pasul 2- indexez trasaturile din df si convertesc din lista in array
    lista_trasaturi = dataframe[coloana_trasaturi].tolist()
    valori_trasaturi = np.asarray(lista_trasaturi)
    
    #pasul 3- aplic cosine similarity pairwise.cosine_similarity(x,y); y-matricea reprezentativa a unei fete 
    similar = pairwise.cosine_similarity(valori_trasaturi,valoare_cu_care_compar.reshape(1,-1))
    similar_arr = np.array(similar).flatten()
    dataframe['cos'] = similar_arr

    #pasul 4- filtrez datele (trasaturile persoanelor identificate)
    data_filter = dataframe.query(f'cos >= {punct_detectie}')
    if len(data_filter) > 0:
        #pasul 5- extrag numele persoanelor din lista obtinuta cu cosine simiarity
        data_filter.reset_index(drop=True,inplace=True)
        argmax = data_filter['cos'].argmax()
        nume, functie = data_filter.loc[argmax][nume_functie]
        
    else:
        nume = 'Necunoscut'
        functie = 'Necunoscut'
        
    return nume, functie

# aici se apeleaza algoritmul ml si se prelucreaza imaginile
def analiza_fata(imagine,dataframe, coloana_trasaturi,nume_functie=['Nume','Functie'], punct_detectie = 0.5 ): 

    #data curenta
    ziua = date.today().strftime("%Y-%m-%d")
    # iau imagine test si o aplic pe insightface
    rezultate=aplicatie.get(imagine)
    copie=imagine.copy()
    #extrag fiecare trasatura din poza
    for rez in rezultate:
        x1,y1,x2,y2 = rez['bbox'].astype(int)
        embeddings= rez ['embedding']
        nume, functie = algoritm_ml(dataframe,'Trasaturi',valoare_cu_care_compar=embeddings, nume_functie=nume_functie,punct_detectie=punct_detectie)
    
        if nume == 'Necunoscut':
            color =(0,0,255) # bgr
        else:
            color = (0,255,0)
            
            
        cv2.rectangle(copie,(x1,y1),(x2,y2),color)
        
        text_gen = nume
        cv2.putText(copie,text_gen,(x1,y1),cv2.FONT_HERSHEY_DUPLEX,0.7,color,1)
        cv2.putText(copie,ziua,(x1,y2),cv2.FONT_HERSHEY_DUPLEX,0.5,color,1)
    return copie   

### Formular inregisreare

class Inregistrare:
    def __init__(self):
        self.sample = 0
    def reset(self):
        self.sample = 0

    def get_embedding(self,frame):
        #ca sa afiseze in tiomp real import modelul
        results = aplicatie.get(frame,max_num=1)
        embeddings = None
        for res in results:
            self.sample += 1
            x1, y1, x2, y2 = res['bbox'].astype(int)
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),1)
            #nr de samples
            text = f"capturi = {self.sample}"
            cv2.putText(frame,text,(x1,y1),cv2.FONT_HERSHEY_DUPLEX,0.5,(225,255,0),2)

            # facial features
            embeddings = res['embedding']


        return frame, embeddings
    

    def save_data_in_redis_db(self,nume,functie):
        # 
        if nume is not None:
            if nume.strip() != '':
                key = f'{nume}@{functie}'
            else:
                return 'nume_fals'
        else:
            return 'name_fals'
        
        # if face_embedding.txt exists
        if 'face_embedding.txt' not in os.listdir():
            return 'file_false'
        
        
        # step-1: load "face_embedding.txt"
        x_array = np.loadtxt('face_embedding.txt',dtype=np.float32) # flatten array            
        
        # step-2: convert into array 
        received_samples = int(x_array.size/512)
        x_array = x_array.reshape(received_samples,512)
        x_array = np.asarray(x_array)       
        
        # step-3: cal. mean embeddings
        x_mean = x_array.mean(axis=0)
        x_mean = x_mean.astype(np.float32)
        x_mean_bytes = x_mean.tobytes()
        
        # step-4: save this into redis database
        # redis hashes
        r.hset(name='inregistrare',key=key,value=x_mean_bytes)
        
        # 
        os.remove('face_embedding.txt')
        self.reset()
        
        return True