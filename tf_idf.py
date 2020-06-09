import csv
import ast
from collections import Counter
import math

# Use to merge a node of comments by rating into a domain
def merge_comments_with_node_by_domain(domain_name,dir_segpos):
    """This is a merge node of comments by domain name.
    That merge google negative comments and tripadvisor negative comments 
    in one file.  

    Arguments:
        domain_name {string} -- Use for path file of domain 
        dir_segpos {string} -- Use for path file into folder segpos type
    """
    path_google_neg = f'{dir_segpos}/data/{domain_name}_google_negative.csv'
    path_tripadvisor_neg = f'{dir_segpos}/data/{domain_name}_trip_negative.csv'
    
    path_google_pos = f'{dir_segpos}/data/{domain_name}_google_positive.csv'
    path_tripadvisor_pos = f'{dir_segpos}/data/{domain_name}_trip_positive.csv'

    # get negative comments
    neg_comments = get_data_by_one_column(path_google_neg,"comment") \
         + get_data_by_one_column(path_tripadvisor_neg,"comment")
    # get positive comments
    pos_comments = get_data_by_one_column(path_google_pos,"comment") \
         + get_data_by_one_column(path_tripadvisor_pos,"comment") 

    # write file
    path_pos_comment_by_domain = f'{dir_segpos}/{domain_name}/{domain_name}_pos.csv'
    path_neg_comment_by_domain = f'{dir_segpos}/{domain_name}/{domain_name}_neg.csv'

    write_data_by_one_column(path_pos_comment_by_domain,"comment",pos_comments)
    write_data_by_one_column(path_neg_comment_by_domain,"comment",neg_comments)

# Use for get any rows csv by only one column.
def get_data_by_one_column(path,column_name):
    rows = []
    with open(path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            data_at_row = row[column_name]
            rows.append(data_at_row)
    return rows

# Use for write a csv file by only one column.
def write_data_by_one_column(path,column_name,data):
    with open(path, mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = [column_name]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data :
            writer.writerow({column_name:row})  

# Use for write a csv file by more than one column.
def write_data_by_columns(path,fieldnames,data):
    with open(path, mode='w', newline='', encoding='utf-8') as writefile:
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data :
            writer.writerow(row)  

# Output of this file can be use for any funtions of tf-idf. 
def transforming_comments(comments):
    transformed_comments = []
    for comment in comments:
        comment = comment.replace(' (', '(')
        comment = comment.replace("', '", ' - ')
        comment = comment.replace("'", '')
        comment = comment.replace('(ไม่ - PART),(', '(*')
        comment = comment.replace('],[','], [')
        transformed_comments.append(comment)
    return transformed_comments

# Divide comments by 2 node.
# There are positive comments and negative comments.
# Actual rating more than 2.5 there is a positive comment 
# and other comments there is a negative comment. 
def divide_comments_by_pos_neg(comments,rating):
    comments_with_node_dict = []
    index = 0
    while index <len(comments) and index <len(rating):
        if float(rating[index]) > 2.5 :
            comments_with_node_dict.append({"comment":comments[index],"node":"pos"})
        else:
            comments_with_node_dict.append({"comment":comments[index],"node":"neg"})
        index +=1
    return comments_with_node_dict

# Use to return comments by node
def get_comments_by_node(comments_with_node_dict,node):
    comments = []
    for comment in comments_with_node_dict:
        if comment["node"] == node:
            comments.append(comment["comment"])
    return comments

# Use to return noun words that found into frequency words
def get_noun_from_frequency_words(frequency_words):
    noun_words = []
    for element in frequency_words :
        if element.find("NOUN") != -1 and element != '' and element != ' ' and element != ' - NOUN)':
            noun  = element
            count = frequency_words.get(element, '')
            noun_words.append({"noun":noun,"count":count})
    return noun_words

# Use for find frequency noun words by domain that contain
# comments in google and tripadvisor.
# Than write file.
def frequency_noun_by_domain(domain_name,dir_segpos):
    path_google = f'{dir_segpos}/data/{domain_name}_google.csv'
    path_tripadvisor = f'{dir_segpos}/data/{domain_name}_trip.csv'
    #read files .csv
    comments = get_data_by_one_column(path_google,"comment") \
        + get_data_by_one_column(path_tripadvisor,"comment")
    
    #write file .csv (for lookup later)
    path_merge_comments_file = f'{dir_segpos}/{domain_name}/{domain_name}.csv'
    write_data_by_one_column(path_merge_comments_file,"comment",comments)  
    
    all_words = []
    for comment in comments:
        sentences = []
        comment = comment.replace("[[", "").replace("]]", "")
        for line in comment.split('], ['):
            word_list = list(line.split(','))
            word = []
            for word_ in word_list:
                word_.replace('[','')
                word_.replace(']','')
                word.append(word_)
            sentences.append(word)
        unique_words = []
        for sentence in sentences:
            for word in sentence:
                unique_words.append(word)
        all_words.extend(unique_words)
    bf = dict(Counter(all_words))  # counting words
    af = {k: bf[k]
        for k in sorted(bf, key=bf.get, reverse=True)}  # sort asending

    # write file noun
    path_noun_frequency_file = f'{dir_segpos}/{domain_name}/{domain_name}_noun.csv'
    fieldnames = ["noun","count"]
    noun_words = get_noun_from_frequency_words(af)
    write_data_by_columns(path_noun_frequency_file,fieldnames,noun_words)

# Use to find tfidf by specific node, percentile, type into a domain 
def tf_idf_fun(domain_name,node,percentile,type,dir_segpos) :
    use_vb = False
    use_aj = False
    use_av = False

    if type == 1:
        use_vb = True
    elif type == 2:
        use_aj = True
    elif type == 3:
        use_av = True
    elif type == 4:
        use_vb = use_aj = True
    elif type == 5:
        use_vb = use_av = True
    elif type == 6:
        use_aj = use_av = True
    elif type == 7:
        use_vb = use_aj = use_av = True

    lines = 0
    path_noun = f'{dir_segpos}/{domain_name}/{domain_name}_noun.csv'
    all_noun = get_data_by_one_column(path_noun,"noun")
    lines = len(list(all_noun))
    top_lines = int(lines-percentile/100*(lines+1))
    print("Domain "+domain_name+", p",percentile,", type",type,", count nouns at p",percentile,"is",top_lines)

    ##noun top at percentile
    words_noun = []
    index = 0
    while index < top_lines:
        words_noun.append(all_noun[index])
        index += 1
    
    ##matching word
    words_match = []
    ##
    
    path_node_comments = f'{dir_segpos}/{domain_name}/{domain_name}_{node}.csv'
    with open(path_node_comments, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            sentences = []
            comment = row["comment"]
            comment = comment.replace("[[", "").replace("]]", "") 
            ############ PROBLEMS IN FUTURE ############
            for line in comment.split('], ['):
                word = list(line.split(','))
                sentences.append(word)
            for sentence in sentences :
                for noun in words_noun:
                    index = 0
                    while index < len(sentence):
                        word = sentence[index]
                        if word.find(noun) != -1: 
                            left = index 
                            right = index
                            count_left = 0
                            count_right = 0
                            while left >= 0 and count_left<=4:
                                word_left = sentence[left]
                                if (word_left.find("ADJ") != -1 and use_aj)or\
                                (word_left.find("ADV") != -1 and use_av) or\
                                (word_left.find("VERB") != -1 and use_vb):                                
                                    words_match.append({"word":word_left,"noun":noun
                                    ,"position":"left","range":count_left,"index":left})
                                count_left +=1
                                left -=1
                            while right <len(sentence) and count_right<=4:
                                word_right = sentence[right]
                                if (word_right.find("ADJ") != -1 and use_aj)or\
                                (word_right.find("ADV") != -1 and use_av) or\
                                (word_right.find("VERB") != -1 and use_vb):
                                    words_match.append({"word":word_right,"noun":noun
                                    ,"position":"right","range":count_right,"index":right})
                                count_right +=1
                                right +=1
                        index +=1
    
    path_match_words = f'{dir_segpos}/{domain_name}/match_words/{domain_name}_match_p{percentile}_type{type}_{node}.csv'
    fieldnames_match_words = ["word","noun","position","range","index"]
    write_data_by_columns(path_match_words,fieldnames_match_words,words_match)
    
    # count word   
    words_match_forcount = []    
    words_forcheck = []
    words_noun_f = []
    for word in words_match:
        wordma = word["word"]+","+word["noun"]
        words_match_forcount.append(wordma)
        words_forcheck.append(word["word"])
        words_noun_f.append(word["noun"])

    bf = dict(Counter(words_match_forcount))  # counting words function
    words_forcheck = dict(Counter(words_forcheck))
    af = {k: bf[k]
        for k in sorted(bf, key=bf.get, reverse=True)}     
    
    #frequency noun 
    words_noun_f = dict(Counter(words_noun_f))  # counting words

    comments = []
    with open(path_node_comments, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            sentences = []
            comment = row["comment"]
            comment = comment.replace("[[", "").replace("]]", "") 
            ############ PROBLEMS IN FUTURE ############
            for line in comment.split('], ['):
                word = list(line.split(','))
                sentences.append(word)
            comments.append(sentences)
    words_comment_f = []
    for word_c in words_forcheck :
        for comment in comments:
            word_not_found = True
            for sentence in comment:
                if word_not_found :
                    for word in sentence:
                        if word.find(word_c) !=-1:
                            words_comment_f.append(word_c)
                            word_not_found = False
                            #break
                    
    count_comment = 0
    with open(path_node_comments, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        count_comment= len(list(csv_reader))

    words_comment_f = dict(Counter(words_comment_f))  # counting words      

    tf_idf_arr = []

    for word_c in words_forcheck :
        count_overall_f = 0
        count_f = 0
        count_comment_f = 0
        for word in af :
            if word.find(word_c) !=-1:
                count = int(af.get(word, ''))
                poly = word.split(",")
                noun = poly[1]
                for word_n in words_noun_f :
                    if noun.find(word_n) !=-1:
                        count_noun = int(words_noun_f.get(word_n, ''))
                        count_overall_f += count_noun
                count_f +=count
        for word in words_comment_f :
            if word.find(word_c) !=-1:
                count_c = words_comment_f.get(word, '')
                count_comment_f = count_c
                break

        tf = count_f/count_overall_f
        val_for_idf = count_comment/count_comment_f
        #print(word_c,node,count_comment,count_comment_f)
        idf = math.log10(val_for_idf)
        tf_idf = tf * idf
        #if tf_idf > 1:
        #    print("p",percentile,"review",node,word_c,'tf(',count_f,"/",count_overall_f,") = ",tf,"idf(log10(",count_comment,"/",count_comment_f,")) = log10(",val_for_idf,") = ",idf,"tf-idf = ",tf_idf)
        if node == "pos":
            tf_idf_arr.append({"word":word_c,"tf-idf":tf_idf})
        if node == "neg":
            tf_idf_arr.append({"word":word_c,"tf-idf":-tf_idf})

    return tf_idf_arr

# Use to find tfidf by specific percentile, type into a domain
def find_tfidf_at(domain_name,percentile,type,dir_segpos):
    tf_idf_pos = tf_idf_fun(domain_name,"pos",percentile,type,dir_segpos)
    tf_idf_neg = tf_idf_fun(domain_name,"neg",percentile,type,dir_segpos)

    tf_idf_pos_size = len(tf_idf_pos)
    tf_idf_neg_size = len(tf_idf_neg)

    tf_idf_bank_word = []
    tfIdfObjs = []
    all_len = []

    for word in tf_idf_pos :
        all_len.append(word["word"])
    for word in tf_idf_neg:
        all_len.append(word["word"])

    all_len = dict(Counter(all_len))
    tf_idf_size = len(all_len)

    index = 0
    for word_ in all_len :
        tf_idf_pos_val = 0
        tf_idf_neg_val = 0
        for word in tf_idf_pos:
            if word_.find(word["word"]) != -1:
                tf_idf_pos_val = word["tf-idf"]
                break
        for word in tf_idf_neg:
            if word_.find(word["word"]) != -1:
                tf_idf_neg_val = word["tf-idf"]
                break
        

        tf_idf_val = tf_idf_pos_val + tf_idf_neg_val
        node_label = ""
        if tf_idf_val > 0 :
            node_label = "pos"
        else :
            node_label = "neg"
        
        tf_idf_bank_word.append({"word":word_,"tf-idf-pos":tf_idf_pos_val,"tf-idf-neg":tf_idf_neg_val,"tf-idf-val":tf_idf_val,"node-label":node_label})
        index +=1

    bankWordSorted = sorted(tf_idf_bank_word, key=lambda  tfIdf: abs(tfIdf["tf-idf-val"]),reverse=True)
    path_tfidf = f'{dir_segpos}/{domain_name}/bankwords/{domain_name}_tfidf_p{percentile}_type{type}.csv'
    fieldnames_tfidf = ["word","tf-idf-pos","tf-idf-neg","tf-idf-val","node-label"]
    write_data_by_columns(path_tfidf,fieldnames_tfidf,bankWordSorted)

# Use to find tfidf by all percentiles, all types into any domains 
def find_tfidf(domains,dir_segpos):
    percentiles = [95,90,85,80,75]
    for domain in domains:
        for p in percentiles :
            type = 1 
            while type <=7:
                find_tfidf_at(domain,p,type,dir_segpos)
                type+=1

# Use to test bankword by specific percentile, type, into a domain
def test_bank(domain_name,p,type,dir_segpos):
    bank_words = []
    comments_pos = []
    comments_neg = []
    with open(f'{dir_segpos}/{domain_name}/bankwords/{domain_name}_tfidf_p{p}_type{type}.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            word = row["word"]
            node_label = row["node-label"]
            tf_idf = row["tf-idf-val"]
            bank_words.append({"word":word,"node":node_label,"tfidf":tf_idf})
    
    with open(f'{dir_segpos}/{domain_name}/{domain_name}_pos.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            sentences = []
            comment = row["comment"]
            comment = comment.replace("[[", "").replace("]]", "") 
            ############ PROBLEMS IN FUTURE ############
            for line in comment.split('], ['):
                word = list(line.split(','))
                sentences.append(word)
            comments_pos.append(sentences)

    with open(f'{dir_segpos}/{domain_name}/{domain_name}_neg.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            sentences = []
            comment = row["comment"]
            comment = comment.replace("[[", "").replace("]]", "") 
            ############ PROBLEMS IN FUTURE ############
            for line in comment.split('], ['):
                word = list(line.split(','))
                sentences.append(word)
            comments_neg.append(sentences)
    
    results = check_by_comment(comments_pos,bank_words,"pos") + check_by_comment(comments_neg,bank_words,"neg")
    fieldnames_test_result = ['expert','node_actual','comment'
        ,'scores_by_node','scores_by_tfidf','scores_by_tfidf_sum'
        ,'predict_by_node_label','predict_by_tfidf','corrective_node_label'
        ,'corrective_tfidf','corrective_expert_node_label','corrective_expert_tfidf']
    # expert rating added
    # fieldnames = ["comment","scores_by_node","score_by_tfidf","score_by_tfidf_sum","node_actual"
    #    ,"node_predict_by_node_label","corrective_by_node_label","node_predict_by_tfidf","corrective_by_tfidf"]
    results = merge_expert_corrective(results,domain_name)
    path_test_result = f'{dir_segpos}/{domain_name}/test_results/type{type}/{domain_name}_tfidf_p{p}_type{type}.csv'
    write_data_by_columns(path_test_result,fieldnames_test_result,results)

# Use to check by comments with bankword by a node
def check_by_comment(comments,bank_words,node):
    
    results = []
    for comment in comments:
        scores = 0
        scores_tfidf = 0
        scores_tfidf_string = ""

        corrective_by_node = False
        corrective_by_tfidf = False
        node_predict_by_node = node
        node_predict_by_tfidf = node
        index = 0
        for sentence in comment:
            for word_s in sentence:
                for word_b in bank_words:
                    if word_s == word_b["word"]:
                        s_tfidf =float(word_b["tfidf"])
                        scores_tfidf += s_tfidf
                        if index == 0 :
                            scores_tfidf_string += f'{word_b["word"]}{s_tfidf}'
                        else :
                            scores_tfidf_string += f', {word_b["word"]}{s_tfidf}'
                        index += 1
                        if word_b["node"] == "pos":
                            scores +=1
                        elif word_b["node"] == "neg":
                            scores -=1
                        break
        if scores > 0:
            node_predict_by_node = "pos"
        else:
            node_predict_by_node = "neg"

        if scores_tfidf >= 0 :
            node_predict_by_tfidf = "pos"
        else:
            node_predict_by_tfidf = "neg"

        if node_predict_by_node == node:
            corrective_by_node = True

        if node_predict_by_tfidf == node:
            corrective_by_tfidf = True

        results.append({"comment":comment,"scores_by_node":scores
        ,"score_by_tfidf":scores_tfidf_string
        ,"score_by_tfidf_sum":scores_tfidf
        ,"node_actual":node
        ,"node_predict_by_node_label":node_predict_by_node
        ,"corrective_by_node_label":corrective_by_node
        ,"node_predict_by_tfidf":node_predict_by_tfidf
        ,"corrective_by_tfidf":corrective_by_tfidf})

    return results

# Use to test bankword by all percentiles, all types into a domain
def test_all_types_by_domain(domain_name,dir_segpos):
    percentiles = [95,90,85,80,75]
    for p in percentiles :
        type = 1
        while type < 8:
            test_bank(domain_name,p,type,dir_segpos)
            print(f"test {domain_name} at p{p} type{type}")
            type+=1

# Use to combine the set of functions that contain find tfidf function
# and test bankword function for any domains
def tf_idf_by_segpos_type(segpos_t):
    dir_segpos = f'./segpos_type{segpos_t}'
    path_segpos_t = f'./data/segpos_type{segpos_t}.csv'
    path_rating_original = f'./data/rating_by_original.csv'
    path_rating_expert = f'./data/rating_by_expert.csv'
    columns_name = ["PatongGoogle","PatongTrip","PromthepGoogle","PromthepTrip","WatGoogle","WatTrip"]
    domains_name = ["patong","promthep","wat"]
    
    #transforming data
    for column_name in columns_name:
        print('segpos_t',segpos_t,column_name)

        comments = get_data_by_one_column(path_segpos_t,column_name)
        ratings_origianl = get_data_by_one_column(path_rating_original,column_name)
        ratings_expert = get_data_by_one_column(path_rating_expert,column_name)

        #transforming comments
        comments = transforming_comments(comments)
        
        #divide pos neg comments
        comment_with_node_dict =divide_comments_by_pos_neg(comments,ratings_origianl)

        pos_comments = get_comments_by_node(comment_with_node_dict,"pos")
        neg_comments = get_comments_by_node(comment_with_node_dict,"neg")


        column_name = column_name.lower()
        column_name = column_name.replace('google','_google')
        column_name = column_name.replace('trip','_trip')
        
        path_file_for_write = f'{dir_segpos}/data/{column_name}.csv'
        column_comment = "comment"
        write_data_by_one_column(path_file_for_write,column_comment,comments)

        #comments pos neg
        path_pos_comments = f'{dir_segpos}/data/{column_name}_positive.csv'
        write_data_by_one_column(path_pos_comments,column_comment,pos_comments)
        path_neg_comments = f'{dir_segpos}/data/{column_name}_negative.csv'
        write_data_by_one_column(path_neg_comments,column_comment,neg_comments)

    #tf idf processes
    for domain_name in domains_name:
        merge_comments_with_node_by_domain(domain_name,dir_segpos)
        frequency_noun_by_domain(domain_name,dir_segpos)
    find_tfidf(domains_name,dir_segpos)

    #test tfidf
    for domain_name in domains_name:
        test_all_types_by_domain(domain_name,dir_segpos)

# Use for sort the rating that merge for test bankwords
def sort_rating():
    domains = ["Patong","Promthep","Wat"]
    expert_rating_all_file = []
    path_rating_by_expert = f'./data/rating_by_expert.csv'
    path_rating_by_original = f'./data/rating_by_original.csv'
    for domain in domains :
        rating_g = get_data_by_one_column(path_rating_by_original,f'{domain}Google')
        rating_t = get_data_by_one_column(path_rating_by_original,f'{domain}Trip')
        rating_ex_g = get_data_by_one_column(path_rating_by_expert,f'{domain}Google')
        rating_ex_t = get_data_by_one_column(path_rating_by_expert,f'{domain}Trip')
        index = 0
        rating_pair_pos_g = []
        rating_pair_neg_g = []
        rating_pair_pos_t = []
        rating_pair_neg_t = []
        while index<len(rating_g):
            if float(rating_g[index]) >2.5:
                rating_pair_pos_g.append({"actual_rating":"pos","expert":rating_ex_g[index]})
            else :
                rating_pair_neg_g.append({"actual_rating":"neg","expert":rating_ex_g[index]})
            index +=1
        index = 0
        while index<len(rating_t):
            if float(rating_t[index]) >2.5:
                rating_pair_pos_t.append({"actual_rating":"pos","expert":rating_ex_t[index]})
            else :
                rating_pair_neg_t.append({"actual_rating":"neg","expert":rating_ex_t[index]})
            index +=1

        sorted_expert_rating = rating_pair_pos_g + rating_pair_pos_t \
            + rating_pair_neg_g + rating_pair_neg_t
        
        path_sorted_rating_by_expert = f'./data/{domain.lower()}_sorted_rating.csv'
        fields_name = ["actual_rating","expert"]
        write_data_by_columns(path_sorted_rating_by_expert,fields_name,sorted_expert_rating)

# Use for test bankword by using rating experts
def merge_expert_corrective(results,domain_name):
    new_results = []
    path_sorted_rating = f'./data/{domain_name}_sorted_rating.csv'
    sorted_rating_expert = get_data_by_one_column(path_sorted_rating,"expert")
    index = 0 
    count_corrective_node_label = 0
    count_corrective_tfidf = 0
    count_corrective_expert_node_label = 0
    count_corrective_expert_tfidf = 0
    while index < len(results):
        old_result = results[index]
        corrective_expert_node_label = False
        corrective_expert_tfidf = False
        if old_result['node_predict_by_node_label'] == sorted_rating_expert[index]:
            corrective_expert_node_label = True
            count_corrective_expert_node_label +=1
        else :
            corrective_expert_node_label = False
        if old_result['node_predict_by_tfidf'] == sorted_rating_expert[index]:
            corrective_expert_tfidf = True
            count_corrective_expert_tfidf +=1
        else :
            corrective_expert_tfidf = False
        if old_result['node_predict_by_node_label'] == old_result['node_actual']:
            count_corrective_node_label+=1
        if old_result['node_predict_by_tfidf'] == old_result['node_actual']:
            count_corrective_tfidf +=1

        new_result = {'expert':sorted_rating_expert[index]
        ,'node_actual':old_result['node_actual']
        ,'comment':old_result['comment']
        ,'scores_by_node':old_result['scores_by_node']
        ,'scores_by_tfidf':old_result['score_by_tfidf']
        ,'scores_by_tfidf_sum':old_result['score_by_tfidf_sum']
        ,'predict_by_node_label':old_result['node_predict_by_node_label']
        ,'predict_by_tfidf':old_result['node_predict_by_tfidf']
        ,'corrective_node_label':old_result['corrective_by_node_label']
        ,'corrective_tfidf':old_result['corrective_by_tfidf']
        ,'corrective_expert_node_label':corrective_expert_node_label
        ,'corrective_expert_tfidf':corrective_expert_tfidf}
        new_results.append(new_result)
        index+=1
    new_result = {'expert':''
    ,'node_actual':''
    ,'comment':''
    ,'scores_by_node':''
    ,'scores_by_tfidf':''
    ,'scores_by_tfidf_sum':''
    ,'predict_by_node_label':''
    ,'predict_by_tfidf':''
    ,'corrective_node_label':count_corrective_node_label
    ,'corrective_tfidf':count_corrective_tfidf
    ,'corrective_expert_node_label':count_corrective_expert_node_label
    ,'corrective_expert_tfidf':count_corrective_expert_tfidf}
    new_results.append(new_result)    
    return new_results

# Use for combine all type of word segment and POS tag (1,2,3 and 4)
def main():
    sort_rating()
    tf_idf_by_segpos_type(1)
    tf_idf_by_segpos_type(2)
    tf_idf_by_segpos_type(3)
    tf_idf_by_segpos_type(4)

# Use for run main() that contain all processes
main()