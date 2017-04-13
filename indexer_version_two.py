import pickle

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0
        
    def get_total_words(self):
        return self.total_words
        
    def get_msg_size(self):
        return self.total_msgs
        
    def get_msg(self, n):
        return self.msgs[n]
        
        # implement
    def add_msg(self, m):
        self.msgs.append(m)
        self.total_msgs += 1
        
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

        # implement
    def indexing(self, m, l):
        # remove trailing punctuation marks
        # when encountering the heading of a poem (len(words) == 1), pass
        punctuations = ',.?!:;"\''
        words = m.split()
        for i, w in enumerate(words):
            # Return a copy of the string with the leading and trailing characters removed. 
            # The chars argument is a string specifying the set of characters to be removed.
            if len(words) == 1 and w[-1] == '.' and w[-2].isupper():
                pass
            else:
                w = w.strip(punctuations)
            
            # index both the column number (line number) and the row number (the position of the word in that line)
            try:
                self.index[w].append((l, i))
            except KeyError:
                self.index[w] = []
                self.index[w].append((l, i))
        
        # implement: query interface
        '''
        return a list of tuples. If we index the first sonnet (p1.txt), then
        calling this function with term 'thy' will return the following:
        [(7, " Feed'st thy light's flame with self-substantial fuel,"),
        (9, ' Thy self thy foe, to thy sweet self too cruel:'),
        (9, ' Thy self thy foe, to thy sweet self too cruel:'),
        (12, ' Within thine own bud buriest thy content,')]
        
        searching for phrases：
        both the column numbers and the row numbers of words are recorded,
        if two are next to each other, then they are considerd to consitute a phrase
        '''
    def search(self, term):
        msgs = []
        # used to store the list of words in term
        words = term.split()
        # used to record the length of the phrase term, if 1 -> single word
        length = len(words)
        # used to remove duplicates
        line_index = set()
        
        # search for single words, also deal with null term
        if length <= 1:
            try:
                for i in self.index[term]:
                    if i[0] not in line_index:
                        line_index.add(i[0])
                        msgs.append((i[0], self.msgs[i[0]]))
            except KeyError:
                pass

        # search for phrases
        else:
            try:
                for i in self.index[words[0]]:
                    found = True
                    # checking the words right following the first word
                    for j in range(1, length):
                        if (i[0], i[1] + j) not in self.index[words[j]]:
                            found = False
                            break
                    if found:
                        if i[0] not in line_index:
                            line_index.add(i[0])
                            msgs.append((i[0], self.msgs[i[0]]))
            except KeyError:
                pass

        return msgs

class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
        # Implement: 1) open the file for reading, then call
        # the base class's add_msg_and_index
    def load_poems(self):
        lines = open(self.name, 'r').readlines()
        self.total_lines = len(lines)
        for l in lines:
            l = l.strip()
            super().add_msg_and_index(l)
    
        # Implement: p is an integer, get_poem(1) returns a list,
        # each item is one line of the 1st sonnet
    def get_poem(self, p):
        poem = []

        # if cannot find poem p, return []
        try:
            pos = super().search(self.int2roman[p] + '.')[0][0]
        except:
            return []

        # if cannot find the starting point of the next poem, set pos_end to the end of file
        try:
            pos_end = super().search(self.int2roman[p + 1] + '.')[0][0]
        except:
            pos_end = self.total_lines

        while pos < pos_end:
            poem.append(super().get_msg(pos))
            pos += 1

        return poem

if __name__ == "__main__":
    # The next three lines are just for testing
    # You are encouraged to add to this and create your own tests!
    # Call your functions as you implement them and see if they work
    testIndex = Index("testIndex")
    testIndex.add_msg_and_index("X.")
    testIndex.add_msg_and_index("who who? who")
    testIndex.add_msg_and_index("'who?")
    
    print(testIndex.get_msg(1))
    print(testIndex.search(""))
    print(testIndex.search("X."))
    print(testIndex.search("who"))
    print(testIndex.search("null"))
    
    sonnets = PIndex("AllSonnets.txt")
    # check for getting the last poem 
    p154 = sonnets.get_poem(154)
    print(p154)
    # check for getting a non-existing poem 
    p200 = sonnets.get_poem(200)
    print(p200)
    # check for searching for single words
    s_five = sonnets.search("five")
    print(s_five)
    # check for searching for phrases
    s_where_all = sonnets.search("where all")
    print(s_where_all)
    s_my_five_senses = sonnets.search("my five senses")
    print(s_my_five_senses)
    s_null_null = sonnets.search("null null")
    print(s_null_null)