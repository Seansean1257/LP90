# The-Learn-Of-Python
The Learn Of Python   

-----------------------------Chinese Version -------------------------------------------------------------------------------------------------------------


记录学习python的过程  

安装python教程：[点击链接](https://github.com/Seansean1257/-python-)

目标：利用python画出FPS游戏敌人的方框  

原理：利用python的pymen读取游戏内存数据然后通过tkinter的canvas来实现画出敌人方框

画敌人方框的方法有两个，一个是矩阵法， 另外一个是三角函数法，本代码采用矩阵法，优点是计算出敌人方框准确，缺点是需要理解矩阵

另外一种三角函数方法优点是不用找矩阵，缺点是精度不高，需要后面自己调试代码将敌人方框调准

## 安装 Pymem

您可以使用以下命令通过 pip 安装 Pymem：

```bash
pip install pymem
```
更多关于 Pymem 的信息，请访问 [Pymem GitHub](https://github.com/srounet/Pymem)


注意：

1、需要懂python的基础，比如tkinter库的使用等


2、需要懂得矩阵，例如fps游戏的矩阵是什么


3、需要会使用cheat engine（俗称ce），如何根据需要找的数据判断出数据类型，比如血量一般选择4字节，坐标一般选择浮点数  <br><br>


-------------English Version--------------------------------------------------------------------------------------------------------------------------------


Objective: Use Python to draw enemy boxes in an FPS game

Principle: Read game memory data using Python's Pymem library, then use Tkinter's Canvas to draw enemy boxes

There are two methods to draw enemy boxes: the matrix method and the trigonometric method.
This code uses the matrix method, which has the advantage of accurately calculating enemy boxes, but it requires an understanding of matrices.

The other method, the trigonometric method, has the advantage of not finding a matrix by ce , but it is less accurate and may require manual code adjustments to align the enemy boxes correctly.
## Install  Pymem

you can use  pip to install Pymem：

```bash
pip install pymem
```
about Pymem information , please visit [Pymem GitHub](https://github.com/srounet/Pymem)



Notes:

1、You need a basic understanding of Python, such as how to use the Tkinter library.

2、You should understand matrices, particularly in the context of FPS games.

3、You should know how to use Cheat Engine (CE) to identify data types based on games,for example, health is typically a 4-byte integer, while coordinates are usually floating-point numbers
