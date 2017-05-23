close all; clear;clc

Work_path = '/Users/chenyu/Workspace/Nuerohackason2017/';

load([Work_path 'Data/2105_NC_170516_PLANE1_PINKNOISE_dataOut.mat'])


a = dataOut.trial(1).segmentmask;

figure;
a_=[];
b_=[];
labels={};
for i=1:max(a(:))
% for i=1:2
	[x,y]=find(a==i);
	xx=mean(x);
	yy=mean(y);
	a_=[a_,xx];
	b_=[b_,yy];
	labels{i}=num2str(i);
end

a(a == 0) = -1;
a(a > 0) = 0;
a(a == -1) = 1;
% a = mat2gray(a);
% imshow(a)
% hold on
plot(b_,a_,'o', 'Color', [0.7 0.7 0.7], 'Markersize', 10); 
hold on
grid on
text(b_ - 5,a_,labels, 'Color', [0.8 0 0], 'FontSize', 10);






load([Work_path 'Data/2105_NC_170518_PLANE1_PINKNOISE_dataOut.mat'])

a = dataOut.trial(1).segmentmask;

figure
a_=[];
b_=[];
labels={};
for i=1:max(a(:))
% for i=1:2
	[x,y]=find(a==i);
	xx=mean(x);
	yy=mean(y);
	a_=[a_,xx];
	b_=[b_,yy];
	labels{i}=num2str(i);
end


a(a == 0) = -1;
a(a > 0) = 0;
a(a == -1) = 1;
a = mat2gray(a);
% imshow(a)
% hold on
plot(b_,a_,'o', 'Color', [0.7 0.7 0.7], 'Markersize', 10); 
grid on
text(b_ - 5,a_,labels, 'Color', [0 0 0.8]);








