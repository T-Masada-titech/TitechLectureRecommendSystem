# 参考：https://qiita.com/pocket_kyoto/items/1e5d464b693a8b44eda5
import sqlite3
import os
sysFile = os.path.dirname(os.path.abspath(__file__))

# 含まれるテーブルの確認
# cur = conn.execute("select name from sqlite_master where type='table'")
# for row in cur:
#     print(row)
# 特定の単語を入力とした時に、類義語を検索する関数


def SearchSimilarWords(word):
    if os.path.exists(sysFile + "/wnjpn.db"):
        conn = sqlite3.connect(sysFile + "/wnjpn.db")
    else:
        print("wnjpn.db does not exist")
    # 問い合わせしたい単語がWordnetに存在するか確認する
    cur = conn.execute("select wordid from word where lemma='%s'" % word)
    word_id = 99999999  # temp
    for row in cur:
        word_id = row[0]

    # Wordnetに存在する語であるかの判定
    if word_id == 99999999:
        #         print("「%s」は、Wordnetに存在しない単語です。" % word)
        return
#     else:
#         print("【「%s」の類似語を出力します】\n" % word)

    # 入力された単語を含む概念を検索する
    cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
    synsets = []
    for row in cur:
        synsets.append(row[0])

    # 概念に含まれる単語を検索して画面出力する
    no = 1
    similar_words = []
    for synset in synsets:
        cur1 = conn.execute("select name from synset where synset='%s'" % synset)
#         for row1 in cur1:
#             print("%sつめの概念 : %s" %(no, row1[0]))
        cur2 = conn.execute(
            "select def from synset_def where (synset='%s' and lang='jpn')" %
            synset)
        sub_no = 1
        for row2 in cur2:
            #             print("意味%s : %s" %(sub_no, row2[0]))
            sub_no += 1
        cur3 = conn.execute(
            "select wordid from sense where (synset='%s' and wordid!=%s)" %
            (synset, word_id))
        sub_no = 1
        for row3 in cur3:
            target_word_id = row3[0]
            cur3_1 = conn.execute("select lemma from word where wordid=%s" % target_word_id)
            for row3_1 in cur3_1:
                #                 print("類義語%s : %s" % (sub_no, row3_1[0]))
                similar_words.append(row3_1[0])
                sub_no += 1
#         print("\n")
        no += 1
    return similar_words
# lis = SearchSimilarWords('猫')
# print(lis)
