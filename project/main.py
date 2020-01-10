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
            "Options:\n"
            "'sa' to start quiz for all vocabulary till Japanese 3\n"
            "'s' to start a quiz with custom size\n"
            "'sl' to start a quiz according to Lessons based on みんなの日本語\n"
            "'j1' or 'j2' or 'j3' to test vocabulary for the respective Japanese modules"
            "Type 'q' to quit'")
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
            isValidCommand = command in ['sa', 's', 'sl', 'q', 'j1', 'j2', 'j3']
            if isValidCommand:
                if command == 'sa':
                    print('Starting quiz!\n\n')
                    language = self.selectLanguage()
                    quiz.startall(language)
                elif command == 's':
                    numQuestions = self.selectNumQuestions()
                    language = self.selectLanguage()
                    print('Starting quiz!\n\n')
                    quiz.start(language, numQuestions)
                elif command == 'sl':
                    startLesson, endLesson = self.selectLessons()
                    language = self.selectLanguage()
                    print('Starting quiz!\n\n')
                    quiz.start(language, startLesson=startLesson, endLesson=endLesson)
                elif command == 'j1':
                    language = self.selectLanguage()
                    print('Starting quiz for Japanese 1 vocabulary!\n\n')
                    quiz.start(language, startLesson=1, endLesson=10)
                elif command == 'j2':
                    language = self.selectLanguage()
                    print('Starting quiz for Japanese 2 vocabulary!\n\n')
                    quiz.start(language, startLesson=11, endLesson=20)
                elif command == 'j3':
                    language = self.selectLanguage()
                    print('Starting quiz for Japanese 3 vocabulary!\n\n')
                    quiz.start(language, startLesson=21, endLesson=31)
                elif command == 'q':
                    print('Quiting program')
                    break

    
    def selectNumQuestions(self):
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
        return numQuestions

    def selectLanguage(self):
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
        return value

    def selectLessons(self):
        clearCli()
        print('(s)ingle or (r)ange of lessons? (s/r)')
        while True:
            value = input()
            isValidInput = value == 's' or value == 'r'
            if isValidInput:
                break
            clearCli()
            print('(s)ingle or (r)ange of lessons? (s/r)')
            print(CLI.invalid_command)
        if value == 's':
            startLesson, endLesson = self.selectSingleLesson()
        elif value == 'r':
            startLesson, endLesson = self.selectRangeOfLessons()
        return startLesson, endLesson
    
    def selectSingleLesson(self):
        clearCli()
        print('Type lesson number?')
        while True:
            value = input()
            isValidInput = self.vocabulary.hasLesson(int(value))
            if isValidInput:
                print('Valid lesson', value)
                break
            clearCli()
            print('Type lesson number?')
            print('Lesson does not exist')
        selectedLesson = value
        return selectedLesson , selectedLesson

    def selectRangeOfLessons(self):
        clearCli()
        print('Type start lesson number?')
        while True:
            value = input()
            isValidInput = self.vocabulary.hasLesson(int(value))
            if isValidInput:
                print('Valid lesson', value)
                break
            clearCli()
            print('Type start lesson number?')
            print('Lesson does not exist')
        startLesson = value

        clearCli()
        print('Start lesson: ', startLesson)
        print('Type end lesson number?')
        while True:
            value = input()
            isLargerThanStart = int(value) > int(startLesson) 
            doesLessonExist = self.vocabulary.hasLesson(int(value))
            isValidInput = isLargerThanStart and doesLessonExist
            if isValidInput:
                print('Valid lesson', value)
                break
            clearCli()
            print('Start lesson: ', startLesson)
            print('Type end lesson number?')
            if not doesLessonExist: print('Lesson does not exist')
            elif not isLargerThanStart: print('End lesson should be greater than start lesson')
        endLesson = value
        assert int(endLesson) > int(startLesson)
        return startLesson, endLesson

class Quiz:
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        self.numTotalQuestions = 0
        self.numIncorrect = 0
        self.numCorrect = 0
        self.report = '...'
    
    def startall(self, qnLanguage):
        self.start(qnLanguage, self.vocabulary.getVocabularySize())

    def start(self, qnLanguage, numQuestions=None, startLesson=None, endLesson=None):
        if numQuestions is not None and startLesson is None and endLesson is None:
            indices = random.sample(range(self.vocabulary.getVocabularySize()), numQuestions)
            self.numTotalQuestions = numQuestions
        elif numQuestions is None and startLesson is not None and endLesson is not None:
            indices = self.buildIndicesFromLessons(startLesson, endLesson)
            self.numTotalQuestions = len(indices)
        for index in indices:
            mcqqn = McqQuestion(index, qnLanguage, self.vocabulary)
            clearCli()
            self.printProgress()
            mcqqn.printQuestion()
            while True:
                value = input()
                isValidOption = value  == '1' or value == '2' or value == '3' or (value == '4' and mcqqn.numOptions == 4)
                isValidQuitCommand = value == 'q' 
                isValidValue = isValidOption or isValidQuitCommand
                if isValidValue:
                    break
                clearCli()
                self.printProgress()
                mcqqn.printQuestion()
                print(CLI.invalid_answer)
            if value == 'q':
                break
            isCorrect = mcqqn.answerQuestion(value)
            self.updateProgress(isCorrect, mcqqn)
        
        clearCli()        
        self.printProgress()
        print('Quiz Ended!')
        input("Press Enter to continue...")

    def buildIndicesFromLessons(self, startLesson, endLesson):
        indices = []
        for lessonNum in range(int(startLesson), int(endLesson) + 1):
            indicesFromLesson = self.vocabulary.lessonList[lessonNum]
            indices = indices + indicesFromLesson
        indices = random.sample(indices, len(indices))
        return indices

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