import string,re,sys,os,random,glob
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

def division(x,y):
    if y==0:
        return 0
    else:
        return float(x)/y

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

directoryPath=sys.argv[1]

print "filename, sentences, wordtypes, swordtypes, lextypes, slextypes, wordtokens, swordtokens, lextokens, slextokens, ld, ls1, ls2, vs1, vs2, cvs1, ndw, ndwz, ndwerz, ndwesz, ttr, msttr, cttr, rttr, logttr, uber, lv, vv1, svv1, cvv1, vv2, nv, adjv, advv, modv"

for filename in glob.glob( os.path.join(directoryPath, '*') ):
    lemfile=open(filename,"r")
    lemlines=lemfile.readlines()
    lemfile.close()
    filename=filename.split("/")[-1]

    output=filename
    if not lemlines:
        output+=",0.0"*31
        print output
        continue

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
    mls=division(wordtokens,sentences)

    # 1. lexical density
    ld=division(lextokens,wordtokens)

    # 2. lexical sophistication
    # 2.1 lexical sophistication
    ls1=division(slextokens,lextokens)
    ls2=division(len(swordtypes.keys()),len(wordtypes.keys()))

    # 2.2 verb sophistication
    vs1=division(len(sverbtypes.keys()),verbtokens)
    vs2=division(len(sverbtypes.keys())*len(sverbtypes.keys()),verbtokens)
    cvs1=division(len(sverbtypes.keys()),sqrt(2*verbtokens))

    # 3 lexical diversity or variation
    # 3.1 NDW, may adjust the values of "standard"
    ndw=ndwz=ndwerz=ndwesz=len(wordtypes.keys())
    if len(lemmalist)>=standard:
        ndwz=getndwfirstz(standard,lemmalist)
        ndwerz=getndwerz(standard,lemmalist)
        ndwesz=getndwesz(standard,lemmalist)

    # 3.2 TTR
    ttr=msttr=division(len(wordtypes.keys()),wordtokens)
    if len(lemmalist)>=standard:
        msttr=getmsttr(standard,lemmalist)
    cttr=division(len(wordtypes.keys()),sqrt(2*wordtokens))
    rttr=division(len(wordtypes.keys()),sqrt(wordtokens))
    logttr=division(log(len(wordtypes.keys())),log(wordtokens))
    uber=(log(wordtokens,10)*log(wordtokens,10))/log(wordtokens/float(len(wordtypes.keys())),10)

    # 3.3 verb diversity
    vv1=division(len(verbtypes.keys()),verbtokens)
    svv1=division(len(verbtypes.keys())*len(verbtypes.keys()),verbtokens)
    cvv1=division(len(verbtypes.keys()),sqrt(2*verbtokens))

    # 3.4 lexical diversity
    lv=division(len(lextypes.keys()),lextokens)
    vv2=division(len(verbtypes.keys()),lextokens)
    nv=division(len(nountypes.keys()),nountokens)
    adjv=division(len(adjtypes.keys()),lextokens)
    advv=division(len(advtypes.keys()),lextokens)
    modv=division((len(advtypes.keys())+len(adjtypes.keys())),lextokens)

    output=filename
    for measure in [sentences, len(wordtypes.keys()), len(swordtypes.keys()), len(lextypes.keys()), len(slextypes.keys()), wordtokens, swordtokens, lextokens, slextokens, ld, ls1, ls2, vs1, vs2, cvs1, ndw, ndwz, ndwerz, ndwesz, ttr, msttr, cttr, rttr, logttr, uber, lv, vv1, svv1, cvv1, vv2, nv, adjv, advv, modv]: 
        if type(measure)==type(0.0):
            measure="%.2f" % measure
        output+=", "+str(measure)
    print output
