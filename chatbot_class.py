import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
import json
import random

class chatBot:
    def __init__(self):
        self.intents = json.loads(open('intents.json').read())
        self.words = pickle.load(open('words.pkl','rb'))
        self.classes = pickle.load(open('classes.pkl','rb'))
        self.model = load_model('chatbot_model.h5')
        self.index = None

    def clean_up_sentence(self,sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_word = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_word

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def bow(self,sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)

        # get index of previous class
        contextList = [0] * len(self.classes)
        
        # skip first time through
        if self.index != None:
            contextList[self.index] = 1

        # add context to bag
        bag = bag + contextList

        return(np.array(bag))

    def predict_class(self,sentence, model):
        # filter out predictions below a threshold
        p = self.bow(sentence, self.words,show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
            self.index = r[0]

        return return_list

    def getResponse(self,ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result

    def chatbot_response(self,msg):
        ints = self.predict_class(msg,self.model)
        res = self.getResponse(ints, self.intents)
        return res

def main():
    chatbot = chatBot()
    print(chatbot.chatbot_response('thank you'))
    print(chatbot.chatbot_response('can you save that image?'))
    print(chatbot.chatbot_response('thanks'))

main()