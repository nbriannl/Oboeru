import pandas as pd
from enum import Enum
from pykakasi import kakasi
import random

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
    def __init__(self, japanese, japanese_all_hiragana, english, lesson, partOfSpeech, 
                    isTransitive, preJapanese, preJapaneseParticle, postJapanese, preEnglish, postEnglish):
        # print(japanese, english, lesson, partOfSpeech)
        self.japanese = japanese
        self.japanese_all_hiragana = japanese_all_hiragana
        self.english = english
        self.lesson = lesson
        self.partOfSpeech = partOfSpeech
        self.isTransitive = isTransitive
        self.preJapanese = preJapanese
        self.preJapaneseParticle = preJapaneseParticle
        self.postJapanese = postJapanese
        self.preEnglish = preEnglish
        self.postEnglish = postEnglish

        if self.isTransitive is not None and PartOfSpeech.VERB not in self.partOfSpeech:
            raise Exception(self.japanese, self.partOfSpeech, self.isTransitive, " is not a verb but is either transitive/intransitive.")
        # if PartOfSpeech.VERB in self.partOfSpeech and self.isTransitive is None:
        #     print('Info: ' + self.japanese + ' [' + str(self.lesson) + '] has no intransitive of instrasitive defined')

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
            splitPOS = self.parsePartOfSpeech(row['pos'])
            if self.checkValidData(row):
                lessonNum = row['lesson']
                conv = kksi.getConverter()
                japanese_all_hiragana = conv.do(row['japanese'])                    
                if row['intransitive'] == 't':
                    isTransitive = True
                    english_meaning = row['english'] + ' (transitive)'
                elif row['intransitive'] == 'i':
                    isTransitive = False
                    english_meaning = row['english'] + ' (intransitive)'
                else:
                    isTransitive = None
                    english_meaning = row['english']
                
                word = Word(row['japanese'], japanese_all_hiragana, english_meaning, row['lesson'], splitPOS, isTransitive, 
                    self.convertNanToEmptyString(row['preJapanese']), self.convertNanToEmptyString(row['preJapaneseParticle']), 
                    self.convertNanToEmptyString(row['postJapanese']), self.convertNanToEmptyString(row['preEnglish']), self.convertNanToEmptyString(row['postEnglish']))
                wordList.append(word)
                
                indexOfAddedWord = len(wordList) - 1
                if lessonNum not in lessonList:
                    indices = []
                else:
                    indices = lessonList[lessonNum] 
                indices.append(indexOfAddedWord)
                lessonList[lessonNum] = indices
                for pos in splitPOS:
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

    def checkValidData(self, rowData):
        listColNames = ['lesson','japanese', 'english']
        for colNames in listColNames:
            if pd.isnull(rowData[colNames]):
                return False
        return True

    def convertNanToEmptyString(self, input):
        if pd.isnull(input):
            return ''
        else:
            return input
        

    # [nan 'n' 'exp' 'v' 'adverb' 'な-adj' 'い-adj' 'な-adj, n' 'adverb, n', 'counter']
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
