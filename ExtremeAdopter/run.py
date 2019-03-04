import main.auto_encoder as app
import main.cross_validation as cross_app
import utilities.utilities as util
import time

train=False
test=False
classifier=True
n_folds = 10

# app.init(train=train, test=test, classifier=classifier)
start_time = time.time()

util.write_post_in_json()

# cross_app.init(n_folds=n_folds)

print("Elapsed time in %s seconds: " % round(time.time() - start_time, 4) )