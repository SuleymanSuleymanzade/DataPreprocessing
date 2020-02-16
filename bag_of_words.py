from collections import Counter
import weakref

class MetaSingleton(type):
    __instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]

class Dictionary(metaclass = MetaSingleton):
    __instances = set()
    def __init__(self, mx_limit = 10, dictionary = {}, counter = 0):
        self.__global_dictionary = dictionary
        self.__counter = counter
        self.__limit = mx_limit
        self.__instances.add(weakref.ref(self)) # Singleton
        self.___out_of_dict = False

    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls.__instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls.__instances -= dead
    
    def add_to_dictionary(self, word):
        if word not in self.__global_dictionary and self.__counter < self.limit:
            self.__global_dictionary[word] = self.__counter
            self.__counter += 1
        else:
            self.__out_of_dict = True 

    def update_dictionary(self, phrase):
        words_counter = Counter([word for word in phrase.lower().split()])
        for key, repetitions in words_counter.items():
            if key not in self.__global_dictionary:
                glob_dictionary.add_to_dictionary(key)
    @property
    def limit(self):
       return self.__limit
    
    @property
    def dictionary(self):
        return self.__global_dictionary
    
    @property
    def len(self):
        return self.__counter
    @property
    def fulfilled(self):
        return len(list(self.get_instances())) > 0

    @property
    def out_of_dictionary(self):
        return self.__out_of_dict


class BOW:    
    def __init__(self, phrase):
        global glob_dictionary
        self.phrase = phrase

    def get_bow(self):
        words_counter = Counter([word for word in self.phrase.lower().split()])
        global_dictionary = next(Dictionary.get_instances()) or None
        if not global_dictionary:
            return
        res = [0] * global_dictionary.limit
        
        for key, repetitions in words_counter.items():            
            if key not in glob_dictionary.dictionary:
                glob_dictionary.add_to_dictionary(key)
            res[glob_dictionary.dictionary[key]] = repetitions
        return res 


glob_dictionary = Dictionary()

phrases = ["hello what's up",
           "the cat in the bag so what's up",
           "what's whong in the whrong jungle",
           "where are you honey",
           "hohoho not yet",]

for phrase in phrases:
    glob_dictionary.update_dictionary(phrase)

bows = []
if Dictionary.fulfilled:
    for phrase in phrases:
        bows.append(BOW(phrase))
    

for bow in bows:
    print(bow.get_bow())





        
