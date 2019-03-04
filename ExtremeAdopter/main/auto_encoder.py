from pandas import read_csv
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras import regularizers
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

import matplotlib.pyplot as plt
import seaborn as sns
from pylab import rcParams

sns.set(style='whitegrid', palette='muted', font_scale=1.5)
rcParams['figure.figsize'] = 14, 8

from sklearn.metrics import confusion_matrix, roc_curve, auc, recall_score, classification_report, precision_score, accuracy_score
from sklearn.metrics import precision_recall_fscore_support as score

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.layers import Input, Dense
from keras.models import Model, load_model
import os
import numpy as np
import pandas as pd

LABELS = ["Extreme", "Normal"]

import utilities.IOProperties as prop

def train_model(X_train, X_test):
    X_test = X_test.drop(['Class'], axis=1)
    X_test = X_test.values

    input_dim = X_train.shape[1]
    input_layer = Input(shape = (input_dim, ))

    # DEFINE THE DIMENSION OF ENCODER ASSUMED 3
    encoding_dim = 20
    # DEFINE THE ENCODER LAYERS

    encoder = Dense(encoding_dim, activation="tanh",
                    activity_regularizer=regularizers.l1(10e-5))(input_layer)
    encoder = Dense(int(encoding_dim / 2), activation="relu")(encoder)
    # DEFINE THE DECODER LAYERS
    decoder = Dense(int(encoding_dim / 2), activation='tanh')(encoder)
    decoder = Dense(input_dim, activation='relu')(decoder)
    # COMBINE ENCODER AND DECODER INTO AN AUTOENCODER MODEL
    autoencoder = Model(inputs=input_layer, outputs=decoder)
    # CONFIGURE AND TRAIN THE AUTOENCODER
    autoencoder.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

    # define the checkpoint and save the best model
    checkpoint = ModelCheckpoint(prop.model_filepath, monitor='val_loss', verbose=0, save_best_only=True)
    earlyStopping = EarlyStopping(monitor='val_loss', patience=20, verbose=0)
    callbacks_list = [checkpoint,earlyStopping]

    autoencoder.fit(X_train, X_train, epochs = 1000, batch_size = 32, shuffle = True, validation_data=(X_test, X_test),
                    verbose=1, callbacks=callbacks_list)

def test_model(X_test):
    autoencoder = load_model(prop.model_filepath)

    y_test = X_test['Class']
    X_test = X_test.drop(['Class'], axis=1)
    X_test = X_test.values

    unique, counts = np.unique(y_test, return_counts=True)
    print(unique, counts)

    predictions = autoencoder.predict(X_test)
    print(predictions[0:2])

    mse = np.mean(np.power(X_test - predictions, 2), axis=1)
    error_df = pd.DataFrame({'reconstruction_error': mse,
                            'true_class': y_test})
    # print(error_df.describe())
    print(error_df)

    # fpr, tpr, thresholds = roc_curve(error_df.true_class, error_df.reconstruction_error)
    # roc_auc = auc(fpr, tpr)
    #
    # plt.title('Receiver Operating Characteristic')
    # plt.plot(fpr, tpr, label='AUC = %0.4f'% roc_auc)
    # plt.legend(loc='lower right')
    # plt.plot([0,1],[0,1],'r--')
    # plt.xlim([-0.001, 1])
    # plt.ylim([0, 1.001])
    # plt.ylabel('True Positive Rate')
    # plt.xlabel('False Positive Rate')
    # plt.show();

    fpr, tpr, thresholds = roc_curve(error_df.true_class, error_df.reconstruction_error)
    # roc_auc = auc(fpr, tpr)
    # print(thresholds)
    threshold_tmp = thresholds.reshape(thresholds.shape[0],1)
    # print(threshold_tmp)
    print(threshold_tmp.mean(axis=0))

    threshold = 0.00024
    groups = error_df.groupby('true_class')
    fig, ax = plt.subplots()

    for name, group in groups:
        ax.plot(group.index, group.reconstruction_error, marker='o', ms=3.5, linestyle='',
                label= "Extreme" if name == 1 else "Normal")
    ax.hlines(threshold, ax.get_xlim()[0], ax.get_xlim()[1], colors="r", zorder=100, label='Threshold')
    ax.legend()
    plt.title("Reconstruction error for different classes")
    plt.ylabel("Reconstruction error")
    plt.xlabel("Data point index")
    plt.show();

    y_pred = [1 if e > threshold else 0 for e in error_df.reconstruction_error.values]
    conf_matrix = confusion_matrix(error_df.true_class, y_pred)
    print(conf_matrix)

    print('recall: {}'.format(recall_score(error_df.true_class, y_pred, average='macro')))
    print('precision: {}'.format(precision_score(error_df.true_class, y_pred, average='macro')))
    print('accuracy: {} \n'.format(accuracy_score(error_df.true_class, y_pred)))

    precision, recall, fscore, support = score(error_df.true_class, y_pred)

    print('precision: {}'.format(precision))
    print('recall: {}'.format(recall))
    print('fscore: {}'.format(fscore))
    print('support: {}'.format(support))

    # plt.figure(figsize=(12, 12))
    # sns.heatmap(conf_matrix, xticklabels=LABELS, yticklabels=LABELS, annot=True, fmt="d");
    # plt.title("Confusion matrix")
    # plt.ylabel('True class')
    # plt.xlabel('Predicted class')
    # plt.show()

def create_classifier_model():
	# create model
	model = Sequential()
	model.add(Dense(60, input_dim=60, kernel_initializer='normal', activation='relu'))
	model.add(Dense(30, kernel_initializer='normal', activation='relu'))
	# model.add(Dense(150, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

def train_classifier(X, encoded_Y):
    estimators = []
    estimators.append(('standardize', StandardScaler()))
    estimators.append(('mlp', KerasClassifier(build_fn=create_classifier_model, epochs=1000, batch_size=10, verbose=0)))
    # estimators.append(('mlp', KerasClassifier(build_fn=create_classifier_model(X.shape[1]), epochs=100, batch_size=5, verbose=0)))
    pipeline = Pipeline(estimators)
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)
    results = cross_val_score(pipeline, X, encoded_Y, n_jobs=-1, cv=kfold)
    print("Larger: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

# 1 -- Extreme Adopters
# 0 -- Normal Users
def init(train=True, test=True, classifier=True):
    df = read_csv(prop.sonar_fv_filepath, header=None)
    dataset = df.values
    # split into input (X) and output (Y) variables
    X_train = dataset[:,0:60].astype(float)
    Y = dataset[:,60]

    # X_train, X_test = train_test_split(df, test_size=0.2, random_state=123)
    # print(X_train.shape)
    # print(X_test.shape)

    # X_train = X_train[X_train.Class == 0]
    # X_train = X_train.drop(['Class'], axis=1)
    # Y = df['Class'].values
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    #
    # X_train = df.drop(['Class'], axis=1)

    # if train:
    #     train_model(X_train, X_test)
    # if test:
    #     test_model(X_test)
    if classifier:
        train_classifier(X_train, encoded_Y)