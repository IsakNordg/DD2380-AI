import math

class HMM:
    def __init__(self):
        self.readInput()
        self.delta, self.backptr = self.forwardPass()
        output = self.backwardPass()
        print(" ".join(map(str, output)))
    
    def forwardPass(self):
        delta = []
        backptr = []
        A_T = self.transpose(self.A)
        B_T = self.transpose(self.B)

        delta.append([])
        delta_0 = self.elementWiseProduct(self.pi, B_T[self.sequence[0]])
        for i in range(len(delta_0)):
            tmp = -math.inf if delta_0[i] == 0.0 else math.log(delta_0[i])
            delta[0].append(tmp)

        for i in range(1, self.M):
            delta.append([])
            backptr.append([])
            for j in range(len(self.A)):
                tmp = []
                for k in range(len(self.A)):                    
                    
                    a = delta[i-1][k]
                    b = -math.inf if A_T[j][k] == 0.0 else math.log(A_T[j][k])
                    c = -math.inf if B_T[self.sequence[i]][j] == 0.0 else math.log(B_T[self.sequence[i]][j])

                    tmp.append(a + b + c)

                delta[i].append(max(tmp))
                backptr[i-1].append(tmp.index(max(tmp)))

        return delta, backptr

    def backwardPass(self):
        mostProbableSequence = []
        mostProbableSequence.append(self.delta[self.M-1].index(max(self.delta[self.M-1])))
        for i in range(self.M-2, -1, -1):
            mostProbableSequence.append(self.backptr[i][mostProbableSequence[self.M-2-i]])

        return mostProbableSequence[::-1]


    def elementWiseProduct(self, X, Y):
        result = []
        for i in range(len(X)):
            result.append(X[i] * Y[i])
        
        return result

    def transpose(self, X):
        return list(map(list, zip(*X)))
    
    def multiplyMatrixWithVector(self, M, v):
        result = []
        for i in range(len(M)):
            result.append(0)
            for j in range(len(M[0])):
                result[i] += M[i][j] * v[j]
        
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

    def readInput(self):
        A = input()
        B = input()
        pi = input()
        sequence = input()

        self.A = self.formatMatrix(A)
        self.B = self.formatMatrix(B)
        self.pi = self.formatMatrix(pi)[0]
        self.sequence = self.formatSequence(sequence)
    
    def formatSequence(self, sequence):
        sequence = sequence.split(" ")
        self.M = int(sequence[0])
        sequence = sequence[1:-1]
        formattedSequence = []
        for i in range(self.M):
            formattedSequence.append(int(sequence[i]))
        
        return formattedSequence

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
            
            

def main():
    hmm = HMM()



if __name__ == "__main__":
    main()