
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# neural_network.py
#

# Barnaby brain. The neural network responsible for interpreting user inputs.

import pandas as pd
import pickle
import tensorflow as tf

class NeuralNetwork:

    def __init__(self, barnaby_config):
        self.barnaby_config = barnaby_config
        self.NUM_WORDS = 50
        self.SEQ_LEN = 5
        self.EMBEDDING_SIZE = 50
        self.BATCH_SIZE = 8
        self.EPOCHS = 25
        self.labels = ["news", "term_definitions", "weather"]

    # removes stop words from string to make each one more concise and relevant
    def remove_stopwords(self, string):
        f = open("../data/neural_network_{}/stopwords.txt".format(self.barnaby_config['lang']), "r")
        stopwords = f.read().split("\n")
        f.close()
        
        for word in stopwords:
            string = string.replace(" {} ".format(word), " ")

        return string 
    
    # get training and testing data from files
    def get_data(self):
        
        path = "../data/neural_network_{}".format(self.barnaby_config['lang'])

        for t in ["train", "test"]:
            x = 0 # functionality label
            text = []
            func = []
            df = pd.DataFrame(columns=['text', 'func'])
            df = df.sample(frac=1).reset_index(drop=True) # shuffle data for better accuracy
            for functionality in ["news", "term_definitions", "weather"]:
                f = open(path + "/{}_{}.txt".format(functionality, t), "r")
                sentences = f.read().split("\n")
                f.close()
                for sentence in sentences:
                    if sentence != "":
                        sentence = self.remove_stopwords(sentence)
                        text.append(sentence)
                        func.append(x)
                x += 1
            df['text'] = text
            df['func'] = func
            if t == "train":
                self.train_df = df
            else:
                self.test_df = df

        print(self.train_df)
        print(self.test_df)

    # processes text
    def process_text(self):

        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=self.NUM_WORDS, oov_token='<UNK>')
        tokenizer.fit_on_texts(self.train_df['text'])
        
        train_seqs = tokenizer.texts_to_sequences(self.train_df['text'])
        test_seqs = tokenizer.texts_to_sequences(self.test_df['text'])

        train_seqs = tf.keras.preprocessing.sequence.pad_sequences(train_seqs, maxlen=self.SEQ_LEN, padding="post")
        test_seqs = tf.keras.preprocessing.sequence.pad_sequences(test_seqs, maxlen=self.SEQ_LEN, padding="post")

        self.train_seqs = train_seqs
        self.test_seqs = test_seqs

        self.tokenizer = tokenizer

    # builds and compiles neural network model
    def build_model(self):

        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(self.NUM_WORDS, self.EMBEDDING_SIZE),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(200, activation='relu'),
            tf.keras.layers.Dense(3, activation='softmax')])
        
        model.compile(optimizer='adam',
                        loss='sparse_categorical_crossentropy',
                        metrics=['accuracy'])

        history = model.fit(self.train_seqs, self.train_df['func'].values,
                            batch_size = self.BATCH_SIZE,
                            epochs = self.EPOCHS,
                            validation_split = 0.2)

        model.evaluate(self.test_seqs, self.test_df['func'].values)

        self.model = model

    # saves model in file
    def save_model(self):
        self.model.save("../data/neural_network_{}/model.h5".format(self.barnaby_config['lang']))
        
        with open("../data/neural_network_{}/tokenizer.pickle".format(self.barnaby_config['lang']), 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # loads model from file
    def load_model(self):
        self.model = tf.keras.models.load_model("../data/neural_network_{}/model.h5".format(self.barnaby_config['lang']))
        
        with open("../data/neural_network_{}/tokenizer.pickle".format(self.barnaby_config['lang']), 'rb') as f:
            self.tokenizer = pickle.load(f)

    # predicts which functionality the user requested
    def predict(self, sentence, train):
        if train:
            self.get_data()
            self.process_text()
            self.build_model()
            self.save_model()
        self.load_model()

        sentence = self.remove_stopwords(sentence)
        
        seqs = self.tokenizer.texts_to_sequences([sentence])
        seqs = tf.keras.preprocessing.sequence.pad_sequences(seqs, maxlen=self.SEQ_LEN, padding="post")
        
        pred = self.model.predict(seqs)

        print(pred)

        pred = self.labels[pred[0].argmax()]

        return str(pred)
