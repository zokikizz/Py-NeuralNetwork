import random
import math

#number of layers == number of inputs that is logic!

class NeuralNetwork:
    def __init__(self, numberOfLayers, numberOfInputs):
        self.bias = 1.0
        self.learningRate = 0.1

        self.trainingData = []
        self.validationData = []
        #creating neuron and delta matix, they are same dimentions
        self.Neurons = []
        self.delta = []
        numOfNeuronsInOneLayer = numberOfLayers
        counter = 0
        for i in range(numberOfLayers):
            self.Neurons.append([])
            self.delta.append([])
            for j in range(numOfNeuronsInOneLayer):
                self.Neurons[i].append(counter)
                self.delta[i].append(counter)
                counter = counter + 1
            numOfNeuronsInOneLayer = numOfNeuronsInOneLayer - 1
        
        #creating weights matix
        self.weights = []
        layerCounter = 0
        neuronCounter = 0
        noOfInputs = numberOfInputs

        for list in self.Neurons:
            self.weights.append([])
            for item in list:

                numOfWeights = noOfInputs + 1 # + 1 is bias

                self.weights[layerCounter].append([])

                for i in range(numOfWeights):
                    # self.weights[layerCounter][neuronCounter].append(neuronCounter)
                    self.weights[layerCounter][neuronCounter].append(random.random())

                neuronCounter = neuronCounter + 1

            noOfInputs = len(list)
            neuronCounter = 0
            layerCounter = layerCounter + 1
        

    
    def printNeurons(self):
        for list in self.Neurons:
            for item in list:
                print(item)
       
    def printDelta(self):
        for list in self.delta:
            for item in list:
                print(item)

    def printWeights(self):
        for layer in self.weights:
            print(layer)

    def readTrainingAndValidationData(self, fileName):
        
        with open(fileName, "r") as f:
            counter = 0
            for line in f:
                if counter < 1500:
                    self.trainingData.append([])

                    for s in line.split(","):
                        self.trainingData[counter].append(float(s))

                else:
                    self.validationData.append([])

                    currentIndex = counter-1500
                    for s in line.split(","):
                        self.validationData[currentIndex].append(float(s))

                
                counter = counter + 1

    #sigmoid
    def activationFunction(self, net):
        return (1 / (1 + math.exp(-net)))
    
    #counting net
    def computeNet(self, neuronI, neuronJ, listOfInputs):
        net = 0
        
        count = 0
        for w in self.weights[neuronI][neuronJ]:
            if count < len(listOfInputs):
                net = net + w * listOfInputs[count]
                conut = count + 1
            else:
                net = net + self.bias * w
        
        return net
    

    def Trening(self, num):
        

        for i in range(num):
            for inp in self.trainingData:
                inputs = []
                for i in range(3):
                    inputs.append(inp[i])
                
                target = inp[3]
                if target == 1:
                    target = 0.75
                else:
                    target = 0.25

                self.Execute(inputs)

                self.BackPropagation(inputs, target)
            
        
    def Execute(self, inputs):

        previousLayerOutput = inputs
        i = 0
        j = 0
        for layer in self.Neurons:

            for neuron in layer:
                neuron = self.activationFunction(self.computeNet(i,j,previousLayerOutput))
                j = j + 1

            previousLayerOutput = layer
            i = i+1
            j = 0

    def BackPropagation(self, inputs, target):
        self.OutputLayerBackPropagation(target)

        #hiddenlayers
        for i in range(len(self.Neurons) - 2, -2, -1):
            self.hiddenlayers(i)

        for i in range(len(self.Neurons)-1, 0, -1):
            if i == 0:
                input = inputs
            else:
                input = self.Neurons[i-1]
            self.updateWeights(i, input)

    def updateWeights(self, layer, inputs):
        wListNeuron = self.weights[layer]
        deltaLayer = self.delta[layer]

        i = 0
        j = 0

        for list in wListNeuron:
            for w in list:
                
                if j < (len(list) -1):
                    w =  w + (self.learningRate * deltaLayer[i] * inputs[j])
                else:
                    w =  w + (self.learningRate * deltaLayer[i] * self.bias)
                      
                j = j + 1 

            j = 0
            i = i + 1
        
        return
    
    def OutputLayerBackPropagation(self, target):
        output = self.Neurons[-1][0]
        self.delta[-1][0] = output * (1 - output) * (target - output)
        return
    
    def hiddenlayers(self, noOfLayer):
        neurons = self.Neurons[noOfLayer]

        i = 0
        for neuronOutput in neurons:
            self.Help(noOfLayer, i)
            i = i + 1

    def Help(self, noLayer, CurrentNeuron):
        next = noLayer + 1

        temp = 0
        for i in range(len(self.Neurons[next])):
            temp = temp + self.weights[next][i][CurrentNeuron] * self.delta[next][i]

        self.delta[noLayer][CurrentNeuron] = (1 - self.Neurons[noLayer][CurrentNeuron]) * self.Neurons[noLayer][CurrentNeuron] * temp

    
    def validate(self):
        correct = 0
        survived = 0
        jackPot = 0

        for person in self.validationData:
            inputs = []
            for i in range(3):
                inputs.append(person[i])

            target = person[3]
            if target == 1:
                target = 'S'
                survived = survived + 1
            else:
                target = 'D'

            self.Execute(inputs)
            
            res = ''
            if self.Neurons[-1][0] >= 0.5:
                res = 'S'
            else:
                res = 'D'

            print(res)

            if(res == target):
                correct = correct + 1
                if res == 'S':
                    jackPot = jackPot + 1
        

        print(str((correct/700.00)*100) + "%")
        print(str(((jackPot/survived)*100)) + "%")
        return

        
        
