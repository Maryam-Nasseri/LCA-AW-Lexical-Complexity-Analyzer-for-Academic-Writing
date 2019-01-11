import string,re,sys,os,random
from math import sqrt,log

# adjust minimum sample size here
standard=50

# Returns the keys of dictionary d sorted by their values
def sort_by_value(d):
    items=d.items()
    backitems=[ [v[1],v[0]] for v in items]
    backitems.sort()
    return [ backitems[i][1] for i in range(0,len(backitems))]

# NDW for first z words in a sample
def getndwfirstz(z,lemmalist):
    ndwfirstztype={}
    for lemma in lemmalist[:z]:
        ndwfirstztype[lemma]=1
    return len(ndwfirstztype.keys())

# NDW expected random z words, 10 trials
def getndwerz(z,lemmalist):
    ndwerz=0
    for i in range(10):
        ndwerztype={}
        erzlemmalist=random.sample(lemmalist,z)
        for lemma in erzlemmalist:
            ndwerztype[lemma]=1
        ndwerz+=len(ndwerztype.keys())
    return ndwerz/10.0

# NDW expected random sequences of z words, 10 trials
def getndwesz(z,lemmalist):
    ndwesz=0
    for i in range(10):
        ndwesztype={}
        startword=random.randint(0,len(lemmalist)-z)
        eszlemmalist=lemmalist[startword:startword+z]
        for lemma in eszlemmalist:
            ndwesztype[lemma]=1
        ndwesz+=len(ndwesztype.keys())
    return ndwesz/10.0

# MSTTR
def getmsttr(z,lemmalist):
    samples=0
    msttr=0.0
    while len(lemmalist)>=z:
        samples+=1
        msttrtype={}
        for lemma in lemmalist[:z]:
            msttrtype[lemma]=1
        msttr+=len(msttrtype.keys())/float(z)
        lemmalist=lemmalist[z:]    
    return msttr/samples

def isLetterNumber(character):
    if character in string.printable and not character in string.punctuation:
        return 1
    return 0

def isSentence(line):
    for character in line:
        if isLetterNumber(character):
            return 1
    return 0

#reads the bawe_list words


bawe_list = [line.split(',') for line in open("bawe_list.txt")]


# reads information from bnc wordlist
adjdict={}
verbdict={}
noundict={}
worddict={}
wordlistfile=open("bnc_all_filtered.txt","r")
wordlist=wordlistfile.readlines()
wordlistfile.close()
for word in wordlist:
    wordinfo=word.strip()
    if not wordinfo or "Total words" in wordinfo:
        continue
    infolist=wordinfo.split()
    lemma=infolist[0]
    pos=infolist[1]
    frequency=int(infolist[2])
    worddict[lemma]=worddict.get(lemma,0)+frequency
    if pos=="Adj":
        adjdict[lemma]=adjdict.get(lemma,0)+frequency
    elif pos=="Verb":
        verbdict[lemma]=verbdict.get(lemma,0)+frequency
    elif pos=="NoC" or pos=="NoP":
        noundict[lemma]=noundict.get(lemma,0)+frequency
wordranks=sort_by_value(worddict)
verbranks=sort_by_value(verbdict)

# input file is output of morph
filename=sys.argv[1]
lemfile=open(filename,"r")
lemlines=lemfile.readlines()
lemfile.close()
filename=sys.argv[1].split("/")[-1]

# process input file
wordtypes={}
wordtokens=0
swordtypes={}
swordtokens=0
lextypes={}
lextokens=0
slextypes={}
slextokens=0
verbtypes={}
verbtokens=0
sverbtypes={}
adjtypes={}
adjtokens=0
advtypes={}
advtokens=0
nountypes={}
nountokens=0
sentences=0
lemmaposlist=[]
lemmalist=[]

for lemline in lemlines:
    lemline=lemline.strip()
    lemline=lemline.lower()
    if not isSentence(lemline):
        continue
    sentences+=1
    lemmas=lemline.split()
    for lemma in lemmas:
        word=lemma.split("_")[0]
        pos=lemma.split("_")[-1]
        if (not pos in string.punctuation) and pos!="sent" and pos!="sym":
            lemmaposlist.append(lemma)
            lemmalist.append(word)  
            wordtokens+=1
            wordtypes[word]=1
            if (not word in wordranks[-2000:] or word in bawe_list) and pos != "cd":
                swordtypes[word]=1
                swordtokens+=1
            if pos[0]=="n":
                lextypes[word]=1
                nountypes[word]=1
                lextokens+=1
                nountokens+=1
                if not word in wordranks[-2000:] or word in bawe_list:
                    slextypes[word]=1
                    slextokens+=1
            elif pos[0]=="j":
                lextypes[word]=1
                adjtypes[word]=1
                lextokens+=1
                adjtokens+=1
                if not word in wordranks[-2000:] or word in bawe_list:
                    slextypes[word]=1
                    slextokens+=1
            elif pos[0]=="r" and (adjdict.has_key(word) or (word[-2:]=="ly" and adjdict.has_key(word[:-2]))):
                lextypes[word]=1
                advtypes[word]=1
                lextokens+=1
                advtokens+=1
                if not word in wordranks[-2000:] or word in bawe_list:
                    slextypes[word]=1
                    slextokens+=1
            elif pos[0]=="v" and not word in ["be","have"]:
                verbtypes[word]=1
                verbtokens+=1
                lextypes[word]=1
                lextokens+=1
                if not word in wordranks[-2000:] or word in bawe_list:
                    sverbtypes[word]=1
                    slextypes[word]=1
                    slextokens+=1

# 0. basic statistics
mls=wordtokens/float(sentences)

# 1. lexical density
ld=float(lextokens)/wordtokens

# 2. lexical sophistication
# 2.1 lexical sophistication
ls1=slextokens/float(lextokens)
ls2=len(swordtypes.keys())/float(len(wordtypes.keys()))

# 2.2 verb sophistication
vs1=len(sverbtypes.keys())/float(verbtokens)
vs2=(len(sverbtypes.keys())*len(sverbtypes.keys()))/float(verbtokens)
cvs1=len(sverbtypes.keys())/sqrt(2*verbtokens)

# 3 lexical diversity or variation

# 3.1 NDW, may adjust the values of "standard"
ndw=ndwz=ndwerz=ndwesz=len(wordtypes.keys())
if len(lemmalist)>=standard:
    ndwz=getndwfirstz(standard,lemmalist)
    ndwerz=getndwerz(standard,lemmalist)
    ndwesz=getndwesz(standard,lemmalist)

# 3.2 TTR
msttr=ttr=len(wordtypes.keys())/float(wordtokens)
if len(lemmalist)>=standard:
    msttr=getmsttr(standard,lemmalist)
cttr=len(wordtypes.keys())/sqrt(2*wordtokens)
rttr=len(wordtypes.keys())/sqrt(wordtokens)
logttr=log(len(wordtypes.keys()))/log(wordtokens)
uber=(log(wordtokens,10)*log(wordtokens,10))/log(wordtokens/float(len(wordtypes.keys())),10)

# 3.3 verb diversity
vv1=len(verbtypes.keys())/float(verbtokens)
svv1=len(verbtypes.keys())*len(verbtypes.keys())/float(verbtokens)
cvv1=len(verbtypes.keys())/sqrt(2*verbtokens)

# 3.4 lexical diversity
lv=len(lextypes.keys())/float(lextokens)
vv2=len(verbtypes.keys())/float(lextokens)
nv=len(nountypes.keys())/float(nountokens)
adjv=len(adjtypes.keys())/float(lextokens)
advv=len(advtypes.keys())/float(lextokens)
modv=(len(advtypes.keys())+len(adjtypes.keys()))/float(lextokens)

print "filename, sentences, wordtypes, swordtypes, lextypes, slextypes, wordtokens, swordtokens, lextokens, slextokens, ld, ls1, ls2, vs1, vs2, cvs1, ndw, ndwz, ndwerz, ndwesz, ttr, msttr, cttr, rttr, logttr, uber, lv, vv1, svv1, cvv1, vv2, nv, adjv, advv, modv"

output=filename
for measure in [sentences, len(wordtypes.keys()), len(swordtypes.keys()), len(lextypes.keys()), len(slextypes.keys()), wordtokens, swordtokens, lextokens, slextokens, ld, ls1, ls2, vs1, vs2, cvs1, ndw, ndwz, ndwerz, ndwesz, ttr, msttr, cttr, rttr, logttr, uber, lv, vv1, svv1, cvv1, vv2, nv, adjv, advv, modv]: 
    if type(measure)==type(0.0):
        measure="%.2f" % measure
    output+=", "+str(measure)
print output
