# Octave tips

## Install

Refer https://www.gnu.org/software/octave/.

- Ubuntu: `apt-get install octave gnuplot`
- Max OSX: `brew tap homebrew/science && brew update && brew upgrade && brew install octave`

## Basic operations

Normal Equation: `theta = inv(X'*X)*X'*y`

What if X'X is non-invertible? `theta = pinv(X'*X)*X'*y`

```
PS1('>> ');

>> a=pi;
>> disp(a);
 3.1416
>> disp(sprintf('2 decimals: %0.2f', a))
2 decimals: 3.14

>> A=[1 2;3 4; 5 6];
>> v=[1 2 3];
>> s=[1;2;3];

>> v=1:0.1:2
v =

    1.0000    1.1000    1.2000    1.3000    1.4000    1.5000    1.6000    1.7000    1.8000    1.9000    2.0000


>> ones(2,3)
ans =

   1   1   1
   1   1   1

zeros(1,3)
rand(3,3)   % Return a matrix with random elements uniformly distributed on the interval (0, 1)
randn(3,3)  % Return a matrix with normally distributed pseudo-random elements having zero mean and variance one

>> eye(4)
ans =

Diagonal Matrix

   1   0   0   0
   0   1   0   0
   0   0   1   0
   0   0   0   1


w = -6 + sqrt(10)*randn(1,10000);
hist(w)
hist(w, 50)

help eye
help rand

>> A=eye(3);
>> sz=size(A)
sz =

   3   3


>> load data.dat  % load data from file
>> data
data =

   3232      3
   2322      4
    212      3
    232      5
   2342      3

>> who
Variables in the current scope:

A     ans   data  sz
>> whos
Variables in the current scope:

  Attr Name        Size                     Bytes  Class
  ==== ====        ====                     =====  =====
       A           3x3                         24  double
       ans         1x5                          5  char
       data        5x2                         80  double
       sz          1x2                         16  double

Total is 26 elements using 125 bytes

>> save hello.dat data; % save data to file

>> clear % clear all vars

>> data
data =

   3232      3
   2322      4
    212      3
    232      5
   2342      3

>> data(1,1)
ans =  3232
>> data([1,3],:)    % get first line and third line data
ans =

   3232      3
    212      3
>> data(:, 2)   % get second column data
ans =

   3
   4
   3
   5
   3
>> data(:)  % put all data in a single vector
ans =

   3232
   2322
    212
    232
   2342
      3
      4
      3
      5
      3

>> A=ones(3,2)
A =

   1   1
   1   1
   1   1

>> B=eye(2)
B =

Diagonal Matrix

   1   0
   0   1

>> A*B
ans =

   1   1
   1   1
   1   1

>> C=rand(3,2)
C =

   0.24450   0.46890
   0.60861   0.15189
   0.12748   0.86532

>> A.*C
ans =

   0.24450   0.46890
   0.60861   0.15189
   0.12748   0.86532

>> A.^2
ans =

   1   1
   1   1
   1   1

>> v=[1;2;3]
v =

   1
   2
   3

>> exp(v)
ans =

    2.7183
    7.3891
   20.0855

>> 1./v
ans =

   1.00000
   0.50000
   0.33333

>> v+1
ans =

   2
   3
   4

C =

   0.24450   0.46890
   0.60861   0.15189
   0.12748   0.86532

>> C'
ans =

   0.24450   0.60861   0.12748
   0.46890   0.15189   0.86532


octave:5> A
A =

   1   2
   3   4
   2   3

octave:6> B
B =

    2    2    3
    3    2   90

octave:7> A*B
ans =

     8     6   183
    18    14   369
    13    10   276

>> max(v)
ans =  3

>> max(A)
ans =

   3   4

>> A=magic(3)
A =

   8   1   6
   3   5   7
   4   9   2


>> [r,c]=find(A<3)
r =

   1
   3

c =

   2
   3


A =

   8   1   6
   3   5   7
   4   9   2

>> max(A)
ans =

   8   9   7

>> max(A, [], 1) % max of each column
ans =

   8   9   7

>> max(A, [], 2) % max of each row
ans =

   8
   7
   9


>> A=magic(9)
A =

   47   58   69   80    1   12   23   34   45
   57   68   79    9   11   22   33   44   46
   67   78    8   10   21   32   43   54   56
   77    7   18   20   31   42   53   55   66
    6   17   19   30   41   52   63   65   76
   16   27   29   40   51   62   64   75    5
   26   28   39   50   61   72   74    4   15
   36   38   49   60   71   73    3   14   25
   37   48   59   70   81    2   13   24   35

>> sum(A,1)
ans =

   369   369   369   369   369   369   369   369   369

>> sum(A)
ans =

   369   369   369   369   369   369   369   369   369

>> sum(A,2)
ans =

   369
   369
   369
   369
   369
   369
   369
   369
   369

>> sum(sum(A))
ans =  3321


>> flipud(eye(3))
ans =

Permutation Matrix

   0   0   1
   0   1   0
   1   0   0


>> A=magic(3)
A =

   8   1   6
   3   5   7
   4   9   2

>> inv(A)
ans =

   0.147222  -0.144444   0.063889
  -0.061111   0.022222   0.105556
  -0.019444   0.188889  -0.102778

>> pinv(A)
ans =

   0.147222  -0.144444   0.063889
  -0.061111   0.022222   0.105556
  -0.019444   0.188889  -0.102778

>> A*inv(A)
ans =

   1.0000e+00   7.6328e-17  -4.1633e-17
  -2.7756e-17   1.0000e+00   6.9389e-17
   2.0817e-17   2.0817e-17   1.0000e+00

>> v=zeros(10,1);
>> for i=1:10,
>     v(i)=2^i;
> end
>> v
v =

      2
      4
      8
     16
     32
     64
    128
    256
    512
   1024


>> i=1;
>> while i<=5
> v(i)=100;
> i=i+1;
> end
>> v
v =

    100
    100
    100
    100
    100
     64
    128
    256
    512
   1024

>> clc
>> v=1:20;
>> if v(1)==1
>     disp('v(1)==1')
> else
>     disp('false')
> end
v(1)==1

% function definition
% # cat sq.m
function y=sq(x)
y=x*x;
```

## Plot

```
>> t=[0:0.01:0.98];
>> y1=sin(2*pi*t);
>> plot(t,y1)
>>
>> y2=cos(2*pi*t);
>> plot(t,y2);
>>
>> plot(t,y1, 'b');hold on;plot(t, y2, 'r')
>>
>> plot(t,y1, 'b');hold on;plot(t, y2, 'r')
>> xlabel('time')
>> ylabel('value')
>> legend('sin', 'sos')
>> title('my plot')
>> print -dpng test.png

>> figure(1); plot(t, y1);
>> figure(2); plot(t, y2);
>> subplot(1,2,1); plot(t, y1);subplot(1,2,2);plot(t, y2);
>> axis([0.5 1 -1 1])
>>
>> A=magic(5)
A =

   17   24    1    8   15
   23    5    7   14   16
    4    6   13   20   22
   10   12   19   21    3
   11   18   25    2    9

>> imagesc(A)
>> figure(3); imagesc(A); colorbar
```
