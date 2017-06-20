import os
import time
import pdb
import file_path

def word_count(howoften, often_index, nowtime):
    issue_dir = ['30minute', 'today', 'thisweek']

    now = time.localtime()
    now_float = time.time()

    path = file_path.get_file_path()

    file_name_list = os.listdir(path['data_path'])
    freq_file_name_list = []
    arti_file_name_list = []

    summary_path = path['summary_path'] + "summary.txt"
    daily_summary_path = path['summary_path'] + 'daily_summary.txt'
    weekly_summary_path = path['summary_path'] + 'weekly_summary.txt'
    if nowtime == 960:
        past_float = now_float - 360
        string_nowtime = "%04d%02d%02d" % (time.localtime(past_float).tm_year, time.localtime(past_float).tm_mon, time.localtime(past_float).tm_mday)
    else:
        string_nowtime = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

    if often_index == 0:
        f = open(summary_path, 'r', encoding='utf-8')
        #병합할 파일들 리스트 만들기
        for file_name in file_name_list:
            filetime = (int(file_name[13:15]) - 8) * 60 + int(file_name[15:17])
            if(file_name[0:4] == 'freq') and (file_name[5:13] == string_nowtime) and nowtime - filetime <= howoften:
                freq_file_name_list.append(file_name)
            if(file_name[0:4] == 'arti') and (file_name[5:13] == string_nowtime) and nowtime - filetime <= howoften:
                arti_file_name_list.append(file_name)
    if often_index == 1:
        f = open(daily_summary_path, 'r', encoding='utf-8')
        for file_name in file_name_list:
            if (file_name[0:4] == 'freq') and (file_name[5:13] == string_nowtime):
                freq_file_name_list.append(file_name)
            if (file_name[0:4] == 'arti') and (file_name[5:13] == string_nowtime):
                arti_file_name_list.append(file_name)
    if often_index == 2:
        f = open(weekly_summary_path, 'r', encoding='utf-8')
        week = now.tm_wday
        for i in range(week + 1):
            now_float = now_float - 86400
            string_nowtime = "%04d%02d%02d" % (time.localtime(now_float).tm_year, time.localtime(now_float).tm_mon, time.localtime(now_float).tm_mday)
            for file_name in file_name_list:
                if (file_name[0:4] == 'freq') and (file_name[5:13] == string_nowtime):
                    freq_file_name_list.append(file_name)
                if (file_name[0:4] == 'arti') and (file_name[5:13] == string_nowtime):
                    arti_file_name_list.append(file_name)


    score_list = []
    topic_list = []
    section_list = []
    link_list = []

    article_dictionary = {}

    word_list = []
    temp_list = []
    if(len(freq_file_name_list) == 0):
        return

    tweet_count = 0
    article_tweet_count = 0
    for file in arti_file_name_list:
        f_word = open(path['data_path'] + file, 'r', encoding='utf-8')
        total_word = f_word.read()
        temp_list = total_word.split('\n')
        tweet_count += int(temp_list[0])
        article_tweet_count += int(temp_list[1])
        del temp_list[1]
        del temp_list[0]
        for line in temp_list:
            if(line == ''):
                break
            index = line.find('|')
            sentence = line[:index - 1]
            word_freq = int(line[index+2:])
            if sentence not in article_dictionary and sentence != '':
                article_dictionary[sentence] = word_freq
            else:
                article_dictionary[sentence] += word_freq
        f_word.close()

#week_summary에서 article_score_list, article_section_list 불러오기




    news_full_word = f.read()
    list_news_word = news_full_word.split('\n')
    for temp_split in list_news_word:
        if temp_split == '':
            continue
        list_temp_split = temp_split.split('|')
        if len(list_temp_split) == 1 or list_temp_split[0] == '':
            continue
        one_sentence = list_temp_split[1]
        if one_sentence not in article_dictionary and one_sentence != '':
            continue
        score_list.append(article_dictionary[one_sentence])
        topic_list.append(one_sentence)
        link_list.append(list_temp_split[3])
        if len(list_temp_split) > 2:
            section_list.append(int(list_temp_split[2]))
        else:
            section_list.append(4)
    f.close()

    #message 선택
    for i in range(len(score_list)):
        for j in range(i, len(score_list)):
            if score_list[i] < score_list[j]:
                temp = score_list[i]
                score_list[i] = score_list[j]
                score_list[j] = temp
                temp_string = topic_list[i]
                topic_list[i] = topic_list[j]
                topic_list[j] = temp_string
                temp_int = section_list[i]
                section_list[i] = section_list[j]
                section_list[j] = temp_int
                temp_link = link_list[i]
                link_list[i] = link_list[j]
                link_list[j] = temp_link

#여기서 바뀌어야 함
    message = topic_list[0]
    share = score_list[0] / article_tweet_count * 100
    f_send = open(path['issue_path'] + issue_dir[often_index] + '/sending_all.txt', 'w',
                  encoding='utf-8')
    f_send.write('|6\n')
    f_send.write(message)
#    f_share = open(path['issue_path'] + issue_dir[often_index] + '/sending_all_share.txt', 'w',
#                   encoding='utf-8')
    share_string = "%0.1f" % share
    score = str(score_list[0])
    count = str(article_tweet_count)
    str_tweet_count = str(tweet_count)
    f_send.write('\n' + share_string + '\n' + score + '\n' + count + '\n' + str_tweet_count + '\n' + link_list[0])


    check= [0,0,0,0,0,0]
    for j in range(1, len(topic_list[1:])):
        if check[0] == 1 and check[1] == 1 and check[2] == 1 and check[3] == 1 and check[4] == 1 and check[5] == 1:
            break

        message = topic_list[j]
        share = score_list[j] / article_tweet_count * 100
        if check[section_list[j]] == 0:
#            f_send = open(path['issue_path'] + issue_dir[often_index] + '/sending_' + str(section_list[j]) + '_message.txt', 'w', encoding='utf-8')
            f_send.write('\n|' + str(section_list[j]) + '\n')
            f_send.write(message)
#            f_share = open(path['issue_path'] + issue_dir[often_index] + '/sending_' + str(section_list[j]) +'_share.txt', 'w', encoding='utf-8')
            share_string = "%0.1f" % share
            score = str(score_list[j])
            count = str(article_tweet_count)
            str_tweet_count = str(tweet_count)


            f_send.write('\n' + share_string + '\n' + score + '\n' + count + '\n' + str_tweet_count + '\n' + link_list[j])
            check[section_list[j]] = 1

    f_send.close()
#    f_update = open(path['issue_path'] + 'update_time.txt', 'r', encoding='utf-8')
#    update_times = f_update.read()
#    f_update.close()

#    update_time_list = update_times.split('\n')
#    for k in range(len(update)):
#        if update[k] == 1:
#           update_time_list[often_index * 7 + k] = str(now_float)

#    f_update = open(path['issue_path'] + 'update_time.txt', 'w', encoding='utf-8')
#    for update_time in update_time_list:
#        f_update.write(update_time + '\n')
#    f_update.close()

    del topic_list
    del arti_file_name_list
    del freq_file_name_list
    del word_list
    del temp_list
    del score_list
    del section_list
    del link_list

    print(issue_dir[often_index] + " done")


