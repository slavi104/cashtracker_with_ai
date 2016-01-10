from math import sqrt
# import sys


class Item(object):

    """Object to classify. When create new item
    add comma separated string with data, used for classifing."""

    def __init__(self, data):
        super(Item, self).__init__()
        data = data.split(',')
        self.data = [float("{0:.2f}".format(float(x))) for x in data]


class TrainData(object):

    """All train data used from artificial intelligence."""

    def __init__(self, raw_data):
        super(TrainData, self).__init__()
        self.raw_data = raw_data
        self.data = dict()
        self.process()

    def process(self):
        for payment_id, data in self.raw_data.items():
            class_id = data
            # data = [float("{0:.2f}".format(float(x))) for x in data]
            if class_id in self.data:
                self.data[class_id].append(data)
            else:
                self.data[class_id] = [data]


class Classifier(object):

    """Artificial intelligence that can classify ani item in specific class."""

    def __init__(self, train_data, item):
        super(Classifier, self).__init__()
        self.train_data = train_data
        self.item = item

    def find_item_distance(self, point):
        result = 0
        item_point = self.item.data
        index = 0
        for coor in point:
            result += (coor-item_point[index])**2
            index += 1
        return sqrt(result)

    def execute(self, k):
        neighbours = dict()
        classes = []
        train_data = self.train_data.data.items()
        for class_id, class_data in train_data:
            for current_data in class_data:
                neighbours[self.find_item_distance(current_data)] = class_id
        for key in sorted(neighbours)[:k]:
            classes.append(neighbours[key])
        return max(set(classes), key=classes.count)


# main
# if __name__ == '__main__':

#     k = int(sys.argv[1:][0])
#     train_data = TrainData('iris_train.txt')
#     good_test = 0
#     with open('iris_test.txt') as test_file:
#         test_data = test_file.readlines()
#         with open('iris_test_result.txt') as test_result_file:
#             result_data = test_result_file.readlines()
#             index = 0
#             for data in test_data:
#                 item = Item(data)
#                 classifier = Classifier(train_data, item)
#                 result = classifier.execute(k)
#                 if result != result_data[index].replace("\n", ""):
#                     pass
#                 else:
#                     good_test += 1
#                 index += 1

#             print('Tests: {}% success!'.format(
#                 int((good_test/len(test_data))*100))
#             )

#     if len(sys.argv[2:]):
#         item = Item(sys.argv[2:][0])
#         classifier = Classifier(train_data, item)
#         result = classifier.execute(k)
#         print('Class of item: ', result)
