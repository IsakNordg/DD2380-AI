import math

class Baum_Welch():
 
    def __init__(self):
        self.readInput()
        self.maxIters = 300
        self.iters = 0
        self.oldLogProb = float("-inf")

        self.iterate()

    def iterate(self):
        self.alpha = self.alphaPass()
        self.beta = self.betaPass()
        self.gamma = self.gammaPass()
        self.reestimate()
        self.logprob = self.computeLogProb()
        self.iters += 1
        if self.iters < self.maxIters and self.logprob > self.oldLogProb:
            self.oldLogProb = self.logprob
            self.iterate()
        else:
            self.printOutput()
    
    def printOutput(self):
        print("          " + str(len(self.A)), len(self.A), end="")
        for i in range(len(self.A)):
            for j in range(len(self.A[0])):
                print(" " + str(round(self.A[i][j], 6)), end="")
        print()
        print(len(self.B), len(self.B[0]), end="")
        for i in range(len(self.B)):
            for j in range(len(self.B[0])):
                print(" " + str(round(self.B[i][j], 6)), end="")
        print()


    def alphaPass(self):
        alpha = [[]]
        c = [0]
        for i in range(len(self.A)):
            alpha[0].append(self.pi[i] * self.B[i][self.sequence[0]])
            c[0] += alpha[0][i]
        
        #Scale the alpha 0 (i)
        c[0] = 1 / c[0]
        for i in range(len(self.A)):
            alpha[0][i] = c[0] * alpha[0][i]

        # Compute alpha t (i)
        for t in range(1, self.M):
            c.append(0)
            alpha.append([])
            for i in range(len(self.A)):
                alpha[t].append(0)
                for j in range(len(self.A)):
                    alpha[t][i] += alpha[t-1][j] * self.A[j][i] # transposed
                alpha[t][i] *= self.B[i][self.sequence[t]]
                c[t] += alpha[t][i]

            #Scale alpha t (i)
            c[t] = 1 / c[t]
            for i in range(len(self.A)):
                alpha[t][i] *= c[t]
        
        self.c = c
        return alpha
        
    def betaPass(self):
        beta = [[]]
        for i in range(len(self.A)):
            beta[0].append(1)

        for t in range(self.M-2, -1, -1):
            beta.insert(0, [])
            for i in range(len(self.A)):
                beta[0].append(0)
                for j in range(len(self.A)):
                    beta[0][i] += self.A[i][j] * self.B[j][self.sequence[t+1]] * beta[1][j]
                beta[0][i] *= self.c[t]

        return beta

    def gammaPass(self):
        gamma = []
        digamma = []
        for t in range(len(self.sequence)-1):
            gamma.append([])
            digamma.append([])
            for i in range(len(self.A)):
                gamma[t].append(0)
                digamma[t].append([])
                for j in range(len(self.A)):                    
                    digamma[t][i].append(self.alpha[t][i] * self.A[i][j] * self.B[j][self.sequence[t+1]] * self.beta[t+1][j])
                    gamma[t][i] += digamma[t][i][j]
        
        gamma.append([])
        for i in range(len(self.A)):
            gamma[self.M-1].append(self.alpha[self.M-1][i])
        self.digamma = digamma
        return gamma
    
    def reestimate(self):
        # pi
        for i in range(len(self.A)):
            self.pi[i] = self.gamma[0][i]
        
        # A
        for i in range(len(self.A)):
            denom = 0
            for t in range(self.M-1):
                denom += self.gamma[t][i]
            
            for j in range(len(self.A)):
                numer = 0
                for t in range(self.M-1):
                    numer += self.digamma[t][i][j]
                self.A[i][j] = numer / denom

        # B
        for i in range(len(self.A)):
            denom = 0
            for t in range(self.M):
                denom += self.gamma[t][i]
            
            for j in range(len(self.B[0])):
                numer = 0
                for t in range(self.M):
                    if self.sequence[t] == j:
                        numer += self.gamma[t][i]
                    
                self.B[i][j] = numer / denom

    def computeLogProb(self):
        logProb = 0
        for i in range(self.M):
            logProb += math.log(self.c[i])

        logProb = -logProb

        return logProb
            
# ---------------------------------------------------------------
    def readInput(self):
        A = input()
        A = A.replace("          ", "")
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
    

test = Baum_Welch()