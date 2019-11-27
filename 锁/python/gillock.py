# -*- coding: utf-8 -*- 
"""
author：     yangcheng
date：       2019/11/22 10:16
desc：
在第一章的时候，我就和大家介绍到，多线程和多进程是不一样的。
多进程是真正的并行，而多线程是伪并行，实际上他只是交替执行。
是什么导致多线程，只能交替执行呢？是一个叫GIL（Global Interpreter Lock，全局解释器锁）的东西。
什么是GIL呢？

任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。
这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。

需要注意的是，GIL并不是Python的特性，它是在实现Python解析器(CPython)时所引入的一个概念。而Python解释器，并不是只有CPython，除它之外，还有PyPy，Psyco，JPython，IronPython等。
在绝大多数情况下，我们通常都认为 Python == CPython，所以也就默许了Python具有GIL锁这个事。
都知道GIL影响性能，那么如何避免受到GIL的影响？

使用多进程代替多线程。
更换Python解释器，不使用CPython
"""