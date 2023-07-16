from datetime import datetime
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau
from models.model import get_net
import tensorflow as tf
import os
from training import load_data, VolumeDataGenerator
from models import input_dim
from utilities.utilities import *

if __name__ == "__main__":

    base_path = os.path.abspath(__file__ + "/..")
    normal = sys.argv[1]
    name_model = sys.argv[2]
    batch_size = 6
    epochs = 50
    print(name_model)
    print(normal)

    # change 200 to 100 if not doing double
    training_path = base_path + f"/data/training/training-set_normal_{normal}_100"
    validation_path = base_path + f"/data/validation/validation-set_normal_True_100"

    # load data needs to correspond to volumne generator
    x_train, y_train = load_data(training_path, normal = normal)
    x_validation, y_validation = load_data(validation_path, normal = True)


    datagen = VolumeDataGenerator(
        horizontal_flip=True,
        vertical_flip=True,
        depth_flip=True,
        min_max_normalization=True,
        scale_range=0.1,
        scale_constant_range=0.2,
        normal =normal
    )

    datagen_val = VolumeDataGenerator(
        horizontal_flip=False,
        vertical_flip=False,
        depth_flip=False,
        min_max_normalization=True,
        scale_range=0,
        scale_constant_range=0,
        normal = True
    )



    train_generator = datagen.flow(x_train, y_train, batch_size)
    validation_generator =  datagen_val.flow(x_validation, y_validation, batch_size)

    now = datetime.now()
    logdir = base_path + f"/data/tf-logs/{name_model}_normal_{normal}" +  now.strftime("%B-%d-%Y-%I:%M%p") + "/"

    tboard = TensorBoard(log_dir=logdir, histogram_freq=0, write_graph=True, write_images=False)

    current_checkpoint = ModelCheckpoint(filepath=base_path + f'/data/model-weights/latest_model_{epochs:03d}_{name_model}_normal_{normal}.hdf5', verbose=1)
    period_checkpoint = ModelCheckpoint(base_path + f'/data/model-weights/weights_{epochs:03d}_{name_model}_normal_{normal}.hdf5', period=20)
    best_weight_checkpoint = ModelCheckpoint(filepath=base_path + f'/data/model-weights/best_weights_checkpoint_{name_model}_normal_{normal}.hdf5',
                                             verbose=1, save_best_only=True)

    

    weights_path = base_path + "/data/model-weights/trailmap_model.hdf5"
    print(weights_path)

    model = get_net()
    # This will do transfer learning and start the model off with our current best model.
    # Remove the model.load_weight line below if you want to train from scratch
    model.load_weights(weights_path)
    if normal== False:
        lr_scheduler = ReduceLROnPlateau()
        # use more steps in the epochs
        #https://stackoverflow.com/questions/39779710/setting-up-a-learningratescheduler-in-keras
        model.fit_generator(train_generator,
                            steps_per_epoch=400//batch_size,
                            epochs=epochs,
                            validation_data=validation_generator,
                            validation_steps=100//batch_size,
                            use_multiprocessing=False,
                            workers=1,
                            callbacks=[lr_scheduler, tboard, period_checkpoint, best_weight_checkpoint],
                            verbose=1)
        
    else:

        #https://stackoverflow.com/questions/39779710/setting-up-a-learningratescheduler-in-keras
        model.fit_generator(train_generator,
                            steps_per_epoch=400//batch_size,
                            epochs=epochs,
                            validation_data=validation_generator,
                            validation_steps=100//batch_size,
                            use_multiprocessing=False,
                            workers=1,
                            callbacks=[tboard, period_checkpoint, best_weight_checkpoint],
                            verbose=1)

    model_name = 'model_' + now.strftime("%B-%d-%Y-%I:%M%p")
