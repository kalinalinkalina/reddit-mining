# CS412: Mining of Reddit Text Data by Kalina Borkiewicz and Kat Schroeder

This project mines the unstructured text of  conversation threads (submissions and comments) from the website www.reddit.com within three domains -- Common [Software] Vulnerabilities and Exposures (CVE), Crypto-currency, and Cybersecurity -- to find keywords that indicate relevant dimensions in the data.

Though other methods were attempted (most notably using the RAKE algorithm), these are the final three scripts that were used in obtaining the K-means clustering results:

1) preprocess.py   - The data preprocessing script that was run to clean the data
2) findBestK.py    - A script that tests multiple values of K for K-means clustering and creates a plot to show the costs.
3) redditMining.py - The script that computes K-Means clustering to find best keywords
