import keras.backend as K
from itertools import product

import json

import model.script as db
import utilities.IOProperties as props

def abs_KL_div(y_true, y_pred):
    y_true = K.clip(y_true, K.epsilon(), None)
    y_pred = K.clip(y_pred, K.epsilon(), None)
    return K.sum( K.abs( (y_true- y_pred) * (K.log(y_true / y_pred))), axis=-1)

def w_categorical_crossentropy(y_true, y_pred, weights):
    nb_cl = len(weights)
    final_mask = K.zeros_like(y_pred[:, 0])
    y_pred_max = K.max(y_pred, axis=1)
    y_pred_max = K.reshape(y_pred_max, (K.shape(y_pred)[0], 1))
    y_pred_max_mat = K.equal(y_pred, y_pred_max)
    for c_p, c_t in product(range(nb_cl), range(nb_cl)):
        final_mask += (weights[c_t, c_p] * y_pred_max_mat[:, c_p] * y_true[:, c_t])
    return K.categorical_crossentropy(y_pred, y_true) * final_mask

def write_post_in_json():
    db.group_concat()
    tbl_normal_user = 'tbl_flashback_posts_user_day'
    tbl_extreme_adopter = 'tbl_extreme_adopters_info'

    # users = db.get_normal_users(tbl_normal_user)
    users = db.get_extreme_users(tbl_extreme_adopter)
    json_info = {}
    json_info_dict = []

    for single_user in users:
        print(single_user)
        json_info['user'] = single_user
        json_info['post'] = db.get_user_post(single_user)
        json_info['label'] = 'EA'

        json_info_dict.append(json_info.copy())

    with open(props.json_post_filepath, 'a', encoding='utf-8') as fp:
        json.dump(json_info_dict, fp, indent=4, ensure_ascii=False)
