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

def loadData(file):
    outputSet = []
    with open(file, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(1, len(dataset)):
            hoax = 0
            if(dataset[x][5] == '?') :
                hoax = -1
            else :
                hoax = float(dataset[x][5])
            berita = Berita(dataset[x][0],float(dataset[x][1]),float(dataset[x][2]),float(dataset[x][3]),float(dataset[x][4]),hoax)
            outputSet.append(berita)
    return outputSet

def euclideanDistance(berita1, berita2):
    distance = 0
    distance += pow(berita1.like - berita2.like,2) + pow(berita1.provokasi - berita2.provokasi,2) + pow(berita1.komentar - berita2.komentar,2) + pow(berita1.emosi - berita2.emosi,2)
    return math.sqrt(distance)

def fold_dataset(dataset, kfold) :
    folded_dataset = []
    folded_n_data = len(dataset) / kfold
    for x in range(0, kfold):
        folded_dataset.append(dataset[int(x * folded_n_data):int(((x + 1) * folded_n_data))])
    return folded_dataset

def getNeighbors(dataset, berita, k):
    distances = []
    for x in range(len(dataset)):
        distance = euclideanDistance(berita, dataset[x])
        distances.append((dataset[x], distance))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def classification(neighbors):
    hoax = 0
    not_hoax = 0
    for neighbor in neighbors :
        if neighbor.hoax == 1:
            hoax += 1
        else:
            not_hoax += 1
    if hoax > not_hoax:
        return float(1)
    else:
        return float(0)

def fold_classification(fold_class) :
    hoax = 0
    not_hoax = 0
    for x in fold_class:
        if x == 1:
            hoax += 1
        else:
            not_hoax += 1
    if hoax > not_hoax:
        return float(1)
    else:
        return float(0)

def calculateAccuracy(dataset, predictions):
    correct = 0
    for x in range(len(dataset)) :
        print(dataset[x].id , " = " ,dataset[x].hoax, ", Predictions = ", predictions[dataset[x].id])
        if dataset[x].hoax == predictions[dataset[x].id] :
            correct += 1
    return (correct / float(len(dataset))) * 100.0

def writeToCsv(name, data, predictions) :
    file = open(name,'w')
    with file :
        writer = csv.writer(file)
        writer.writerow(['Berita','Like','Provokasi','Komentar','Emosi','Hoax'])
        for berita in data :
            writer.writerow([berita.id,berita.like,berita.provokasi,berita.komentar,berita.emosi,predictions[berita.id]])

def main():
    datatraining = loadData('Datatraining.csv')
    datatest = loadData('Datates.csv')
    k_folds = 4
    k_kind = [63]
    folded_datatraining = fold_dataset(datatraining,k_folds)
    #validasi biasa
    '''for k in k_kind :
        prediction = {}
        for berita in datatraining :
            neighbors = getNeighbors(datatraining,berita,k)
            prediction[berita.id] = classification(neighbors)
        print("K = ", k, ", Accuracy = ", calculateAccuracy(datatraining, prediction))
'''
    # #validasi k_fold
    # for k in k_kind :
    #     prediction = {}
    #     fold_classes = {}
    #     for k_fold in range(0, k_folds) :
    #         for berita in folded_datatraining[k_fold] :
    #             fold_classes[berita.id] = []
    #             for x in range(0,k_folds) :
    #                 if(x != k_fold) :
    #                     neighbors = getNeighbors(folded_datatraining[x], berita, k)
    #                     fold_classes[berita.id].append(classification(neighbors))
    #             prediction[berita.id] = fold_classification(fold_classes[berita.id])
    #     print("K = ", k, ", Accuracy = ",calculateAccuracy(datatraining, prediction))

    #testing
    #testing biasa
    # for k in k_kind:
    #     prediction = {}
    #     for berita in datatest:
    #         neighbors = getNeighbors(datatraining, berita, k)
    #         prediction[berita.id] = classification(neighbors)
    #     name = 'Normal Testing K=' + str(k) + '.csv'
    #     writeToCsv(name,datatest,prediction)

    #testing k_fold
    for k in k_kind:
        prediction = {}
        fold_classes = {}
        for k_fold in range(0, k_folds):
            for berita in datatest:
                fold_classes[berita.id] = []
                for x in range(0, k_folds):
                    if (x != k_fold):
                        neighbors = getNeighbors(folded_datatraining[x], berita, k)
                        fold_classes[berita.id].append(classification(neighbors))
                prediction[berita.id] = fold_classification(fold_classes[berita.id])
        name = 'K-Fold=4 Testing K=' + str(k) + '.csv'
        print("K = ", k)
        for key in prediction :
            print(key, ' = ' ,prediction[key])
        writeToCsv(name, datatest, prediction)

main()