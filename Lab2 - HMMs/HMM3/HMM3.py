import math

class Baum_Welch():
 
    def __init__(self):
        self.readInput()
        sum = 0
        for element in self.forwardPass():
            sum += math.exp(element)
        print(round(sum, 6))
        #self.alphaPass()
        #self.betaPass()
        #self.gamma()
        self.maxIters = 10 #godtyckligt vald, har ingen aning
        self.iters = 0
        self.oldLogProb = float("-inf")


    def forwardPass(self):
        self.alpha = []
        B_T = self.transpose(self.B)
        self.alpha.append(self.elementWiseProduct(self.pi, B_T[self.sequence[0]]))
        for i in range(1, self.M):
            A_T = self.transpose(self.A)
            self.alpha.append(self.elementWiseProduct(self.multiplyMatrixWithVector(A_T, self.alpha[i - 1]), self.transpose(self.B)[self.sequence[i]]))

        return self.alpha[self.M-1]
    
    def alphaPass(self):
        self.alpha = [[]]
        self.c = [0]

        #compute alpha 0(i)
        for i in range(len(self.A)):
            pi = -math.inf if self.pi[i] == 0 else math.log(self.pi[i])
            b = -math.inf if self.B[self.sequence[0]][i] == 0 else math.log(self.B[self.sequence[0]][i])
            self.alpha[0].append(pi + b)
            self.c[0] += self.alpha[0][i]

        #Scale the alpha 0 (i)
        self.c[0] = math.log(1 / self.c[0])
        for i in range(len(self.A)):
            self.alpha[0][i] = 0

           
    def betaPass(self):
        self.beta = [[]]

        #Timestep T
        for i in range(len(self.A)):
            self.beta[0].append(1)

        for t in range(len(self.sequence)-1):
            self.beta.insert(0,[])
            for i in range(len(self.A)): #current states
                sum = 0
                for j in range(len(self.A)): #states after

                    nextVal = self.beta[1][j] # Next beta value
                    transVal = -math.inf if self.A[i][j] == 0.0 else math.log(self.A[i][j])
                    obsVal = -math.inf if self.B[j][self.sequence[i]] == 0.0 else math.log(self.B[j][self.sequence[i]])
                    sum += nextVal + transVal + obsVal
                self.beta[0].append(sum)


    def di_gamma(self):
        di_gamma = [] #Ev göra om till self? Och ropa på i const.
        denom = math.log(sum(self.alpha[self.M-1]))
        for t in range(len(self.sequence)):
            di_gamma.append([])
            for i in range(len(self.A)):
                di_gamma[t].append([])
                for j in range(len(self.A)):
                    nom = -math.inf if self.alpha[t][i] == 0.0 else math.log(self.alpha[t][i])
                    nom += -math.inf if self.A[j][i] == 0.0 else math.log(self.A[j][i])
                    nom += -math.inf if self.B[j][self.sequence[t+1]] == 0.0 else math.log(self.B[j][self.sequence[t+1]])
                    nom += self.beta[t+1][j]
                    di_gamma[t][i].append(nom / denom) 

    def gamma(self):
        di_gamma = self.di_gamma() 
        self.gamma = [] #Ev göra om till self? Och ropa på i const.
        for t in range(len(self.sequence)):
            self.gamma.append([])
            for i in range(len(self.A)):
                self.gamma[t].append(sum(di_gamma[t][i]))

    def readInput(self):
        A = input()
        B = input()
        pi = input()
        sequence = input()

        self.A = self.formatMatrix(A)
        self.B = self.formatMatrix(B)
        self.pi = self.formatMatrix(pi)[0]
        self.sequence = self.formatSequence(sequence)

    # Format input to a matrix of log values
    def formatMatrix(self, matrix):
        matrix = matrix.split(" ")
        rows = int(matrix[0])
        columns = int(matrix[1])
        matrix = matrix[2:-1]

        formattedMatrix = []
        for i in range(rows):
            formattedMatrix.append([])
            for j in range(columns):
                val = -math.inf if float(matrix[i * columns + j]) == 0.0 else math.log(float(matrix[i * columns + j])) 
                formattedMatrix[i].append(val)
        
        return formattedMatrix
    
    def formatSequence(self, sequence):
        sequence = sequence.split(" ")
        self.M = int(sequence[0])
        sequence = sequence[1:-1]
        formattedSequence = []
        for i in range(self.M):
            formattedSequence.append(int(sequence[i]))
        
        return formattedSequence
    
    def transpose(self, X):
        return list(map(list, zip(*X)))
    
    def elementWiseProduct(self, X, Y):
        result = []
        for i in range(len(X)):
            result.append(X[i] + Y[i])
    
        return result

    def multiplyMatrices(self, X, Y):
        result = [[0 for x in range(len(Y[0]))] for y in range(len(X))]
        # iterate through rows of X
        for i in range(len(X)):
            # iterate through columns of Y
            for j in range(len(Y[0])):
                # iterate through rows of Y
                for k in range(len(Y)):
                    result[i][j] += X[i][k] + Y[k][j]

        return result

    def multiplyMatrixWithVector(self, M, v):
        result = []
        for i in range(len(M)):
            result.append(0)
            for j in range(len(M[0])):
                result[i] += M[i][j] + v[j]
        
        return result


    
test = Baum_Welch()