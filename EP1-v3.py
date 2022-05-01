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
        d = np.zeros(n)
        diagC = np.zeros(n)
        diagA = np.zeros(n)
        diagB = np.zeros(n)

        ## Valores da diagonal superior ##
        diagC[0] = 3
        diagC[1] = 2
        diagC[2] = -1
        diagC[3] = 2
        diagC[4] = 0

        ## Valores da diagonal principal ##
        diagB[0] = -1
        diagB[1] = 5
        diagB[2] = -2
        diagB[3] = 6
        diagB[4] = 1
        
        ## Valores da diagoal inferior ##
        diagA[0] = 0
        diagA[1] = 4
        diagA[2] = 1
        diagA[3] = 4
        diagA[4] = 9       

        ## Resultado do sistema ##
        d[0] = 10
        d[1] = -7
        d[2] = -5
        d[3] = 4
        d[4] = 2

        ## Geracao da matriz tridiagonal A completa com os coeficientes,   ##
        ## para usar o algoritmo de resolucao de matriz sem otimizacao     ##
        A = np.zeros((n,n))
        for i in range (0,n-1):
            A[i][i]   = diagB[i]
            A[i+1][i] = diagA[i+1]
            A[i][i+1] = diagC[i]
        A[n-1][n-1] = diagB[n-1]


    elif(opcao == 2): ## CASO 2: usuario informa a matriz ##
        ## Usuario define tamanho n da matriz ##
        ciclica = int(input("A matriz tridiagonal a ser digitada é ciclica? 0- NAO | 1- SIM    "))
        n = int(input("Qual o tamanho desejado para a matriz quadrada?  "))

        ## Gera os vetores/matrizes com todos as casas iguais a zero ##
        d = np.zeros(n)
        diagA = np.zeros(n)
        diagB = np.zeros(n)
        diagC = np.zeros(n)

        ## Input da matriz A ##
        print("Preencheremos a matriz A agora:")

        print("Diagonal Superior:")
        if (ciclica == 0):
            for i in range(0, n-1):
                print("c[", i+1, "]:  ", sep='',end='')
                diagC[i] = input()
        elif(ciclica == 1):
            for i in range(0, n):
                print("c[", i+1, "]:  ", sep='',end='')
                diagC[i] = input()
        
        print("Diagonal Principal:")
        for i in range(0, n):
            print("b[", i+1, "]:  ", sep='',end='')
            diagB[i] = input()
        
        print("Diagonal Inferior:")
        if (ciclica == 0):
            for i in range(1, n):
                print("a[", i+1, "]:  ", sep='',end='')
                diagA[i] = input()
        elif(ciclica == 1):
            for i in range(0, n):
                print("a[", i+1, "]:  ", sep='',end='')
                diagA[i] = input()              

        ## Input da matriz resultado ##
        print("Preencha os valores da matriz 'b' agora:")
        for l in range(0, n):
            print("d[", l+1, "]:  ", end='', sep ='')
            d[l] = int(input())

        ## Geracao da matriz tridiagonal A completa com os coeficientes,   ##
        ## para usar o algoritmo de resolucao de matriz sem otimizacao     ##
        A = np.zeros((n,n))
        if (ciclica == 0):
            for i in range (0,n-1):
                A[i][i]   = diagB[i]
                A[i+1][i] = diagA[i+1]
                A[i][i+1] = diagC[i]
            A[n-1][n-1] = diagB[n-1]
        elif(ciclica == 1):
            A[0][n-1] = diagA[0]
            A[n-1][0] = diagC[n-1]
            for i in range (0,n-1):
                A[i][i]   = diagB[i]
                A[i+1][i] = diagA[i+1]
                A[i][i+1] = diagC[i]
            A[n-1][n-1] = diagB[n-1]

    else: ## CASO 3: usuario escolhe que o programa gere a matriz e o resultado ##
        n = int(input("Qual o tamanho desejado para a matriz quadrada? "))
        
        ## Cria vetores/arrays preenchidos com zero ##
        diagA = np.zeros(n)
        diagC = np.zeros(n)
        diagB = np.zeros(n)
        d = np.zeros(n)

        ## Gera matriz com coeficientes baseados em formulas dadas pelo enunciado ##
        gerarMatrizTridiagonal(n,diagA,diagB,diagC,d)

        ## Geracao da matriz tridiagonal A completa com os coeficientes,   ##
        ## para usar o algoritmo de resolucao de matriz sem otimizacao     ##
        A = np.zeros((n,n))
        A[0][n-1] = diagA[0]
        A[n-1][0] = diagC[n-1]
        for i in range (0,n-1):
            A[i][i]   = diagB[i]
            A[i+1][i] = diagA[i+1]
            A[i][i+1] = diagC[i]
        A[n-1][n-1] = diagB[n-1]
       
    ## Geracao dos vetores L e U do sistema ##
    vetU = np.zeros(n)
    vetL = np.zeros(n)
    decomposicaoLU(n, diagA, diagB, diagC, vetU, vetL)

    print("Aqui estão as diagonais da matriz A:")
    printBonito('       c', diagC)
    printBonito('       b', diagB)
    printBonito('       a', diagA)
    print()

    print("Aqui está o resultado do sistema linear:")
    printBonito('       d', d)
    print()

    print("Aqui estão os vetores resultados da decomposição LU:")
    printBonito('       L', vetL)
    printBonito('       U', vetU)
    print()

    print("Aqui está o resultado final:")
    printBonito('       x', resolveTridiagonalCiclica(n, diagA, diagB, diagC, d))

    print("\nObserve, por fim, que o resultado obtido acima é compatível com o resultado abaixo do algoritmo mais básico, que não possui nenhuma otimizacao levando em conta as casas iguais a zero: ")

    ## Calcula a resposta e printa para o usuario, usando ##
    ## o algoritmo nao otimizado, que usa matrizes        ##                                                  ##
    resposta = resolveMatrizQualquer(n,A,d)
    printBonito("x",resposta)



## Funcao auxiliar para imprimir vetores deste exercicio-programa ##
def printBonito(letra, vetor):
    print(letra, " = [", end='', sep='')
    for i in range(0, len(vetor)):
        print("%.8f" % vetor[i], end='')
        if (i < len(vetor)-1):
            print("; ", end='')
    print("]")



## Funcao que retorna os vetores L e U de matrizes tridiagonais ##
def decomposicaoLU(n, diagA, diagB, diagC,vetU,vetL):
    vetU[0] = diagB[0]
    for i in range (1,n):
        vetL[i] = (diagA[i])/vetU[i-1]
        vetU[i] = diagB[i] - vetL[i]*diagC[i-1]



## Funcao que resolve uma matriz generica usando LU sem otimizacao ##
def resolveMatrizQualquer(n,A,b):
    ## Cria as matrizes L, U, x e y ##
    L = np.zeros((n,n))
    U = np.zeros((n,n))

    y = np.zeros((n,1))
    x = np.zeros((n,1))

    ## Calcula os valores das matrizes L e U ##
    for i in range(0,n):
        U[i, i:n] = A[i, i:n] - np.dot(L[i, 0:i], U[0:i, i:n])
        L[i:n, i] = (A[i:n, i] - np.dot(L[i:n, 0:i],U[0:i, i])) / U[i,i]

    ## Calcula as raizes de y ##
    for i in range(0,n):
        y[i] = -1*(np.dot(L[i, 0:i], y[0:i])) + b[i]

    ## Calcula as raizes de x ##
    for i in range(n-1,-1,-1):
        x[i] = (-1*(np.dot(U[i, i+1:n], x[i+1:n])) + y[i]) / U[i][i]

    ## Retorna vetor com raizes do sistema ##
    return x



## Funcao que resolve uma matriz tridiagonal usando vetores com otimizacao ##
def resolveTridiagonal(n, diagA, diagB, diagC, d):
    ## Geracao dos vetores L e U do sistema ##
    vetU = np.zeros(n)
    vetL = np.zeros(n)
    decomposicaoLU(n, diagA, diagB, diagC, vetU, vetL)

    ## Criacao dos vetores x e y ##
    vetX = np.zeros(n)
    vetY = np.zeros(n)

    ## Obtencao dos valores de y ##
    vetY[0] = d[0]
    for i in range(1, n):
        vetY[i] = d[i] - vetL[i]*vetY[i-1]

    ## Obtencao dos valores de x ##
    vetX[n-1] = vetY[n-1]/vetU[n-1]
    for i in range(n-2, -1, -1):
        vetX[i] = (vetY[i] - (diagC[i]*vetX[i+1]))/vetU[i]
    
    ## Retorna o vetor x ##
    return vetX



## Funcao que resolve uma matriz tridiagonal ciclica usando vetores com otimizacao ##
def resolveTridiagonalCiclica(n, diagA, diagB, diagC, d):
    ## Geracao dos vetores a, b e c da matriz T ##
    diagAT = np.zeros(n-1)
    diagAT[1:n-1] = diagA[1:n-1]

    diagBT = diagB[0:n-1]

    diagCT = np.zeros(n-1)
    diagCT[0:n-2] = diagC[0:n-2]

    ## Geracao dos vetores dTil e v ##
    dTil = d[0:n-1]
    v = np.zeros(n-1)
    v[0] = diagA[0]
    v[n-2] = diagC[n-2]

    ## Resolve os sistemas T.yTil = dTil e T.zTil = v, encontrando ##
    ## os vetores yTil e zTil.                                     ##
    yTil = resolveTridiagonal(n-1, diagAT, diagBT, diagCT, dTil)
    zTil = resolveTridiagonal(n-1, diagAT, diagBT, diagCT, v)
    
    ## Encontra o vetor x ##
    xn = ( d[n-1] - (diagC[n-1]*yTil[0]) - (diagA[n-1]*yTil[n-2]) ) / ( diagB[n-1] - (diagC[n-1]*zTil[0]) - (diagA[n-1]*zTil[n-2]) )
    xTil = yTil - (xn * zTil)
    x = np.zeros(n)
    x[0:n-1] = xTil
    x[n-1] = xn
    
    ## Retorna o vetor x ##
    return x



## Funcao que gera valores ai, bi, ci e di com as equacoes fornecidas nas instrucoes, para n qualquer ##
def gerarMatrizTridiagonal(n,diagA,diagB,diagC,d):
    ## Geracao do vetor da diagonal inferior ##
    for i in range(0, n-1):
       diagA[i] = (2*(i+1) - 1)/(4*(i+1))
    diagA[n-1] = ((2*n)-1)/(2*n)

    ## Geracao do vetor da diagonal superior ##
    diagC[0:n] = 1 - diagA[0:n]

    ## Geracao do vetor da diagonal principal ##
    diagB[0:n] = 2

    ## Geracao o vetor de respostas do sistema linear ##
    for i in range(0,n):
        d[i] = np.cos((2*np.pi*(i+1)*(i+1))/(n*n))



## Comanda o programa a voltar para a funcao main ##
if __name__ == '__main__':
    main()