function total(n,acc=0)=n<=0?acc:total(n-1,acc+sin(n)*sin(n)+cos(n)*cos(n));
v=total(20000); assert(abs(v-20000)<0.001);
cube([v/1000,15,8]);
