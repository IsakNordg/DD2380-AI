import math

class HMM:
    def __init__(self):
        self.readInput()
        print(round(self.forwardPass(), 6))
    
    def forwardPass(self):
        alpha = []
        alpha.append(self.elementWiseProduct(self.pi, self.transpose(self.B)[self.sequence[0]]))
        A_T = self.transpose(self.A)
        B_T = self.transpose(self.B)
        for i in range(1, self.M):
            tmp = self.multiplyMatrixWithVector(A_T, alpha[i - 1])
            print("mult: ", tmp)
            tmp = self.elementWiseProduct(tmp, B_T[self.sequence[i]])
            print("prod:", tmp)
            alpha.append(tmp)

        print(alpha)


    def elementWiseProduct(self, X, Y):
        result = []
        for i in range(len(X)):
            result.append(X[i] + Y[i])
        
        return result

    def transpose(self, X):
        return list(map(list, zip(*X)))
    
    def multiplyMatrixWithVector(self, M, v):
        result = []
        for i in range(len(M)):
            result.append(0)
            for j in range(len(M[0])):
                result[i] += M[i][j] + v[j] #HÄR ÄR DET KNAS
        
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
                val = -math.inf if float(matrix[i * columns + j]) == 0.0 else math.log(float(matrix[i * columns + j]))
                formattedMatrix[i].append(val)
        
        return formattedMatrix
            

def main():
    hmm = HMM()


if __name__ == "__main__":
    main()