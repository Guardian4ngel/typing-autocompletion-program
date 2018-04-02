import sys
from sys import stdin, stderr, stdout

class node:
    def __init__(self):
        self.words=0 # the number of words/expressions that matches this node completely
        self.prefix=0 # the number of words/expressions that share the node as its proper prefix
        self.top={'':0} # the top three most frequent expressions that share this node as its proper prefix
        self.child={} # the children of this node (the possible next letter that comes after it)
    def addword(self,word,pos=0):# add an expression to the trie
        if(pos==len(word)):
            self.words+=1
            return self.words
        ch=ord(word[pos])
        if (ch>122 or ch<97) and ch!=32:
            return -1
        if ch not in self.child:
            self.child[ch]=node()
        wordcount=self.child[ch].addword(word,pos+1)
        if wordcount==-1:
            return -1
        self.prefix+=1
        self.top[word[pos:]]=wordcount
        while len(self.top)>3:
            discard=list(self.top.keys())[0]
            for k in self.top:
                if self.top[k]<self.top[discard]:
                    discard=k
            del self.top[discard]
        return wordcount
    def recommand(self,word,pos=0):# given a prefix, recommend the top three most frequent expressions
        if(pos==len(word)):
            return self.top,max(self.prefix,1)
        ch=ord(word[pos])
        if ch not in self.child:
            return {'a':0},1
        return self.child[ch].recommand(word,pos+1)

def clean(w):# clean a word from training data
    if w=='':
        return ''
    w=w.lower()# turn all letters to lower case
    wl=list(w)
    for i in range(len(wl)):
        if ord(wl[i])>122 or ord(wl[i])<97:
            if i==0 and wl[i]=='(': # ignore leading bracket
                wl[i]=''
            elif i!=len(wl)-1: # ignore tailing punctuation
                wl[i]=''
            else:  # if after all above procedures there is still non alphabetical characters, ignore this word
                return ''
    cleanword=''
    for c in wl:
        cleanword+=c
    return cleanword

def train(train_amount,review):
    print('Training',file=stderr)
    reviews=open('reviews_{}.txt'.format(review),'r',encoding="utf8")
    print('Loading review_{}'.format(review),file=stderr)
    trie=node()
    linecount=0
    for rv in reviews:
        s=rv.split()
        pre=' '
        sentencestart=True
        for word in s:
            w=clean(word)# clean the word
            if w!='': # add single word to the trie if it passed cleaning procedure
                trie.addword(w)
            if (not sentencestart) and w!='' and pre!='': # if this word and its previous word are in the same sentence and both passed the 'clean' procedure, add them to the trie
                trie.addword(pre+' '+w)
            pre=w
            if word[len(word)-1].isalpha():
                sentencestart=False
            else:
                sentencestart=True
        linecount+=1
        if linecount%1000==0:
            print("{} reviews loaded".format(linecount),file=stderr)
        if linecount==train_amount:
            break
    print('Training ended, {} reviews loaded in total'.format(linecount),file=stderr)
    return trie

def select(pred):# if the recommendation from trie is graater than 3, compute their percentage of appearance and pick the 3 most frequent entry as final recommendation
    top_pred={}
    for p in pred:
        for cand in p[0]:
            prob=p[0][cand]/p[1]
            if cand in top_pred:
                top_pred[cand]=max(top_pred[cand],prob)
            else:
                top_pred[cand]=prob
            if len(top_pred)>3:
                discard=list(top_pred.keys())[0]
                for k in top_pred:
                    if top_pred[k]<top_pred[discard]:
                        discard=k
                del top_pred[discard]
    final_pred=[]
    for p in top_pred:
        final_pred.append(p+' ')
    while len(final_pred)<3:
        final_pred.append(' ')
    return final_pred

def predict(review,trie):
    r=review.split()
    if review[len(review)-1]==' ':
        r.append('')
    w1=clean(r[len(r)-1]) # w1 is the last word (including incomplete word) so far
    pred=[]
    pred.append(trie.recommand(w1)) # get the recommendation with w1
    if len(r)==1:
        return select(pred)
    w2=r[len(r)-2] # w2 is the second word from the bottom
    if w2[len(w2)-1]=='.':
        return select(pred)
    w2=clean(r[len(r)-2])
    pred.append(trie.recommand(w2+' '+w1)) # get the recommendation with w2+' '+w1 if they are in the same sentence
    return select(pred)