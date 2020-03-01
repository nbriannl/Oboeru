import pandas as pd
from enum import Enum
from pykakasi import kakasi
import random
import json

class Vocabulary:
    def __init__(self):
        self.wordList = []
        self.partOfSpeechList = {}
        self.lessonList = {}

    def buildVocabulary(self):
        self.wordList, self.partOfSpeechList, self.lessonList = VocabularyBuilder().buildVocabulary('vocab.xlsx')

    def getVocabularySize(self):
        return len(self.wordList)

    def getWord(self, index):
        return self.wordList[index]

    def printWholeVocabulary(self):
        for word in self.wordList:
            print(word.__str__())
        input()

    def hasLesson(self, lessonNumber):
        return lessonNumber in self.lessonList

    def get3WordsSimilarPos(self, index):
        similarWords = []
        word = self.getWord(index)
        indicesWordsSimilarPOS = list(self.partOfSpeechList[word.partOfSpeech[0]])
        indicesWordsSimilarPOS.remove(index)
        if len(indicesWordsSimilarPOS) < 3:
            sampleIndicesWordSimilarPOS = indicesWordsSimilarPOS
        else:
            sampleIndicesWordSimilarPOS = random.sample(indicesWordsSimilarPOS, 3)
        for index in sampleIndicesWordSimilarPOS:
            similarWord = self.getWord(index)
            similarWords.append(similarWord)

        return similarWords

class Word:
    def __init__(self,  lesson, partOfSpeech, isTransitive, 
                    preJapanese, preJapaneseParticle, japanese_all_hiragana, japanese, postJapanese,
                    preEnglish, english, postEnglish):
        self.lesson = lesson # int
        self.partOfSpeech = partOfSpeech # list of PartOfSpeech Enum
        self.isTransitive = isTransitive
        self.preJapanese = preJapanese
        self.preJapaneseParticle = preJapaneseParticle
        self.japanese = japanese
        self.japanese_all_hiragana = japanese_all_hiragana
        self.postJapanese = postJapanese
        self.preEnglish = preEnglish
        self.english = english
        self.postEnglish = postEnglish

        if self.isTransitive is not None and PartOfSpeech.VERB not in self.partOfSpeech:
            raise Exception(self.japanese, self.partOfSpeech, self.isTransitive, " is not a verb but is either transitive/intransitive.")

    def getAsFullString(self, language, allHiragana=False):
        if language == 'jp':
            preString = self.preJapanese + self.preJapaneseParticle
            postString = self.postJapanese
        if language == 'en':
            preString = self.preEnglish
            postString = self.postEnglish
        
        if preString != '':
            preString = '[' + preString + ']'
        if postString != '':
            postString = '[' + postString + ']'
        
        if language == 'jp':
            if allHiragana:
                fullString = preString + self.japanese_all_hiragana + ' (' + self.japanese + ') '+ postString 
            else:
                fullString = preString + self.japanese + postString
        if language == 'en':
            if preString != '':
                fullString = preString + ' '
            else:
                fullString = ''
            fullString = fullString + self.english
            if postString != '': 
                fullString = fullString + ' ' + postString

            if self.isTransitive == True:
                fullString = fullString + ' ' + '(transitive)'
            elif self.isTransitive == False:
                fullString = fullString + ' ' + '(intransitive)'

        return fullString

    def getAsStringWithBlank(self, language):
        if language == 'jp':
            preString = self.preJapanese + self.preJapaneseParticle
            postString = self.postJapanese
        if language == 'en':
            preString = self.preEnglish
            postString = self.postEnglish
        
        if preString != '':
            preString = '[' + preString + ']'
        if postString != '':
            postString = '[' + postString + ']'
        
        if language == 'jp':
            stringWithBlank = preString + '(     ?     )' + postString
        if language == 'en':
            if preString != '':
                stringWithBlank = preString + ' '
            else:
                stringWithBlank = ''
            stringWithBlank = stringWithBlank + '(     ?     )'
            if postString != '': 
                stringWithBlank = stringWithBlank + ' ' + postString

        return stringWithBlank
    
    def getAsAnswerOnly(self, answerLanguage, allHiragana=False):
        if answerLanguage == 'jp':
            if allHiragana == True:
                return self.japanese_all_hiragana
            elif allHiragana == False:
                return self.japanese
        elif answerLanguage == 'en':
            answer = self.english
            if self.isTransitive == True:
                answer = answer + ' ' + '(transitive)'
            elif self.isTransitive == False:
                answer = answer + ' ' + '(intransitive)'
            return answer

    def __str__(self):
        return (self.preJapanese +' '+ self.preJapaneseParticle +' '+ self.japanese + ' ' + self.postJapanese + ' ' + 
            self.japanese_all_hiragana + ' ' + 
            self.preEnglish + ' ' + self.english + ' ' + self.postEnglish + ' ' +
            str(self.lesson) + ' ' + ''.join(str(self.partOfSpeech)) + str(self.isTransitive))

# [nan 'n' 'exp' 'v' 'adverb' 'な-adj' 'い-adj' 'な-adj, n' 'adverb, n', 'counter']
class PartOfSpeech(Enum):
    NOUN = 0 
    VERB = 1
    ADVERB = 2 
    NA_ADJ = 3
    I_ADJ = 4
    EXP = 5
    COUNTER = 6
    OTHERS = 7

# builds a vocabulary from a xlsx file
# ['lesson', 'pos', 'verbGroup', 'intransitive', 'hasKatakanaOrKanji', 'japanese', 'english', 'isSuruVerb', 'suruMeaning']
class VocabularyBuilder:
    # returns an array of Word objects and a part of speech list
    def buildVocabulary(self, filePath):
        print('Loading vocabulary from ' + filePath)
        df = pd.read_excel(filePath)
        print('Vocabulary file loaded')
        wordList = []
        partOfSpeechList = {}
        lessonList = {}
        kksi = kakasi()
        kksi.setMode("J","H")
        for index, row in df.iterrows():
            if self.checkValidData(row):
                lesson_num = row['lesson']
                pos_list = self.parsePartOfSpeech(row['pos'])
                
                if row['intransitive'] == 't':
                    isTransitive = True
                elif row['intransitive'] == 'i':
                    isTransitive = False
                else:
                    isTransitive = None                

                pre_japanese = self.convertNanToEmptyString(row['preJapanese'])
                pre_japanese_particle = self.convertNanToEmptyString(row['preJapaneseParticle'])
                japanese_all_hiragana = row['japaneseAllHiragana']               
                japanese = row['japanese']
                post_japanese = self.convertNanToEmptyString(row['postJapanese'])
                pre_english = self.convertNanToEmptyString(row['preEnglish'])
                english = row['english']
                post_english = self.convertNanToEmptyString(row['postEnglish'])

                word = Word(lesson_num, pos_list, isTransitive, 
                                pre_japanese, pre_japanese_particle, japanese_all_hiragana, japanese, post_japanese,
                                pre_english, english, post_english)
                wordList.append(word)
                
                indexOfAddedWord = len(wordList) - 1
                if lesson_num not in lessonList:
                    indices = []
                else:
                    indices = lessonList[lesson_num] 
                indices.append(indexOfAddedWord)
                lessonList[lesson_num] = indices
                for pos in pos_list:
                    if pos not in partOfSpeechList:
                        indices = []
                    else:
                        indices = partOfSpeechList[pos]
                    indices.append(indexOfAddedWord)
                    partOfSpeechList[pos] = indices
        
        for posType in PartOfSpeech:
            for index in partOfSpeechList[posType]:
                assert posType in wordList[index].partOfSpeech
        print('Vocabulary built')
        return wordList, partOfSpeechList, lessonList

    # in vocab.xlsx, an entry (row) must have the following columns
    def checkValidData(self, rowData):
        requiredColNames = ['lesson', 'japanese', 'japaneseAllHiragana', 'english']
        for colName in requiredColNames:
            if pd.isnull(rowData[colName]):
                return False
        return True

    def convertNanToEmptyString(self, input):
        if pd.isnull(input):
            return ''
        else:
            return input
    
    def parsePartOfSpeech(self, unparsedData):
        if pd.isnull(unparsedData):
            splitPOS = ['undefined']
        else:
            splitPOS = unparsedData.split(",")
        cleanSplit = []
        for posElem in splitPOS:
            posElem = posElem.strip()
            if posElem == 'n':
                convertedPosElem = PartOfSpeech.NOUN
            elif posElem == 'v':
                convertedPosElem = PartOfSpeech.VERB
            elif posElem == 'adverb':
                convertedPosElem = PartOfSpeech.ADVERB
            elif posElem == 'な-adj':
                convertedPosElem = PartOfSpeech.NA_ADJ
            elif posElem == 'い-adj':
                convertedPosElem = PartOfSpeech.I_ADJ
            elif posElem == 'exp':
                convertedPosElem = PartOfSpeech.EXP
            elif posElem == 'counter':
                convertedPosElem = PartOfSpeech.COUNTER
            elif posElem == 'undefined':
                convertedPosElem = PartOfSpeech.OTHERS
            else: 
                raise Exception('invalid part of speech', posElem)
            cleanSplit.append(convertedPosElem)
        return cleanSplit
