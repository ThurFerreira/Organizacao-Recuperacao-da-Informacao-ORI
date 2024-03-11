import sys
import spacy

def splitWords(string):
    return string.split(' ');

def removeSeparators(frase):
    separators = ".,!?"
    frase = ["".join(caracter for caracter in palavra if caracter not in separators) for palavra in frase.split()]
    
    for i in range(len(frase)-1):
        if not frase[i].isalpha():
            frase = frase[:i] + frase[i + 1:]

    return frase

def removeStopwords(frase):
    nlp = spacy.load("pt_core_news_sm")
    stopwords = nlp.Defaults.stop_words
    doc = nlp(' '.join(frase))
    frase = [token.text for token in doc if not token.is_stop]
    return ' '.join(frase)


def readFile(filePath):
    with open(filePath, 'r') as file:
        content = file.read()
    return content

def treatText(text):
    noSeparator = removeSeparators(text)
    noStopWords = removeStopwords(noSeparator)

    return splitWords(noStopWords)

def getInvertedIndex(text, fileNumber):
    invertedIndex = []

    currentArrayIndex = 0
    currentFrequency = 0

    for i in range(len(text)):
        currentWord = text[i]
        for palavra in text:
            if palavra.lower() == currentWord.lower():
                currentFrequency+=1

        invertedIndex.insert(currentArrayIndex, currentWord + ': ' + str(fileNumber) + ', ' + str(currentFrequency))
        currentArrayIndex+=1
        currentFrequency = 0
        
    
    return invertedIndex

def main():
    args = sys.argv
    filePaths = readFile(args[1]).split('\n')

    invertedIndex = []
    fileNumber = 1
    for path in filePaths:
            fileContent = readFile(path)
            treatedText = treatText(fileContent)
            result = getInvertedIndex(treatedText, fileNumber)
            invertedIndex += result
            fileNumber += 1

    return '\n'.join(invertedIndex)

print(main())
