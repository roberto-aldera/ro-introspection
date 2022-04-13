# Comparing RO to INS data


from train import *
from classifier_functions import *
from comms import *

num_elems = 3 # number of handcrafted features
num_scans_used = 7 #18
prob_thresh = 0.2#0.15, 0.25 is great

clf,scaler,training_eigvecs = trainSVM(num_elems,num_scans_used)

# keep track of features from previous eigenvectors
total_features = deque()

# tmp_scores = []
# for i in range(len(training_eigvecs)):
#     score = runClassifier(clf,scaler,training_eigvecs[i],total_features,num_elems,num_scans_used)
#     tmp_scores.append(score)

# print(tmp_scores)
print('Ready to connect...')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

print("connesso")

while True:
    # Get eigenvector
    # print('comms running')
    try:
        tmp = receive(conn)
        # print(tmp[:100])
    except:
        print('Error in receiving eigenvector from RO')

    eigenvec = []
    for x in tmp.split(','):
        try:
            x1 = double(x)
            eigenvec.append(x1)
        except:
            print('error in converting eigenvector element:',x)

    # Run classifier
    try:
        score = runClassifier(clf, scaler, eigenvec, total_features, prob_thresh, num_elems, num_scans_used)
        if(score == -1.):
            score = 0.
    except:
        print('error in runClassifier, assuming Good RO')
        score = 0.
    # Send back result to RO
    # print('Sending score:',score)
    try:
        send(str(score), conn)
    except:
        print('Error in sending score to RO')