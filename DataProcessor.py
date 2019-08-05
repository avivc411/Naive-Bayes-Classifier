import pandas as pd
from pandas.core.algorithms import mode


def binning(col, cut_points, labels=None):
    return pd.cut(col, bins=cut_points, labels=labels, include_lowest=True)


class data_processor:
    def __init__(self, structure, train, bins, test):
        self.structure = open(structure)
        if sum(1 for line in self.structure) < 2:
            raise Exception("Structure File Is Empty")
        self.train = pd.read_csv(train)
        if self.train.shape[0] < 2 or self.train.shape[1] < 2:
            raise Exception("Train File Is Empty")
        self.bins=bins
        self.meta_data=dict()
        self.test = pd.read_csv(test)
        if self.test.shape[0] < 2 or self.test.shape[0] < 2:
            raise Exception("Test File Is Empty")

    def process_data(self):
        # get all attributes
        for line in self.structure:
            if line[-1] == "\n":
                line = line[:-1]
            if line[:10] != "@ATTRIBUTE":
                print "Error: No Attribute!"
                continue
            if line.__contains__('{'):
                self.meta_data[line.split(" ")[1]] = line[line.find('{')+1:line.rfind('}')].split(",")
            else:
                self.meta_data[line.split(" ")[1]] = "NUMERIC"

        self.missing_values()
        self.discrete_values()

        """le = LabelEncoder()
        for i in self.meta_data.iterkeys():
            self.train[i] = le.fit_transform(self.train[i])
            self.test[i] = le.fit_transform(self.test[i])"""

        return self.structure, self.train, self.meta_data, self.test

    # fill missing values in data (both train and test): for numeric-mean, for nominal-mode
    def missing_values(self):
        for attribute in self.meta_data:
            if self.meta_data[attribute]=="NUMERIC":
                self.train[attribute] = self.train.groupby("class").transform(lambda x: x.fillna(x.mean()))
                self.test[attribute] = self.test.groupby("class").transform(lambda x: x.fillna(x.mean()))
            else:
                self.train[attribute].fillna(mode(self.train[attribute])[0], inplace=True)
                self.test[attribute].fillna(mode(self.test[attribute])[0], inplace=True)

    # discrete the values of numeric attributes.
    # labels are the widths between the bins
    def discrete_values(self):
        labels=[]
        for i in range(0, self.bins):
            labels.append(i)
        for attribute in self.meta_data:
            if self.meta_data[attribute] == "NUMERIC":
                self.train[attribute] = binning(self.train[attribute], self.bins, labels)
                self.test[attribute] = binning(self.test[attribute], self.bins, labels)


