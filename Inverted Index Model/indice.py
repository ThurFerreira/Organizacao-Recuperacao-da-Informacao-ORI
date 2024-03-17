import sys
import spacy

nlp = spacy.load("pt_core_news_lg")
invertedIndexArray = {}

class TermCount: #z
    def __init__(self, documento, qtdTermos):
        self.documento = documento
        self.qtdTermos = qtdTermos

    def __str__(self):
        return f"{self.documento},{self.qtdTermos}"
    
    def toString(self):
        return f"{self.documento},{self.qtdTermos} "


class InvertedIndexLine: #y
    def __init__(self, word):
        self.word = word
        self.line = []

    def addNewInvertedIndex(self, termCount):
        self.line.append(termCount)


    def printLine(self):
        line = f"{self.word}: "

        for obj in self.line:
            line += obj.toString()
        return line

def splitWords(string):
    return string.split(' ');

def removeSeparators(frase):
    separators = ".,!? "
    frase = ["".join(caracter for caracter in palavra if caracter not in separators) for palavra in frase.split()]
    
    for i in range(len(frase)-1):
        if not frase[i].isalpha():
            frase = frase[:i] + frase[i + 1:]

    return frase

def removeStopwords(frase):
    stopwords = nlp.Defaults.stop_words
    doc = nlp(' '.join(frase))
    frase = [token.text for token in doc if not token.is_stop]
    return ' '.join(frase)


def readFile(filePath):
    with open(filePath, 'r') as file:
        content = file.read()
    return content

def lemmatizeText(text):
    doc = nlp(text)
    lemmatizedText = []

    for token in doc:

        if token.pos_ == "VERB":
            #a biblioteca spacy está definindo "engracada" como um verbo
            lemmatizedText.append(token.lemma_)
        else:
            lemmatizedText.append(token.text)

    return ' '.join(lemmatizedText)


def treatText(text):
    noSeparator = removeSeparators(text)
    noStopWords = removeStopwords(noSeparator)
    lemmatizedText = lemmatizeText(noStopWords)
    
    return splitWords(lemmatizedText)

def getInvertedIndex(text, fileNumber):
    currentArrayIndex = 0
    currentFrequency = 0

    for i in range(len(text)):
        currentWord = text[i].lower()
        for palavra in text:
            if palavra.lower() == currentWord.lower():
                currentFrequency+=1
        
        termCount = TermCount(fileNumber, currentFrequency)
        separateFromDocuments(currentWord, termCount, fileNumber)

        currentFrequency = 0

    return invertedIndexArray

def alreadyHasDocument(currentFileNumber, array):
    for obj in array:
        if (currentFileNumber == obj.documento):
            return True
    
    return False


def separateFromDocuments(currentWord, termCount, currentFileNumber):
    if currentWord in invertedIndexArray:
            #palavra já registrada anteriormente
            line = invertedIndexArray[currentWord]
            if not alreadyHasDocument(currentFileNumber, line.line):
                line.addNewInvertedIndex(termCount)
                invertedIndexArray[currentWord] = line

    else:
        #palavra ainda não registrada
        newLine = InvertedIndexLine(currentWord)
        newLine.addNewInvertedIndex(termCount)
        invertedIndexArray[currentWord] = newLine

def generateFile():
    with open('indice.txt', 'w') as file:
        for line in invertedIndexArray.values():
            file.write(line.printLine() + '\n')

def main():
    args = sys.argv
    filePaths = readFile(args[1]).split('\n')

    fileNumber = 1
    for path in filePaths:
        fileContent = readFile(path)
        treatedText = treatText(fileContent)
        getInvertedIndex(treatedText, fileNumber)
        fileNumber += 1
    
    generateFile()

main()
