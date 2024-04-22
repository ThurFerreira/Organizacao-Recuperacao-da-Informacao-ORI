import sys
import math

def readReferenceCollection(filepath):
    cMatrix = []

    with open(filepath, 'r') as file:
        n = int(file.readline())
        for i in range(n*2):
            line = file.readline().strip()
            array = list(map(int, line.split()))
            cMatrix.append(array)

    return cMatrix

def print_matrix(matrix):
    for row in matrix:
        for element in row:
            print(element, end=" ")  # Imprime o elemento seguido de um espaço
        print() 
    
def writeInFile(media):
    asString = [str(value) for value in media]
    asString = ' '.join(asString)

    with open('media.txt', 'w') as file:
        file.write(asString)

def calcInterpolacao(precisao, revocacao):
    interpolacao  = []
    chooseMax = []

    maiorPrecisao = max(precisao)
    for padraoRevocacao in range(11): #dado um padraoRevocacao(r) escolho a precisao maior ou igual ao seu correspondente
        if(not (padraoRevocacao*10 >= maiorPrecisao*100)):
            for i in range(len(revocacao)): 
                p = precisao[i]
                r = revocacao[i]

                if(padraoRevocacao*10 <= p*100):
                    #print(r)
                    chooseMax.append(r)
                
            maior = max(chooseMax)
            chooseMax.clear()
            interpolacao.append(maior)
            #print("maior: " + str(maior))
        else:
            interpolacao.append(0)
            

def main():
    arg = sys.argv
    filepath = arg[1]

    cMatrix = readReferenceCollection(filepath)
    
    mLen = len(cMatrix)
    referenceCollection = []
    consultResponse = []

    for i in range(mLen):
        if(i < mLen/2):
            referenceCollection.append(cMatrix[i])
        else:
            consultResponse.append(cMatrix[i])

    #colecaoReferencia = ["d12", "d56", "d9", "d25", "d3"]
    #consulta = ["d12", "d84", "d56", "d6", "d8", "d9", "d51", "d19", "d18", "d25", "d38", "d48", "d27", "d11", "d3"]

    matrizDeInterpolacoes = []
    aux = 0

    for i in range(int(mLen/2)):
        respostasSistema = consultResponse[i]
        respostasIdeais = referenceCollection[i]

        numVisitados = 0
        numRelevantes = 0
        totalRelevantes = len(respostasIdeais)
        precisao = []
        revocacao = []

        #calcula a precisao e revocacao
        for q in respostasSistema:
            numVisitados = numVisitados + 1
            for r in respostasIdeais:
                if(q == r): ## o documento r é relevante
                    numRelevantes = numRelevantes + 1
                    # calcula
                    r = round(numRelevantes/totalRelevantes, 2)
                    p = round(numRelevantes/numVisitados, 2)
                    
                    precisao.append(r)
                    revocacao.append(p) #esta certo  

        interpolacao  = []
        chooseMax = []

        #calcula a interpolacao
        maiorPrecisao = max(precisao)
        for padraoRevocacao in range(11): #dado um padraoRevocacao(r) escolho a precisao maior ou igual ao seu correspondente
            if(not (padraoRevocacao*10 >= maiorPrecisao*100)):
                for i in range(len(revocacao)): 
                    p = precisao[i]
                    r = revocacao[i]

                    if(padraoRevocacao*10 <= p*100):
                        #print(r)
                        chooseMax.append(r)
                    
                maior = max(chooseMax)
                chooseMax.clear()
                interpolacao.append(maior)
                #print("maior: " + str(maior))
            else:
                interpolacao.append(0)
        
        matrizDeInterpolacoes.append(interpolacao)

    medias = [0]*11 
    for linhaPorInterpolacao in matrizDeInterpolacoes:
        for i in range(len(linhaPorInterpolacao)):
            medias[i] += linhaPorInterpolacao[i]

    mediasFinais = []
    for x in medias:
        result = round(x / len(matrizDeInterpolacoes), 2)
        mediasFinais.append(result)

    writeInFile(mediasFinais)
main()