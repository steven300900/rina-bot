import nltk
import json
import numpy as np
import random
import tensorflow
from tensorflow import keras
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pymongo

class Bot:
    def __init__(self, train=False, printInfo=False):
        self.train = train
        self.printInfo = printInfo
        # parser that the bot will use
        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()

        # setup the words and data known by the bot
        with open('model/intentions.json') as data:
            self.data = json.load(data)
        self.ignore_words = ["?", "!", ".", ",", ""]

        # Setup all of these:
        # vocabularies will store all the known words within intentions.json
        # labels will store all the intent name within intentions.json
        # training data will store all the data known by the AI
        self.vocabularies = []
        self.labels = []
        self.training_data = []
        for intent in self.data["intents"]:
            for utterance in intent["patterns"]:
                # insert the intent if not found
                if intent["tag"] not in self.labels:
                    self.labels.append(intent["tag"])
                # insert all vocabularies
                utterance = nltk.word_tokenize(utterance)
                tokens = [self.stemmer.stem(token.lower()) for token in utterance if token not in self.ignore_words]
                self.vocabularies.extend(tokens)
                # insert the phrases and intent known by the AI
                self.training_data.append([tokens, intent["tag"]])
        # filter the vocabularies so that only unique terms are placed
        self.vocabularies = sorted(list(set(self.vocabularies)))
        # sort the labels
        self.labels = sorted(self.labels)

        if self.printInfo == True:
            print("LABELS: " + str(len(self.labels)), self.labels)
            print("UTTERANCES: " + str(len(self.vocabularies)), self.vocabularies)
            print("TRAINING DATA: ", str(len(self.training_data)), self.training_data)
        

        if train == True:
            self.model = self.train_model()
        else:
            self.model = keras.models.load_model('model/chatbot_model.h5')
        print("Model Created")
        


    def train_model(self):
        # Setup the training data for AI:
        # the input layer are the words that exist within a given phrase, output layer is the tags
        # because the AI don't really understand words in a direct manner, then we'll represent it with binaries;
        # 0 meaning that the word does not exist while 1 mean that it exist
        # training are the sets of input and output numbers
        training = []
        empty_output = [0] * len(self.labels)
        for data in self.training_data:
            bag = []
            cur_words = data[0]
            for x in self.vocabularies:
                if x in cur_words:
                    bag.append(1)
                else:
                    bag.append(0)

            output_layer = list(empty_output)
            output_layer[self.labels.index(data[1])] = 1
            training.append([bag, output_layer])

        random.shuffle(training)
        training = np.array(training, dtype="object")
        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        # create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
        # equal to number of intents to predict output intent with softmax
        model = keras.models.Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]), ), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        # compile model. stochastic gradient descent with nesterov accelerated gradient gives good results for this model
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        # fitting and saving the model
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        model.save('model/chatbot_model.h5', hist)
        if self.printInfo == True:
            model.summary(line_length=None, positions=None, print_fn=None)
        return model


    def reply(self, user_dialogue):
        user_dialogue = nltk.word_tokenize(user_dialogue)
        user_dialogue = [self.stemmer.stem(words.lower()) for words in user_dialogue if words not in self.ignore_words]

        bag = []

        for words in self.vocabularies:
            if words in user_dialogue:
                bag.append(1)
            else:
                bag.append(0)

        bag = np.array(bag)

        # predict the intent from the user
        res = self.model.predict(np.array([bag]))[0]
        user_intent = self.labels[np.argmax(res)]

        # data-based intent
        special_content = ["ready", "recommendation"]
        item = self.search_item(user_dialogue)

        # get response from a certain intent
        list_of_intents = self.data['intents']
        for i in list_of_intents:
            if i['tag'] == user_intent:
                if i['tag'] in special_content and item != -1:
                    if i['tag'] == 'ready':
                        result = random.choice(i['responses']) + ' ' + item['amount'] + 'pcs'
                    elif i['tag'] == "recommendation":
                        result = random.choice(i['responses']) + ' ' + item['url']
                else:
                    result = random.choice(i['responses'])
                break
        return result

    def search_item(self, user_dialogue):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient['mydatabase']
        dataDB = mydb["items"]
        
        best_item = []
        for items in dataDB.find():
            for words in user_dialogue:
                if words in items['tags']:
                    best_item.append(items['id'])
        best_item = sorted(best_item)

        best_id = {}
        for id in best_item:
            if id in best_id:
                curNum = best_id[id]
                curNum += 1
                best_id[id] = curNum
            else:
                best_id[id] = 1
        output_item = ""
        if best_id:
            output_item = max(best_id, key=best_id.get)
            for items in dataDB.find({'id': output_item}):
                return items
        else:
            return -1

# if __name__ == '__main__':
#     rina_bot = Bot(train=True, printInfo=False)
#     while True:
#         text = input()
#         print(rina_bot.reply(text))

