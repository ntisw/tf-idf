import csv
import ast
from collections import Counter
import math

def count_frequency(filename):
    output_data = []
    universal_pos_tags = ["ADJ", "ADP", "ADV", "AUX",
                          "CCONJ", "DET", "INTJ", "NOUN", "NUM",
                          "PART", "PRON", "PROPN", "PUNCT",
                          "SCONJ", "SYM", "VERB", "X"]
    max_lenght = 0
    with open('./data/'+filename+'.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        all_words = []
        for row in csv_reader:
            line_count += 1
            matrixAr = []
            mystring = row[filename]
            mystring = mystring.replace(' (', '(')
            mystring = mystring.replace("', '", ' - ')
            mystring = mystring.replace("'", '')
            mystring = mystring.replace('(ไม่ - PART),(', '(*')
            b = mystring.replace("[[", "").replace("]]", "")
            for line in b.split('], ['):
                row_ = list(line.split(','))
                matrixAr.append(row_)
            unique_words = []
            for sentence in matrixAr:
                for word in sentence:
                    unique_words.append(word)
            all_words.extend(unique_words)

        bf = dict(Counter(all_words))  # counting words

        af = {k: bf[k]
              for k in sorted(bf, key=bf.get, reverse=True)}  # sort asending
        print(f"Was found {len(af)} unique words. ")
        # sort
        #ADJ: adjective
        #ADP: adposition
        #ADV: adverb
        #AUX: auxiliary
        # CCONJ: coordinating conjunction
        #DET: determiner
        #INTJ: interjection
        #NOUN: noun
        #NUM: numeral
        #PART: particle
        #PRON: pronoun
        # PROPN: proper noun
        #PUNCT: punctuation
        # SCONJ: subordinating conjunction
        #SYM: symbol
        #VERB: verb
        #X: other

        for pos_tag in universal_pos_tags:
            result = []
            for element in af:
                if element.find(pos_tag) != -1:
                    count = af.get(element, '')
                    result.append({"word": element, "count": count})
            output_data.append({"tag": pos_tag, "data": result})

        for tag_with_count in output_data:
            print(
                f'tag {tag_with_count["tag"]} count {len(tag_with_count["data"])}')
            count = len(tag_with_count["data"])
            if max_lenght <= count:
                max_lenght = count
        print(
            f'Read file:{filename} lines:{line_count} lines.')
    with open('./output/'+filename+'.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = ["ADJ", "ADJ_COUNT", "ADP", "ADP_COUNT", "ADV", "ADV_COUNT", "AUX", "AUX_COUNT",
                      "CCONJ", "CCONJ_COUNT", "DET", "DET_COUNT", "INTJ", "INTJ_COUNT", "NOUN", "NOUN_COUNT", "NUM", "NUM_COUNT",
                      "PART", "PART_COUNT", "PRON", "PRON_COUNT", "PROPN", "PROPN_COUNT", "PUNCT", "PUNCT_COUNT",
                      "SCONJ", "SCONJ_COUNT", "SYM", "SYM_COUNT", "VERB", "VERB_COUNT", "X", "X_COUNT"]

        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()

        i = 0

        while(i < max_lenght):
            adj_word = " "
            adj_count = " "
            adp_word = " "
            adp_count = " "
            adv_word = " "
            adv_count = " "
            aux_word = " "
            aux_count = " "
            cconj_word = " "
            cconj_count = " "
            det_word = " "
            det_count = " "
            intj_word = " "
            intj_count = " "
            noun_word = " "
            noun_count = " "
            num_word = " "
            num_count = " "
            part_word = " "
            part_count = " "
            pron_word = " "
            pron_count = " "
            propn_word = " "
            propn_count = " "
            punct_word = " "
            punct_count = " "
            sconj_word = " "
            sconj_count = " "
            sym_word = " "
            sym_count = " "
            verb_word = " "
            verb_count = " "
            x_word = " "
            x_count = " "

            if i < len(output_data[0]["data"]):
                adj_word = output_data[0]["data"][i]["word"]
                adj_count = output_data[0]["data"][i]["count"]
            if i < len(output_data[1]["data"]):
                adp_word = output_data[1]["data"][i]["word"]
                adp_count = output_data[1]["data"][i]["count"]
            if i < len(output_data[2]["data"]):
                adv_word = output_data[2]["data"][i]["word"]
                adv_count = output_data[2]["data"][i]["count"]
            if i < len(output_data[3]["data"]):
                aux_word = output_data[3]["data"][i]["word"]
                aux_count = output_data[3]["data"][i]["count"]
            if i < len(output_data[4]["data"]):
                cconj_word = output_data[4]["data"][i]["word"]
                cconj_count = output_data[4]["data"][i]["count"]
            if i < len(output_data[5]["data"]):
                det_word = output_data[5]["data"][i]["word"]
                det_count = output_data[5]["data"][i]["count"]
            if i < len(output_data[6]["data"]):
                intj_word = output_data[6]["data"][i]["word"]
                intj_count = output_data[6]["data"][i]["count"]
            if i < len(output_data[7]["data"]):
                noun_word = output_data[7]["data"][i]["word"]
                noun_count = output_data[7]["data"][i]["count"]
            if i < len(output_data[8]["data"]):
                num_word = output_data[8]["data"][i]["word"]
                num_count = output_data[8]["data"][i]["count"]
            if i < len(output_data[9]["data"]):
                part_word = output_data[9]["data"][i]["word"]
                part_count = output_data[9]["data"][i]["count"]
            if i < len(output_data[10]["data"]):
                pron_word = output_data[10]["data"][i]["word"]
                pron_count = output_data[10]["data"][i]["count"]
            if i < len(output_data[11]["data"]):
                propn_word = output_data[11]["data"][i]["word"]
                propn_count = output_data[11]["data"][i]["count"]
            if i < len(output_data[12]["data"]):
                punct_word = output_data[12]["data"][i]["word"]
                punct_count = output_data[12]["data"][i]["count"]
            if i < len(output_data[13]["data"]):
                sconj_word = output_data[13]["data"][i]["word"]
                sconj_count = output_data[13]["data"][i]["count"]
            if i < len(output_data[14]["data"]):
                sym_word = output_data[14]["data"][i]["word"]
                sym_count = output_data[14]["data"][i]["count"]
            if i < len(output_data[15]["data"]):
                verb_word = output_data[15]["data"][i]["word"]
                verb_count = output_data[15]["data"][i]["count"]
            if i < len(output_data[16]["data"]):
                x_word = output_data[16]["data"][i]["word"]
                x_count = output_data[16]["data"][i]["count"]

            writer.writerow({"ADJ": adj_word, "ADJ_COUNT": adj_count, "ADP": adp_word, "ADP_COUNT": adp_count,
                             "ADV": adv_word, "ADV_COUNT": adv_count, "AUX": aux_word, "AUX_COUNT": aux_count,
                             "CCONJ": cconj_word, "CCONJ_COUNT": cconj_count, "DET": det_word, "DET_COUNT": det_count,
                             "INTJ": intj_word, "INTJ_COUNT": intj_count, "NOUN": noun_word, "NOUN_COUNT": noun_count,
                             "NUM": num_word, "NUM_COUNT": num_count, "PART": part_word, "PART_COUNT": part_count,
                             "PRON": pron_word, "PRON_COUNT": pron_count, "PROPN": propn_word, "PROPN_COUNT": propn_count,
                             "PUNCT": punct_word, "PUNCT_COUNT": punct_count, "SCONJ": sconj_word, "SCONJ_COUNT": sconj_count,
                             "SYM": sym_word, "SYM_COUNT": sym_count, "VERB": verb_word, "VERB_COUNT": verb_count,
                             "X": x_word, "X_COUNT": x_count})

            i += 1


def unique(sentence):

    # insert the list to the set
    list_set = set(sentence)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list


def transform(filename):

    dataforwrite = []
    with open('./data/'+filename+'.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        for row in csv_reader:
            mystring = row[filename]
            mystring = mystring.replace(' (', '(')
            mystring = mystring.replace("', '", ' - ')
            mystring = mystring.replace("'", '')
            mystring = mystring.replace('(ไม่ - PART),(', '(*')
            dataforwrite.append(mystring)

    with open('./transformed/'+filename+'.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = [filename]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for data in dataforwrite :
            writer.writerow({filename:data})
        


def fre_pos_nag():
    files_name = ["patong_google", "promthep_google",
                  "wat_google", "patong_trip", "promthep_trip", "wat_trip"]
    for file_name in files_name:
        if file_name == 'wat_google' or file_name == 'promthep_trip':
            #count_frequency(f'{file_name}_positive')
            transform(f'{file_name}_positive')
        else:
            #count_frequency(f'{file_name}_positive')
            #count_frequency(f'{file_name}_negative')
            transform(f'{file_name}_positive')
            transform(f'{file_name}_negative')

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

def frequncy_noun(filename):
    all_words = []
    with open('./transformed/'+filename+'.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)   
        
        for row in csv_reader:
            matrixAr = []
            comment = row["comment"]

            b = comment.replace("[[", "").replace("]]", "")
            for line in b.split('], ['):
                row_ = list(line.split(','))
                matrixAr.append(row_)
            unique_words = []
            for sentence in matrixAr:
                for word in sentence:
                    unique_words.append(word)
            all_words.extend(unique_words)
        
    bf = dict(Counter(all_words))  # counting words
    af = {k: bf[k]
        for k in sorted(bf, key=bf.get, reverse=True)}  # sort asending
    with open('./frequency_noun/'+filename+'.csv', mode='w', newline='', encoding='utf-8') as writefile:
        fieldnames = ["noun","count"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)
        writer.writeheader()
        for element in af :
            if element.find("NOUN") != -1:
                noun  =  element
                count = af.get(element, '')
                writer.writerow({"noun":noun,"count":count})

def frequncy_nouns() :
    filesname = ["google","tripadvisor"]
    places = ["patong","promthep","wat"]
    for file in filesname :
        for place in places:
            frequncy_noun(f'{place}_{file}')

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

def tf_idf_fun(domain_name) :
    lines = 0
    with open('./domain/'+domain_name+'_noun.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        lines= len(list(csv_reader))
    percentile = 80
    top_lines = int(lines-percentile/100*(lines+1))


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
    with open('./domain/'+domain_name+'_pos.csv', mode='r', encoding='utf-8') as csv_file:
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
                                if word_left.find("ADJ") != -1 or\
                                    word_left.find("ADV") != -1 or\
                                        word_left.find("VERB") != -1:
                                    words_match.append({"word":word_left,"noun":noun
                                    ,"position":"left","range":count_left,"index":left})
                                count_left +=1
                                left -=1
                            while right <len(sentence) and count_right<=4:
                                word_right = sentence[right]
                                if word_right.find("ADJ") != -1 or\
                                    word_right.find("ADV") != -1 or\
                                        word_right.find("VERB") != -1:
                                    words_match.append({"word":word_right,"noun":noun
                                    ,"position":"right","range":count_right,"index":right})
                                count_right +=1
                                right +=1
                        index +=1
    with open('./domain/'+domain_name+'_match_pos.csv', mode='w', newline='', encoding='utf-8') as writefile:
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
    with open('./domain/'+domain_name+'_pos.csv', mode='r', encoding='utf-8') as csv_file:
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
    with open('./domain/'+domain_name+'_pos.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        count_comment= len(list(csv_reader))
    print(count_comment)
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
        print(word_c,tf,idf,tf_idf)


tf_idf_fun("patong")