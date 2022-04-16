###     MAP3121 - Calculo Numerico - Escola Politecnica                  ###
###     Tarefa 1 - Decomposicao LU para Matrizes Tridiagonais            ###

###     Alunos deste grupo:                                              ###       
###     Fabio Akira Yonamine   - NUSP 11805398                           ###
###     Pedro H. Teodoro Silva - NUSP 11805314                           ###

import numpy as np


def main():
    opcao = int(input("1- Usar valores pre-cadastrados de matriz tridiagonal \n2- Inserir seus proprios valores \n3- Gerar coeficientes tridiagonais\n"))
    if(opcao == 1):#caso em que o usuario escolhe a matriz pre-cadastrada
        #tamanho da matriz
        n = 5

        #zerando os vetores/matrizes
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

        #diagonal principal
        diagB[0] = -1
        diagB[1] = 5
        diagB[2] = -2
        diagB[3] = 6
        diagB[4] = 1
        
        #diagoal inferior
        diagA[0] = 4
        diagA[1] = 1
        diagA[2] = 4
        diagA[3] = 9
        diagA[4] = 0       

        #resultado do sistema
        d[0] = 10
        d[1] = -7
        d[2] = -5
        d[3] = 4
        d[4] = 2

    elif(opcao == 2):#caso em que o usuario da input na matriz
        #tamanho da matriz
        n = int(input("Qual o tamanho desejado para a matriz quadrada?  "))

        #zerando os vetores/matrizes
        A = np.zeros((n,n))
        d = np.zeros((n,1))
        diagA = np.zeros(n)
        diagB = np.zeros(n)
        diagC = np.zeros(n)

        #input da matriz A
        print("Preencheremos a matriz A agora...")
        for l in range(0, n):
            print("Linha [", l, "]    ",sep='')
            for c in range(0, n):
                print("Coluna [", c, "]   ", end ='', sep='')
                A[l][c] = float(input())
            print()


        #checa se a matriz eh tridiagonal (teoricamente so vamos mexer com esse tipo de matriz)
        #caso nao seja tridiagonal da a opcao de dar input novamente
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
    vetY = np.zeros(n)
    resolveSistema(n, diagC, d, vetU, vetL, vetX, vetY)


def decomposicaoLU(n, diagA, diagB, diagC,vetU,vetL):
    #pra mim oq vem abaixo eh magia negra e eu n sei como funciona, so sei que funciona
    vetU[0] = diagB[0]
    for i in range (1,n):
        vetL[i] = (diagA[i-1])/vetU[i-1]
        vetU[i] = diagB[i] - vetL[i]*diagC[i-1]
    #print("L = ",vetL)
    #print("U = ",vetU)

def resolveSistema(n, diagC, d, vetU, vetL, vetX, vetY):
    # sim sim, matematica
    vetY[0] = d[0]
    for i in range(1, n):
        vetY[i] = d[i] - vetL[i]*vetY[i-1]
    #print("Y = ",vetY)
    # quase la
    vetX[n-1] = vetY[n-1]/vetU[n-1]
    for i in range(n-2, -1, -1): #confia, isso daqui eh um jogo de fe
        vetX[i] = (vetY[i] - (diagC[i]*vetX[i+1]))/vetU[i]
    #print("X = ",vetX)
    # finalmente
    print("Resultado encontrado:\n[", end='')
    for i in range(0, n):
        print("%.8f" % vetX[i], end='')
        if (i < n-1):
            print("; ", end='')
    print("]")


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

    #print("A = ", diagA)

    #gerando o vetor da diagonal superior
    for i in range(0, n-1):
        diagC[i] = 1 - diagA[i]

    #print("C = ", diagC)
    #gerando o vetor da diagonal principal
    for i in range(0, n):
        diagB[i] = 2

    #print("B = ", diagB)
    #gerando o vetor de respostas do sistema linear
    for i in range(0,n):
        d[i] = np.cos((2*np.pi*(i+1)*(i+1))/(n*n))
    #print("d = ", d)


#falando pro compilador ir pra main
if __name__ == '__main__':
    main()