import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

CSV_FILE = os.path.join(os.getcwd(), '../data_clean/merged_total_no_keyphrases.csv')

###########################
# LOOKALIKE RECOMMANDATIONS
###########################

def clean_merged(df):
  new_df = df.copy()
  new_df = new_df[['contact_contactpersoon_id','contact_functietitel','functie_naam','account_adres','account_onderneming','afspraak_keyphrases','campagne_campagne_id','campagne_type_campagne','campagne_naam','campagne_soort_campagne']]
  new_df = new_df.drop_duplicates(subset=['contact_contactpersoon_id','campagne_campagne_id'], keep='first')
  return new_df

def vectorizing(df):
  df2 =df
  df2['data'] =df[df.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)

  vectorizer = CountVectorizer()
  vectorized = vectorizer.fit_transform(df2['data'])
  return vectorized

def lookalike_matrix(df):
  vectorized = vectorizing(df)

  similarities = cosine_similarity(vectorized)

  matrix = pd.DataFrame(similarities,columns=df['contact_contactpersoon_id'],index=df['contact_contactpersoon_id']).reset_index()
  return matrix

def recommend_lookalikes(df, input_person_id, top_n=10):
  df = clean_merged(df)
  matrix = lookalike_matrix(df)
  recommendations = pd.DataFrame(matrix.nlargest(top_n+1,input_person_id)['contact_contactpersoon_id']).reset_index(drop=True)
  recommendations = recommendations[recommendations['contact_contactpersoon_id']!=input_person_id]
  return recommendations

########################
# GET THE HULP DATAFRAME
########################

def get_hulp_df():
  df = pd.read_csv(CSV_FILE)
  return df