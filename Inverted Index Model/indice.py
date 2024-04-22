import sys
import matplotlib.pyplot as plt

def readEnty(filepath):
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
            print(element, end=" ")
        print() 
    
def writeInFile(media):
    asString = [str(value) for value in media]
    asString = ' '.join(asString)

    with open('media.txt', 'w') as file:
        file.write(asString)    

def plotSingleGraph(entry):
    plt.plot(entry)
    plt.title("Media")
    plt.show()

def plotGraphs(entries):
    graphsNum = len(entries)
    
    if graphsNum == 1:
        fig, ax = plt.subplots(figsize=(10, 3))  # Create single axis
        ax.plot(entries[0])
        ax.set_title("Consulta 0")  # Adjust title index if necessary
    else:
        fig, axs = plt.subplots(1, graphsNum, figsize=(10, 3))
        for i in range(graphsNum):
            axs[i].plot(entries[i])
            axs[i].set_title("Consulta " + str(i))

    plt.tight_layout()
    plt.show()


def main():
    arg = sys.argv
    filepath = arg[1]

    cMatrix = readEnty(filepath)
    
    mLen = len(cMatrix)
    referenceCollection = []
    consultResponse = []

    for i in range(mLen):
        if(i < mLen/2):
            referenceCollection.append(cMatrix[i])
        else:
            consultResponse.append(cMatrix[i])

    matrizDeInterpolacoes = []

    for i in range(int(mLen/2)):
        respostasSistema = consultResponse[i]
        respostasIdeais = referenceCollection[i]

        visitedNum = 0
        relevantNum = 0
        allRelevants = len(respostasIdeais)
        precision = []
        revocation = []
        interpolation  = []

        #calcula metricas
        for system_response in respostasSistema:
            visitedNum += 1
            for ideal_response in respostasIdeais:
                if system_response == ideal_response:
                    relevantNum += 1
                    #separa as matrizes de resposta
                    revocation.append(relevantNum / allRelevants)
                    precision.append(relevantNum / visitedNum)
                    break

        #calcula a interpolacao
        maiorPrecisao = max(revocation)
        for padraoRevocacao in range(11):
            if padraoRevocacao * 10 <= maiorPrecisao * 100: #calcula apenas as precisões das revocações maiores ou iguais a de interesse
                #calculando max(p()) para o nivel padrão x de revocação em tuplas
                relevant_precisions = []
                for p, r in zip(precision, revocation):
                    if r * 100 >= padraoRevocacao * 10: #verificando valores de interesse
                        relevant_precisions.append(p)

                if relevant_precisions:
                    max_precision = max(relevant_precisions)
                    interpolation.append(max_precision)
                else:
                    interpolation.append(0)
            else:
                interpolation.append(0)

        matrizDeInterpolacoes.append(interpolation)

        medias = [sum(col) for col in zip(*matrizDeInterpolacoes)] #somando as colunas do vetor de media
        mediasFinais = [round(x / len(matrizDeInterpolacoes), 2) for x in medias]  #calculando a média soma coluna/num consultas

    writeInFile(mediasFinais)

    percentageEntry = []

    for value in mediasFinais:
        percentageEntry.append(value*100)
    
    plotSingleGraph(percentageEntry)
    plotGraphs(matrizDeInterpolacoes)
main()