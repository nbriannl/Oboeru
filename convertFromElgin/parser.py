import pandas as pd

def main():
    lines = open("compilation.txt", "r", encoding="utf8")

    df = pd.DataFrame(columns=['lesson', 'pos', 'hasKatakanaOrKanji', 'preJapanese', 'japaneseAllHiragana', 'japanese', 'postJapanese', 
                                    'preEnglish','english', 'postEnglish'])
    lesson = None
    for line in lines.readlines():
        string = line.strip()
        if string[:5] == '_____':
            lesson = string[5:]
        else: 
            entry = parseString(string, lesson)
            df = df.append({
                    'lesson': entry['lesson'],
                    'pos': entry['pos'],
                    'hasKatakanaOrKanji': entry['hasKatakanaOrKanji'], 
                    'preJapanese': entry['preJapanese'],
                    'japaneseAllHiragana': entry['japaneseAllHiragana'],
                    'japanese': entry['japanese'],
                    'preEnglish': entry['preEnglish'],
                    'english': entry['english'],
                    'postEnglish': entry['postEnglish']
            }, ignore_index=True)
    print(df)
    df.to_excel("output.xlsx") 

def parseString(string, lesson):
    if lesson is None:
        raise Exception('Lesson cannot be None', string)
    input = string

    splitString = string.split(' ')
    japanese = splitString[0]
    english = ' '.join(splitString[1:])

    pairs = getBracketPairs(japanese)
    pairs_sorted_by_first = sorted(pairs, key=lambda tup: tup[0])

    preClause = None
    if len(pairs_sorted_by_first) > 0:
        firstPair = pairs_sorted_by_first[0]
        if firstPair[0] == 0:
            preClause = getSubstring(japanese, firstPair[0] + 1, firstPair[1])
            newjapanese = japanese[firstPair[1]+1:]
            newpairs = getBracketPairs(newjapanese)
            pairs_sorted_by_first = sorted(newpairs, key=lambda tup: tup[0])
            japanese = newjapanese


    hiragana_list = []
    for pair in pairs_sorted_by_first:
        hiragana = getSubstring(japanese, pair[0] + 1, pair[1])
        hiragana_list.append((pair[0], pair[1], hiragana))

    hasKatakanaOrKanji = None 
    kanji_extracted = extract_unicode_block(kanji, japanese)
    doesStringHaveKanji = len(kanji_extracted) > 0
    if doesStringHaveKanji:
        hasKatakanaOrKanji = 'J'
        compressed_indices = convertAllKanjiToIndices(japanese, kanji_extracted)
        ranges = getRangesFromCompress(compressed_indices)
        kanji_list = connectKanji(japanese, ranges)
        matches = findMatches(hiragana_list, kanji_list, japanese)
        stringKanji, stringHiragana = replaceString(japanese, matches)
    else:
        stringKanji = japanese
        stringHiragana = japanese

    partOfSpeech = None
    preEnglish = None
    postEnglish = None

    if stringKanji[0] in ['ー', '〜']:
        preClause = stringKanji[0]
        stringKanji = stringKanji[1:]
        stringHiragana = stringHiragana[1:]
    if stringKanji[-3:] == '（な）':
        partOfSpeech = 'な-adj'
        stringKanji = stringKanji[:-3]
        stringHiragana = stringHiragana[:-3]
    elif stringKanji[-2:] == 'ます':
        partOfSpeech = 'v'
        indexopening = english.find('(')
        indexclosing = english.find(')')
        if indexopening != -1 and indexclosing != -1:
            verbObject = getSubstring(english, indexopening + 1, indexclosing)
            english = english.replace('(' + verbObject + ')', '') 
            if english[0] == ' ':
                preEnglish = verbObject
            else:
                postEnglish = verbObject
            english = english.strip()

    # print('===')
    # print('>input :', input)
    # print('===')
    # print('lesson:', lesson)
    # if partOfSpeech is not None: 
    #     print('pos   :', partOfSpeech)   
    # if preClause is not None: 
    #     print('pre-jp:', preClause)    
    # print('kanji :', stringKanji)
    # print('kana  :', stringHiragana)
    # if preEnglish is not None:
    #     print('pre-en:', preEnglish)
    # print('eng   :', english)
    # if postEnglish is not None:
    #     print('posten:', postEnglish)

    entry = {
        'lesson': lesson,
        'pos': partOfSpeech,
        'hasKatakanaOrKanji': hasKatakanaOrKanji, 
        'preJapanese': preClause,
        'japaneseAllHiragana': stringHiragana,
        'japanese': stringKanji,
        'preEnglish': preEnglish,
        'english': english,
        'postEnglish': postEnglish
    }
    return entry


def replaceString(originalstring, matches):
    stringKanji = originalstring
    stringHiragana = originalstring
    if len(matches) == 1:
        match = matches[0]
        leftbound = match[0]
        rightbound = match[2]
        left = originalstring[:leftbound]
        right = originalstring[rightbound+1:]
        stringKanji = left + match[3] + right
        stringHiragana = left + match[4] + right
    elif len(matches) > 1:
        stringKanji = ''
        stringHiragana = ''
        for index in range(0, len(matches)):
            # print('index:', index)
            curr_match = matches[index]
            leftbound = curr_match[0]
            rightbound = curr_match[2]

            if index == 0:
                next_match = matches[index + 1]
                rightbound_prev_segment = 0
                leftbound_next_segment = next_match[0]
            elif (index == len(matches) - 1):
                prev_match = matches[index - 1]
                rightbound_prev_segment = prev_match[2]
                leftbound_next_segment = len(originalstring)
            else:
                prev_match = matches[index - 1]
                next_match = matches[index + 1]
                rightbound_prev_segment = prev_match[2]
                leftbound_next_segment = next_match[0]
            
            left = originalstring[rightbound_prev_segment+1:leftbound]
            right = originalstring[rightbound+1:leftbound_next_segment]
            stringKanji += left + curr_match[3]
            stringHiragana += left + curr_match[4]
        stringKanji += right
        stringHiragana += right
    return stringKanji, stringHiragana
    
def findMatches(hiragana_list, kanji_list, string):
    matches = []
    for hiragana in hiragana_list:
        for kanji in kanji_list:
            if hiragana[0] == kanji[1]:
                # print(kanji, 'matches', hiragana)
                matches.append((kanji[0], kanji[1], hiragana[1], kanji[2], hiragana[2], getSubstring(string, kanji[0], hiragana[1] + 1)))
    return matches

def connectKanji(string, ranges):
    connectedRanges = []
    for range in ranges:
        substring = getSubstring(string, range[0], range[1])
        connectedRanges.append((range[0], range[1], substring))
    return connectedRanges

# replace all kanji with their index location w.r.t. to the string
def convertAllKanjiToIndices(string, kanji_extracted):
    indices = []
    for kanji in kanji_extracted:
        index = string.index(kanji)
        indices.append(index)
    if len(indices) > 0:
        compressed_indices = compressIndices(indices)
    else:
        compressed_indices = indices
    return compressed_indices

def compressIndices(indices):
    if len(indices) == 1:
        return [(indices[0], 1)]
    length = 1
    compressed_indices = []
    for index in range(1, len(indices)):
        currElem = indices[index]
        prevElem = indices[index - 1] 
        if (currElem - prevElem) == 1:
            length += 1
        else:
            compressed_indices.append((prevElem, length))
            length = 1
    prevElem = indices[-1]
    compressed_indices.append((prevElem, length))
    return compressed_indices    
        
# given [(2, 2), (11, 1)]
# output[(1, 3), (11, 12)]
# 2 - 2 + 1, 2 + 1, 11 - 1 + 1, 11 + 1       
def getRangesFromCompress(compressed_indices):
    ranges = []
    for elem in compressed_indices:
        start = elem[0] - elem[1] + 1
        end = elem[0] + 1
        ranges.append((start,end))
    return ranges

def getBracketPairs(string):
    stack_opening = []
    ranges = []
    for index, character in enumerate(string):
        if character == '（':
            stack_opening.append(index)
        elif character == '）':
            index_opening_bracket = stack_opening.pop()
            ranges.append((index_opening_bracket, index))
    return ranges

# from [start_index, end_index) 
def getSubstring(string, start_index, end_index):
    subString = string[start_index:end_index]
    return subString

# returns indices for ch in s
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


# -*- coding: utf-8 -*-
import re

''' This is a library of functions and variables that are helpful to have handy 
	when manipulating Japanese text in python.
	This is optimized for Python 3.x, and takes advantage of the fact that all strings are unicode.
	Copyright (c) 2014-2015, Mads Sørensen Ølsgaard
	All rights reserved.
	Released under BSD3 License, see http://opensource.org/licenses/BSD-3-Clause or license.txt '''

## UNICODE BLOCKS ##

# Regular expression unicode blocks collected from 
# http://www.localizingjapan.com/blog/2012/01/20/regular-expressions-for-japanese-text/

hiragana_full = r'[ぁ-ゟ]'
katakana_full = r'[゠-ヿ]'
kanji = r'[㐀-䶵一-鿋豈-頻]'
radicals = r'[⺀-⿕]'
katakana_half_width = r'[｟-ﾟ]'
alphanum_full = r'[！-～]'
symbols_punct = r'[、-〿]'
misc_symbols = r'[ㇰ-ㇿ㈠-㉃㊀-㋾㌀-㍿]'
ascii_char = r'[ -~]'

## FUNCTIONS ##

def extract_unicode_block(unicode_block, string):
	''' extracts and returns all texts from a unicode block from string argument.
		Note that you must use the unicode blocks defined above, or patterns of similar form '''
	return re.findall( unicode_block, string)

def remove_unicode_block(unicode_block, string):
	''' removes all chaacters from a unicode block and returns all remaining texts from string argument.
		Note that you must use the unicode blocks defined above, or patterns of similar form '''
	return re.sub( unicode_block, '', string)

## EXAMPLES ## 

# text = '初めての駅 自由が丘の駅で、大井町線から降りると、ママは、トットちゃんの手を引っ張って、改札口を出ようとした。ぁゟ゠ヿ㐀䶵一鿋豈頻⺀⿕｟ﾟabc！～、〿ㇰㇿ㈠㉃㊀㋾㌀㍿'

# print('Original text string:', text, '\n')
# print('All kanji removed:', remove_unicode_block(kanji, text))
# print('All hiragana in text:', ''.join(extract_unicode_block(hiragana_full, text)))

if __name__ == '__main__':
    main()