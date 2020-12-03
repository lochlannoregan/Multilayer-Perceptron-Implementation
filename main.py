# Importing required packages
from sys import argv
import pandas as pd
import numpy as np
import mlp_implementation

# sklearn neural network
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler


def get_file_sep(file_name):
    file_extention = file_name.split('.')[-1]
    if file_extention.lower() == "csv":
        return ','
    else: 
        return '\t'


def load_data(file):

    file_name = file.split('/')[-1] if "/" in file else file
    
    sep = get_file_sep(file_name)

    # Loading Data
    data = pd.read_csv(file, sep=sep)


    if file_name == 'beer.txt':
        del data['beer_id']
    
    return data


def run(data): 
    for i in range(10):
        X_train, y_train, X_test, y_test = minipulate_data(data)

        implementation_algorithm(X_train, y_train, X_test, y_test)

        reference_algorithm(X_train, y_train, X_test, y_test)


def minipulate_data(data):
    # Partition Data into training and testing
    # length of beer random numbers, random uniform distribution 0-1
    # condition < 0.66, returns true for numbers less than .66
    # meaning a split of about 2/3 true, 1/3 false
    msk = np.random.rand(len(data)) < 0.66
    # beer[msk] equal to indexes that are true
    # beer[~msk] not equal to indexes that are true, i.e. indexes that are false
    beer_train = data[msk]
    beer_test = data[~msk]

    # Separate the dataset as response variable and feature variables
    X_train = beer_train.drop('style', axis=1)
    y_train = beer_train['style']
    X_test = beer_test.drop('style', axis=1)
    y_test = beer_test['style']

    return X_train, y_train, X_test, y_test


def reference_algorithm(X_train, y_train, X_test, y_test):
    
    # Apply Standard scaling to get better results
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # sklearn neural network
    mlpc = MLPClassifier(hidden_layer_sizes=(9, 12, 9), max_iter=600)
    mlpc.fit(X_train, y_train)
    pred_mlpc = mlpc.predict(X_test)

    # print the models performance
    print(classification_report(y_test, pred_mlpc))
    print(confusion_matrix(y_test, pred_mlpc))


def implementation_algorithm(X_train, y_train, X_test, y_test):
    model = mlp_implementation.init(X_train, y_train, [5, 8])


def main():

    usage = "usage: main.py <file path>"

    input_file = ""
    
    if len(argv) == 2:
        input_file = argv[1]
    elif len(argv) > 2:
        print(usage)
        exit()
    else:
        input_file = './data/beer.txt'


    data = load_data(input_file)

    run(data)



if __name__ == "__main__":
    main()