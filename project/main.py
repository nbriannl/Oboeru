import pandas as pd
import random
import keyboard
from enum import Enum
import time
from os import system, name

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

class Main:
    def main(self):
        vocabulary = Vocabulary()
        vocabulary.buildVocabulary()
        print("Oboeru - 'It's time to 覚える!'\n"
            "Type 'start' to start quiz\n"
            "Type 'quit' to quit'")
        while True:
            command = input()
            if command == 'start' or command == 's':
                print('Starting quiz!\n\n')
                quiz = Quiz(vocabulary)
                quiz.start()

            if command == 'quit' or command == 'q':
                print('Quiting program')
                break
        
class Quiz:
    def __init__(self, vocabulary):
        self.numTotalQuestions = vocabulary.getVocabularySize()
        self.numIncorrect = 0
        self.numCorrect = 0
        self.vocabulary = vocabulary
        self.report = '...'
    
    def start(self):
        for index in range(self.vocabulary.getVocabularySize()):
            mcqqn = McqQuestion(index, 'jp', self.vocabulary)
            clear()
            self.printProgress()
            mcqqn.showQuestion()
            while True:
                event = keyboard.read_key()
                if mcqqn.numOptions == 3:
                    if event == '1' or event == '2' or event == '3':
                        break
                else:
                    if event == '1' or event == '2' or event == '3' or event == '4':
                        break
            isCorrect, report = mcqqn.answerQuestion(event)
            self.updateProgress(isCorrect, report)
            time.sleep(0.5)

    def printProgress(self):
        numLeft = self.numTotalQuestions - self.numCorrect - self.numIncorrect
        print('Left:', numLeft)
        print('Correct:', self.numCorrect)
        print('Wrong:', self.numIncorrect)
        print('Total', self.numTotalQuestions)
        print('Previous word:', self.report)

    def updateProgress(self, isCorrect, report):
        if isCorrect:
            self.numCorrect += 1
        else:
            self.numIncorrect += 1
        self.report = report

class McqQuestion:
    def __init__(self, index, fromLanguage, vocabulary):
        self.vocabulary = vocabulary
        self.getQuestionWordAndCorrectAnswer(index, fromLanguage)
        self.getOtherAnswers(index, fromLanguage)
        self.setNumOptions()
        self.setCorrectOption()
        self.fillOptions()


    def getQuestionWordAndCorrectAnswer(self, index, fromLanguage):
        word = self.vocabulary.getWord(index)
        if fromLanguage == 'jp':
            self.questionWord, self.correctAnswer = word.japanese, word.english
        elif fromLanguage == 'en':
            self.questionWord, self.correctAnswer = word.english, word.japanese

    def getOtherAnswers(self, index, fromLanguage):
        otherWords = self.vocabulary.get3WordsSimilarPos(index)
        otherAnswersList = []
        for otherWord in otherWords:
            if fromLanguage == 'jp':
                otherAnswer = otherWord.english
            elif fromLanguage == 'en':
                otherAnswer = otherWord.japanese
            otherAnswersList.append(otherAnswer)
        self.otherAnswers = otherAnswersList

    def setNumOptions(self):
        self.numOptions = len(self.otherAnswers) + 1

    def setCorrectOption(self):
        self.correctOption = random.randint(0, self.numOptions - 1)

    def fillOptions(self):
        options = list(self.otherAnswers)
        options.insert(self.correctOption, self.correctAnswer)
        self.options = options

    def showQuestion(self):
        print(self.questionWord)
        if self.numOptions >= 1:
            print("1)", self.options[0])
        if self.numOptions >= 2:
            print("2)", self.options[1])
        if self.numOptions >= 3:
            print("3)", self.options[2])
        if self.numOptions >= 3:
            print("4)", self.options[3])
        # print('Correct Answer:', str(self.correctOption + 1))

    def answerQuestion(self, selectedOption):
        isCorrect = int(selectedOption) == self.correctOption + 1
        if isCorrect:
            report = 'Correct! ' + self.questionWord + ' means ' + self.correctAnswer
        else:
            report = 'Wrong! ' + self.questionWord + ' means ' + self.correctAnswer
        return isCorrect, report

class Vocabulary:
    def __init__(self):
        self.wordList = []
        self.partOfSpeechList = {}

    def buildVocabulary(self):
        self.wordList, self.partOfSpeechList = VocabularyBuilder().buildVocabulary('vocab.xlsx')

    def getVocabularySize(self):
        return len(self.wordList)

    def getWord(self, index):
        return self.wordList[index]

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

        # print('given', word.japanese, word.partOfSpeech)
        # for similarWord in similarWords: 
        #     print('similar:', similarWord.__str__())
        return similarWords

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
                #print(wordList[index].__str__())
                assert posType in wordList[index].partOfSpeech
        print('Vocabulary built')
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