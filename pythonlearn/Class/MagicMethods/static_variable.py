# -*- coding: utf-8 -*-

class A(object):  
    count = 0  
    
    def __call__(self, *args, **kwargs):
        self.count += 1   # 会变成实例变量
        # A.count += 1      # 还是静态变量，实例之间共享
        

if __name__=="__main__":
    
    obj1 = A()  
    obj2 = A()   
    
    print obj1.count, obj2.count, A.count   
          
    obj1.count += 1  
    obj1()                                # count 已经变成 obj1 的实例变量了
    print obj1.count, obj2.count, A.count     
      
    A.count += 2                          # obj2的count还是A 的类变量（静态变量），obj.count 为 2
    obj2()                                # count 已经变成 obj2 的实例变量了
    print obj1.count, obj2.count, A.count
    

# 0 0 0
# 2 0 0
# 2 3 2