import csv
import ast
from collections import Counter
import math

def unique(sentence):

    # insert the list to the set
    list_set = set(sentence)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list

def transforming(filename,fieldname):
    path = f'./data/{filename}.csv'
    dataforwrite = []
    with open(path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            mystring = row[fieldname]
            mystring = mystring.replace(' (', '(')
            mystring = mystring.replace("', '", ' - ')
            mystring = mystring.replace("'", '')
            mystring = mystring.replace('(ไม่ - PART),(', '(*')
            dataforwrite.append(mystring)

    with open(f'./transformed/{fieldname}_{filename}.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = ["comment"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for data in dataforwrite :
            writer.writerow({"comment":data})

def transformdata():
    filesname = ["google","tripadvisor"]
    places = ["patong","promthep","wat"]
    for file in filesname :
        for place in places:
            transforming(file,place)

def frequency_noun_bydomain(domain_name):
    path_google = f'./transformed/{domain_name}_google.csv'
    path_tripadvisor = f'./transformed/{domain_name}_tripadvisor.csv'
    comments = []
    with open(path_google, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            comment = row["comment"]
            comments.append(comment)
    with open(path_tripadvisor, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            comment = row["comment"]
            comments.append(comment)
        
    all_words = []
    for comment in comments:
        sentences = []
        comment = comment.replace("[[", "").replace("]]", "")
        for line in comment.split('], ['):
            word = list(line.split(','))
            sentences.append(word)
        unique_words = []
        for sentence in sentences:
            for word in sentence:
                unique_words.append(word)
        all_words.extend(unique_words)
    bf = dict(Counter(all_words))  # counting words
    af = {k: bf[k]
        for k in sorted(bf, key=bf.get, reverse=True)}  # sort asending
    with open('./domain/'+domain_name+'_noun.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = ["noun","count"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for element in af :
            if element.find("NOUN") != -1:
                noun  =  element
                count = af.get(element, '')
                writer.writerow({"noun":noun,"count":count})

    with open('./domain/'+domain_name+'.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = ["comment"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for comment in comments :
            writer.writerow({"comment":comment})    


#frequency_noun_bydomain("patong")

def transform_pos_neg_bydomain(domain_name):

    comments_pos = []
    comments_neg = []

    path_google_neg = f'./transformed/{domain_name}_google_negative.csv'
    path_tripadvisor_neg = f'./transformed/{domain_name}_trip_negative.csv'
    
    path_google_pos = f'./transformed/{domain_name}_google_positive.csv'
    path_tripadvisor_pos = f'./transformed/{domain_name}_trip_positive.csv'

    #### neg
    with open(path_google_neg, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            comment = row["comment"]
            comments_neg.append(comment)
    with open(path_tripadvisor_neg, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            comment = row["comment"]
            comments_neg.append(comment)    
    ### pos
    with open(path_google_pos, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            comment = row["comment"]
            comments_pos.append(comment)
    with open(path_tripadvisor_pos, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            comment = row["comment"]
            comments_pos.append(comment)    

    with open('./domain/'+domain_name+'_neg.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = ["comment"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for comment in comments_neg :
            writer.writerow({"comment":comment})     
   
    with open('./domain/'+domain_name+'_pos.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = ["comment"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for comment in comments_pos :
            writer.writerow({"comment":comment})     

#transform_pos_neg_bydomain("patong")

def tf_idf_fun(domain_name,node,percentile,type) :
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
    with open('./domain/'+domain_name+'_noun.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        lines= len(list(csv_reader))

    top_lines = int(lines-percentile/100*(lines+1))
    #print("Domain "+domain_name+", p",percentile,", type",type,", count nouns at p",percentile,"is",top_lines)

    ##noun top at percentile
    words_noun = []
    ##
    with open('./domain/'+domain_name+'_noun.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)    
        index = 0
        for row in csv_reader:
            if(index <top_lines):
                noun = row["noun"]
                words_noun.append(noun)
                index += 1
            else :
                break
    ##matching word
    words_match = []
    ##
    
    ##pos
    with open(f'./domain/{domain_name}_{node}.csv', mode='r', encoding='utf-8') as csv_file:
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
                                (word_left.find("VERB") != -1 and use_vb):                                words_match.append({"word":word_left,"noun":noun
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
    with open(f'./domain/{domain_name}_match_p{percentile}_{node}_.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = ["word","noun","position","range","index"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for word in words_match :
            writer.writerow(word) 

    ##count word   
    # 
    words_match_forcount = []    
    words_forcheck = []
    words_noun_f = []
    for word in words_match:
        wordma = word["word"]+","+word["noun"]
        words_match_forcount.append(wordma)
        words_forcheck.append(word["word"])
        words_noun_f.append(word["noun"])

    bf = dict(Counter(words_match_forcount))  # counting words
    words_forcheck = dict(Counter(words_forcheck))
    af = {k: bf[k]
        for k in sorted(bf, key=bf.get, reverse=True)}     
    
###frequency noun 
    words_noun_f = dict(Counter(words_noun_f))  # counting words


    words_frequency = []
    comments = []
    with open(f'./domain/{domain_name}_{node}.csv', mode='r', encoding='utf-8') as csv_file:
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
                for word in sentence:
                    for word_c in words_forcheck :
                        if word.find(word_c) !=-1:
                            words_frequency.append(word_c)
            comments.append(sentences)
    words_comment_f = []
    for word_c in words_forcheck :
        for comment in comments:
            word_not_found = True
            if word_not_found :
                for sentence in comment:
                    for word in sentence:
                        if word.find(word_c) !=-1:
                            words_comment_f.append(word_c)
                            word_not_found = False
                            break
                    
    count_comment = 0
    with open(f'./domain/{domain_name}_{node}.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        count_comment= len(list(csv_reader))
    
    words_frequ_bf = dict(Counter(words_frequency))  # counting words  
    words_comment_f = dict(Counter(words_comment_f))  # counting words      

  #  for word in words_comment_f :
  #      print(word,words_comment_f.get(word,''))


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
        idf = math.log10(val_for_idf)
        tf_idf = tf * idf

        if node == "pos":
            tf_idf_arr.append({"word":word_c,"tf-idf":tf_idf})
        if node == "neg":
            tf_idf_arr.append({"word":word_c,"tf-idf":-tf_idf})

    return tf_idf_arr

def find_tf_idf(domain_name,percentile,type):
    tf_idf_pos = tf_idf_fun(domain_name,"pos",percentile,type)
    tf_idf_neg = tf_idf_fun(domain_name,"neg",percentile,type)

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

    with open(f'./domain/{domain_name}_tfidf_p{percentile}_type{type}.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = ["word","tf-idf-pos","tf-idf-neg","tf-idf-val","node-label"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for word in bankWordSorted :
            writer.writerow(word)     

def main():
    percentiles = [95,90,85,80,75]
    for p in percentiles :
        type = 1 
        while type <=7:
            find_tf_idf("patong",p,type)
            type+=1

main()