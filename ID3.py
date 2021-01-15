import numpy as np
import pandas as pd

eps = np.finfo(float).eps
from numpy import log2 as log


def initial_entropy_in_database(df):
    entropy_node = 0  # Initialize Entropy
    values = df.diagnosis.unique()  # Unique objects - 'B', 'M'
    for value in values:
        fraction = df.diagnosis.value_counts()[value] / len(df.diagnosis)
        entropy_node += -fraction * np.log2(fraction)
        # print(entropy_node)  # todo: remove


def find_entropy_attribute(df, attribute):
    #B_or_M = df.diagnosis.unique()  # This gives all 'B' and 'M'
    #print(B_or_M)
    # variables = df[attribute].unique()  # This gives all the values in the column of the attribute ,if there is a
    # duplicate, then only once
    # print(variables)
    borders = dynamic_division(df, attribute)
    sum_of_lines = len(df)
    entropy_attribute = 0
    for border in borders:
        num_B = len(df[attribute][df[attribute] < border][df.diagnosis == 'B'])
        p_B = num_B/sum_of_lines
        num_M = len(df[attribute][df[attribute] < border][df.diagnosis == 'M'])
        p_M = num_M / sum_of_lines
        h_first_sun = -p_B * log(p_B) - p_M * log(p_M)
        num_B = len(df[attribute][df[attribute] > border][df.diagnosis == 'B'])
        p_B = num_B / sum_of_lines
        num_M = len(df[attribute][df[attribute] > border][df.diagnosis == 'M'])
        p_M = num_M / sum_of_lines
        h_second_sun = -p_B * log(p_B) - p_M * log(p_M)

        relation_of_chosen_from_all = len(df[attribute][df[attribute] < border])/len(df)
        new_entropy = relation_of_chosen_from_all * h_first_sun + relation_of_chosen_from_all * h_second_sun

    return new_entropy

    # entropy_attribute = 0
    # for variable in variables: #variable should be a threshold for which after him you are B and after you are M
    #     entropy_each_feature = 0
    #     for target_variable in B_or_M:
    #         num = len(df[attribute][df[attribute] == variable][df.diagnosis == target_variable])  # numerator - for ex. how much from this attribute that are B
    #         den = len(df[attribute][df[attribute] == variable])  # denominator #for how much of this attribute
    #         fraction = num / (den + eps)  # pi
    #         entropy_each_feature += -fraction * log(fraction + eps)  # This calculates entropy for one feature like 'radius_mean'
    #
    #     fraction2 = den / len(df)
    #     entropy_attribute += -fraction2 * entropy_each_feature  # Sums up all the entropy ETaste
    #
    # return (abs(entropy_attribute))


def dynamic_division(df, attribute):
    variables = df[attribute].unique()
    # sort increaing order with lanbda
    variables = sorted(variables, key=lambda x: x, reverse=False)
    #print(variables)
    borders = lambda lst: [(lst[i] + lst[i + 1])/2 for i in range(0, len(lst) - 1)]
    #print(borders(variables))
    return borders

df = pd.read_csv("train.csv", header=0)
initial_entropy_in_database(df)
for attribute in df.keys()[1:]:
    # print(attribute)
    find_entropy_attribute(df, attribute)
# print(df)


#
#
# print(data)
#
#
#
#
# def TDIDT(examples_set, features, default, selectFeature):
#     pass
#     if examples_set.isEmpty() :
#         return (None, {}, default)
#
#     c = MajorityClass(examples_set)
#
#     #if all the objects in E are from the same clasification or the set of fetures is empty
#         #return (None, {}, default)
#
#     selected_feature = SelectFeature(features,examples_set)
#
#     features = features - selected_feature #check how to do - in groups
#
#     Subtrees =
#
#
# def MajorityClass(examples_set):
#     pass
#
#
#
# def entropy(node_set,):
