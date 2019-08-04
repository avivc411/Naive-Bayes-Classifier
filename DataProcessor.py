import pandas as pd


class data_processor:
    def __init__(self, structure, train, test):
        self.structure = open(structure)
        self.train = pd.read_csv(train)
        self.test = pd.read_csv(test)
        self.meta_data=dict()

    def process_data(self):
        # get all attributes
        for line in self.structure:
            if line[-1] == "\n":
                line = line[:-1]
            if line[:10] != "@ATTRIBUTE":
                print "Error: No Attribute!"
                continue
            line = line[11:]
            ind = line.find('{')
            if ind != -1:
                self.meta_data[line[:ind - 1]] = line[ind + 1:-1].split(",")
            else:
                self.meta_data[line.split(" ")[0]] = "NUMERIC"
        self.missing_values()
        self.discrete_values()

    def missing_values(self):
        print "missing"

    def discrete_values(self):
        print "discrete"


