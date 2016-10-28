# Numpy

[NumPy](https://www.dataquest.io/blog/numpy-tutorial-python/) is a commonly used Python data analysis package. By using NumPy, you can speed up your workflow, and interface with other packages in the Python ecosystem, like scikit-learn, that use NumPy under the hood. NumPy was originally developed in the mid 2000s, and arose from an even older package called Numeric. This longevity means that almost every data analysis or machine learning package for Python leverages NumPy in some way.

## Download Wine Quality Data Set


```python
import requests

# download Wine Quality Data Set.
r = requests.get("http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv", stream=True)
if r.status_code == 200:
    with open("winequality-red.csv", 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
```

## Read dataset


```python
import pandas as pd

wines = pd.read_csv("winequality-red.csv", ';')
print wines.shape
wines.head()
```

    (1599, 12)





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fixed acidity</th>
      <th>volatile acidity</th>
      <th>citric acid</th>
      <th>residual sugar</th>
      <th>chlorides</th>
      <th>free sulfur dioxide</th>
      <th>total sulfur dioxide</th>
      <th>density</th>
      <th>pH</th>
      <th>sulphates</th>
      <th>alcohol</th>
      <th>quality</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7.4</td>
      <td>0.70</td>
      <td>0.00</td>
      <td>1.9</td>
      <td>0.076</td>
      <td>11.0</td>
      <td>34.0</td>
      <td>0.9978</td>
      <td>3.51</td>
      <td>0.56</td>
      <td>9.4</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7.8</td>
      <td>0.88</td>
      <td>0.00</td>
      <td>2.6</td>
      <td>0.098</td>
      <td>25.0</td>
      <td>67.0</td>
      <td>0.9968</td>
      <td>3.20</td>
      <td>0.68</td>
      <td>9.8</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7.8</td>
      <td>0.76</td>
      <td>0.04</td>
      <td>2.3</td>
      <td>0.092</td>
      <td>15.0</td>
      <td>54.0</td>
      <td>0.9970</td>
      <td>3.26</td>
      <td>0.65</td>
      <td>9.8</td>
      <td>5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>11.2</td>
      <td>0.28</td>
      <td>0.56</td>
      <td>1.9</td>
      <td>0.075</td>
      <td>17.0</td>
      <td>60.0</td>
      <td>0.9980</td>
      <td>3.16</td>
      <td>0.58</td>
      <td>9.8</td>
      <td>6</td>
    </tr>
    <tr>
      <th>4</th>
      <td>7.4</td>
      <td>0.70</td>
      <td>0.00</td>
      <td>1.9</td>
      <td>0.076</td>
      <td>11.0</td>
      <td>34.0</td>
      <td>0.9978</td>
      <td>3.51</td>
      <td>0.56</td>
      <td>9.4</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>




```python
import csv
with open("winequality-red.csv", 'r') as f:
    wines = list(csv.reader(f, delimiter=";"))

# skip header
wines = np.array(wines[1:], dtype=np.float)
wines.shape
```




    (1599, 12)




```python
import numpy as np
wines = np.genfromtxt("winequality-red.csv", delimiter=";", skip_header=1)
wines.shape
```




    (1599, 12)



## Creating A NumPy Array


```python
a = np.zeros((3,4))
print a
```

    [[ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]]



```python
a.reshape(2,6)
```




    array([[ 0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.]])




```python
a.dtype
```




    dtype('float64')




```python
# create a array of random numbers
b = np.random.rand(3,4)
print b.dtype
print b
```

    float64
    [[ 0.47340722  0.26032462  0.93331738  0.34234496]
     [ 0.54765394  0.165398    0.51294266  0.4961539 ]
     [ 0.06106089  0.34025539  0.31058294  0.21797288]]



```python
c = np.linspace(0, 50, 10)
print c
```

    [  0.           5.55555556  11.11111111  16.66666667  22.22222222
      27.77777778  33.33333333  38.88888889  44.44444444  50.        ]



```python
# convert data type
c.astype(int)
```




    array([ 0,  5, 11, 16, 22, 27, 33, 38, 44, 50])



## Array operations


```python
wines[:, 11] + 10
```




    array([ 15.,  15.,  15., ...,  16.,  15.,  16.])




```python
wines[:, 11] += 10
```


```python
wines[:,11] + wines[:,11]
```




    array([ 30.,  30.,  30., ...,  32.,  30.,  32.])




```python
# Let’s say we want to pick a wine that maximizes alcohol 
# content and quality (we want to get drunk, but we’re classy). 
# We’d multiply alcohol by quality, and select the wine with the highest score:
# Note: /, *, -, +, ^ performs element math for same size vectors.
wines[:,10] * wines[:,11]
```




    array([ 141.,  147.,  147., ...,  176.,  153.,  176.])




```python
# Broadcasting

array_one = np.array(
    [
        [1,2],
        [3,4]
    ]
)
array_two = np.array([4,5])

array_one + array_two
```




    array([[5, 7],
           [7, 9]])




```python
# Array methods

wines.sum()
```




    168074.78193999999




```python
# sums over the first axis of the array. 
# This will give us the sum of all the values in every column. 
wines.sum(axis=0)
```




    array([ 13303.1    ,    843.985  ,    433.29   ,   4059.55   ,
              139.859  ,  25384.     ,  74302.     ,   1593.79794,
             5294.47   ,   1052.38   ,  16666.35   ,  25002.     ])




```python
# If we pass in axis=1, we’ll find the sums over 
# the second axis of the array. This will give us the sum of each row:
wines.sum(axis=1)
```




    array([  84.5438 ,  133.0548 ,  109.699  , ...,  110.48174,  115.21547,
            102.49249])



## Matrix 


```python
A = np.matrix('1.0 2.0; 3.0 4.0')
print A
```

    [[ 1.  2.]
     [ 3.  4.]]



```python
# transpose
A.T
```




    matrix([[ 1.,  3.],
            [ 2.,  4.]])




```python
# matrix multiplication
X = np.matrix('5.0 7.0')
A*X.T
```




    matrix([[ 19.],
            [ 43.]])




```python
# matrix inverse
A.I
```




    matrix([[-2. ,  1. ],
            [ 1.5, -0.5]])



## Vector Stacking


```python
x = np.arange(0,10,2)                     # x=([0,2,4,6,8])
y = np.arange(5)                          # y=([0,1,2,3,4])
m = np.vstack([x,y])                      # m=([[0,2,4,6,8],
                                          #     [0,1,2,3,4]])
xy = np.hstack([x,y])                     # xy =([0,2,4,6,8,0,1,2,3,4])
```

## Histograms


```python
import numpy
import pylab
# Build a vector of 10000 normal deviates with variance 0.5^2 and mean 2
mu, sigma = 2, 0.5
v = numpy.random.normal(mu,sigma,10000)
# Plot a normalized histogram with 50 bins
pylab.hist(v, bins=50, normed=1)       # matplotlib version (plot)
pylab.show()
# Compute the histogram with numpy and then plot it
(n, bins) = numpy.histogram(v, bins=50, normed=True)  # NumPy version (no plot)
pylab.plot(.5*(bins[1:]+bins[:-1]), n)
pylab.show()
```


![png](output_31_1.png)



![png](output_31_2.png)



```python

```
