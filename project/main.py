import pandas as pd
import random
from enum import Enum
import time
from os import system, name

def clearCli(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

class CLI:
    main_menu = ("Oboeru - 'It's time to 覚える!'\n"
            "========Main Menu========\n"
            "Type 'start' or 's' to start quiz\n"
            "Type 'quit' to quit!'")
    invalid_command = 'Invalid command'
    invalid_answer = 'Invalid answer'

class Main:
    def main(self):
        clearCli()
        self.vocabulary = Vocabulary()
        vocabulary = self.vocabulary
        vocabulary.buildVocabulary()

        isValidCommand = True
        while True:
            quiz = Quiz(vocabulary)
            clearCli()
            print(CLI.main_menu)
            if not isValidCommand:
                print(CLI.invalid_command)
            command = input()
            isValidCommand = command in ['sa', 's10jp', 's10en', 'sc', 's', 'q', 't']
            if isValidCommand:
                if command == 'sa':
                    print('Starting quiz!\n\n')
                    quiz.startall('jp')
                elif command == 's10jp' :
                    print('Starting quiz!\n\n')
                    quiz.start(10, 'jp')
                elif command == 's10en':
                    print('Starting quiz!\n\n')
                    quiz.start(10, 'en')
                elif command == 'sc' or command == 's':
                    numQuestions, language = self.selectCustomQuizOptions()
                    print('Starting quiz!\n\n')
                    quiz.start(numQuestions, language)
                elif command == 'q':
                    print('Quiting program')
                    break
                elif command == 't':
                    vocabulary.buildVocabulary()
    
    def selectCustomQuizOptions(self):
        clearCli()
        print('How many questions?')
        while True:
            value = input()
            isANumber = value.isnumeric()
            isNumberWithinVocabSize = isANumber and 1 <= int(value) <= self.vocabulary.getVocabularySize()
            if isNumberWithinVocabSize:
                break
            clearCli()
            print('How many questions?')
            if not isANumber: 
                print('Not a number')
            elif isANumber and not isNumberWithinVocabSize:
                print('Invalid value. Vocabulary size is', self.vocabulary.getVocabularySize())
        numQuestions = int(value)

        clearCli()
        print('Language of questions? (jp/en)')
        while True:
            value = input()
            isValidInput = value == 'jp' or value == 'en'
            if isValidInput:
                break
            clearCli()
            print('Language of questions? (jp/en)')
            print(CLI.invalid_command)
        language = value

        return numQuestions, language

class Quiz:
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        self.numTotalQuestions = 0
        self.numIncorrect = 0
        self.numCorrect = 0
        self.report = '...'
    
    def startall(self, qnLanguage):
        self.start(self.vocabulary.getVocabularySize(), qnLanguage)

    def start(self, size, qnLanguage):
        indices = random.sample(range(self.vocabulary.getVocabularySize()), size)
        self.numTotalQuestions = size
        for index in indices:
            mcqqn = McqQuestion(index, qnLanguage, self.vocabulary)
            hasTypedInvalidAnswer = False
            while True:
                clearCli()
                self.printProgress()
                mcqqn.printQuestion()
                if hasTypedInvalidAnswer:
                    print(CLI.invalid_answer)
                event = input()
                # should i do validilty check here
                hasTypedInvalidAnswer = False
                if event == 'q' or event == '1' or event == '2' or event == '3':
                    break
                elif event == '4' and mcqqn.numOptions == 4:
                    break
                else:
                    hasTypedInvalidAnswer = True
            if event == 'q':
                break
            isCorrect = mcqqn.answerQuestion(event)
            self.updateProgress(isCorrect, mcqqn)
        clearCli()        
        self.printProgress()
        print('Quiz Ended!')
        input("Press Enter to continue...")

    def updateProgress(self, isCorrect, mcqqn):
        if isCorrect:
            self.numCorrect += 1
        else:
            self.numIncorrect += 1
        if isCorrect:
            report = 'Correct! ' + mcqqn.questionWord + ' means ' + mcqqn.correctAnswer
        else:
            report = 'Wrong! ' + mcqqn.questionWord + ' means ' + mcqqn.correctAnswer
        self.report = report

    def printProgress(self):
        numLeft = self.numTotalQuestions - self.numCorrect - self.numIncorrect
        print('Left:', numLeft)
        print('Correct:', self.numCorrect)
        print('Wrong:', self.numIncorrect)
        print('Total', self.numTotalQuestions)
        print('Previous word:', self.report)
        print('\n=====================\n')


class McqQuestion:
    def __init__(self, index, fromLanguage, vocabulary):
        self.questionWord = None
        self.correctAnswer = None
        self.otherAnswers = None
        self.numOptions = None
        self.correctOption = None
        self.options = None
        
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

    def printQuestion(self):
        print(self.questionWord)
        if self.numOptions >= 1:
            print("1)", self.options[0])
        if self.numOptions >= 2:
            print("2)", self.options[1])
        if self.numOptions >= 3:
            print("3)", self.options[2])
        if self.numOptions >= 4:
            print("4)", self.options[3])
        # print('Correct Answer:', str(self.correctOption + 1))

    def answerQuestion(self, selectedOption):
        isCorrect = int(selectedOption) == self.correctOption + 1
        return isCorrect

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
        lessonList = {}
        for index, row in df.iterrows():
            splitPOS = self.parsePartOfSpeech(row['pos'])
            if self.checkValidData(row):
                lessonNum = row['lesson']
                word = Word(row['japanese'], row['english'], row['lesson'], splitPOS)
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