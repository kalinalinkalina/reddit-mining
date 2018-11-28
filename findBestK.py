import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Point to the data
topics = ('Crypto', 'CVE', 'Cyber')
path ='/Users/kalina/CS412/Reddit/Clean/%s/' % (topics[2])
titles = []
posts = []

# Go through all of the files in the specified domain
for filename in os.listdir(path):
    
    # The files labeled "RS" contain the submissions ("RC" are comments)
    if filename.endswith('.json') and "RS" in filename: 
        print filename
        with open(path + filename) as f:
            for line in f:
                data = json.loads(line)
                if 'selftext_m' in data:
                
                    post = data["selftext_m"]
                    title = data["title_m"]
                    posts.append(post)
                    titles.append(title)
                
# Combine titles and posts
text = titles + posts
                
# Initialize vectorizer that converts raw text to matrix of TF-IDF features
vectorizer = TfidfVectorizer() 

# Learn the vocabulary dictionary and return term-document matrix
matrix = vectorizer.fit_transform(text)

# Figure out optimal number of clusters for K-means clustering
costs = []
K = range(1,50)
for k in K:
 
	# Create a kmeans model on our data, using k clusters.  random_state helps ensure that the algorithm returns the same results each time.
	kmeans_model = KMeans(n_clusters=k, random_state=1).fit(matrix)
	
	# These are our fitted labels for clusters -- the first cluster has label 0, and the second has label 1.
	labels = kmeans_model.labels_
 
	# Sum of distances of samples to their closest cluster center
	inertia = kmeans_model.inertia_
	costs.append(inertia)
	print "k:",k, " cost:", inertia

# Create a plot of the results
plt.plot(K, distortions, 'bx-')
plt.xlabel('K')
plt.ylabel('Cost')
plt.title('Optimal K')
plt.show()