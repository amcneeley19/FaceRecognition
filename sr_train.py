from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import math
import numpy as np
from sr_model import  SRGAN
from keras.layers import Input
from PIL import Image
from skimage.transform import resize

def show_img(img, img2, t1, t2):
    fig, arr = plt.subplots(1, 2, figsize=(15, 15))
    arr[0].imshow(img)
    arr[0].set_title(t1)
    arr[1].imshow(img2)
    arr[1].set_title(t2)
    plt.show()


if __name__ == "__main__":
    lfw_people = fetch_lfw_people(data_home="./data", resize=None,min_faces_per_person=70, color=True,slice_=None, funneled=False)
    # print(lfw_people.DESCR)


    print(lfw_people.images[0].shape)
    print(lfw_people.target[0])
    # plots images

    #show_img(lfw_people.images[0], lfw_people.images[1], lfw_people.target_names[0], lfw_people.target_names[1])
    target_shape_hr_img = [128, 128, 3]
    target_shape_lr_img = [25, 25, 3]

    X_train, X_test, y_train, y_test = train_test_split(lfw_people.images, lfw_people.target, test_size=0.25,
                                                        random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.10, random_state=42)
    X_test_lr = resize(X_test, (X_test.shape[0], 25, 25, 3))
    X_test_hr = resize(X_test, (X_test.shape[0], 225,225,3))
    X_train_lr = resize(X_train, (X_train.shape[0], 25,25,3))
    X_train_hr = resize(X_train, (X_train.shape[0], 225,225,3))

    model = SRGAN()
    model.train(X_train_lr,X_train_hr,X_test_lr,X_test_hr)

    #i_h, i_w, i_c = target_shape_hr_img
    #i_h_lr, i_w_lr, i_c_lr = target_shape_lr_img

    # m = len(lfw_people.images)  # number of images
    # y = np.zeros((m, i_h, i_w, i_c), dtype=np.float32)
    # X = np.zeros((m, i_h_lr, i_w_lr, i_c_lr), dtype=np.float32)
    # for i in range(len(lfw_people.images)):
    #     single_img = Image.fromarray((lfw_people.images[i] * 255).astype(np.uint8)).convert('RGB')
    #     single_img = single_img.resize((i_h_lr, i_w_lr))
    #     single_img = np.reshape(single_img, (i_h_lr, i_w_lr, i_c_lr))
    #     single_img = single_img.astype(float)
    #     X[i] = single_img / 255.0
    # for j in range(len(lfw_people.images)):
    #     single_img = Image.fromarray((lfw_people.images[j] * 255).astype(np.uint8)).convert('RGB')
    #     single_img = single_img.resize((i_h, i_w))
    #     single_img = np.reshape(single_img, (i_h, i_w, i_c))
    #     single_img = single_img.astype(float)
    #     y[j] = single_img / 255.0

    #show_img(X[0], y[0], lfw_people.target_names[0], lfw_people.target_names[0])

    #lr_ip = Input(shape=(25,25,3))
    #hr_ip = Input(shape=(128,128,3))
    # train_lr, test_lr, train_hr, test_hr = train_test_split(X, y, test_size=0.2, random_state=123)#training images arrays normalized between 0 & 1

    #gan_model = GAN()

    #gan_model.train(x_train_lr=X_train_lr, y_train_hr=X_train_hr)
    # generator = create_gen((100,))
    # discriminator = create_disc(hr_ip)
    # discriminator.compile(loss="binary_crossentropy", optimizer="adam",
    #   metrics=['accuracy'])
    # vgg = build_vgg()
    # vgg.trainable = False
    # gan_model = create_comb(generator, discriminator, vgg, lr_ip, hr_ip)
    # gan_model.compile(loss=["binary_crossentropy","mse"], loss_weights=
    #   [1e-3, 1], optimizer="adam")
    # batch_size = 20
    # train_lr_batches = []
    # train_hr_batches = []
    # for it in range(int(X_train_hr.shape[0] / batch_size)):
    #     start_idx = it * batch_size
    #     end_idx = start_idx + batch_size
    #     train_hr_batches.append(X_train_hr[start_idx:end_idx])
    #     train_lr_batches.append(X_train_hr[start_idx:end_idx])
    # train_lr_batches = np.array(train_lr_batches)
    # train_hr_batches = np.array(train_hr_batches)
    #
    # epochs = 100
    # for e in range(epochs):
    #     gen_label = np.zeros((batch_size, 1))
    #     real_label = np.ones((batch_size, 1))
    #     g_losses = []
    #     d_losses = []
    #     for b in range(len(train_hr_batches)):
    #         lr_imgs = train_lr_batches[b]
    #         hr_imgs = train_hr_batches[b]
    #         gen_imgs = generator.predict_on_batch(lr_imgs)
    #         # Dont forget to make the discriminator trainable
    #         discriminator.trainable = True
    #
    #         # Train the discriminator
    #         d_loss_gen = discriminator.train_on_batch(gen_imgs,
    #                                                   gen_label)
    #         d_loss_real = discriminator.train_on_batch(hr_imgs,
    #                                                    real_label)
    #         discriminator.trainable = False
    #         d_loss = 0.5 * np.add(d_loss_gen, d_loss_real)
    #         image_features = vgg.predict(hr_imgs)
    #
    #         # Train the generator
    #         g_loss, _, _ = gan_model.train_on_batch([lr_imgs, hr_imgs],
    #                                                 [real_label, image_features])
    #
    #         d_losses.append(d_loss)
    #         g_losses.append(g_loss)
    #     g_losses = np.array(g_losses)
    #     d_losses = np.array(d_losses)
    #
    #     g_loss = np.sum(g_losses, axis=0) / len(g_losses)
    #     d_loss = np.sum(d_losses, axis=0) / len(d_losses)
    #     print("epoch:", e + 1, "g_loss:", g_loss, "d_loss:", d_loss)
    #
    #     label = np.ones((len(X_test_lr), 1))
    #     test_features = vgg.predict(X_test_hr)
    #     eval, _, _ = gan_model.evaluate([X_test_lr, X_test_hr], [label, test_features])
