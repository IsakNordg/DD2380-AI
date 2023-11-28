import math

class Baum_Welch():
 
    def __init__(self):
        self.readInput()
        self.alpha = self.alphaPass()
        self.beta = self.betaPass()
        #self.gamma()
        self.maxIters = 10 #godtyckligt vald, har ingen aning
        self.iters = 0
        self.oldLogProb = float("-inf")

    def alphaPass(self):
        alpha = [[]]
        c = [0]
        for i in range(len(self.A)):
            alpha[0].append(self.pi[i] * self.B[i][self.sequence[0]]) # *
            c[0] += alpha[0][i]
        
        #Scale the alpha 0 (i)
        c[0] = 1 / c[0]
        for i in range(len(self.A)):
            alpha[0][i] = c[0] * alpha[0][i]

        for t in range(1, self.M):
            c.append(0)
            alpha.append([])
            for i in range(len(self.A)):
                alpha[t].append(0)
                for j in range(len(self.A)):
                    alpha[t][i] += alpha[t-1][j] * self.A[i][j] # transposed
                alpha[t][i] *= self.B[i][self.sequence[t]]
                c[t] += alpha[t][i]
        
            #Scale alpha t (i)
            c[t] = 1 / c[t]
            for i in range(len(self.A)):
                alpha[t][i] *= c[t]
            
        return alpha

           
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
        
        return beta


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

    def multiplyMatrixWithVector(self, M, v):
        result = []
        for i in range(len(M)):
            result.append(0)
            for j in range(len(M[0])):
                result[i] += M[i][j] * v[j]
        
        return result


test = Baum_Welch()