# Logistic regression in GraphLab

```python
#!/usr/bin/env python
# Download data from https://s3.amazonaws.com/static.dato.com/files/coursera/course-3/amazon_baby.gl.zip
#
# The goal of this first notebook is to explore logistic regression and feature engineering with
# existing GraphLab functions.
#
# In this notebook you will use product review data from Amazon.com to predict whether the sentiments
# about a product (from its reviews) are positive or negative.
#
# * Use SFrames to do some feature engineering
# * Train a logistic regression model to predict the sentiment of product reviews.
# * Inspect the weights (coefficients) of a trained logistic regression model.
# * Make a prediction (both class and probability) of sentiment for a new product review.
# * Given the logistic regression weights, predictors and ground truth labels, write a function to compute the
#   **accuracy** of the model.
# * Inspect the coefficients of the logistic regression model and interpret their meanings.
# * Compare multiple logistic regression models.
from __future__ import division
import graphlab
import math
import string

products = graphlab.SFrame('amazon_baby.gl/')
print "Products: ", products
print "Proudct[269]: ", products[269]

# Now, we will perform 2 simple data transformations:
#
# 1. Remove punctuation using [Python's built-in](https://docs.python.org/2/library/string.html) string functionality.
# 2. Transform the reviews into word-counts.
#
# **Aside**. In this notebook, we remove all punctuations for the sake of simplicity. A smarter
# approach to punctuations would preserve phrases such as "I'd", "would've", "hadn't" and so
# forth. See [this page](https://www.cis.upenn.edu/~treebank/tokenization.html) for an example
#  of smart handling of punctuations.

def remove_punctuation(text):
    import string
    return text.translate(None, string.punctuation)

review_without_puctuation = products['review'].apply(remove_punctuation)
products['word_count'] = graphlab.text_analytics.count_words(
    review_without_puctuation)
print products[269]['word_count']

# We will **ignore** all reviews with *rating = 3*, since they tend to
# have a neutral sentiment.
products = products[products['rating'] != 3]
print "Length of products: ", len(products)

# Now, we will assign reviews with a rating of 4 or higher to be
# *positive* reviews, while the ones with rating of 2 or lower are
# *negative*. For the sentiment column, we use +1 for the positive class
# label and -1 for the negative class label.
products['sentiment'] = products['rating'].apply(
    lambda rating: +1 if rating > 3 else -1)

# Let's perform a train/test split with 80% of the data in the training
# set and 20% of the data in the test set. We use `seed=1` so that
# everyone gets the same result.
train_data, test_data = products.random_split(.8, seed=1)

# Train a sentiment classifier with logistic regression
#
# **Aside**. You may get an warning to the effect of "Terminated
# due to numerical difficulties --- this model may not be ideal".
# It means that the quality metric (to be covered in Module 3)
# failed to improve in the last iteration of the run. The
# difficulty arises as the sentiment model puts too much weight
# on extremely rare words. A way to rectify this is to apply
# regularization, to be covered in Module 4. Regularization lessens the
# effect of extremely rare words. For the purpose of this assignment,
# however, please proceed with the model above.
sentiment_model = graphlab.logistic_classifier.create(train_data,
                                                      target='sentiment',
                                                      features=['word_count'],
                                                      validation_set=None)

# extract the weights (coefficients)
weights = sentiment_model.coefficients
print weights.column_names()
num_positive_weights = (weights['value'] >= 0).sum()
num_negative_weights = (weights['value'] < 0).sum()
print "Number of positive weights: %s " % num_positive_weights
print "Number of negative weights: %s " % num_negative_weights

# Making predictions with logistic regression
sample_test_data = test_data[10:13]
scores = sentiment_model.predict(sample_test_data, output_type='margin')
print "Class predictions according to GraphLab Create:"
print sentiment_model.predict(sample_test_data)
print sentiment_model.predict(sample_test_data, output_type='probability')
```
