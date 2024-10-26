# The-Learn-Of-Python
The learn of python   Chinese Version --记录学习python的过程

目标：利用python画出FPS游戏敌人的方框  

原理：利用python的pymen读取游戏内存数据然后通过tkinter的canvas来实现画出敌人方框



注意：
1、需要懂一些python的基础，比如tkinter库的使用等 

2、需要懂得矩阵，例如fps游戏的矩阵是什么

3、需要会使用cheat engine（俗称ce），如何根据需要找的数据判断出数据类型，比如血量一般选择4字节，坐标一般选择浮点数


画敌人方框的方法有两个，一个是矩阵法， 另外一个是三角函数法，本代码采用矩阵法，优点是计算出敌人方框准确，缺点是需要理解矩阵；

另外一种三角函数方法优点是不用找矩阵，缺点是精度不高，需要后面自己调试代码将敌人方框调准
