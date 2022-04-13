from train import *

def extractCustomFeaturesFromEigvec(eigvec,num_elems=5):
#     print('Extracting features...')
    eig_features = []
    arr = np.array(eigvec)
    arr_fixed_length = np.zeros(2400)
    arr_fixed_length[:len(arr)] = arr 
    sorted_max_evec = sort(arr_fixed_length)[::-1]
    max_val = sorted_max_evec[0]
    num_landmarks = count_nonzero(sorted_max_evec)
    area_under_curve = []
    temp_sum = 0;
    for i in range(len(arr)):
        temp_sum += arr[i]
    area_under_curve = temp_sum
    eig_features.append(max_val)
    eig_features.append(num_landmarks)
    eig_features.append(area_under_curve)
    print('Current eigvec features:',eig_features)
    return(eig_features)

def extractElementsFromEigvec(eigvec,num_elems=5):
#     print('Extracting features...')
    # Take evenly spaced elements as features
    arr = np.array(eigvec)
    arr_fixed_length = np.zeros(2400)
    arr_fixed_length[:len(arr)] = arr 
    sorted_max_evec = sort(arr_fixed_length)[::-1]
    eig_len = len(sorted_max_evec)
    idx = np.round(np.linspace(0, eig_len - 1, num_elems)).astype(int)
    eig_features = sorted_max_evec[idx]
    print('Current eigvec features:',eig_features)
    return(eig_features)

def extractFeatures(currentFeatures,previousFeatures,num_elems=5,num_scans_used=18):
# Take previous eigenvector features and add them to the list
# Remove older features, shift features along, add latest features
    combinedFeatures = previousFeatures
    combinedFeatures.extend(currentFeatures)
    if(len(combinedFeatures) > (num_scans_used*num_elems)):
        [combinedFeatures.popleft() for _i in range(num_elems)]
    return(combinedFeatures)

def classifyOnFeatures(clf,scaler,combinedFeatures,prob_thresh=0.6,num_elems=5,num_scans_used=18):
    if(len(combinedFeatures) >= (num_scans_used*num_elems)):
        # reshape
        sample = np.array(combinedFeatures)
        sample = sample.reshape((1,sample.shape[0]))
        # run classifier
        X_data = scaler.transform(sample)
        # score = clf.predict(X_data)
        score = clf.predict_proba(X_data)
        augmented_score = (score[:,1] > prob_thresh)
        score = double(augmented_score[0])
    else:
        # not enough eigenvectors yet
        score = -1. # assume good RO
        print('Good RO assumed until we have at least this many matched scans:',num_scans_used)
    return score

# Take in a sorted eigenvector, and output a score (use other functions in this one)
def runClassifier(clf,scaler,eigvec,total_features,prob_thresh,num_elems,num_scans_used):
    # latest_features = extractElementsFromEigvec(eigvec,num_elems)
    latest_features = extractCustomFeaturesFromEigvec(eigvec,num_elems)
    total_features = extractFeatures(latest_features,total_features,num_elems,num_scans_used)
    score = classifyOnFeatures(clf,scaler,total_features,prob_thresh,num_elems,num_scans_used)
    return(score)
