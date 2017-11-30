import csv
import random
import math
import operator

class Berita:
    def __init__(self, id, like, provokasi, komentar, emosi, hoax):
        self.id = id
        self.like = like
        self.provokasi = provokasi
        self.komentar = komentar
        self.emosi = emosi
        self.hoax = hoax


def loadData(file, outputSet=[]):
    with open(file, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(1, len(dataset) - 1):
            hoax = 0
            if(dataset[x][5] == '?') :
                hoax = -1
            else :
                hoax = float(dataset[x][5])
            berita = Berita(dataset[x][0],float(dataset[x][1]),float(dataset[x][2]),float(dataset[x][3]),float(dataset[x][4]),hoax)
            outputSet.append(berita)


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


def main():

    datatraining = []
    datatest = []
    loadData('Datatraining.csv',datatraining)
    loadData('Datates.csv',datatest)
    for x in datatraining :
        print(x.komentar)
    #
    # # prepare data
    # trainingSet = []
    # testSet = []
    # split = 0.67
    # loadDataset('iris.data', split, trainingSet, testSet)
    # print
    # 'Train set: ' + repr(len(trainingSet))
    # print
    # 'Test set: ' + repr(len(testSet))
    # # generate predictions
    # predictions = []
    # k = 3
    # for x in range(len(testSet)):
    #     neighbors = getNeighbors(trainingSet, testSet[x], k)
    #     result = getResponse(neighbors)
    #     predictions.append(result)
    #     print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    # accuracy = getAccuracy(testSet, predictions)
    # print('Accuracy: ' + repr(accuracy) + '%')


main()