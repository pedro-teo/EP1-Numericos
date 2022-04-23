###     MAP3121 - Calculo Numerico - Escola Politecnica                  ###
###     Tarefa 1 - Decomposicao LU para Matrizes Tridiagonais            ###

###     Alunos deste grupo:                                              ###       
###     Fabio Akira Yonamine   - NUSP 11805398                           ###
###     Pedro H. Teodoro Silva - NUSP 11805314                           ###

import numpy as np


def main():
    opcao = int(input("1- Usar valores pre-cadastrados de matriz tridiagonal \n2- Inserir seus proprios valores \n3- Gerar coeficientes tridiagonais\n"))
    if(opcao == 1):## CASO 1: usuario escolhe a matriz pre-cadastrada ##
        ## Tamanho n da matriz ##
        n = 5

        ## Gera os vetores/matrizes com todos as casas iguais a zero ##
        A = np.zeros((n,n))
        d = np.zeros((n,1))
        diagC = np.zeros(n)
        diagA = np.zeros(n)
        diagB = np.zeros(n)

        #aqui tinha uma matriz convencional, troquei pro modo de vetores q ele pede no enunciado
        #diagonal superior
        diagC[0] = 3
        diagC[1] = 2
        diagC[2] = -1
        diagC[3] = 2
        diagC[4] = 0

        ## Diagonal principal ##
        diagB[0] = -1
        diagB[1] = 5
        diagB[2] = -2
        diagB[3] = 6
        diagB[4] = 1
        
        ## Diagoal inferior ##
        diagA[0] = 4
        diagA[1] = 1
        diagA[2] = 4
        diagA[3] = 9
        diagA[4] = 0       

        ## Resultado do sistema ##
        d[0] = 10
        d[1] = -7
        d[2] = -5
        d[3] = 4
        d[4] = 2

    elif(opcao == 2): ## CASO 2: usuario informa a matriz ##
        ## Usuario define tamanho n da matriz ##
        n = int(input("Qual o tamanho desejado para a matriz quadrada?  "))

        ## Gera os vetores/matrizes com todos as casas iguais a zero ##
        A = np.zeros((n,n))
        d = np.zeros((n,1))
        diagA = np.zeros(n)
        diagB = np.zeros(n)
        diagC = np.zeros(n)

        ## Input da matriz A ##
        print("Preencheremos a matriz A agora...")
        for l in range(0, n):
            print("Linha [", l, "]    ",sep='')
            for c in range(0, n):
                print("Coluna [", c, "]   ", end ='', sep='')
                A[l][c] = float(input())
            print()


        ## Checa se a matriz eh tridiagonal (teoricamente so vamos mexer com esse tipo de matriz) ##
        ## OBS: Caso nao seja tridiagonal, da a opcao de dar input novamente                      ##
        while(ehMatrizTridiagonal(A, n) == False):
            print("Aviso: a matriz 'A' preenchida nao eh tridiagonal.")
            print("Deseja preencher a matriz novamente? y/n")
            resp = input()
            if(resp == "y"):
                for l in range(0, n):
                    print("Linha ", l, "    ")
                    for c in range(0, n):
                        print("Coluna[", c, "]   ", end = '', sep='')
                        A[l][c] = int(input())
                    print()
            if(resp == "n"):
                break
        
        #colocando a matriz grande em vetores pra facilitar umas contas la na frente
        if (ehMatrizTridiagonal(A, n) == True):
            #pegando os valores da diagonal superior
            for i in range(0, n-1):
                diagC[i] = A[i][i+1]
            
            #pegando os valores da diagonal principal
            for i in range(0,n):
                diagB[i] = A[i][i]

            #pegando os valores da diagonal infeior
            for i in range(0,n-1):
                diagA[i] = A[i+1][i]
                

        #input da matriz resultado
        print("Preencha os valores da matriz b agora...")
        for l in range(0, n):
            print("Linha[", l, "]    ", end='')
            d[l] = int(input())
        
    else:#caso em que o usuario escolhe que o programa gere a matriz e o resultado
        n = int(input("Qual o tamanho desejado para a matriz quadrada? "))
        
        #zerando os vetores/arrays
        A = np.zeros((n,n))
        diagA = np.zeros((n))
        diagC = np.zeros((n))
        diagB = np.zeros((n))
        d = np.zeros((n))

        #gerando matriz com coeficientes baseados em formulas dadas pelo enunciado
        gerarMatrizTridiagonal(n,diagA,diagB,diagC,d)

       
    #fazendo as contas da decomposicao
    vetU = np.zeros(n)
    vetL = np.zeros(n)
    decomposicaoLU(n, diagA, diagB, diagC, vetU, vetL)

    #resolvendo o sistema
    vetX = np.zeros(n)
    vetX = resolveTridiagonal(n, diagA, diagB, diagC, d)

    respostaFinalCiclico = resolveTridiagonalCiclica(n, diagA, diagB, diagC, d)
    printBonito('resposta', respostaFinalCiclico)



def printBonito(letra, vetor):
    print(letra, " = [", end='', sep='')
    for i in range(0, len(vetor)):
        print("%.8f" % vetor[i], end='')
        if (i < len(vetor)-1):
            print("; ", end='')
    print("]")


def decomposicaoLU(n, diagA, diagB, diagC,vetU,vetL):
    #pra mim oq vem abaixo eh magia negra e eu n sei como funciona, so sei que funciona
    vetU[0] = diagB[0]
    for i in range (1,n):
        vetL[i] = (diagA[i])/vetU[i-1] #aqui tava bugado os indices, arrumei
        vetU[i] = diagB[i] - vetL[i]*diagC[i-1]
    
    printBonito('L', vetL)
    printBonito('U' ,vetU)
    print("")

def resolveTridiagonal(n, diagA, diagB, diagC, d):
    # sim sim, matematica
    vetU = np.zeros(n)
    vetL = np.zeros(n)
    decomposicaoLU(n, diagA, diagB, diagC, vetU, vetL)

    vetX = np.zeros(n)
    vetY = np.zeros(n)

    vetY[0] = d[0]
    for i in range(1, n):
        vetY[i] = d[i] - vetL[i]*vetY[i-1]
    printBonito('Y', vetY)
    # quase la
    vetX[n-1] = vetY[n-1]/vetU[n-1]
    for i in range(n-2, -1, -1): #confia, isso daqui eh um jogo de fe
        vetX[i] = (vetY[i] - (diagC[i]*vetX[i+1]))/vetU[i]
    
    # finalmente
    printBonito('X', vetX)
    return vetX

def resolveTridiagonalCiclica(n, diagA, diagB, diagC, d):
    ## Geracao dos vetores a, b e c da matriz T ##
    diagAT = np.zeros(n-1)
    diagAT[1:n-1] = diagA[1:n-1]

    diagBT = diagB[0:n-1]

    diagCT = np.zeros(n-1)
    diagCT[0:n-2] = diagC[0:n-2]

    printBonito('At', diagAT)
    printBonito('Bt', diagBT)
    printBonito('Ct', diagCT)

    ## Geracao dos vetores dTil e v ##
    dTil = d[0:n-1]
    v = np.zeros(n-1)
    v[0] = diagA[0]
    v[n-2] = diagC[n-2]

    printBonito('Dtil', dTil)
    printBonito('v', v)

    ## Resolve os sistemas T.yTil = dTil e T.zTil = v, encontrando ##
    ## os vetores yTil e zTil.                                     ##
    yTil = resolveTridiagonal(n-1, diagAT, diagBT, diagCT, dTil)
    zTil = resolveTridiagonal(n-1, diagAT, diagBT, diagCT, v)

    printBonito('yTil', yTil)
    printBonito('zTil', zTil)
    
    ## Encontra o vetor x, finalmente ##
    xn = ( d[n-1] - (diagC[n-1]*yTil[0]) - (diagA[n-1]*yTil[n-2]) ) / ( diagB[n-1] - (diagC[n-1]*zTil[0]) - (diagA[n-1]*zTil[n-2]) )
    xTil = yTil - (xn * zTil)
    x = np.zeros(n)
    x[0:n-1] = xTil
    x[n-1] = xn
    
    return x

#check se a matriz eh tridiagonal ou nao. caso seja retorna verdadeiro pq da pra vetorizar a matriz A
def ehMatrizTridiagonal(A, n):
    for i in range(0, n):
        for j in range(0, n):
            #se |i-j|>1 significa que estamos analisando uma casa de A fora das 3 diagonais, e se estamos, essa casa tem que ser == 0
            if(np.abs(i-j) > 1 and A[i][j] != 0):
                return False
    return True


#o enunciado da essa opcao pra gerar casos pra podermos testar se o programa funciona
def gerarMatrizTridiagonal(n,diagA,diagB,diagC,d):
    #gerando o vetor da diagonal inferior
    for i in range(0, n-1):
       diagA[i] = (2*(i+1) - 1)/(4*(i+1))
    diagA[n-1] = ((2*n)-1)/(2*n)

    #gerando o vetor da diagonal superior
    for i in range(0, n): ## ACHO QUE AQUI EH n, MAS TAVA n-1
        diagC[i] = 1 - diagA[i]

    #gerando o vetor da diagonal principal
    for i in range(0, n):
        diagB[i] = 2

    #gerando o vetor de respostas do sistema linear
    for i in range(0,n):
        d[i] = np.cos((2*np.pi*(i+1)*(i+1))/(n*n))
    
    printBonito('A', diagA)
    printBonito('B', diagB)
    printBonito("C", diagC)
    printBonito("D", d)
    print("")


## Comanda o programa a voltar para a funcao main ##
if __name__ == '__main__':
    main()