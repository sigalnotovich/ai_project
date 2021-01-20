

#choose n*p(p is a parameter) for the training set:
import csv

import numpy as np
import pandas as pd
import random

from ID3 import Node, fit, getAttributeCalumn, getMajorityClass

#todo: check



#todo : normalize the centroid so that the distance in the classification will be from all the vectore
#cheked
def get_centroid(df,random_data): #the centroid will have only the features in its vector
    pd.DataFrame(random_data).to_csv("C:/My Stuff/studies/2021a/AI/hw3/random_data.csv") #todo:remove
    number_of_features = len(df[0])
    len_of_random_data = len(random_data)
    feature_average_array = []
    for feature_place in range(1, number_of_features):  # for each feature #the first feature is diagnostic so i give it out
        sum_for_feature = 0
        for i in random_data:
            feature_value_in_line_i = i[feature_place]
            sum_for_feature += feature_value_in_line_i
        average = sum_for_feature/len_of_random_data
        feature_average_array.append(average)  # without the first feature which is diagnostic,is it okay?
    return feature_average_array


def getClassification(header,node,line_to_classify,):
    if node.classification is not None:
        return node.classification
    else:
        # there is partition here
        attribute_column = getAttributeCalumn(header, node)
        if line_to_classify[attribute_column] < node.partition_feature_and_limit[1]:
            return getClassification(header, node.left, line_to_classify)  # under limit
        else:
            return getClassification(header, node.right,line_to_classify)  # above or equal to limit

def bulilt_N_trees(header,data_without_header,number_of_trees_N):
    tree_array = []
    n = len(data_without_header)
    for i in range(0, number_of_trees_N):
        number_of_random = round(p*n)
        random_data = random.sample(list(data_without_header), number_of_random)# no duplicate
        df = (header, random_data)
        centroid = get_centroid(df,random_data)#cheked
        node = Node()
        fit(df, node) #fit = algorithm ID3 thet used in ID3.py  #no pruning todo: maybe change to with pruning
        tree_array.append((node, centroid)) #todo- try to print tree
    return tree_array


def get_dist_from_all_trees_centroid(trees_array,line_to_classify_without_classification):
    tree_dist_arr = []
    for tree, centroid in trees_array:
        euclidean_dist = get_euclidean_dist(line_to_classify_without_classification, centroid)
        # dist = np.linalg.norm(line_to_classify_without_classification - centroid)
        tree_dist_arr.append((euclidean_dist, tree))
    return tree_dist_arr

def getMajorityTreesClasification(header,line_to_classify_without_classification, topKtrees):
    k_classification_array = []
    for _, node in topKtrees:
        classification = getClassification(header, node, line_to_classify_without_classification)
        k_classification_array.append(classification)
    majority_classification = getMajorityClass(k_classification_array)
    return majority_classification


def KNN(p, number_of_trees_N, k):
    true = 0
    false = 0
    df = pd.read_csv("train.csv", header=0)
    data_without_header = df.to_numpy()

    with open('train.csv', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)

    trees_array = bulilt_N_trees(header,data_without_header,number_of_trees_N)

    #check the classification of examples in test.csv:
    df_test = pd.read_csv("test.csv", header=0)
    test_data_without_header = df_test.to_numpy()

    for line_to_classify_without_classification in test_data_without_header:
        real_classification_for_line = line_to_classify_without_classification[0]
        index = [0]
        line_to_classify_without_classification = np.delete(line_to_classify_without_classification, index) #todo: test it removes the first element
        tree_dist_arr = get_dist_from_all_trees_centroid(trees_array, line_to_classify_without_classification)

        trees_sorted_by_dist = sorted(tree_dist_arr, key=lambda tup: tup[0])
        topKtrees = trees_sorted_by_dist[:k]

        majority_classification = getMajorityTreesClasification(header,line_to_classify_without_classification, topKtrees)

        if real_classification_for_line == majority_classification:
            true += 1
        else:
            false += 1

    accuracy = true / len(test_data_without_header)
    return accuracy
        #chose the most classification
        #check if it is the correct one


#cheked
def get_euclidean_dist(vec1,vec2):
    sum = 0
    for i,j in zip(vec1,vec2):
        sum += pow(i-j,2)
    return np.math.sqrt(sum)

# vec1 = [2,3]
# vec2 = [10,20]
# euclidean_dist = get_euclidean_dist(vec1,vec2)
# print(euclidean_dist)


# df = pd.read_csv("check_if_random.csv", header=0)
# data_without_header = df.to_numpy()
#
# random_data = random.sample(list(data_without_header), len(data_without_header))
#
# print("fin")


p = 1 #is number of exmaples will be choosen from all the examples for each Tree
number_of_trees_in_comity_N = 1 #number of trees
number_of_trees_to_classify_by_K = 1
accuracy = KNN(p, number_of_trees_in_comity_N, number_of_trees_to_classify_by_K) #todo: train on p from 0.3 to 0.7
print(accuracy)