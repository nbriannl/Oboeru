# Oboeru
*Python CLI Japanese Language MCQ Quiz* 

Oboeru (The romanization of the Japanese 覚える, which means ‘to remember’) is a program to help Japanese language learning, particularly NUS Japanese Language students using the みんなの日本語 textbook, to practice their vocabulary, especially after a hiatus of language studies.

*Why not use Anki or [insert App name here]?*

Oboeru fills up the other MCQ options with words of similar parts of speech. Plus generation of over 1200 Anki cards would be to tedious. 

## How to Install
This project was developed with `Python 3.7.4`. Please ensure a compatible version is installed in your computer.

This project is developed on Windows. I am not sure whether this is compatible with other operating systems.

I have yet to make a `requirements.txt`, but this project uses `pandas` to load the vocabulary excel file into the program.
`pip install panda` 

Ensure that the font used in the console can print asian fonts, such as MS Gothic, MS Mincho or NSimSun.

Download or clone the repo and open your command line inside `/project` folder and type the command `python main.py` to run the program

## How to Use
Type any of the options to start a quiz. Enter the desired options when prompted. While in a quiz, answer 'q' to quit the quiz.

## How to add Vocabulary
To update the vocabulary, simply open and edit `vocab.xlsx`

### Fields
The excel file was originally made by me for Japanese 3 revision, hence not all fields are used in the current version of the application. It would be best however to fill up all fields when adding vocabulary as future functionality may use these.

⊛ indicates a required field for the current version of the program.

- ⊛ **lesson:** The corresponding lesson of the vocab as found in Minna no Nihongo. For the current version of the program, ensure that the lesson numbers are not discontinuous. (i.e. The current lesson numbers are from 1 to 31. Do not add a lesson number 50 or 43 etc.)

- ⊛ **pos:** The part of speech of the word. The current options are 'n', 'v', 'な-adj', 'い-adj', 'adverb', 'exp' (expression) and ' '. You can leave it blank, and it will be suggested as similar words to other words that have their part of speech undefined.

- **verbGroup:** The Verb group of the word. Use \*2 to indicate a special Group 2 verb. 

- **intransitive:** i for intransitive, t for transitive verbs

- **hasKatakanaOrKanji:** J if the **Japanese** field contains Kanji, K if it contains Katakana

- ⊛ **japanese:** The Japanese word

- ⊛ **english:** The English word

- **isSuruVerb:** Fill with either [を]する or をする or none depending on whether the word (which is likely a noun) can be used with する and in what usage.

- **suruMeaning:** The meaning of the word when added with する 

If you have added entries to the excel sheet. Feel free to share it under Issues or email me at neilbrian.nl@gmail.com 
