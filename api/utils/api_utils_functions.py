### Recommendation Engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

nltk.download('stopwords')
nltk.download('punkt')

CSV_FILE = rf'C:\Users\buyse\AA_WORKSPACE\Data-Engineering-Project-2\data_clean\final_merge_clean.csv'


def recommend(df, new_keyphrase: str, top_n=10):
    # preprocessing
    scaler = MinMaxScaler()
    df['marketing_pressure'] = scaler.fit_transform(df[['marketing_pressure']])
    # vectorization
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['keyphrases'])
    # vectorize the new keyphrase and calculate similarity
    new_keyphrase_tfidf = tfidf.transform([new_keyphrase])
    sim_score_new = cosine_similarity(new_keyphrase_tfidf, tfidf_matrix)
    # sort the similarity scores
    contact_person_similarity = list(enumerate(sim_score_new[0]))
    sorted_contact_persons = sorted(contact_person_similarity, key=lambda x: x[1], reverse=True)
    # get the top n similar contact persons
    top_contact_persons = sorted_contact_persons[:top_n]
    # Create a set to keep track of recommended contact IDs
    recommended_contact_ids = set()
    # Iterate through the sorted contact persons and add unique contact IDs to the set
    for index, _ in top_contact_persons:
        contact_id = df['contact_contactpersoon_id'][index]
        recommended_contact_ids.add(contact_id)
    # Convert the set back to a list
    recommended_contact_ids = list(recommended_contact_ids)
    # This would not remove the duplicates
    # recommended_contact_ids = [df['contact_contactpersoon_id'][index] for index, _ in top_contact_persons]
    # sort the contact ids by marketing pressure
    recommended_contact_ids = sorted(recommended_contact_ids, key=lambda x: df[df['contact_contactpersoon_id'] == x]['marketing_pressure'].values[0], reverse=False)
    # result
    results_list = []
    print("Recommended Contact Persons for the New Campaign:")
    for contact_id in recommended_contact_ids:
        marketing_pressure = df[df['contact_contactpersoon_id'] == contact_id]['marketing_pressure'].values[0]
        results_list.append((contact_id, marketing_pressure))
    return results_list


def preproces_df(link=CSV_FILE):
    df = pd.read_csv(link)
    df.drop(['avg_waarde_jaar', 'afspraak_account_gelinkt', 'campagne_campagne_id', 'inschrijving_aanwezig_afwezig', 'inschrijving_facturatie_bedrag'], axis=1, inplace=True)
    df = df.groupby('contact_contactpersoon_id').agg(list)
    df['marketing_pressure'] = df['marketing_pressure'].apply(lambda x: np.mean(x).round(0).astype(int))
    df['keyphrases'] = df['keyphrases'].apply(lambda x: ','.join(list(set(x))))
    df.reset_index(inplace=True)
    return df