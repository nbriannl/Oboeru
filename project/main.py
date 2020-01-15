import random
import time
from os import system, name
from pykakasi import kakasi
from vocabulary import Vocabulary

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
            "'sa' to start an MCQ quiz for all vocabulary (until L44)\n"
            "'s' to start an MCQ quiz with custom size\n"
            "'sl' to start an MCQ quiz according to Lessons based on みんなの日本語\n"
            "'j1' or 'j2' or 'j3' to start an MCQ quiz for vocabulary in the respective Japanese modules\n"
            "'o' to start an Open-ended quiz. 日本語➝English. You can pick which lessons\n"
            "Type 'q' to quit'")
    invalid_command = 'Invalid command'
    invalid_answer = 'Invalid answer'
    how_to_quit_quiz = "Enter 'q' to quit the quiz at any time."


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
            isValidCommand = command in ['sa', 's', 'sl', 'q', 'j1', 'j2', 'j3', 'la', 't', 'o']
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
                    quiz.start(language, startLesson=startLesson,
                               endLesson=endLesson)
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
                    quiz.start(language, startLesson=21, endLesson=32)
                elif command == 'o':
                    print('Starting open ended quiz')
                    startLesson, endLesson = self.selectLessons()
                    quiz.start_open_ended(startLesson=startLesson, endLesson=endLesson)
                elif command == 'q':
                    print('Quiting program')
                    break
                elif command == 'la':
                    print('Listing all vocabulary')
                    vocabulary.printWholeVocabulary()
                elif command == 't':
                    print('Test')
                    self.testFunction()

    def testFunction(self):
        kksi = kakasi()
        kksi.setMode("J", "H")
        conv = kksi.getConverter()
        all_hiragana = 'がくせい'
        partial_hiragana1 = '学せい'
        partial_hiragana2 = 'がく生'
        all_kanji = '学生'
        print(conv.do(all_hiragana))
        print(conv.do(partial_hiragana1))
        print(conv.do(partial_hiragana2))
        print(conv.do(all_kanji))  
        print(conv.do(all_hiragana) == conv.do(partial_hiragana1) == conv.do(partial_hiragana2) == conv.do(all_kanji))
        input()
    
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
        print('Do you want to do a (s)ingle or a (r)ange of lessons? (s/r)')
        while True:
            value = input()
            isValidInput = value == 's' or value == 'r'
            if isValidInput:
                break
            clearCli()
            print('Do you want to do a (s)ingle or a (r)ange of lessons? (s/r)')
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
        self.mistakes = [] 
    
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
        print("Press Enter to continue...")
        print('\n====Mistakes=====')
        for mistake in self.mistakes:
            print(mistake)
        input("=================")
    
    def start_open_ended(self, startLesson=None, endLesson=None):
        indices = self.buildIndicesFromLessons(startLesson, endLesson)
        self.numTotalQuestions = len(indices)
        for index in indices:
            open_ended_qn = OpenEndedQuestion(index, self.vocabulary)
            clearCli()
            self.printProgress()
            open_ended_qn.printQuestion()
            while True:
                value = input()
                isValidValue = True
                if isValidValue:
                    break
                clearCli()
                self.printProgress()
                open_ended_qn.printQuestion()
                print(CLI.invalid_answer)
            if value == 'q':
                break
            isCorrect = open_ended_qn.answerQuestion(value)
            self.updateProgressOpenEnded(isCorrect, open_ended_qn, value)
        
        clearCli()        
        self.printProgress()
        print('Quiz Ended!')
        print("Press Enter to continue...")
        print('\n====Mistakes=====')
        for mistake in self.mistakes:
            print(mistake, "\n\n")
        input("=================")

    def buildIndicesFromLessons(self, startLesson, endLesson):
        indices = []
        for lessonNum in range(int(startLesson), int(endLesson) + 1):
            try:
                indicesFromLesson = self.vocabulary.lessonList[lessonNum]
                indices = indices + indicesFromLesson
            except KeyError:
                string = 'No vocabulary from Lesson ' + str(lessonNum) + '. Enter to acknowledge'
                input(string)
                pass
        indices = random.sample(indices, len(indices))
        return indices

    def updateProgressOpenEnded(self, isCorrect, open_ended_qn, value):
        if isCorrect:
            self.numCorrect += 1
        else:
            self.numIncorrect += 1
        
        if isCorrect:
            report = ('Correct! ' + open_ended_qn.questionString + ' means ' + open_ended_qn.correctAnswer)
        else:
            report = ('Wrong! "' + open_ended_qn.questionString + '" means "' + open_ended_qn.correctAnswer + '/' + open_ended_qn.correctAnswer_all_hiragana +
                '"   (You typed ' + open_ended_qn.inputAnswer + '/' + open_ended_qn.inputAnswer_all_hiragana +')')
        self.report = report
        if not isCorrect: 
            self.mistakes.append(report)

    def updateProgress(self, isCorrect, mcqqn):
        if isCorrect:
            self.numCorrect += 1
        else:
            self.numIncorrect += 1
        if isCorrect:
            report = 'Correct! "' + mcqqn.questionString + '" means "' + mcqqn.correctAnswerString + "'"
        else:
            report = 'Wrong! "' + mcqqn.questionString + '" means "' + mcqqn.correctAnswerString + "'"
        self.report = report
        if not isCorrect:
            self.mistakes.append(report)

    def printProgress(self):
        numLeft = self.numTotalQuestions - self.numCorrect - self.numIncorrect
        print('Left:', numLeft)
        print('Correct:', self.numCorrect)
        print('Wrong:', self.numIncorrect)
        print('Total', self.numTotalQuestions)
        print('Previous word:', self.report)
        print(CLI.how_to_quit_quiz)
        print('\n=====================\n')

# Open ended questions are aways english word, give japanese answer.
class OpenEndedQuestion:
    def __init__(self, index, vocabulary):
        self.questionString = None
        self.stringWithBlank = None
        self.correctAnswer = None
        self.correctAnswer_all_hiragana = None
        self.inputAnswer = None
        self.inputAnswer_all_hiragana = None

        self.vocabulary = vocabulary
        self.getQuestionWordAndCorrectAnswer(index)
        
    def getQuestionWordAndCorrectAnswer(self, index):
        word = self.vocabulary.getWord(index)
        self.questionString = word.getAsFullString('en')
        self.stringWithBlank = word.getAsStringWithBlank('jp')
        self.correctAnswer = word.japanese
        self.correctAnswer_all_hiragana = word.japanese_all_hiragana 


    def printQuestion(self):
        print(self.questionString)
        print(self.stringWithBlank)

    def answerQuestion(self, input):
        kksi = kakasi()
        kksi.setMode("J", "H") 
        conv = kksi.getConverter()
        convertedInput_all_hiragana = conv.do(input)
        self.inputAnswer = input
        self.inputAnswer_all_hiragana = convertedInput_all_hiragana
        
        isKanjiAnswerCorrect = self.inputAnswer == self.correctAnswer
        isHiraganaAnswerCorrect = self.inputAnswer_all_hiragana == self.correctAnswer_all_hiragana
        isCorrect = isKanjiAnswerCorrect or isHiraganaAnswerCorrect
        return isCorrect   


class McqQuestion:
    def __init__(self, index, fromLanguage, vocabulary):
        self.questionString = None
        self.questionStringAllHiragana = None
        self.answerStringBlanked = None
        self.correctAnswer = None
        self.correctAnswerString = None
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
        questionLanguage = fromLanguage
        if questionLanguage == 'en':
            answerLanguage = 'jp'
        elif questionLanguage == 'jp':
            answerLanguage = 'en'
            questionStringAllHiragana = word.getAsFullString(questionLanguage, allHiragana=True) 

        questionString = word.getAsFullString(questionLanguage)
        answerStringBlanked = word.getAsStringWithBlank(answerLanguage)
        answer = word.getAsAnswerOnly(answerLanguage)
        correctAnswerString = word.getAsFullString(answerLanguage)
        self.questionString, self.answerStringBlanked, self.correctAnswer, self.correctAnswerString = questionString, answerStringBlanked, answer, correctAnswerString
        self.questionStringAllHiragana = questionStringAllHiragana

    def getOtherAnswers(self, index, fromLanguage):
        otherWords = self.vocabulary.get3WordsSimilarPos(index)
        otherAnswersList = []
        questionLanguage = fromLanguage
        if questionLanguage == 'en':
            answerLanguage = 'jp'
        elif questionLanguage == 'jp':
            answerLanguage = 'en' 
        for otherWord in otherWords:
            otherAnswer = otherWord.getAsAnswerOnly(answerLanguage)
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
        print(self.questionString)
        if self.questionStringAllHiragana is not None: 
            print(self.questionStringAllHiragana)
        print(self.answerStringBlanked)
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

if __name__ == '__main__':
    main = Main()
    main.main()
