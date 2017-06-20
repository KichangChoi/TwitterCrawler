import time
import tweepy
import file_path

def crawl_tweetdata():

    #tweetter에서 계정당 하나씩 제공하는 key와 token
    consumer_key='AAAAAAAAAAAAAAAA'
    consumer_secret='AAAAAAAAAAAAAAAA'
    access_token='AAAAAAAAAAAAAAAA'
    access_token_secret='AAAAAAAAAAAAAAAA'

    now = time.localtime()

    string_nowtime = "%04d%02d%02d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)

    path = file_path.get_file_path()

    file_name = path['data_path'] + 'data_' + string_nowtime + '.txt'

    # 파일 data 출력
    f = open(file_name, encoding='utf-8', mode='w')

    word_dictionary = {}
    word_list = []
    article_list = []
    sentence_list = []
    issue_list = []

    weekly_summary_path = path['summary_path'] + 'weekly_summary.txt'


    #뉴스 word 메모리로 로드
    file_summary = open(weekly_summary_path, 'r', encoding='utf-8')

    temp_split = file_summary.read()
    list_temp_split = temp_split.split('\n')
    for temp_split in list_temp_split:
        if temp_split == '':
            continue
        list_temp_split = temp_split.split('|')
        temp_split = list_temp_split[0]
        article_list.append(list_temp_split[0])
        if len(list_temp_split) < 3:
            sentence_list.append(list_temp_split[0])
        else:
            sentence_list.append(list_temp_split[1])
        issue_list.append(0)
        list_temp_split = temp_split.split(',')
        for word in list_temp_split:
            if word not in word_dictionary and word != '':
                word_dictionary[word] = 0
                word_list.append(word)

    tweet_count = 0
    tweet_article_count = 0

    while True:
        exit_flag = 0
        #key, token을 사용하여 user auth 접속
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, api_root= '/1.1')

        array_text = []
        array_date = []

        #중복 tweet check flag
        flag = 0

        try:
        #tweet 수집 핵심 loop
        #지정한 갯수만큼 텍스트를 획득한 이후 loop 탈출함
            for tweet in tweepy.Cursor(api.search,
                                       geocode='35.874,128.246,400km',
                                       #q=query_keyword,
                                       #since="2016-08-06 05:00",
                                       #until="2016-08-06 05:15",
                                       lang = 'ko',
                                       count = 100).items():

                #15 분당 180번 요청 제한에 걸리지 않기 위한 브레이크
                #한계량의 절반정도 수준에서 수집이 가능
                time.sleep(0.1)

                #무의미한 광고나 링크를 1차적으로 필터링
                if tweet.text.count('#') > 1 \
                        or tweet.text.count('https') > 0 \
                        or tweet.text.count('http') > 0 \
                        or tweet.text.count('★') > 2 \
                        or tweet.text.count('♡') > 5 \
                        or tweet.text.count('△') > 2 \
                        or tweet.text.count('▶') > 2 \
                        or tweet.text.count('▷') > 0 \
                        or tweet.text.count('토토') > 0 \
                        or tweet.text.count('배팅') > 0 \
                        or tweet.text.count('|') > 0:
                    continue;

                else:
                    #tweetter에서 무의미하게 대량으로 발생하는
                    # '@dsfkje' 등의 대량 리트윗을 막기위한 block
                    # '@'로 시작되는 단어를 삭제함
                    while True:
                        at_index =  tweet.text.find('@')
                        if at_index != -1:
                            for i in range(at_index, len(tweet.text)):
                                if tweet.text[i] == ' ' or i == len(tweet.text) - 1:
                                    first_text = tweet.text[0:at_index]
                                    last_text = tweet.text[i + 1:len(tweet.text)]
                                    tweet.text = first_text + last_text
                                    break
                        else:
                            break

                    #이전 수집 tweet중 중복되는 텍스트가 있을 경우 필터링
                    for text in array_text:
                        if text == tweet.text:
                            flag = 1;
                            break
                    if flag == 1:
                        flag = 0
                        continue

                    array_text.append(tweet.text)
                    da = str(tweet.created_at)
                    tweet_count += 1
                    if tweet_count % 500 == 0:
                        print(tweet_count)

                    #뉴스 noun count 출력 기사별
                    for word in word_list:
                        if tweet.text.find(word) != -1:
                            word_dictionary[word] += 1

                    check_flag = 0
                    article_index = 0
                    for article in article_list:
                        word_in_article_list = article.split(',')
                        for word_in_article in word_in_article_list:
                            if tweet.text.find(word_in_article) != -1 and word_in_article != "":
                                issue_list[article_index] += 1
                                check_flag = 1
                                break
                        article_index += 1

                    if check_flag == 1:
                        tweet_article_count += 1


                    f.write(da + '  |  ')
                    f.write('Tweet : ' + tweet.text +'|')
                    f.write('\n\n')

                present = time.localtime()
                a = (now.tm_hour * 60) + now.tm_min
                b = (present.tm_hour * 60) + present.tm_min
                #######빠져나오는 시간 수정
                if b != a and b % 15 == 0:
                    exit_flag = 1
                    break
        except tweepy.error.RateLimitError:
            print('Timeout, retry in 5 minutes...\n')
            time.sleep(60 * 5)
            continue
        except tweepy.error.TweepError as er:
            print('TweepError')
            continue

        if exit_flag == 1:
            f.close()
            file_frequency = open(path['data_path'] + 'freq_' + string_nowtime + '.txt', 'w', encoding='utf-8')
            for word in word_list:
                file_frequency.write(word +' : '+ str(word_dictionary[word]) + '\n')
            file_frequency.close()

            file_article = open(path['data_path'] + 'arti_' + string_nowtime + '.txt', 'w', encoding='utf-8')
            file_article.write(str(tweet_count) + '\n' + str(tweet_article_count) + '\n')

            for i in range(len(sentence_list)):
                file_article.write(sentence_list[i] +' | '+ str(issue_list[i]) + '\n')
            file_article.close()
            #뉴스별 워드 카운트 파일 저장
            break

    del word_dictionary
    del word_list
    del list_temp_split
    del array_text
    del array_date
    del article_list
    del issue_list
    del sentence_list

#오늘, 문제, 때문, 국민, 입장
