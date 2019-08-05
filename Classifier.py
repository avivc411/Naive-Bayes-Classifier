class Classifier:
    def __init__(self, test, structure, train, meta_data, bins):
        self.test = test
        self.structure = structure
        self.train = train
        self.meta_data = meta_data
        self.bins = bins

    def classify(self):
        classification = list()

        classes_prob = self.train['class'].value_counts(normalize=True)

        for index, record in self.test.iterrows():
            cond_prob_class1 = 1
            cond_prob_class2 = 1
            for attribute in self.meta_data:
                if attribute == 'class':
                    continue
                cond_prob_class1 *= self.calculate_prob_m_estimate(attribute, record[attribute], self.meta_data['class'][0])
                cond_prob_class2 *= self.calculate_prob_m_estimate(attribute, record[attribute], self.meta_data['class'][1])
            cond_prob_class1 *= classes_prob[0]
            cond_prob_class2 *= classes_prob[1]
            if cond_prob_class1 > cond_prob_class2:
                classification.append(self.meta_data["class"][0])
            else:
                classification.append(self.meta_data["class"][1])
        return classification

    def calculate_prob_m_estimate(self, attribute, row_val, class_val):
        # number of rows where col_name = row_val and class = class_val
        a = (self.train[attribute] == row_val)
        b = (self.train['class'] == class_val)
        nc = self.train[a & b].count()[0]
        p = 0.5
        m = 2
        n = self.train['class'].value_counts()[class_val]
        return (nc + m*p) / (n + m)
