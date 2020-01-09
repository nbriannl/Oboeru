import pandas as pd
from enum import Enum

class Main:
    def main(self):
        print("Oboeru - 'It's time to 覚える!'\n"
            "Type 'start' to start quiz\n"
            "Type 'quit' to quit'")
        while True:
            command = input()
            if command == 'start' or command == 's':
                print('Starting quiz!')
                quiz = Quiz(10)
                print(quiz.numTotalQuestions)
                vocabulary = Vocabulary()
                vocabulary.foo()

            if command == 'quit' or command == 'q':
                print('Quiting program')
                break

            if command == 't':
                vocabularyBuilder = VocabularyBuilder()
                vocabularyBuilder.buildVocabulary('vocab.xlsx')

        
class Quiz:
    def __init__(self, numTotalQuestions):
        self.numTotalQuestions = numTotalQuestions
        self.numIncorrect = 0
        self.numCorrect = 0

class Vocabulary:
    

class Word:
    def __init__(self, japanese, english, lesson, partOfSpeech):
        #print(japanese, english, lesson, partOfSpeech)
        self.japanese = japanese
        self.english = english
        self.lesson = lesson
        self.partOfSpeech = partOfSpeech

    def __str__(self):
        return self.japanese + ' ' + self.english + ' ' + str(self.lesson) + ' ' + ''.join(str(self.partOfSpeech))

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
        for index, row in df.iterrows():
            splitPOS = self.parsePartOfSpeech(row['pos'])
            if self.checkValidData(row):
                word = Word(row['japanese'], row['english'], row['lesson'], splitPOS)
                wordList.append(word)
                indexOfAddedWord = len(wordList) - 1
                for pos in splitPOS:
                    if pos not in partOfSpeechList:
                        indices = []
                        indices.append(indexOfAddedWord)
                        partOfSpeechList[pos] = indices
                    else:
                        indices = partOfSpeechList[pos]
                        indices.append(indexOfAddedWord)
                        partOfSpeechList[pos] = indices
        
        for posType in PartOfSpeech:
            for index in partOfSpeechList[posType]:
                print(wordList[index].__str__())
                assert posType in wordList[index].partOfSpeech

        return wordList, partOfSpeechList

    def checkValidData(self, rowData):
        listColNames = ['lesson','japanese', 'english']
        for colNames in listColNames:
            if pd.isnull(rowData[colNames]):
                return False
        return True

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



if __name__ == '__main__':
    main = Main()
    main.main()