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

	
    cD4_DATA =pd.DataFrame()
    cA4_DATA = pd.DataFrame()
    cD3_DATA = pd.DataFrame()
    cD2_DATA = pd.DataFrame()
    cD1_DATA = pd.DataFrame()

    column_name = ['EEG.AF3', 'EEG.T7','EEG.Pz', 'EEG.T8', 'EEG.AF4']
    for c in column_name:
        coeffs = wavedec(df[c], 'db2', level=4)

        cA4, cD4, cD3, cD2, cD1 = coeffs

        result_D4 = pd.DataFrame({str(c): cD4[:13].tolist()})

        cD4_DATA = pd.concat([cD4_DATA, result_D4], axis=1)

        result_A4 = pd.DataFrame({str(c): cA4[:13].tolist()})
        cA4_DATA = pd.concat([cA4_DATA, result_A4], axis=1)
    
        result_D3 = pd.DataFrame({str(c) : cD3[:13].tolist()})
        cD3_DATA = pd.concat([cD3_DATA, result_D3], axis=1)
    
        result_D2 = pd.DataFrame({str(c) : cD2[:13].tolist()})
        cD2_DATA = pd.concat([cD2_DATA, result_D2], axis=1)
    
        result_D1 = pd.DataFrame({str(c): cD1[:13].tolist()})
        cD1_DATA = pd.concat([cD1_DATA, result_D1], axis=1)
    

    A_features = pd.concat([cA4_DATA, cD4_DATA, cD3_DATA, cD2_DATA, cD1_DATA],axis = 1)
#    y = A_features["Label"]
#    X = A_features.drop("Label", axis = 1)

    pca = PCA(n_components = 13, whiten=True).fit(A_features)
    x_pca = pca.transform(A_features)

    scaler.fit(x_pca)
    scaled_features = scaler.transform(x_pca)
    #eeg_features = pd.DataFrame(scaled_features)
    #eeg_features.to_csv("features_model.csv", sep=',',index=False, encoding='utf-8')
    return scaled_features


if __name__ == "__main__":
    csv = sys.argv[1]
    features = feature_extraction(csv)
    features_list = [feature.tolist() for feature in features]  # Convert ndarray to list
    print(json.dumps(features_list))
