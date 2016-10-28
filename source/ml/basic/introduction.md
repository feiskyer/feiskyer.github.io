# Machine Learning

## What is machine learning

Machine learning is the subfield of computer science that "gives computers the ability to learn without being explicitly programmed". It's a computer program learning from experience $E$ with respect to some task $T$ and some performance measure $P$, if its performance on $T$ as measured by $P$, improves with $E$ : Tom Mitchell 1998

Machine learning tasks are typically classified into three broad categories:

* Supervised learning: The computer is presented with example inputs and their desired outputs, given by a "teacher", and the goal is to learn a general rule that maps inputs to outputs.
  * Regression - algorithms that predict continuous outputs
  * Categorization - algorithms that predict discrete outputs
* Unsupervised learning: No labels are given to the learning algorithm, leaving it on its own to find structure in its input. Unsupervised learning can be a goal in itself (discovering hidden patterns in data) or a means towards an end (feature learning).
* Reinforcement learning: A computer program interacts with a dynamic environment in which it must perform a certain goal (such as driving a vehicle), without a teacher explicitly telling it whether it has come close to its goal. Another example is learning to play a game by playing against an opponent

There are a lot approaches to achieve machine learning:

* Decision tree learning
* Association rule learning
* Artificial neural networks
* Deep Learning
* Inductive logic programming
* Support vector machines
* Clustering
* Bayesian networks
* Reinforcement learning
* Representation learning
* Similarity and metric learning
* Sparse dictionary learning
* Genetic algorithms
* Rule-based machine learning
* [More](https://en.wikipedia.org/wiki/List_of_machine_learning_concepts)

## A Little Probability

Assume we have a random variable (RV) $X$. In the case where $X$ is a discrete random variable, the probability that $X$ takes some particular value $x$ is $p(X=x)=p\_X(x)$ where $p\_X$ is the *probability distribution function* of the RV $X$. For simplicity, we will usually drop the $X$ subscript when using the probability distribution function, i.e.

$p(x)=p\_X(x)$ and $p(x,y)=p\_{X,Y}(x,y)$.

Now assume we have a second RV, $Y$. The probability that $X$ and $Y$ together take some particular value $(x,y)$ is the *joint probability* $p\_{X,Y}(x,y)=p(X=x, Y=y)$. The
joint probability can be defined in terms of conditional and marginal probabilities as follows:

- **product rule** $p(X,Y) = p\_Y\left(Y|X\right)p\_X\left(X\right) = p(Y,X) = p\_X\left(X|Y\right)p\_Y\left(Y\right)$
- **sum rule** $p(X)=\sum\_Yp\left(X,Y\right)$

where the *conditional probability*, $p\_X(X|Y)$ , is the probability distribution of X given that Y has taken some specific value and $p\_X(x)$ is the *marginal probability*. Note
that the marginal probability is simply the probability distribution of $X$ as described above, but when considered as part of a larger set of RVs, as in $(X,Y)$ in this case, the 
probability distribution of an isolated RV is referred to as the marginal probability. If $X$ and $Y$ are independent events, then 
$p(X,Y)=p(X)p(Y)$. 

If $X$ is a continuous RV, then the probability distribution gives way to a *probability density function*, $p\_X(x)$. What's the difference? In the case of a discrete RV, we think of $p\_X(x)$
as being a finite value in $[0,1]$ representing the probability that $X=x$. In the case of a continuous RV, we can only think of the probability that $X$ is in some range $(a,b)$ defined by


$P(X\in (a,b)) = \int\_a^b p\_X(x)dx$


From this definition, one sees that the $P(X=a)=\int\_a^a p\_X(x)dx = 0$. The *product* rule remains the same rules for continuous RVs, however the *sum* rule becomes: 

**sum rule** $p(X) = \int p\_{X,Y}(x,y) dy = \int p\_X(X|Y=y) p\_Y(y) dy = E\_Y[p(X|Y)]$ 

where $E\_{\Phi}[X]$ is the **expected value** of $X$ under the distribution $\Phi$. Normally, $\Phi$ is the marginal distribution of $X$ so that $E\_X[X] = \int x p\_X(x) dx$ for the RV $X$. 

The following definition of a **compound distribution** will also be useful. Let $t$ be a RV with distribution $F$ paramaterized by $\mathbf{w}$ and let $\mathbf{w}$ be a RV distributed by $G$ 
parameterized by $\mathbf{t}$, then the compound distribution $H$ parameterized by $\mathbf{t}$ for the random variable $t$ is defined by:

$p\_H(t|\mathbf{t}) = \int\_{\mathbf{w}} P\_F(t|\mathbf{w}) P\_G(\mathbf{w}|\mathbf{t})d\mathbf{w}$ 


## Bayesian Modeling

Using the probability rules above, it is possible to obtain the following, known as *Bayes' theorem*, 

$p(Y|X) = \frac{p\left(X|Y\right)p\left(Y\right)}{p\left(X\right)}$


Bayes' theorem will appear repeatadly in the discussion of machine learning.
Not surprisingly, Bayes' theorem plays a fundamental role in Bayesian modelling. Assume, that we model some process where the model has free parameters contained in the vector $\mathbf{w}$. Now assume that we have some notion of the probability distribution of these parameters, $p(\mathbf{w})$, called the *prior*. That is, we assume that **any** set of values from some space (e.g. the real numbers) is a possible best choice for $\mathbf{w}$ with some probability $p(\mathbf{w})$. Finally, assume that we observe a set of data, $\mathbf{D}$, for the output we are attempting to predict with our model. Our objective is to find the *best* set of parameters $\mathbf{w}$ given the observed data. How we choose the *best* set is the challenge and is where Bayesian modeling departs from frequentist modeling. In the Bayesian approach we attempt to maximize the *the probability of the parameters given the data*, $p(\mathbf{w}|D)$, known as the *posterior*. Using Bayes' theorem we can express the *posterior* as 

$p(\mathbf{w}|D) = \frac{p(D|\mathbf{w})p(\mathbf{w})}{p(D)}$ 


In order to apply a fully Bayesian approach, we must formulate models for both the *prior*, $p(\mathbf{w})$, and the *likelihood function*, $p(D|\mathbf{w})$. Given these models and a set of data we can compute appropriate values for our free parameter vector $\mathbf{w}$ by maximizing 
$p(\mathbf{w}|D) \propto p(D|\mathbf{w})p(\mathbf{w})$. How does this differ from frequentist modeling?
The frequentist approach, or *maximum likelihood* approach, ignores the formulation of a *prior*, and goes directly to maximizing the likelihood function to find the model parameters. Thus, the frequentist approach can be described as *maximizing the probability of the data given the parameters*. Under certain conditions the results of Bayesian and frequentist modeling will conincide, but this is not true in general. 

One could obtain a point estimate for $\mathbf{w}$ by maximizing the *posterior probability* model, but this not typical. Instead a *predictive distribution* of the value of the target variable, $t$, is formed based on the compound distribution definition provided above. Taking the mean of this distribution provides a point estimate of $t$ while distribution itself provides a measure of the uncertainty in the estimate, say by considering the standard deviation.

Note: A simple example illustrating the difference can found (here)[http://www.behind-the-enemy-lines.com/2008/01/are-you-bayesian-or-frequentist-or.html].

## Maximum Likelihood

A maximum likelihood approach does not attempt to formulate models for the parameter *priors*, $p(\mathbf{w})$, or the parameter *posterior probabilities*, $p(\mathbf{w}|D)$. Rather it views the data, $D$, as fixed and 
attempts to determine the model parameters, $\mathbf{w}$, by maximizing the likelihood function. As we will frequently use this approach, it is useful to understand the likelihood function. 

We assume we have specified a probability density model, $p\_{\mathbf{w}}(d)$ for the observed data elements, ${d \in D}$ that is parameterized by $\mathbf{w}$, i.e. $p$ is a parametric model for the distribution of $D$. As
an example, if $D$ ahs a normal distribution with mean $\mu$ and variance $\sigma^2$, then 

$\mathbf{w} = (\mu, \sigma^2)$ 

and 

$p\_{\mathbf{w}}(d) = \frac{1}{\sqrt{2 \pi} \sigma} e^{-(d-\mu)^2/2\sigma^2}$ 

The likelihood function, regardless of our choice of model $p$, is defined by 

$L(\mathbf{w}; D) = \prod\_{i=1}^N p\_{\mathbf{w}}(d\_i)$ 

where $N$ is the number of elements in $D$. Thus the likelihood function is simply the product of the probability of all the individual data points, $d\_i \in D$, under the probability model, $p\_{\mathbf{w}}$. Note that this
definition implicitly assumes these data points are independent events. 

Out of mathematical convenience, we will most often work with the *log-likelihood* function (which turns the product into a sum by properties of the log function), i.e. the logarithm of $L(\mathbf{w}; D)$, defined as 

$$l(\mathbf{w};D) = \sum_{i=1}^N l(\mathbf{w};d_i) = \sum_{i=1}^N \log p_{\mathbf{w}}(d_i)$$

where we recall that $\log(ab) = \log(a) + \log(b)$. 

The method of maximum likelihood chooses the value $\mathbf{w} = \widehat{\mathbf{w}}$ that maximizes the *log-likelihood* function. We will also often work with an **error function**, $E(\mathbf{w})$, defined as the
negative of the log-likelihood function 

$$E(\mathbf{w}) = -l(\mathbf{w};D)$$

where we note $-\log(a) = \log(1/a)$.
