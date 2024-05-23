from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pywt import wavedec
import pandas as pd
import sys
import json

scaler = StandardScaler()


def feature_extraction(num1):

    df = pd.read_csv(num1,skiprows=1)

    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    df.set_index('Timestamp', inplace=True)
    df = df.iloc[:,3:8]

    A_features = pd.DataFrame()

    column_name = ['EEG.AF3', 'EEG.T7','EEG.Pz', 'EEG.T8', 'EEG.AF4']


    for c in column_name:
        coeffs = wavedec(df[c], 'db2', level=4)

        cA4, cD4, cD3, cD2, cD1 = coeffs

        result_D4 = pd.DataFrame({"1": cD4[:14].tolist()})
        result_A4 = pd.DataFrame({"1": cA4[:14].tolist()})
        result_D3 = pd.DataFrame({"1": cD3[:25].tolist()})
        result_D2 = pd.DataFrame({"1": cD2[:47].tolist()})
        result_D1 = pd.DataFrame({"1": cD1[:92].tolist()})


        ress = pd.concat([result_D4.T, result_A4.T, result_D3.T, result_D2.T, result_D1.T],ignore_index = True, axis = 1)
        A_features = pd.concat([A_features, ress], axis = 0)

    A_features = pd.concat([A_features,A_features,A_features,A_features,A_features,A_features,A_features,A_features])
    scaler.fit(A_features)
    scaled_features = scaler.transform(A_features)
    eeg_features = pd.DataFrame(scaled_features)

    pca = PCA(n_components = 40).fit(eeg_features)
    x_pca = pca.transform(eeg_features)

    return x_pca


if __name__ == "__main__":
    csv = sys.argv[1]
    features = feature_extraction(csv)
    features_list = [feature.tolist() for feature in features]  # Convert ndarray to list
    print(json.dumps(features_list))
