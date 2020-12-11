import os
import re
import json
import pickle
import inspect

class Transformer:
    """
    A data transformer which can receive inputs and return outputs
    """

    inputs = []

    def __init__(self):
        self.name = self.__class__.__name__
        #print('Init:', self.name)

        self.state = {}
        #model_filename = os.path.join(self.myDirectory(), 'state.pkl')
        model_filename = "state3.pkl"

        #data_file = open(filename, 'rb')
        new_state = self.loadSerialized(model_filename)
        if not new_state:
            #print('Transformer has no state:', self.name)
            self.state = {}
        else:
            self.state = new_state
    #clf_1 = state['clf_1']
    #print(clf_1)

    @classmethod
    def loadSerialized(cls, filename):
        name = cls.__name__
        #print('Transformer {} load pickle file: {}'.format(name, repr(filename)))

        data_file = None
        try:
            data_file = open(filename, 'rb')
        except Exception as e:
            #print(e)
            #print('No data file for {}: {}'.format(name, filename))
            return None

        body = None
        try:
            body = data_file.read()
        except Exception as e:
            print('Bad data in file for {}: {}: {}'.format(name, filename, e))
            return None
        else:
            #print('Data in file for {}: {}: {} bytes'.format(name, filename, len(body)))
            pass
        finally:
            data_file.close()

        result = None
        try:
            if re.search(r'\.json$', filename):
                result = json.loads(body)
            else:
                result = pickle.loads(body)
        except Exception as e:
            print(e)
            print('Bad pickle data in file for {}: {}'.format(name, filename))
            return None

        #print('Good serialized load for {}: {}'.format(name, filename))
        return result

    @classmethod
    def myDirectory(cls):
        result = inspect.getfile(cls)
        if not os.path.isdir(result):
            result = os.path.dirname(result)
        return result

    @classmethod
    def getTestData(cls, suffix):
        #print('Get test data:', cls.__name__)
        class_definition_dir = cls.myDirectory()

        data_file_extensions = ['.pkl', '.json']
        data_filenames = ['test_data_'+suffix+extn for extn in data_file_extensions]

        for filename in data_filenames:
            data = cls.loadSerialized(os.path.join(class_definition_dir, filename))
            if data is not None:
                return data
        return None

    @classmethod
    def writeState(cls, new_state):
        #print('Write state file:', cls.__name__)
        class_definition_dir = cls.myDirectory()
        model_filename = os.path.join(class_definition_dir, 'state.pkl')

        with open(model_filename,'wb') as f:
            pickle.dump(new_state,f)

#    def __init__(self, model_file, feature_file):
#        self.predictive_model = pickle.load(open(model_file, 'rb'))
#        self.features = pickle.load(open(feature_file, 'rb'))

#result = Transformer()
