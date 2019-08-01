import math
import collections
import ast

def entropy(p):
#     print(p)
    if p==1 or p==0:
        return 0
    return -p*math.log(p,2) - (1-p)*math.log(1-p,2)

def IG(clicks,nclicks,clicklen,nclicklen,threshold):
    words=[]
    commonList = clicks.most_common(clicklen)
    p = float(clicklen / (clicklen + nclicklen))
    entropy1 = entropy(p)
    IGs=[]
#     print(entropy1)
    for i in commonList:
        if i[1]<threshold:
            break
        posKeyword = i[1]
        negKeyword = nclicks[i[0]]
        words.append(i[0])
#         print(posKeyword)
#         print(negKeyword)
        
        pKeyword = (posKeyword+negKeyword)/(clicklen+nclicklen) #probability keyword appears
#         print(pKeyword)
        entropy2 = pKeyword * entropy(posKeyword/(negKeyword+posKeyword)) + (1-pKeyword) * entropy((clicklen-posKeyword)/(nclicklen+clicklen-negKeyword-posKeyword))
        IGs.append(entropy1 - entropy2)
    index = sorted(range(len(IGs)), key=lambda k: IGs[k], reverse = True) #sort IG in descending order and give index
    orderedwords = [words[x] for x in index] 
    orderedIGs = [IGs[x] for x in index] 

    return orderedwords,orderedIGs

def analyzeUser(clickresult,nclickresult,allClicks,allNclicks,threshold):
    result=[]
    for index in range(len(allClicks)):
        counter1=collections.Counter(clickresult[index])
        counter2=collections.Counter(nclickresult[index])
        words1,IG1 = IG(counter1,counter2,len(allClicks[index]),len(allNclicks[index]), threshold)
        words2,IG2 = IG(counter2,counter1,len(allNclicks[index]),len(allClicks[index]), threshold)
        len1 = len(words1)
        len2 = len(words2)
        i=0
        j=0
        posWords=[]
        posIGs=[]
        negWords=[]
        negIGs=[]
        unique = set()
        while (i<len1 and j<len2 and (len(posWords)<5 or len(negWords)<5)):
            if IG1[i] >= IG2[j]:
                if words1[i] in unique:
                    i+=1
                    continue
                unique.add(words1[i])
                if counter1[words1[i]] > counter2[words1[i]]:
                    if len(posWords)==5:
                        i+=1
                        continue
                    posWords.append(words1[i])
                    posIGs.append(IG1[i])
                else:
                    if len(negWords)==5:
                        i+=1
                        continue
                    negWords.append(words1[i])
                    negIGs.append(IG1[i])
                i+=1
            else:
                if words2[j] in unique:
                    j+=1
                    continue
                unique.add(words2[j])
                if counter1[words2[j]] > counter2[words2[j]]:
                    if len(posWords)==5:
                        i+=1
                    posWords.append(words2[j])
                    posIGs.append(IG2[j])
                else:
                    if len(negWords)==5:
                        i+=1
                        continue
                    negWords.append(words2[j])
                    negIGs.append(IG2[j])
                j+=1
        result.append([posWords,posIGs,negWords,negIGs])
    return result

# Code starts here
# Create mapping
ct=0
aid2ct = {}
with open('./documents.json') as f:
    for line in f:
        article=ast.literal_eval(line)
        aid2ct[article['_id']] = ct
        ct+=1
# print(ct)


#Read Through Users
ct=0
allClicks=[]
allNclicks=[]
users=[]
with open('./user-clicks-nclicks.json') as f:
    for line in f:
        user=ast.literal_eval(line)
        uid = user['userid']
        users.append(uid)
        clicks = user['clicks']
        nclicks = user['nclicks']
        userclicks=[]
        for i in clicks:
            userclicks.append(aid2ct[i])
        clickset = set(userclicks)
        usernclicks=[]
        for i in nclicks:
            if aid2ct[i] in clickset:
                continue
            usernclicks.append(aid2ct[i])
        userclicks.sort()
        usernclicks.sort()
        allClicks.append(userclicks)
        allNclicks.append(usernclicks)
#         print(userclicks)
#         print(usernclicks)
#         print(user['userid'])
#         print(user['clicks'])
#         print(user['nclicks'])
        ct+=1
#        if ct==100:
#            break
    

# Iterate articles and extract ones user clicked/nclicked
clickresult1=[[] for x in range(len(allClicks))]
nclickresult1=[[] for x in range(len(allNclicks))]
clickresult2=[[] for x in range(len(allClicks))]
nclickresult2=[[] for x in range(len(allNclicks))]
for userct in range(len(allClicks)):
    ct=0
    i=0
    j=0
    numClicks = len(allClicks[userct]) #one particular user's number of clicks
    numNclicks = len(allNclicks[userct]) #one particular user's number of nclicks
    with open('./documents.json') as f:
        for line in f:
            if i < numClicks and ct==allClicks[userct][i]:
                article=ast.literal_eval(line)
#                 aid = article['_id']
#                 title = article['stitle']
#                 domain = article['domain']
                keywords = article['kws']
                categories = article['cat']
                try:
                    categories += article['text_cat_class']
                except:
                    pass
                clickresult1[userct].extend(keywords)
                for kek in categories:
                    if kek.startswith('poi_'):
                        clickresult2[userct].append(kek)
                i+=1
            if j < numNclicks and ct==allNclicks[userct][j]:
                article=ast.literal_eval(line)
#                 aid = article['_id']
#                 title = article['stitle']
#                 domain = article['domain']
                keywords = article['kws']
                categories = article['cat'] 
                try:
                    categories += article['text_cat_class']
                except:
                    pass
                nclickresult1[userct].extend(keywords)
                for kek in categories:
                    if kek.startswith('poi_'):
                        nclickresult2[userct].append(kek)
                j+=1
            ct+=1
            
            if i==numClicks and j==numNclicks:
#                 print(ct)
                break
print('done')

kwResult = analyzeUser(clickresult1,nclickresult1,allClicks,allNclicks,5)
poiResult = analyzeUser(clickresult2,nclickresult2,allClicks,allNclicks, 2)
profiles=[]
for i in range(len(kwResult)):
    profile = {'userid':users[i],'pos_pois':poiResult[i][0],'neg_pois':poiResult[i][2],'pos_keywords':kwResult[i][0],'neg_keywords':kwResult[i][2]}
    profiles.append(profile)
# for i in range(20):
#     print(profiles[i])
#     print('')