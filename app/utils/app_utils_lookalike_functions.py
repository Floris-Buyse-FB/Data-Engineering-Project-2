import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import re

CSV_FILE = os.path.join(os.getcwd(), '../data_clean/merged_total_no_keyphrases.csv')

#########################
# CLEAN NEW CONTACT DATA
#########################

def titelChange(data):
    for col in data.columns:
        if col.startswith('crm_') or col.startswith('CDI_'):
            data.columns = data.columns.str.replace('crm_', '')
            data.columns = data.columns.str.replace('CDI_', '')

def create_column_names(dataframe, pk='Contact_Contactpersoon'):
    columns = dataframe.columns
    columns = [col + '_id' if col == pk else col for col in columns]
    columns = [re.sub(r'\W+', '', col) for col in columns]
    columns = [col.lower() for col in columns]
    dict_columns = dict(zip(dataframe.columns, columns))
    return dict_columns

def basic_clean(df):
    data = df.copy()
    data.drop_duplicates(inplace=True)
    numeric = data.select_dtypes(include='number').columns
    non_numeric = data.select_dtypes(exclude='number').columns
    data[numeric] = data[numeric].fillna(-1)
    data[non_numeric] = data[non_numeric].fillna('unknown')
    return data

def clean_new_contact_data(df):
    preclean_df = df.copy()
    titelChange(preclean_df)
    preclean_df.rename(columns=create_column_names(preclean_df), inplace=True)
    df_contact = basic_clean(preclean_df)

    # Drop kolommen
    df_contact = df_contact[df_contact['contact_status'] != 'Inactief']
    df_contact['contact_functietitel'] = df_contact['contact_functietitel'].str.lower().str.replace(r'[^\w\s]', '', regex=True) \
                                                            .str.replace('  ', ' ').str.strip()
    df_contact.drop(['contact_status', 'contact_voka_medewerker','contact_account'], axis=1, inplace=True)

    final_df = df_contact.copy()
    return final_df

###########################
# LOOKALIKE RECOMMANDATIONS
###########################

# def clean_merged(df):
#   new_df = df.copy()
#   new_df = new_df[['contact_contactpersoon_id','contact_functietitel','functie_naam','account_adres','account_onderneming','afspraak_keyphrases','campagne_campagne_id','campagne_type_campagne','campagne_naam','campagne_soort_campagne']]
#   new_df = new_df.drop_duplicates(subset=['contact_contactpersoon_id','campagne_campagne_id'], keep='first')
#   return new_df

# def vectorizing(df):
#   df2 =df
#   df2['data'] =df[df.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)

#   vectorizer = CountVectorizer()
#   vectorized = vectorizer.fit_transform(df2['data'])
#   return vectorized


# def similarities(df):
#   similarities = cosine_similarity(df)
#   return similarities

# def lookalike_matrix(df):
#   data = clean_merged(df)
#   vectorized = vectorizing(data)
#   similarities = similarities(vectorized)
#   matrix = pd.DataFrame(similarities,columns=df['contact_contactpersoon_id'],index=df['contact_contactpersoon_id']).reset_index()
#   return matrix

# def recommend_lookalikes(df, input_person_id):
#   matrix = lookalike_matrix(df)
#   recommendations = pd.DataFrame(matrix.nlargest(11,input_person_id)['contact_contactpersoon_id'])
#   recommendations = recommendations[recommendations['contact_contactpersoon_id']!=input_person_id]
#   return recommendations

############################################
# RECOMMENDATIONS BASED ON NEW CONTACT DATA
############################################

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

def similarities_CONTACT(df,contact_df):
  similarities = cosine_similarity(df,contact_df)
  return similarities

def lookalike_matrix_CONTACT(df,contact_df):
  data = clean_merged(df)
  vectorized_df = vectorizing(data)
  vectorized_contact = vectorizing(contact_df)
  similarities = similarities_CONTACT(vectorized_df,vectorized_contact)
  matrix = pd.DataFrame(similarities,columns=contact_df['contact_contactpersoon_id'],index=df['contact_contactpersoon_id']).reset_index()
  return matrix

def recommend_lookalikes_CONTACT(df,contact_df, input_contact_id, top_n=10):
  matrix = lookalike_matrix_CONTACT(df,contact_df)
  recommendations = pd.DataFrame(matrix.nlargest(top_n,input_contact_id)['contact_contactpersoon_id'])
  recommendations = recommendations[recommendations['contact_contactpersoon_id']!=input_contact_id]
  return recommendations

########################
# GET THE HULP DATAFRAME
########################

def get_hulp_df():
  df = pd.read_csv(CSV_FILE)
  return df