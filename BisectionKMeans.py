import numpy as np
import gzip
import random

def getFurthest(kwVec,kwList,kw):
    maxDist=0
    farWord=''
    for word in kwList:
#         print(kwVec[kw])
#         print(kwVec[word])
        dist = np.linalg.norm(kwVec[kw]-kwVec[word])
        if dist > maxDist:
            dist=maxDist
            farWord = word
    return farWord

def splitGroup(kwVec,kwList,kw1,kw2):
    group1=[]
    group2=[]
    for word in kwList:
        dist1 = np.linalg.norm(kwVec[kw1]-kwVec[word])
        dist2 = np.linalg.norm(kwVec[kw2]-kwVec[word])
        if dist1 <= dist2:
            group1.append(word)
        else:
            group2.append(word)
#     print(group1)
#     print(group2)
#     print('')
    return group1,group2

def binaryKMeans(kwVec,group):
#     print(1)
#     print(group)
    if len(group)<5:
#         print(group)
        return group
    else:
        rand = random.randint(0, len(group)-1)
        word1 = getFurthest(kwVec,group,group[rand])
        word2 = getFurthest(kwVec,group,word1)
        group1,group2 = splitGroup(kwVec,group,word1,word2)
        child1 = binaryKMeans(kwVec,group1)
        child2 = binaryKMeans(kwVec,group2)
        result=[]
        if type(child1[0]) == list:
            if type(child2[0]) == list:
                result=child1+child2
            else:
                result=child1+[child2]
        else:
            if type(child2[0]) == list:
                result=[child1]+child2
            else:
                result=[child1]+[child2]
        return result

kwVec={}
ct=0
with gzip.open('w2v.csv.min.gz','rt') as f:
    f.readline()
    for line in f:
        info=line.rstrip().split()
        kwVec[info[0]] = np.array([float(i) for i in info[1:]])

test=[('police', 35), ('man', 28), ('home', 25), ('iran', 17), ('hormuz', 10), ('court', 10), ('tehran', 9), ('daughter', 9), ('july', 9), ('tensions', 8), ('facebook', 8), ('attack', 7), ('shooting', 7), ('suspect', 7), ('people', 7), ('husband', 7), ('u.s.', 6), ('county^^sheriff', 6), ('time', 6), ('texas', 5), ('pentagon', 5), ('attacks', 5), ('walmart', 5), ('united^^states', 5), ('virginia', 5), ('investigators', 5), ('drive', 5), ('fire', 4), ('nbc', 4), ('prison', 4), ('surveillance', 4), ('navy', 4), ('aircraft', 4), ('video', 4), ('justice', 4), ('kids', 4), ('persian^^gulf', 4), ('weapons', 4), ('drugs', 4), ('family', 4), ('jail', 4), ('khloe^^kardashian', 4), ('instagram', 4), ('camera', 4), ('strike', 3), ('gun', 3), ('authorities', 3), ('teen', 3), ('country', 3), ('fighter^^jets', 3), ('flying', 3), ('abc^^news', 3), ('face', 3), ('detectives', 3), ('star', 3), ('chores', 3), ('medical', 3), ('iranian^^territorial^^waters', 3), ('foreign^^ministry', 3), ('rape', 3), ('bars', 3), ('drug', 3), ('richmond', 3), ('iraq', 3), ('officer', 3), ('gunshot^^wounds', 3), ('things', 3), ('company', 3), ('driving', 3), ('anonymous', 3), ('trump', 2), ('men', 2), ('unit', 2), ('women', 2), ('turning', 2), ('houston', 2), ('surveillance^^video', 2), ('unmanned^^aircraft', 2), ('iranian^^airspace', 2), ('iranian^^forces', 2), ('missions', 2), ('israel', 2), ('commander', 2), ('drinking', 2), ('friends', 2), ('north^^korea', 2), ('korean', 2), ('wonsan', 2), ('rockets', 2), ('russia', 2), ('russian', 2), ('japan', 2), ('ufos', 2), ('kansas^^city', 2), ('goodbye', 2), ('michael', 2), ('crude^^oil', 2), ('iranian^^waters', 2), ('iranian^^officials', 2), ('boats', 2), ('international^^waters', 2), ('west^^virginia', 2), ('plastic', 2), ('w.va', 2), ('sex', 2), ('pregnant', 2), ('twins', 2), ('footage', 2), ('shoplifting', 2), ('drug^^paraphernalia', 2), ('smoking', 2), ('jeans', 2), ('ali^^khamenei', 2), ('islamic^^republic', 2), ('paraphernalia', 2), ('treatment', 2), ('u.s.^^sanctions', 2), ('b-52^^bombers', 2), ('u.s.^^troops', 2), ('afghanistan', 2), ('u.s.^^forces', 2), ('dating', 2), ('pic', 2), ('garbage', 2), ('cause^^of^^death', 2), ('drug^^charges', 2), ('crack^^cocaine', 2), ('illegal^^possession', 2), ('city^^police', 2), ('child^^abuse', 2), ('food', 2), ('kylie^^jenner', 2), ('kim^^kardashian', 2), ('kuwtk', 2), ('jordyn^^woods', 2), ('tristan^^thompson', 2), ('us^^army', 2), ('law^^enforcement', 2), ('juveniles', 2), ('viral^^video', 2), ('washington', 2), ('virginia^^state^^police', 2), ('bedroom', 2), ('saudi^^arabia', 2), ('fuel', 2), ('walking', 2), ('raleigh', 2), ('god', 2), ('incident', 2), ('county^^jail', 2), ('deputy', 2), ('happy', 2), ('knoxville^^police^^department', 2), ('crime^^hotline', 2), ('knoxville', 2), ('callers', 2), ('pink', 2), ('syria', 2), ('britain', 2), ('source', 2), ('gulf', 2), ('commercial^^shipping', 2), ('basement', 2), ('social', 2), ('investigation', 2), ('london', 2), ('vacation', 2), ('u.s.^^allies', 2)]

exist=[]
nonex=[]

kws = [kek for (kek,kek1) in test]
for i in range(len(kws)):
    if kws[i] in kwVec:
        exist.append(kws[i])
#         print(kws[i])
    else:
        if '^^' in kws[i]:
            kws[i] = kws[i].replace('^^','_')
            if kws[i] not in kwVec:
                nonex.append(kws[i])
            else:
                exist.append(kws[i])

result=binaryKMeans(kwVec,exist)
print(len(result))

for i in result:
#     print(len(i))
    print(i)