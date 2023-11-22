
class HMM:
    def __init__(self):
        self.readInput()
        output = self.calcOutDist(self.A, self.B, self.pi)
        self.printOutput(output)

    def calcOutDist(self, A, B, pi):
        # A is the transition matrix
        # B is the emission matrix
        # pi is the initial distribution

        # pi * A * B
        output = self.multiplyMatrices(self.multiplyMatrices(pi, A), B)

        return output[0]
    
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

        self.A = self.formatMatrix(A)
        self.B = self.formatMatrix(B)
        self.pi = self.formatMatrix(pi)

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
                
    def printOutput(self, output):
        print("1 " + str(len(output)) + " ", end="")
        for i in range(len(output)):
            print(str(round(output[i], 2)) + " ", end="")
            

def main():
    hmm = HMM()



if __name__ == "__main__":
    main()