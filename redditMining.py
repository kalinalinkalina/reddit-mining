import os
import json
import sys
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import adjusted_rand_score
from sklearn import preprocessing

# Some default parameters, if unspecified
doCosine = False # Whether to measure Euclidean Distance or Cosine Similarity
doWeights = True # Whether to assign weights to titles and posts
ngrams = 2       # Keywords and key-phrases of max length 2
topic = 'CVE' 
numClusters = 15 # Figured this out using findBestK.py
numTopWords = 10 # This is arbitrary
pathStem = '/Users/kalina/CS412/' 


# Get input from command line arguments
ii = 1
while len(sys.argv) > ii+1 and sys.argv[ii][0] == "-":
    a = sys.argv[ii]
    b = sys.argv[ii+1]
    if a == "-k":
        k = int(b)
        ii += 2
    elif a == "-words":
        numTopWords = int(b)
        ii += 2
    elif a == "-domain":
        topic = b
        ii += 2
    elif a == "-ngrams":
        ngrams = int(b)
        ii += 2
    elif a == "-metric":
        if 'cos' in b.lower():
            doCosine = True
        elif 'euc' in b.lower():
            doCosine = False
        else:
            print "ERROR: metric must be 'cos' or 'euclid', not '%s'" % b
        ii += 1
    elif a == "-weights":
        if b in ['true', 'True', 'T', 't', '1']:
            doWeights = True
        else:
            doWeights = False
        ii += 1
    else:
        print "ERROR: '%s' is not a valid argument", a
        print sys.exit()
if doCosine:
    distance = "Cosine"
else:
    distance = "Euclidean"

# Write some header metadata information to the out file
outFileName = topic + "_" + distance
outFile = open(pathStem + outFileName + '.txt', "w")
outFile.write("Domain: %s\n" % topic)
outFile.write("Distance: %s\n" % distance)
outFile.write("Weight: %s\n\n" % str(doWeights))

path = pathStem + 'Reddit/Clean/' + topic + '/'

titles = []
posts = []

# Go through all of the files in the specified domain
for filename in os.listdir(path):

    # Go through all the json files
    if filename.endswith('.json') and "RS" in filename: # Post files contain "RS"; comment files contain "RC"

        with open(path + filename) as f:
            for line in f:

                data = json.loads(line)
                
                # If this is a post file 
                if 'selftext_m' in data:
                    post = data["selftext_m"]
                    title = data["title_m"]
                    if post not in posts:
                        posts.append(post)
                        titles.append(title)

                
# Combine titles and posts into one big document
text = titles + posts 
                
# Initialize vectorizer that converts raw text to matrix of TF-IDF features
vectorizer = TfidfVectorizer(ngram_range=(1,ngrams)) 

# Learn the vocabulary dictionary and return term-document matrix
matrix = vectorizer.fit_transform(text)

print matrix.shape
sys.exit()

# Normalize data, so that we can get cosine similarity
if doCosine:
    matrixNorm = preprocessing.normalize(matrix)
    matrix = matrixNorm

# Add weight of 4 to titles and 2 to posts 
if doWeights:
    numPosts = len(posts)
    numTitles = len(titles)
    
    postWeights = np.empty(numPosts)
    titleWeights = np.empty(numTitles)
    
    titleWeights.fill(4)
    postWeights.fill(2)
    
    npWeights = np.concatenate((postWeights, titleWeights), axis=None)
    weights = npWeights.tolist()
    
# K-Means clustering
#kmeans = KMeans(n_clusters=numClusters, n_init=100)
kmeans = MiniBatchKMeans(n_clusters=numClusters, n_init=100, batch_size=1000000)
kmeans.fit(matrix, sample_weight=weights)

# Coordinates of cluster centers
centerCoords = kmeans.cluster_centers_
orderedCenterCoords = centerCoords.argsort()[:, ::-1]

# Get array mapping from feature integer indices to feature names (the actual words in the text)
terms = vectorizer.get_feature_names()

# Get the top words in each cluster
topWords = [[None for x in range(numTopWords)] for y in range(numClusters)]
for iCluster in range(numClusters):
    i = 0
    for ind in orderedCenterCoords[iCluster, :numTopWords]:
        topWords[iCluster][i] = terms[ind]
        i += 1        

# Write out the results
for x in range(len(topWords)):
    outFile.write("Cluster %d: " % x)
    for y in range(len(topWords[0])):
        outFile.write("'" + topWords[x][y] + "' ")
    print ""
    outFile.write("\n")

outFile.close()
    