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
    combo_number = int(sys.argv[-1])
    name_model = sys.argv[1]
    batch_size = 6
    epochs = 100
    print(name_model)
    combo = [
        # (False, True, True, False, 1.0, 1.0, "encode_layer","0001", "_val_2_test_5"),
        # (True, False, True, False, 0, 1.0, "encode_layer","0001", "_val_2_test_5"),
        # (True, False, True, False, 1.0, 0, "encode_layer","0001", "_val_2_test_5"),
        # (True, True, False, False, 1.0, 1.0, "encode_layer","0001", "_val_2_test_5"),
        # (True, True, True, True, 1.0, 1.0, "encode_layer","0001", "_val_2_test_5"),
        # (True, True, True, 1.0, 1.0, "all_layer", "001", "_test_1_4"),
        # (True, True, True, 1.0, 1.0, "encode_layer", "0001", "_test_1_4"),
        # (True, True, True, 1.0, 1.0, "encode_layer", "0001", "_test_2_6"),
        # (True, True, True, 1.0, 1.0, "encode_layer", "0001", "_test_1_4"),
        (True, True, False, 1.0, 1.0, "last_layer", "0001", "_test_3_5"),
        # (True, True, True, 1.0, 1.0, "encode_layer", "0001", "_test_3_5"),
    ]

    aug_bol, lr_bol, flip_bol, el_percentage, rot_percentage, encode_train, loss_weight, training_data = combo[combo_number]
    name_model = f'aug_bol_{aug_bol}_lr_bol_{lr_bol}_flip_bol_{flip_bol}_el_{el_percentage}_rot_{rot_percentage}__encode_{encode_train}_loss_start_{loss_weight}_training_{training_data}_{name_model}'
    print(name_model)
    # change 200 to 100 if not doing double
    training_path = base_path + f"/data/training/training-set{training_data}"
    validation_path = base_path + f"/data/validation/validation-set{training_data}"

    # load data needs to correspond to volumne generator
    x_train, y_train = load_data(training_path, normal = aug_bol)
    x_validation, y_validation = load_data(validation_path, normal = True)


    datagen = VolumeDataGenerator(
        horizontal_flip=flip_bol,
        vertical_flip=flip_bol,
        depth_flip=flip_bol,
        min_max_normalization=True,
        scale_range=0.1,
        scale_constant_range=0.2,
        normal =aug_bol,
        el_precentage = el_percentage,
        rot_precentage = rot_percentage
    )

    datagen_val = VolumeDataGenerator(
        horizontal_flip=False,
        vertical_flip=False,
        depth_flip=False,
        min_max_normalization=True,
        scale_range=0,
        scale_constant_range=0,
        normal = True,
        el_precentage = el_percentage,
        rot_precentage = rot_percentage
    )



    train_generator = datagen.flow(x_train, y_train, batch_size)
    validation_generator =  datagen_val.flow(x_validation, y_validation, batch_size)

    now = datetime.now()
    logdir = base_path + f"/data/tf-logs/{name_model}" +  now.strftime("%B-%d-%Y-%I:%M%p") + "/"

    tboard = TensorBoard(log_dir=logdir, histogram_freq=0, write_graph=True, write_images=False)

    current_checkpoint = ModelCheckpoint(filepath=base_path + f'/data/model-weights/latest_model_{epochs:03d}_{name_model}.hdf5', verbose=1)
    period_checkpoint = ModelCheckpoint(base_path + f'/data/model-weights/weights_{epochs:03d}_{name_model}.hdf5', period=20)
    best_weight_checkpoint = ModelCheckpoint(filepath=base_path + f'/data/model-weights/best_weights_checkpoint_{name_model}.hdf5',
                                             verbose=1, save_best_only=True)

    

    weights_path = base_path + "/data/model-weights/trailmap_model.hdf5"
    print(weights_path)

    model = get_net()
    # This will do transfer learning and start the model off with our current best model.
    # Remove the model.load_weight line below if you want to train from scratch
    model.load_weights(weights_path)
    if lr_bol == False:
        lr_scheduler = ReduceLROnPlateau()
        # use more steps in the epochs
        #https://stackoverflow.com/questions/39779710/setting-up-a-learningratescheduler-in-keras
        model.fit_generator(train_generator,
                            steps_per_epoch=(7*75)//batch_size,
                            epochs=epochs,
                            validation_data=validation_generator,
                            validation_steps= (7*25)//batch_size,
                            use_multiprocessing=False,
                            workers=1,
                            callbacks=[lr_scheduler, tboard, period_checkpoint, best_weight_checkpoint],
                            verbose=1)
        
    else:

        #https://stackoverflow.com/questions/39779710/setting-up-a-learningratescheduler-in-keras
        model.fit_generator(train_generator,
                            steps_per_epoch=(7*75)//batch_size,
                            epochs=epochs,
                            validation_data=validation_generator,
                            validation_steps=(7*25)//batch_size,
                            use_multiprocessing=False,
                            workers=1,
                            callbacks=[tboard, period_checkpoint, best_weight_checkpoint],
                            verbose=1)

    model_name = 'model_' + now.strftime("%B-%d-%Y-%I:%M%p")


    # def write_tiff_stack_paper(vol, fname):
    #     # convert to number rather than decimal and to 8 so can adjust

    #     im = Image.fromarray((vol[0] * 255).astype(np.uint8))
    #     ims = []

    #     for i in range(1, vol.shape[0]):
    #         ims.append(Image.fromarray((vol[i] * 255).astype(np.uint8)))

    #     im.save(fname, save_all=True, append_images=ims)
    

    # for i in range(1):
    #     x2, y2 = next(validation_generator)

    #     write_tiff_stack_paper(
    #         x2[i, :, :, :, 0],
    #         base_path + "/data/look/augment_spatial-input-n" + str(i) + "_test.tiff",
    #     )
    #     write_tiff_stack_paper(
    #         y2[i, :, :, :, 0].astype(float),
    #         base_path + "/data/look/augment_spatial-labeln" + str(i) + "_test.tiff",
    #     )
    #     write_tiff_stack_paper(
    #         np.sum(y2[i, :, :, :, :].astype(float), -1),
    #         base_path
    #         + "/data/look/augment_spatial-label-all-infon"
    #         + str(i)
    #         + "_test.tiff",
    #     )
             
        
    # for i in range(1):
    #     x2, y2 = next(train_generator)

    #     write_tiff_stack_paper(
    #         x2[i, :, :, :, 0],
    #         base_path + "/data/look/augment_spatial-input-n" + str(i) + "_train.tiff",
    #     )
       
    #     write_tiff_stack_paper(
    #         y2[i, :, :, :, 0].astype(float),
    #         base_path + "/data/look/augment_spatial-labeln" + str(i) + "_train.tiff",
    #     )
    #     write_tiff_stack_paper(
    #         np.sum(y2[i, :, :, :, :].astype(float), -1),
    #         base_path
    #         + "/data/look/augment_spatial-label-all-infon"
    #         + str(i)
    #         + "_train.tiff",
    #     )