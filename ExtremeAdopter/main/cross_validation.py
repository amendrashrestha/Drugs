from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, roc_curve, auc, recall_score, classification_report, precision_score, accuracy_score
from sklearn.metrics import precision_recall_fscore_support as score

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import ModelCheckpoint, EarlyStopping

from pandas import read_csv
import numpy as np

import utilities.IOProperties as prop
import utilities.utilities as util

def load_data():
    # load your data using this function
    df = read_csv(prop.fv_filepath)
    # dataset = df.values
    # # split into input (X) and output (Y) variables
    # X_train = dataset[:,0:60].astype(float)
    # Y = dataset[:,60]
    Y = df['Class'].values
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)

    X_train = df.drop(['Class'], axis=1)

    return X_train.values, encoded_Y

def create_model(dim):
    next_units = round(dim / 2)
    second_last_units = round(next_units / 2)
    last_units = round(second_last_units / 2)
    # create your model using this function
    model = Sequential()
    model.add(Dense(dim, input_dim=dim, kernel_initializer='uniform', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(next_units, kernel_initializer='uniform', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(second_last_units, kernel_initializer='uniform', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(last_units, kernel_initializer='uniform', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))

    # Compile model
    # opt_adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    # model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    model.compile(loss=util.abs_KL_div, optimizer='adam', metrics=['accuracy'])
    return model

def train_and_evaluate_model(model, X_train, Y_train, X_test, Y_test):
    # checkpoint = ModelCheckpoint(prop.model_filepath, monitor='val_loss', verbose=0, save_best_only=True)
    # earlyStopping = EarlyStopping(monitor='val_loss', patience=20, verbose=0)
    # callbacks_list = [checkpoint,earlyStopping]

    model.fit(X_train, Y_train, epochs=500, batch_size = 32, verbose=0, shuffle = True)
    pred = model.predict_classes(X_test)
    #
    # unique, counts = np.unique(Y_test, return_counts=True)
    # print(unique, counts)

    # conf_matrix = confusion_matrix(Y_test, pred)
    # print(conf_matrix)

    recall = recall_score(Y_test, pred, average='macro')
    precision = precision_score(Y_test, pred, average='macro')
    accuracy = accuracy_score(Y_test, pred)

    return recall, precision, accuracy
    # print('recall: {}'.format(recall))
    # print('precision: {}'.format(precision))
    # print('accuracy: {} \n'.format(accuracy))

def init(n_folds=None):
    seed = 7
    np.random.seed(seed)

    idx = 0
    eval_matrix = np.zeros(shape=(n_folds,3))

    data, labels = load_data()
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)

    for train, test in skf.split(data, labels):
        model = None # Clearing the NN.

        model = create_model(data[train].shape[1])
        recall, precision, accuracy = train_and_evaluate_model(model, data[train], labels[train], data[test], labels[test])

        eval_matrix[idx][0] = recall
        eval_matrix[idx][1] = precision
        eval_matrix[idx][2] = accuracy
        idx += 1

    print(eval_matrix.mean(axis=0))