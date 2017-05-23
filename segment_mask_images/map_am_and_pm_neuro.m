function map_am_and_pm_neuro(am_p1,str)
% a=am_p1.dataOut.trial(1).segmentmask;
% pre_b=pm_p1.dataOut.trial(1).segmentmask;
% a(a>0)=1;
% pre_b(pre_b>0)=1;
% b=zeros(size(a,1)+size(pre_b,1),size(a,2)+size(pre_b,2));
% offset=[size(a,1),size(a,2)];
% b((1:size(a,1))+offset(1),(1:size(a,2))+offset(2))=a;


% cc = xcorr2(b,a);
% [max_cc, imax] = max(abs(cc(:)));
% [ypeak, xpeak] = ind2sub(size(cc),imax(1));


% corr_offset = [(ypeak-size(a,1)) (xpeak-size(a,2))];


% a = 0.2*ones(11);
% a(6,3:9) = 0.6;
% a(3:9,6) = 0.6;
% b = 0.2*ones(22);
% offset = [8 6];
% b((1:size(a,1))+offset(1),(1:size(a,2))+offset(2)) = a;
% cc = xcorr2(b,a);
% [max_cc, imax] = max(abs(cc(:)));
% [ypeak, xpeak] = ind2sub(size(cc),imax(1));

% corr_offset = [(ypeak-size(a,1)) (xpeak-size(a,2))];

% isequal(corr_offset,offset)




a=am_p1.dataOut.trial(1).segmentmask;

g=figure;
a_=[];
b_=[];
labels={};
for i=1:max(a(:))
% for i=1:2
	[x,y]=find(a==i);
	xx=x(floor(length(x)/2));
	yy=y(floor(length(y)/2));
	a_=[a_,xx*2];
	b_=[b_,yy*2];
	labels{i}=num2str(i);
end
plot(a_,b_,'b*');
text(a_,b_,labels);
% imwrite(g,[str,'.png']);
saveas(g,[str,'.png']);





