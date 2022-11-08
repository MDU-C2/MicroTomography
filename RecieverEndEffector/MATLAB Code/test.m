clear all;
clc;

while (1)
    tic
    system('python communicate.py 10.132.158.239 1884 10.132.158.190 1000');
    toc
end