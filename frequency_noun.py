
from konlpy.tag import Twitter
#from konlpy.tag import Komoran
import operator

#komoran = Komoran()
twitter = Twitter()

file_name = [   '20160806211301_data.txt' ]

for i in range (1):
    f = open('/home/alimiuser/sns_alimi/data/' + file_name[i], encoding='utf-8', mode='r')
    tweets = f.read()

    tweet_list = tweets.split('|')

    text_list = []
    text_dictionary = {}
    for one_tweet in tweet_list:
        if one_tweet[2:7] == 'Tweet' :
            text_list.append(one_tweet[10:])
        else:
            continue

    f = open('error.txt', 'w', encoding='utf-8')
    for text in text_list:
        f.write(text)
        noun_list = twitter.nouns(text.encode().decode('utf-8'))
        for noun in noun_list:
            if (noun in text_dictionary):
                text_dictionary[noun] += 1
            else:
                text_dictionary[noun] = 1

    a = sorted(text_dictionary.items(), key=operator.itemgetter(1), reverse=True)

    b = a

'''
    for text in positive_text_list:
        noun_list = twitter.nouns(text)
        for noun in noun_list:
            if (noun in positive_dictionary):
                positive_dictionary[noun] += 1
            else:
                positive_dictionary[noun] = 1

    for text in negative_text_list:
        noun_list = twitter.nouns(text)
        for noun in noun_list:
            if (noun in negative_dictionary):
                negative_dictionary[noun] += 1
            else:
                negative_dictionary[noun] = 1


a = sorted(positive_dictionary.items(), key=operator.itemgetter(1), reverse=True)
b = sorted(negative_dictionary.items(), key=operator.itemgetter(1), reverse=True)

a_count = 0
b_count = 0
a_index = 0
b_index = 0
a_list = []
b_list = []
a_flag = 0
b_flag = 0

while True:
    if a_count >= 20 and b_count >= 20:
        break
    if a_count >= 20:
        b_key = b[b_index][0]
        b_list.append(b_index)

        b_count += 1

        for i in range(len(a_list)):
            if (b_key == a[a_list[i]][0]):
                a_count -= 1
                b_count -= 1
                del a_list[i]
                del b_list[b_count]
                break

        b_index += 1
    else:
        if b_count >= 20:
            a_key = a[a_index][0]
            a_list.append(a_index)

            a_count += 1

            for i in range(len(b_list)):
                if (a_key == b[b_list[i]][0]):
                    a_count -= 1
                    b_count -= 1
                    del b_list[i]
                    del a_list[a_count]
                    break

            a_index += 1

        else:
            if a[a_index][0] != b[b_index][0]:
                a_key = a[a_index][0]  # 을 b_list에서 찾고
                b_key = b[b_index][0]  # 을 a_list에서 찾고 있으면 둘다 삭제 count -1
                a_list.append(a_index)
                b_list.append(b_index)

                a_count += 1
                b_count += 1

                for i in range(len(b_list)):
                    if(a_key == b[b_list[i]][0]):
                        a_count -= 1
                        b_count -= 1
                        del b_list[i]
                        del a_list[a_count]
                        break

                for i in range(len(a_list)):
                    if (b_key == a[a_list[i]][0]):
                        a_count -= 1
                        b_count -= 1
                        del a_list[i]
                        del b_list[b_count]
                        break


            a_index += 1
            b_index += 1

buz_file_pos = open('sorted_positive_nouns.txt', 'w')
buz_file_neg = open('sorted_negative_nouns.txt', 'w')

for k in a_list:
    buz_file_pos.write('%6s  |  빈도수 : %4d' % (a[k][0], a[k][1]))
    buz_file_pos.write('\n\n')


for k in b_list:
    buz_file_neg.write('%6s  |  빈도수 : %4d' % (b[k][0], b[k][1]))
    buz_file_neg.write('\n\n')
'''