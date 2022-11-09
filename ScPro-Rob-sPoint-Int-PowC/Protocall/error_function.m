function E=error_function(initialparameter,xm,ym)
t=linspace(0,2*pi,length(xm));
xao=initialparameter(1)*cos(t);
yao=initialparameter(2)*sin(t);
a=initialparameter(3);
z=[cos(a) -sin(a);sin(a) cos(a)];
m=[xao;yao];
k=z*m;
xao=k(1,:);
yao=k(2,:);
Ex=sum(abs(xao'-xm).^2);
Ey=sum(abs(yao'-ym).^2);
E=(Ex+Ey)/2;
% clf
% scatter(xm,ym);
% hold on;
% plot(xao,yao,'k');
% hold off;
% axis([-50 50 -50 50]);
% axis equal;
% drawnow;
end
