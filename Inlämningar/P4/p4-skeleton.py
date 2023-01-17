# TDP015 Programming Assignment 4
# Image Classification
# Skeleton Code

import math
import mnist
import png
import random

# ## Introduction
#
# In this assignment you will implement a probabilistic classifier for
# handwritten digit recognition: a system that takes an image of a
# digit as its input, and predicts the digit depicted in it.
#
# To train and evaluate your system, you will use the 70,000 images in
# the MNIST Database of Handwritten Digits:
#
# https://en.wikipedia.org/wiki/MNIST_database
#
# Each image in this database consists of 28x28 pixels with grayscale
# values, and has been manually labelled with the digit depicted in
# the image. For the purposes of this assignment, the grayscale values
# have been converted to black-or-white values.

# ## Problem 0
#
# Write code that reads the training data for the assignment, picks
# out 10 random images, one for each digit, and writes the images to
# disk as PNG files.
#
# Use the following code pattern to loop over the training data:
#
# for image, digit in mnist.read_training_data():
#     ...
#
# On the Python side of things, an image is represented as a tuple
# with 784 components: each component corresponds to a pixel, and has
# a value of either 1 or 0 ("black" or "white").
#
# To save images as PNG files, use `png.save_png()`. This function
# takes four arguments: (1) the width of the image to be generated,
# (2) its height, (3) a list with the grayscale values of the image
# (integers between 0 and 255), and (4) the name of the file to which
# the image should be written. Call the function like this:
#
# png.save_png(28, 28, values, 'digit-{}.png'.format(digit))


def make_images():
    """Generates PNG files from random digits in the training data."""
    # TODO: Replace the following line with your own code.
    
    values = []
    saved = []
    r = random.randint(1, 70000)
    data = mnist.read_training_data()

    for x in range(r):
        next(data)

    for image, digit in data:
        if digit in saved:
            continue
        else:
            for i in image:
                if i == 0:
                    values.append(255)
                else:
                    values.append(0)
            saved.append(digit)
            png.save_png(28, 28, values, 'digit-{}.png'.format(digit))
            values.clear()



# ## Problem 1
#
# The first problem that you have to solve is to estimate the two
# types of probabilities required by the classifier:
#
# 1. For each possible digit d, the a priori probability that an image
# represents d, rather than any other digit. You should estimate this
# probability as the percentage of images in the training data that
# have been labelled with d.
#
# To store probabilities of type 1, use a dictionary `pd` that maps
# digits (integers) to probabilities (floats). For example, `pd[7]`
# should give the probability that a random image depicts the digit 7.
#
# 2. For each possible digit d and each possible pixel p (indexed by
# an integer between 0 and 783), the conditional probability that p is
# black given that the image represents d. You should estimate this
# probability as the percentage of d-images in the training data in
# which pixel p is black.
#
# To store probabilities of type 2, use a two-layer dictionary
# `pp`. For example, `pp[7][42]` should give the conditional
# probability that pixel 42 is black in a random image of the digit 7.
#
# Implementation detail: To avoid zero probabilities, pretend that
# each pixel is black in one additional d-image. For example, if pixel
# 0 is never black in images of the digit 7, pretend that it is
# actually black in 1 image; and if pixel 391 is black in 130 images
# of the digit 7, pretend that it is actually black in 131 images.
#
# The following numbers may be useful for debugging:
#
# * Number of images depicting the digit 7: 6265
# * Number of black pixels in images depiciting the digit 7: 568207
# * The same number, but including "hallucinated" pixels: 568991


def train(data):
    """Estimate the probabilities of the classifier from data.

    Args:
        data: An iterable yielding image–label pairs.

    Returns:
        A pair of two dictionaries `pd`, `pp`, as decribed above.
    """
    pd = {d: 0 for d in range(10)}
    pp = {d: {p: 1 for p in range(784)} for d in range(10)}
    # TODO: Replace the following line with your own code

    count = 0
    for src in data:
        pd[src[1]] += 1
        for px in src[0]:
            if px == 1:
                pp[src[1]][count] += 1
            count += 1
            if count == 784:
                count = 0

    tot = sum(pd.values())
    for key, val in pd.items():
        pd[key] = val / tot * 100

    a = 0
    for i, j in pp.items():
        summ = sum(pp[a].values())
        print(summ)
        for key, value in j.items():
            j[key] = value / summ * 100
        a += 1
    return pd, pp


# ## Problem 2
#
# Once you have estimated the relevant probabilities, you can use them
# to predict the digit that a given image represents. Implement the
# following algorithm: For each possible digit d, compute a "score",
# defined as the product of the a priori probability that the image
# represents d (from the `pd` dictionary) and, for each black pixel p
# in the image, the conditional probability that p is black given that
# the image represents d (from the `pp` dictionary). Then, return that
# digit which got the highest score.
#
# Implementation detail: Probabilities are small numbers, and when
# many small numbers are multiplied, there is a risk for underflow. To
# avoid this, convert evaluated numbers to logarithmic scale (using
# `math.log`) and add probabilities instead of multiplying them.


def predict(model, image):
    """Predict the digit depicted by an image.

    Args:
        model: A pair of two dictionaries `pd`, `pp`, as decribed above.
        image: A tuple representing an image.

    Returns:
        The digit depicted by the image.
    """
    # TODO: Replace the following line with your own code

    value = {a: 0 for a in range(10)}
    pd = model[0]
    pp = model[1]
    for i, j in pd.items():
        value[i] = math.log(pd[i])
    pr = image[0]
    n = image[1]

    pix = 0
    value_a = 0
    for numb in pp:
        for px in pr:
            if px == 1:
                value[value_a] += math.log(pp[value_a][pix])
            pix += 1
            if pix == 784:
                pix = 0
        value_a += 1
    val = max(list(value.values()))
    for k, v in value.items():
        if v == val:
            return [k, n]
    return

# ## Problem 3
#
# The last step is to assess the accuracy of your classifier on the
# test portion of the MNIST database. Here, accuracy is defined as the
# percentage of correctly classified images, that is, the percentage
# of images for which your system predicts the same digit that is
# specified in the test data.
#
# The classification accuracy should be above 80%.


def evaluate(model, data):
    """Evaluate the classifier on test data.

    Args:
        model: A pair of two dictionaries `pd`, `pp`, as decribed above.
        data: An iterable yielding image–label pairs.

    Returns:
        The accuracy of the classifier on the specified data.
    """
    # TODO: Replace the following line with your own code

    accurate = 0
    evaluated = 0

    for image in data:
        evaluated += 1
        check = predict(model, image)
        if check[0] == check[1]:
            accurate += 1
    print(evaluated)
    print(accurate)
    return str(accurate/evaluated * 100)

if __name__ == '__main__':
    print("Generating image files ...")
    make_images()
    print("Estimating the probabilities ...")
    model = train(mnist.read_training_data())
    print("Evaluating the classifier ...")
    print("Accuracy:", evaluate(model, mnist.read_test_data()))
