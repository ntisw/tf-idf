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

def count_words_in_a_comment(comment):
    noun_words = []
    verb_words = []
    adj_words = []
    adv_words = []
    for sentence in comment:
            for word in sentence:
                print()

def main():
    type_segpos = 1
    path_segpos_type = f'./segpos_type{type_segpos}'
    
    path_patong_g_inner_segpos = f'{path_segpos_type}/data/patong_google.csv'
    patong_google_comments = get_data_by_one_column(path_patong_g_inner_segpos,'comment')
    transformed_patong_google_comments = transform_comments_from_string_to_list2d(patong_google_comments)
    result_patong_google_comments = get_results_of_count_words_in_comments(transformed_patong_google_comments)
    
    path_count_words_patong_google = f''
    fieldnames = []
    write_data_by_columns(path_count_words_patong_google,fieldnames,result_patong_google_comments)

    path_patong_t_inner_segpos = f'{path_segpos_type}/data/patong_tripadvisor.csv'
    patong_trip_comments = get_data_by_one_column(path_patong_t_inner_segpos,'comment')
    
main()