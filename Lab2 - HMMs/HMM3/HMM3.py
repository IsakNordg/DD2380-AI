import math

class Baum_Welch():
 
    def __init__(self):
        self.readInput()
        self.betaPass()
        self.maxIters = 10 #godtyckligt vald, har ingen aning
        self.iters = 0
        self.oldLogProb = float("-inf")

    def readInput(self):
        A = input()
        B = input()
        pi = input()
        sequence = input()

        self.A = self.formatMatrix(A)
        self.B = self.formatMatrix(B)
        self.pi = self.formatMatrix(pi)[0]
        self.sequence = self.formatSequence(sequence)

    def formatMatrix(self, matrix):
        matrix = matrix.split(" ")
        rows = int(matrix[0])
        columns = int(matrix[1])
        matrix = matrix[2:-1]

        formattedMatrix = []
        for i in range(rows):
            formattedMatrix.append([])
            for j in range(columns):
                formattedMatrix[i].append(float(matrix[i * columns + j]))
        
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
            result.append(X[i] * Y[i])
    
        return result

    def multiplyMatrices(self, X, Y):
        result = [[0 for x in range(len(Y[0]))] for y in range(len(X))]
        # iterate through rows of X
        for i in range(len(X)):
            # iterate through columns of Y
            for j in range(len(Y[0])):
                # iterate through rows of Y
                for k in range(len(Y)):
                    result[i][j] += X[i][k] * Y[k][j]

        return result


    def alphaPass(self):
        alpha = []
        alpha.append(self.elementWiseProduct(self.pi, self.transpose(self.B)[self.sequence[0]]))
        for i in range(1, self.M):
            A_T = self.transpose(self.A)
            alpha.append(self.elementWiseProduct(self.multiplyMatrixWithVector(A_T, alpha[i - 1]), self.transpose(self.B)[self.sequence[i]]))

        return sum(alpha[self.M-1]) 
           
    def betaPass(self):
        beta = [[]]

        #Timestep T
        for i in range(len(self.A)):
            beta[0].append(1)

        for t in range(len(self.sequence)-1):
            beta.insert(0,[])
            for i in range(len(self.A)): #current states
                sum = 0
                for j in range(len(self.A)): #states after

                    nextVal = beta[1][j] # Next beta value
                    transVal = -math.inf if self.A[i][j] == 0.0 else math.log(self.A[i][j])
                    obsVal = -math.inf if self.B[j][self.sequence[i]] == 0.0 else math.log(self.B[j][self.sequence[i]])
                    sum += nextVal + transVal + obsVal
                beta[0].append(sum)

            print(t)

    
test = Baum_Welch()