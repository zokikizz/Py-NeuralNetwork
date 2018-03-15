# test = input("Something:")

# print(test)

from NeuralNetworkLibrary.NeuralNetwork import NeuralNetwork


#works creating weights, delta and neuron matix
n = NeuralNetwork(3,3)

#n.printWeights()

n.readTrainingAndValidationData("./Data/titanicRecords.dat")

n.Trening(50)
n.validate()
