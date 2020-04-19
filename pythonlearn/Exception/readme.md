

- [Python 异常处理](http://www.runoob.com/python/python-exceptions.html)
- [Python-try except else finally有return时执行顺序探究](http://www.cnblogs.com/JohnABC/p/4065437.html)

## 实例代码
```
异常处理在任何一门编程语言里都是值得关注的一个话题，良好的异常处理可以让你的程序更加健壮，清晰的错误信息更能帮助你快速修复问题。
在Python中，和不部分高级语言一样，使用了try/except/finally语句块来处理异常，如果你有其他编程语言的经验，实践起来并不难。

异常处理语句 try...excpet...finally
    try:
        print(a / b)
    except ZeroDivisionError:
        print("Error: b should not be 0 !!")
    except Exception as e:
        print("Unexpected Error: {}".format(e))
    else:
        print('Run into else only when everything goes well')
    finally:
        print('Always run into finally block.')
```
#### 总结如下: 
1. except语句不是必须的，finally语句也不是必须的，但是二者必须要有一个，否则就没有try的意义了。
2. except语句可以有多个，Python会按except语句的顺序依次匹配你指定的异常，如果异常已经处理就不会再进入后面的except语句。
3. except语句可以以元组形式同时指定多个异常，参见实例代码。
4. except语句后面如果不指定异常类型，则默认捕获所有异常，你可以通过logging或者sys模块获取当前异常。
5. 如果要捕获异常后要重复抛出，请使用raise，后面不要带任何参数或信息。
6. 不建议捕获并抛出同一个异常，请考虑重构你的代码。
7. 不建议在不清楚逻辑的情况下捕获所有异常，有可能你隐藏了很严重的问题。
8. 尽量使用内置的异常处理语句来 替换try/except语句，比如with语句，getattr()方法。

## 抛出异常 raise
- 如果你需要自主抛出异常一个异常，可以使用raise关键字，等同于C#和Java中的throw语句，其语法规则如下。
   `raise NameError("bad name!")`

## 自定义异常类型
   - Python中也可以自定义自己的特殊类型的异常，只需要要从Exception类继承(直接或间接)即可：
```
class SomeCustomException(Exception): 
        pass
一般你在自定义异常类型时，需要考虑的问题应该是这个异常所应用的场景。
如果内置异常已经包括了你需要的异常，建议考虑使用内置 的异常类型。
比如你希望在函数参数错误时抛出一个异常，你可能并不需要定义一个InvalidArgumentError，使用内置的ValueError即可。
```

## 两个特殊的处理异常的简便方法
   1. 断言（assert）
   - 其中assert是断言的关键字。执行该语句的时候，先判断表达式expression，如果表达式为真，则什么都不做；如果表达式不为真，则抛出异常。reason跟我们之前谈到的异常类的实例一样。
```
assert的一般格式为：assert test [,msg]
test是一个表达式，其值为True或False。如果test的求值是False，assert就会引发AssertionError异常并使用在assert中提供的可选消息msg。
note：assert语句用于检查的内容应该始终为真，如果assert语句引发异常，这就意味着程序有Bug，而不是用户数据出错。
```
```
>>> assert len('love') == len('like')  
>>> assert 1==1  
>>> assert 1==2,"1 is not equal 2!"  
Traceback (most recent call last):  
  File "<stdin>", line 1, in <module>  
AssertionError: 1 is not equal 2!  
可以看到，如果assert后面的表达式为真，则什么都不做，如果不为真，就会抛出AssertionErro异常，而且我们传进去的字符串会作为异常类的实例的具体信息存在。
其实，assert异常也可以被try块捕获： 
>>> try:
...     assert 1 == 2 , "1 is not equal 2!"
... except AssertionError,reason:
...     print "%s:%s"%(reason.__class__.__name__,reason)
... 
AssertionError:1 is not equal 2!
>>> type(reason)
<type 'exceptions.AssertionError'>
```
   
   2. 上下文管理（with语句）
```
with可以用来简化 try...except...finally 代码，看起来可以比try...except...finally更清晰。
只要重载了__enter__() 和 __exit__(exc_type, exc_val, exc_tb) 方法，那么就可以用with 关键字调用。
```
   - 如果你使用try,except,finally代码仅仅是为了保证共享资源（如文件，数据）的唯一分配，并在任务结束后释放它，那么你就有福了！这个with语句可以让你从try,except,finally中解放出来！
   - 只有支持上下文管理协议（context management protocol）的对象 就可以使用with语句。

## 最佳实践
- 最佳实践不限于编程语言，只是一些规则和填坑后的收获。
1. 只处理你知道的异常，避免捕获所有 异常然后吞掉它们。
2. 抛出的异常应该说明原因，有时候你知道异常类型也猜不出所以然的。
3. 避免在catch语句块中干一些没意义的事情。
4. 不要使用异常来控制流程，那样你的程序会无比难懂和难维护。
5. 如果有需要，切记使用finally来释放资源。


## Python-try except else finally有return时执行顺序探究
因为有异常发生，所以try中的return语句肯定是执行不到的，然后在捕获到的except中进行执行，
并且except中存在return 语句，那么是不是就直接返回？ 因为finally 语句是必须要执行的，
所以这里的return语句需要先暂且放下，进入finally进行执行，然后finnaly执行完以后再返回到 except中进行执行。
看到这里，我们貌似找到了一些规律
1. 如果没有异常发生， try中有return 语句， 这个时候else块中的代码是没有办法执行到的， 但是finally语句中如果有return 语句会修改最终的返回值， 我个人理解的是try中return 语句先将要返回的值放在某个 CPU寄存器，然后运行finally语句的时候修改了这个寄存器的值，最后在返回到try中的return语句返回修改后的值。
2. 如果没有异常发生， try中没有return语句，那么else块的代码是执行的，但是如果else中有return， 那么也要先执行finally的代码， 返回值的修改与上面一条一致。
3. 如果有异常发生，try中的return语句肯定是执行不到， 在捕获异常的 except语句中，如果存在return语句，那么也要先执行finally的代码，finally里面的代码会修改最终的返回值，然后在从 except 块的retrun 语句返回最终修改的返回值， 和第一条一致。