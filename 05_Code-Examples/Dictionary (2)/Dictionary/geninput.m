for i=1:8000
	if(randi(2)-1) a(i)=rand/rand; else a(i)=-rand/rand; end
end
printf("10000 8000\n");
printf("%f\n",a);
