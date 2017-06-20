# -*- coding: utf-8 -*-


#기자 =
#[한겨래][ㅇ라널] 첫문단만 가지고 해볼것
#바로 시작
#】
#3문장까지 X일 없으면 첫문장
#X일이 있으면 포함된 문장

#X일이 없는경우 칼럼 and 기자라는 언급이 1번 이하이면
#[앵커] 영상뉴스
def summation(article):

    #영상 뉴스 수집하지 않음
    if article.count('앵커') > 0:
        return False

    if article[:150].count('=') > 0:
        article = article[article[:150].rfind('=') + 1:]

    if article[:10].count(')') > 0:
        article = article[article[:20].rfind(')') + 1:]

    if article[:100].count(']') > 0:
        article = article[article[:100].rfind(']') + 1:]

    if article[:100].count('】') > 0:
        article = article[article[:100].rfind('】') + 1:]

    list_sentence = split_article(article)

    index = 0
    for sentence in list_sentence:
        if sentence.count('1일') > 0 \
                or sentence.count('2일') > 0 \
                or sentence.count('3일') > 0 \
                or sentence.count('4일') > 0 \
                or sentence.count('5일') > 0 \
                or sentence.count('6일') > 0 \
                or sentence.count('7일') > 0 \
                or sentence.count('8일') > 0 \
                or sentence.count('9일') > 0 \
                or sentence.count('0일') > 0:
            sentence = sentence.replace('\t', '')
            sentence = sentence.replace('\n', '')
            sentence = sentence.replace('\r', '')
            sentence = sentence.strip()
            return sentence
        else:
            index += 1
            if index == 3:
                return False
#precision을 극대화 recall이 약간 올라가더라도
#                if article.count('기자') == 0:
#                    return False
#                else:
#                    list_sentence[0] = list_sentence[0].replace('\t', '')
#                    list_sentence[0] = list_sentence[0].strip()
#                    return list_sentence[0]

    return False

def split_article(article):
    list_sentence = []
    temp_sentence = ''
    while True:
        q_index = article.find('?')
        index = article.find('.')
        if  index == -1:
            break
        if q_index < index and q_index != -1:
            list_sentence.append(temp_sentence + article[:index + 1])
            article = article[index + 1:]
            temp_sentence = ''
            continue
        if article[index - 1] == '다':
            if len(article) > index + 1:
                #chr(8217)은 ’chr(8221)은 ” 로서 (") (') 과는 다르다. 좌우를 구분하는 따옴표
                #ord(") = 34
                if article[index + 1] == '"' or article[index + 1] == "'"or article[index + 1] == chr(8217)or article[index + 1] == chr(8221):
                    list_sentence.append(temp_sentence + article[:index + 2])
                    article = article[index + 2:]
                else:
                    list_sentence.append(temp_sentence + article[:index + 1])
                    article = article[index + 1:]
            else:
                list_sentence.append(temp_sentence + article[:index + 1])
                article = article[index + 1:]
            temp_sentence = ''
        else:
            temp_sentence += article[:index + 1]
            article = article[index + 1 :]

    return list_sentence

'''
string = '소나기에 불어난 하천…고립된 도심 피서객    (광주=연합뉴스) 정회성 기자 = 7일 오후 3시 10분께 광주 북구 임동 광주천 광운교 아래에서 119구조대가 소나기로 불어난 하천에 고립된 시민 3명을 구하고 있다. 2016.8.7 [광주 서부소방서 제공=연합뉴스]    (광주=연합뉴스) 정회성 기자 = 7일 오후 3시 10분께 광주 북구 임동 광주천 광운교 아래에서 이모(73)씨 등 피서객 3명이 불어난 하천에 고립됐다가 구조됐다.    신고를 받고 출동한 119소방구조대는 로프 등 장비를 이용해 이씨 등을 다리 위로 끌어올렸다. 3명 모두 건강에 이상이 없는 상태다.    소방당국 관계자는 "상류 쪽에 내린 소나기로 광주천 수위가 갑자기 올라갔는데, 이씨 등은 비가 내리지 않은 곳에 머물고 있어 이런 사실을 몰랐던 것 같다"고 말했다.    hs@yna.co.kr'

one_sentence = summation(string)

print(one_sentence)
print(string)
'''