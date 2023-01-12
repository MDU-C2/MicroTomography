close all 
clear all 
clc
theta = [0 pi/100 pi/10 pi/5 pi/2 0.7*pi 0.8*pi pi 1.2*pi 1.4*pi  1.7*pi 1.9*pi]
u = 2*cos(theta);
v = 4*sin(theta);
% u = [1,0,-1,0];
% v = [0,1,0,-1];
t = zeros(size(u));
s = u + i.*v;
for j = 2:size(u,2)
    t(j) = t(j-1) + sqrt( (u(j)-u(j-1))^2 + (v(j)-v(j-1))^2 );
end

T = [sum( exp(2*pi*1i*0*t)), sum( exp(2*pi*1i*(-1)*t)), sum( exp(2*pi*1i*(-2)*t)),sum( exp(2*pi*1i*(-3)*t)), sum( exp(2*pi*1i*(-4)*t)), sum( exp(2*pi*1i*(-5)*t)), sum( exp(2*pi*1i*(-6)*t));
    sum( exp(2*pi*1i*1*t)), sum( exp(2*pi*1i*(0)*t)), sum( exp(2*pi*1i*(-1)*t)),sum( exp(2*pi*1i*(-2)*t)), sum( exp(2*pi*1i*(-3)*t)), sum( exp(2*pi*1i*(-4)*t)), sum( exp(2*pi*1i*(-5)*t));
    sum( exp(2*pi*1i*2*t)), sum( exp(2*pi*1i*(1)*t)), sum( exp(2*pi*1i*(0)*t)),sum( exp(2*pi*1i*(-1)*t)), sum( exp(2*pi*1i*(-2)*t)), sum( exp(2*pi*1i*(-3)*t)), sum( exp(2*pi*1i*(-4)*t));
    sum( exp(2*pi*1i*3*t)), sum( exp(2*pi*1i*(2)*t)), sum( exp(2*pi*1i*(1)*t)),sum( exp(2*pi*1i*(0)*t)), sum( exp(2*pi*1i*(-1)*t)), sum( exp(2*pi*1i*(-2)*t)), sum( exp(2*pi*1i*(-3)*t));
    sum( exp(2*pi*1i*4*t)), sum( exp(2*pi*1i*(3)*t)), sum( exp(2*pi*1i*(2)*t)),sum( exp(2*pi*1i*(1)*t)), sum( exp(2*pi*1i*(0)*t)), sum( exp(2*pi*1i*(-1)*t)), sum( exp(2*pi*1i*(-2)*t));
    sum( exp(2*pi*1i*5*t)), sum( exp(2*pi*1i*(4)*t)), sum( exp(2*pi*1i*(3)*t)),sum( exp(2*pi*1i*(2)*t)), sum( exp(2*pi*1i*(1)*t)), sum( exp(2*pi*1i*(0)*t)), sum( exp(2*pi*1i*(-1)*t));
    sum( exp(2*pi*1i*6*t)), sum( exp(2*pi*1i*(5)*t)), sum( exp(2*pi*1i*(4)*t)),sum( exp(2*pi*1i*(3)*t)), sum( exp(2*pi*1i*(2)*t)), sum( exp(2*pi*1i*(1)*t)), sum( exp(2*pi*1i*(0)*t));
    ];

b = [sum(abs(s).*exp(2*pi*1i*(-3)*t));
    sum(abs(s).*exp(2*pi*1i*(-2)*t));
    sum(abs(s).*exp(2*pi*1i*(-1)*t));
    sum(abs(s).*exp(2*pi*1i*(0)*t));
    sum(abs(s).*exp(2*pi*1i*(1)*t));
    sum(abs(s).*exp(2*pi*1i*(2)*t));
    sum(abs(s).*exp(2*pi*1i*(3)*t)) ];


x = cgs(T,b)
new_t = linspace(0,2*pi,50)

P = x(1)*exp(2*pi*1i*(-3)*new_t) + x(2)*exp(2*pi*1i*(-2)*new_t) + x(3)*exp(2*pi*1i*(-1)*new_t)+ x(4)*exp(2*pi*1i*(0)*new_t)
+ x(5)*exp(2*pi*1i*(1)*new_t)+ x(6)*exp(2*pi*1i*(2)*new_t)+ x(7)*exp(2*pi*1i*(3)*new_t)
s
T*x
b
figure; hold on; 
plot(real(P),imag(P),'o')
plot(real(s),imag(s),'o')
legend('Approximate','True values')

%% New TRY 
close all 
clear all 
clc


