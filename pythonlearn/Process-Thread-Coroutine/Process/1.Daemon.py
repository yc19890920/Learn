#-*-coding=utf-8-*-
#

import sys, os, time, signal, atexit
from AC_Process import *

class AC_Daemon(object):
    """
    A generic daemon class.
    Usage: subclass the Daemon class and override the run() method
    """

    # 初始化操作
    def __init__(self, pidfile, logger, mainprocess=None, threads=[], usesignal=True, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        # 设置程序的 PID 文件
        self.pidfile = pidfile
        # 设置日志记录器
        self.logger  = logger
        # 设置要执行的主进程 (两种进行方式：“主进程”、“线程池”二选一)
        self.mainprocess = mainprocess
        # 设置要执行的线程池 (两种进行方式：“主进程”、“线程池”二选一)
        self.threads = threads
        # 设置输入输出文件
        self.stdin   = stdin
        self.stdout  = stdout
        self.stderr  = stderr
        # 设置是否使用信号量
        self.usesignal = usesignal
    # def end


    ############################################################
    # 进程启动相关操作

    # 创建精灵程序
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            # exit first parent
            if pid > 0 : sys.exit(0)
        except OSError, e:
            self.logger.outerror('Daemon', "fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        # try end

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            # exit from second parent
            if pid > 0 : sys.exit(0)
        except OSError, e:
            self.logger.outerror('Daemon', "fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # 重定向标准输入输出文件 (redirect standard file descriptors)
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # 生成 pidfile
        try:
            atexit.register(self._delpid)
            pid = str(os.getpid())
            file(self.pidfile, 'w+').write("%s\n" % pid)
        except IOError, e:
            self.logger.outerror('Daemon', "[Error %d] %s: '%s'\n" % (e.errno, e.strerror, e.filename))
            sys.exit(1)


    # 启动 daemon 进程
    def start(self):
        self.logger.outinfo('Daemon', 'service try run')

        # 检测 pidfile 文件，以判断 daemon 进程是否已运行
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        # 如果 daemon 进程已运行则进行提示并退出
        if pid:
            self.logger.outerror('Daemon', "pidfile %s already exist. Daemon already running?\n" % self.pidfile)
            sys.exit(1)

        # 启动进程
        self.daemonize()            # 将当前进程更改为精灵程序
        self.logger.outinfo('Daemon', 'service running')
        self.run()                  # 运行主程序

    ############################################################
    # 进程停止相关操作

    # 删除 PID 文件操作，一般注册为 atexit 调用
    def _delpid(self):
        self.logger.outinfo('Daemon', 'service stopping')
        self._delfile(self.pidfile)

    # 停止 daemon 进程
    def stop(self):
        self.logger.outinfo('Daemon', 'service try stop')

        # 从 pidfile 中取得PID
        try:
            pf  = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        # 如果不存在PID则退出
        if not pid:
            self.logger.outerror('Daemon', "pidfile %s does not exist. Daemon not running?\n" % self.pidfile)
            return  # not an error in a restart

        # 尝试杀掉 daemon 进程
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.5)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                self._delpid()
            else:
                self.logger.outerror('Daemon', err)
                sys.exit(1)


    """
    # 重新启动 daemon 进程
    def restart(self):
        self.stop()
        self.start()
    # def end
    """


    ############################################################
    # 其他操作

    # 删除指定的文件
    def _delfile(self, filepath):
        if os.path.exists(filepath):
            return os.remove(filepath)
        return True

    # 执行目标对象
    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
        if self.mainprocess != None :
            self.mainprocess.run()
        else :
            # 创建进程对象
            mainProcess = AC_MainProcess(self.threads, self.logger);

            # 设置信号量处理
            if self.usesignal == True :
                signal.signal(signal.SIGINT,  mainProcess.exitHandler)	        # 处理 Ctrl-c
                signal.signal(signal.SIGTERM, mainProcess.exitHandler)	        # 处理 kill
                signal.signal(signal.SIGALRM, mainProcess.exitHandler)	        # 处理 signal.alarm()
            else :
                signal.signal(signal.SIGINT,  mainProcess.roughExitHandler)     # 处理 Ctrl-c
                signal.signal(signal.SIGTERM, mainProcess.roughExitHandler)	    # 处理 kill
                signal.signal(signal.SIGALRM, mainProcess.roughExitHandler)	    # 处理 signal.alarm()

            # 运行进程
            mainProcess.run()

