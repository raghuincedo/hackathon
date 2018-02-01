import spacy
nlp = spacy.load('en')
from nltk.corpus import stopwords
from LoadData import actions, actions2
from __NLP_utils__ import text2int


class ProcessNaturalLanguageQuery(object):
    """
    - > process incoming query
    - > extract all np chunks
    - > get all column names from the sheets
    - > normalize np chunks and table names
    - > get intersection of column names and np chunks
    """
    def __init__(self, query = '', columns = [], action = {}, row_wise_column = {}):
        self.query = query
        self.columns = columns
        self.stopwords = stopwords.words('english')
        self.row_wise_column = row_wise_column

        self.transformed_query = self._transform_sentence()
        #print("transformed", self.transformed_query)
        self.transformed_columns = self._transform_column_names()
        self.doc = nlp(self.transformed_query)
        self.dic_action1_column = {}
        self.dic_action2_column = {}

    def _transform_column_names(self):
        """
        -> normalize column names
        -> lower case
        -> replace space with underscore
        :param columns: list of column names
        :return: normalized column names
        """
        columns = []
        for column in self.columns:
            columns.append(column.lower().replace(" ", "_"))

        return columns

    def _transform_sentence(self):
        """
        -> identify the named entities(columns names) in the sentence
        :param columns:
        :param sentence:
        :return:
        """
        self.columns = [column.lower().strip() for column in self.columns]
        transformed_columns = self._transform_column_names()
        sent = self.query.lower()

        for (column_name, transformed) in zip(self.columns, transformed_columns):
            if column_name in sent:
                sent = sent.replace(column_name, transformed)
                break

        for row in self.row_wise_column:
            if row in sent:
                sent = sent.replace(row, "row_"+self.row_wise_column[row]+"_"+row)
                break

        return sent


    def extract_action1_columns(self):
        """
        -> wrapper at highest level
        -> parser
        :return:
        """
        self.dic_action1_column = {}
        tree = self._get_transformed_structure()
        self._helper_extract_action1_columns(tree)

    def _helper_extract_action1_columns(self, node):
        """
        -> parser at level 1
        -> check for column in the current node
        -> check for action in the child nodes
        :param node:
        :return:
        """
        if 'type' in node:
            if node['type'] == 'column':
                self.dic_action1_column[self._helper_get_action1(node)] = node['word']

        for item in node['modifiers']:
            self._helper_extract_action1_columns(item)

    def _helper_get_action1(self, node):
        """
        -> finds action type 1 in node's children
        :param node:
        :return:
        """
        for item in node['modifiers']:
            if 'type' in item:
                if item['type'] == 'action1':
                    return item['word']



    def extract_action2_columns(self):
        """
        -> wrapper at highest level
        -> parser
        :return:
        """
        self.dic_action2_column = {}
        tree = self._get_transformed_structure()
        self._helper_extract_action2_columns(tree)

    def _helper_extract_action2_columns(self, node):
        """
        -> parser at level 1
        -> check for column in the current node
        -> check for action in the child nodes
        :param node:
        :return:
        """
        if 'type' in node:
            if node['type'] == 'column':
                obj = self._helper_get_action2(node)
                if obj is not None:
                    print("parameter", obj['parameter'])
                    #try:
                    parameter = text2int(str(obj['parameter']))
                    #except:
                        #parameter = int(str(obj['parameter']))

                    self.dic_action2_column[obj['action']] = {'column' : node['word'], 'parameter' : parameter}

        for item in node['modifiers']:
            self._helper_extract_action2_columns(item)

    def _helper_get_action2(self, node):
        """
        -> finds action type 1 in node's children
        :param node:
        :return:
        """
        for item in node['modifiers']:
            if 'type' in item:
                if item['type'] == 'action2':
                    return {'action': item['word'], 'parameter': self._helper_action2_parameter(item)}

    def _helper_action2_parameter(self, node):
        """
        - > get parameters of action type 2
        - > node's type is action2
        :param node:
        :return:
        """
        for item in node['modifiers']:
            if item['NE'] == 'CARDINAL':
                return item['word']
            else:
                return self._helper_action2_parameter(item)

    def extract_action1_columns_old(self):
        """

        :return:
        """
        self.dic_action1_column = {}
        tree = self._get_transformed_structure()
        if 'type' in tree:
            if tree['type'] == 'column':
                self.dic_action1_column[self._helper_get_action1_old(tree)] = tree['word']

        self._helper_extract_action1_columns_old(tree)

    def _helper_extract_action1_columns_old(self, node):
        """
        -> parser for tree
        -> helper for _get_transformed_structure
        -> parse tree structure
        :param node: tree node
        :return: transformed tree structure
        """

        for item in node['modifiers']:
            if 'type' in item:
                if item['type'] == 'column':
                    self.dic_action1_column[self._helper_get_action1_old(item)] = item['word']
            self._helper_extract_action1_columns_old(item)

    def _helper_get_action1_old(self, node):
        """

        :return:
        """
        for item in node['modifiers']:
            if 'type' in item:
                if item['type'] == 'action1':
                    return item['word']

    def extract_action2_columns_old(self):
        """
        :return:
        """
        self.dic_action2_column = {}
        tree = self._get_transformed_structure()
        if 'type' in tree:
            if tree['type'] == 'column':
                self.dic_action2_column[self._helper_get_action2_old(tree)] = tree['word']

        self._helper_extract_action2_columns_old(tree)


    def _helper_extract_action2_columns_old(self, node):
        """
        -> parser for tree
        -> helper for _get_transformed_structure
        -> parse tree structure
        :param node: tree node
        :return: transformed tree structure
        """

        for item in node['modifiers']:
            if 'type' in item:
                if item['type'] == 'column':
                    self.dic_action2_column[self._helper_get_action2_old(item)] = item['word']
            self._helper_extract_action2_columns_old(item)

    def _helper_get_action2_old(self, node):
        """

        :return:
        """
        for item in node['modifiers']:
            if 'type' in item:
                if item['type'] == 'action2':
                    return item['word']

    def _remove_stop_words(self, np_chunks):
        """
        - > remove stop words from the np chunks
        :param np_chunks: a list of noun phrases (normalised)
        :return: np_chunks with stopwords removed
        """
        new_chunks = []
        for chunk in np_chunks:
            chunk_new = ''
            for word in chunk.split():
                if word not in self.stopwords:
                    chunk_new += word + ' '
            new_chunks.append(chunk_new.strip())

        return new_chunks

    def _get_transformed_structure(self):
        """
        -> get transformed spacy tree
        -> will contain information about columns and operations
        :return: transformed structure
        """
        tree = self.doc.print_tree()[0]

        if tree['word'] in self.transformed_columns:
            tree['type'] = 'column'

        action1_flag = False
        action2_flag = False

        for key in actions2:
            if str(tree['word']) == key:
                action2_flag = True
            elif str(tree['word']) in actions2[key]:
                action2_flag = True

        for key in actions:
            if str(tree['word']) == key:
                action1_flag = True
            elif str(tree['word']) in actions[key]:
                action1_flag = True

        if action1_flag:
            tree['type'] = 'action1'

        if action2_flag:
            tree['type'] = 'action2'


        self._helper_parse_tree(tree)
        return tree

    def _helper_parse_tree(self, node):
        """
        -> helper for _get_transformed_structure
        -> parse tree structure
        :param node: tree node
        :return: transformed tree structure
        """
        for item in node['modifiers']:
            if item['word'] in self.transformed_columns:
                item['type'] = 'column'

            action1_flag = False
            action2_flag = False

            for key in actions2:
                if str(item['word']) == key:
                    action2_flag = True
                elif str(item['word']) in actions2[key]:
                    action2_flag = True

            for key in actions:
                if str(item['word']) == key:
                    action1_flag = True
                elif str(item['word']) in actions[key]:
                    action1_flag = True

            if action1_flag:
                item['type'] = 'action1'

            if action2_flag:
                item['type'] = 'action2'
            self._helper_parse_tree(item)

    def _get_np_chunks(self):
        """
        -> get noun phrases from self.query
        :return: -> normalised NP chunks
        """
        np_chunks = []
        for np in self.doc.noun_chunks:
            np_chunks.append(str(np).lower().strip())

        return self._remove_stop_words(np_chunks)

    def find_common(self):
        """
        - > find common items from column names and np chunks
        - > both are normalized
        :return:common items
        """
        pass
#doc = nlp(u"""What is the average age of students whose name is Doe or age over 25""")
#doc = nlp(u"""Sales for last quarter""")

#tree = doc.print_tree()[0]
#root = tree['word']

#for np in doc.noun_chunks:
     #print(np.text)

#print("root", root)

"""
for ele in tree['modifiers']:
    print(ele["word"],ele["POS_fine"], ele["arc"])
    for internal in ele['modifiers']:
        print(internal)
"""

#from pprint import pprint
#pprint(tree)

