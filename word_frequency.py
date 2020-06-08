import csv
from collections import Counter

# Use for get any rows csv by only one column.
def get_data_by_one_column(path,column_name):
    rows = []
    with open(path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            data_at_row = row[column_name]
            rows.append(data_at_row)
    return rows

# Use for write a csv file by more than one column.
def write_data_by_columns(path,fieldnames,data):
    with open(path, mode='w', newline='', encoding='utf-8') as writefile:
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data :
            writer.writerow(row)  

# Transform string to list 2d
def transform_string_to_list2d(string_form):
    two_d = []
    string_form = string_form.replace("[[", "").replace("]]", "") 
    ############ PROBLEMS IN FUTURE ############
    for line in string_form.split('], ['):
        one_d = list(line.split(','))
        two_d.append(one_d)
    return two_d

def transform_comments_from_string_to_list2d(comments_string):
    comments = []
    for comment_s in comments_string:
        transformed_comment = transform_string_to_list2d(comment_s)
        comments.append(transformed_comment)
    return comments

# Use for get word by type of postag in all comments 
def get_results_of_count_words_in_comments(comments):
    results = []
    for comment in comments:
        result = count_words_in_a_comment(comment)
        results.append(result)
    return results

def get_sum_count_in_collection(collection):
    sum = 0
    for item in collection:
        sum += collection.get(item,'')
    return sum 

def count_words_in_a_comment(comment):
    noun_words = []
    verb_words = []
    adj_words = []
    adv_words = []
    for sentence in comment:
            for word in sentence:
                if word.find('NOUN') != -1:
                    noun_words.append(word)
                elif word.find('VERB') != -1:
                    verb_words.append(word)
                elif word.find('ADJ') != -1:
                    adj_words.append(word)
                elif word.find('ADV') != -1:
                    adv_words.append(word)

    noun_words_c = dict(Counter(noun_words))
    verb_words_c = dict(Counter(verb_words))
    adj_words_c = dict(Counter(adj_words))
    adv_words_c = dict(Counter(adv_words))

    sum_noun = get_sum_count_in_collection(noun_words_c)
    sum_verb = get_sum_count_in_collection(verb_words_c)
    sum_adj = get_sum_count_in_collection(adj_words_c)
    sum_adv = get_sum_count_in_collection(adv_words_c)
    noun_count = len(noun_words_c)
    verb_count = len(verb_words_c)
    adj_count = len(adj_words_c)
    adv_count = len(adv_words_c)
    result = {"comment":comment,"noun":noun_words_c,"noun_count":noun_count,"sum_noun":sum_noun
    ,"verb":verb_words_c,"verb_count":verb_count,"sum_verb":sum_verb
    ,"adj":adj_words_c,"adj_count":adj_count,"sum_adj":sum_adj
    ,"adv":adv_words_c,"adv_count":adv_count,"sum_adv":sum_adv}

    return result

def count_words_by_types_in_segpos(segpos_type):
    path_segpos_type = f'./segpos_type{segpos_type}'

    places_list = ['patong','promthep','wat']
    web_site_list = ['google','trip']

    for web in web_site_list:
        for place in places_list:
            count_words_in_place_of_web(place,web,segpos_type,path_segpos_type)



def count_words_in_place_of_web(place,web,segpos_type,path_segpos_type):
    path_patong_g_inner_segpos = f'{path_segpos_type}/data/{place}_{web}.csv'
    patong_google_comments = get_data_by_one_column(path_patong_g_inner_segpos,'comment')
    transformed_patong_google_comments = transform_comments_from_string_to_list2d(patong_google_comments)
    result_patong_google_comments = get_results_of_count_words_in_comments(transformed_patong_google_comments)
    
    path_count_words_patong_google = f'./count_words/segpos_type{segpos_type}_{place}_{web}.csv'
    fieldnames = ["comment","noun","noun_count","sum_noun"
    ,"verb","verb_count","sum_verb"
    ,"adj","adj_count","sum_adj"
    ,"adv","adv_count","sum_adv"]
    write_data_by_columns(path_count_words_patong_google,fieldnames,result_patong_google_comments)

def main():
    count_words_by_types_in_segpos(1)
    count_words_by_types_in_segpos(2)
    count_words_by_types_in_segpos(3)
    count_words_by_types_in_segpos(4)

    

main()