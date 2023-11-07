### Recommendation Engine
import pandas as pd
import numpy as np
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

CSV_FILE = '../data_clean/final_merge_clean.csv'
CONTACT = '../data_clean/zz_account_contact_persoon_finance.csv'

def remove_stopwords(text):
    stop_words_nl = set(stopwords.words('dutch'))
    
    word_tokens = word_tokenize(text, language='dutch')

    result = [x for x in word_tokens if x not in stop_words_nl]

    seperator = ', '
    return seperator.join(result)


def team_name_change(text):
    teams_dict = {
        'jo': ' jong ondernemen ',
        'do': ' duurzaam ondernemen ',
        'in': ' innovatie digitalisering ',
        'io': ' internationaal ondernemen ',
        'ao': ' arbeidsmarkt ',
        'ex': ' expert ',
        'gr': ' groei ',
        'bb': ' belangenbehartiging ',
        'co': ' communicatie ',
        'nw': ' netwerking ',
        'ha': ' haven ',
        'ma': ' match '
    }
    word_tokens = word_tokenize(text, language='dutch')
    # apply dict to list
    result = [teams_dict.get(word, word) for word in word_tokens]
    # join list to string
    cleaned_list = ', '.join(result)
    # tokenize string
    tokenize_list = word_tokenize(cleaned_list, language='dutch')
    # remove comma
    tokenize_list_no_comma = [x for x in tokenize_list if x != ',']
    # join list to string and remove duplicates from list
    return ', '.join(list(set(tokenize_list_no_comma)))


def stemmer(text):
    stemmer = SnowballStemmer(language='dutch')
    stem_sentence=[]
    for word in text.split(','):
        stem_sentence.append(stemmer.stem(word))
    stem_sentence= ', '.join(stem_sentence)
    return stem_sentence


def clean_text(df, col='keyphrase'):

    df_copy = df.copy()

    for row in range(len(df_copy)):
        name_change = team_name_change(df_copy[col][row])
        no_stopwords = remove_stopwords(name_change)
        tokenize_list = word_tokenize(no_stopwords, language='dutch')
        tokenize_list = [x for x in tokenize_list if x != ',']
        df_copy.at[row, col] = ', '.join(list(set(tokenize_list)))
        stemmer_list= stemmer(df_copy[col][row])
        df_copy.at[row, col] = stemmer_list
    
    df_copy[col] = df_copy[col].str.replace('voka', ' ') \
        .str.replace('ov', '').str.replace('unknown', '').str.replace(r'\b\w{1,3}\b', '', regex=True).str.replace(r'\d+', '', regex=True) \
        .str.replace(r'(\s{2},\s{2}),*+', '', regex=True).str.replace(' ', '').str.replace(r'^,+|,+$', '', regex=True) \
        .str.replace(r',,+', ',', regex=True)

    return df_copy


def titelChange(data):
    for col in data.columns:
        if col.startswith('crm_') or col.startswith('CDI_'):
            data.columns = data.columns.str.replace('crm_', '')
            data.columns = data.columns.str.replace('CDI_', '')


def create_column_names(dataframe, pk='Campagne_Campagne'):
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


def clean_new_campaign_data(df):

    preclean_df = df.copy()

    titelChange(preclean_df)

    preclean_df.rename(columns=create_column_names(preclean_df), inplace=True)

    df_campagne = basic_clean(preclean_df)

    # campagne naam cleanen
    df_campagne['campagne_naam'] = df_campagne['campagne_naam'].str.replace('OV-', '').str.replace('ov-', '') \
                                                            .str.replace('-', ' ').str.replace(r'[^\w\s]', '', regex=True) \
                                                            .str.replace('  ', ' ').str.strip().str.lower().str.replace('  ', ' ')

    # Drop kolommen
    df_campagne.drop(['campagne_einddatum', 'campagne_startdatum', 'campagne_campagne_nr', 
                  'campagne_naam_in_email', 'campagne_reden_van_status', 'campagne_status',
                  'campagne_url_voka_be'
                  ], axis=1, inplace=True)

    # Create keyphrase column
    cols_for_key = ['campagne_naam', 'campagne_type_campagne', 'campagne_soort_campagne']

    for col in cols_for_key:
        df_campagne[col] = df_campagne[col].astype(str).str.split().str.join(', ')

    df_campagne['keyphrase'] = df_campagne[cols_for_key].apply(lambda x: ', '.join(x), axis=1)

    # keyphrases cleanen
    df_campagne['keyphrase'] = df_campagne['keyphrase'].str.replace(', ,', ',').str.replace(r'(\s{2},\s{2}),*+', '') \
        .str.replace('  ', ' ').str.replace(r'[^\w\s]', '', regex=True).str.replace('  ', ' ').str.strip().str.lower()
    
    final_df = clean_text(df_campagne, 'keyphrase') 

    return final_df


def clean_contact_df(lijst, response_df):
    contact_df = pd.read_csv(CONTACT)
    contact_df = contact_df[contact_df['contact_contactpersoon_id'].isin(lijst)]
    contact_df = contact_df.drop(['marketing_pressure'], axis=1)
    response_df = pd.merge(response_df, contact_df, on='contact_contactpersoon_id')
    response_df['functie_naam'] = response_df['functie_naam'].apply(lambda x: ', '.join(list(set(x.split(' ')))))
    response_df['account_adres'] = response_df['account_adres'].apply(lambda x: ', '.join(list(set(x.split(' ')))))
    return response_df
