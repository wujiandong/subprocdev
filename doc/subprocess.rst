
:mod:`subprocess` --- Subprocess management
===========================================

.. module:: subprocess
   :synopsis: Subprocess management.
.. moduleauthor:: Peter Åstrand <astrand@lysator.liu.se>
.. sectionauthor:: Peter Åstrand <astrand@lysator.liu.se>


The :mod:`subprocess` module allows you to spawn new processes, connect to their
input/output/error pipes, and obtain their return codes.  This module intends to
replace several other, older modules and functions, such as::

   os.system
   os.spawn*

Information about how the :mod:`subprocess` module can be used to replace these
modules and functions can be found in the following sections.

.. seealso::

   :pep:`324` -- PEP proposing the subprocess module


Using the subprocess Module
---------------------------

This module defines one class called :class:`Popen`:


.. class:: Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)

   Arguments are:

   *args* should be a string, or a sequence of program arguments.  The program
   to execute is normally the first item in the args sequence or the string if
   a string is given, but can be explicitly set by using the *executable*
   argument.  When *executable* is given, the first item in the args sequence
   is still treated by most programs as the command name, which can then be
   different from the actual executable name.  On Unix, it becomes the display
   name for the executing program in utilities such as :program:`ps`.

   On Unix, with *shell=False* (default): In this case, the Popen class uses
   :meth:`os.execvp` to execute the child program. *args* should normally be a
   sequence.  A string will be treated as a sequence with the string as the only
   item (the program to execute).

   On Unix, with *shell=True*: If args is a string, it specifies the command string
   to execute through the shell.  If *args* is a sequence, the first item specifies
   the command string, and any additional items will be treated as additional shell
   arguments.

   On Windows: the :class:`Popen` class uses CreateProcess() to execute the child
   program, which operates on strings.  If *args* is a sequence, it will be
   converted to a string using the :meth:`list2cmdline` method.  Please note that
   not all MS Windows applications interpret the command line the same way:
   :meth:`list2cmdline` is designed for applications using the same rules as the MS
   C runtime.

   *bufsize*, if given, has the same meaning as the corresponding argument to the
   built-in open() function: :const:`0` means unbuffered, :const:`1` means line
   buffered, any other positive value means use a buffer of (approximately) that
   size.  A negative *bufsize* means to use the system default, which usually means
   fully buffered.  The default value for *bufsize* is :const:`0` (unbuffered).

   The *executable* argument specifies the program to execute. It is very seldom
   needed: Usually, the program to execute is defined by the *args* argument. If
   ``shell=True``, the *executable* argument specifies which shell to use. On Unix,
   the default shell is :file:`/bin/sh`.  On Windows, the default shell is
   specified by the :envvar:`COMSPEC` environment variable.

   *stdin*, *stdout* and *stderr* specify the executed programs' standard input,
   standard output and standard error file handles, respectively.  Valid values
   are :data:`PIPE`, an existing file descriptor (a positive integer), an
   existing file object, and ``None``.  :data:`PIPE` indicates that a new pipe
   to the child should be created.  With ``None``, no redirection will occur;
   the child's file handles will be inherited from the parent.  Additionally,
   *stderr* can be :data:`STDOUT`, which indicates that the stderr data from the
   applications should be captured into the same file handle as for stdout.

   If *preexec_fn* is set to a callable object, this object will be called in the
   child process just before the child is executed. (Unix only)

   If *close_fds* is true, all file descriptors except :const:`0`, :const:`1` and
   :const:`2` will be closed before the child process is executed. (Unix only).
   Or, on Windows, if *close_fds* is true then no handles will be inherited by the
   child process.  Note that on Windows, you cannot set *close_fds* to true and
   also redirect the standard handles by setting *stdin*, *stdout* or *stderr*.

   If *shell* is :const:`True`, the specified command will be executed through the
   shell.

   If *cwd* is not ``None``, the child's current directory will be changed to *cwd*
   before it is executed.  Note that this directory is not considered when
   searching the executable, so you can't specify the program's path relative to
   *cwd*.

   If *env* is not ``None``, it must be a mapping that defines the environment
   variables for the new process; these are used instead of inheriting the current
   process' environment, which is the default behavior.

   .. note::

      If specified, *env* must provide any variables required
      for the program to execute.  On Windows, in order to run a
      `side-by-side assembly`_ the specified *env* **must** include a valid
      :envvar:`SystemRoot`.

   .. _side-by-side assembly: http://en.wikipedia.org/wiki/Side-by-Side_Assembly

   If *universal_newlines* is :const:`True`, the file objects stdout and stderr are
   opened as text files, but lines may be terminated by any of ``'\n'``, the Unix
   end-of-line convention, ``'\r'``, the old Macintosh convention or ``'\r\n'``, the
   Windows convention. All of these external representations are seen as ``'\n'``
   by the Python program.

   .. note::

      This feature is only available if Python is built with universal newline support
      (the default).  Also, the newlines attribute of the file objects :attr:`stdout`,
      :attr:`stdin` and :attr:`stderr` are not updated by the :meth:`communicate` method.

   The *startupinfo* and *creationflags*, if given, will be passed to the
   underlying CreateProcess() function.  They can specify things such as appearance
   of the main window and priority for the new process.  (Windows only)


.. data:: PIPE

   Special value that can be used as the *stdin*, *stdout* or *stderr* argument
   to :class:`Popen` and indicates that a pipe to the standard stream should be
   opened.


.. data:: STDOUT

   Special value that can be used as the *stderr* argument to :class:`Popen` and
   indicates that standard error should go into the same handle as standard
   output.


Convenience Functions
^^^^^^^^^^^^^^^^^^^^^

This module also defines four shortcut functions:


.. function:: call(*popenargs, **kwargs)

   Run command with arguments.  Wait for command to complete, then return the
   :attr:`returncode` attribute.

   The arguments are the same as for the Popen constructor.  Example::

      retcode = call(["ls", "-l"])

   .. warning::

      Like :meth:`Popen.wait`, this will deadlock if the child process
      generates enough output to a stdout or stderr pipe such that it blocks
      waiting for the OS pipe buffer to accept more data.


.. function:: check_call(*popenargs, **kwargs)

   Run command with arguments.  Wait for command to complete. If the exit code was
   zero then return, otherwise raise :exc:`CalledProcessError`. The
   :exc:`CalledProcessError` object will have the return code in the
   :attr:`returncode` attribute.

   The arguments are the same as for the Popen constructor.  Example::

      check_call(["ls", "-l"])

   .. warning::

      See the warning for :func:`call`.


.. function:: check_output(*popenargs, **kwargs)

   Run command with arguments and return its output as a byte string.

   If the exit code was non-zero it raises a :exc:`CalledProcessError`.  The
   :exc:`CalledProcessError` object will have the return code in the
   :attr:`returncode`
   attribute and output in the :attr:`output` attribute.

   The arguments are the same as for the :class:`Popen` constructor.  Example::

      >>> subprocess.check_output(["ls", "-l", "/dev/null"])
      'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

   The stdout argument is not allowed as it is used internally.
   To capture standard error in the result, use ``stderr=subprocess.STDOUT``::

      >>> subprocess.check_output(
              ["/bin/sh", "-c", "ls non_existent_file ; exit 0"],
              stderr=subprocess.STDOUT)
      'ls: non_existent_file: No such file or directory\n'

   .. versionadded:: 3.1


.. function:: getstatusoutput(cmd)
   Return ``(status, output)`` of executing *cmd* in a shell.

   Execute the string *cmd* in a shell with :func:`os.popen` and return a 2-tuple
   ``(status, output)``.  *cmd* is actually run as ``{ cmd ; } 2>&1``, so that the
   returned output will contain output or error messages.  A trailing newline is
   stripped from the output.  The exit status for the command can be interpreted
   according to the rules for the C function :cfunc:`wait`.  Example::

      >>> import subprocess
      >>> subprocess.getstatusoutput('ls /bin/ls')
      (0, '/bin/ls')
      >>> subprocess.getstatusoutput('cat /bin/junk')
      (256, 'cat: /bin/junk: No such file or directory')
      >>> subprocess.getstatusoutput('/bin/junk')
      (256, 'sh: /bin/junk: not found')

   Availability: UNIX.


.. function:: getoutput(cmd)
   Return output (stdout and stderr) of executing *cmd* in a shell.

   Like :func:`getstatusoutput`, except the exit status is ignored and the return
   value is a string containing the command's output.  Example::

      >>> import subprocess
      >>> subprocess.getoutput('ls /bin/ls')
      '/bin/ls'

   Availability: UNIX.


Exceptions
^^^^^^^^^^

Exceptions raised in the child process, before the new program has started to
execute, will be re-raised in the parent.  Additionally, the exception object
will have one extra attribute called :attr:`child_traceback`, which is a string
containing traceback information from the childs point of view.

The most common exception raised is :exc:`OSError`.  This occurs, for example,
when trying to execute a non-existent file.  Applications should prepare for
:exc:`OSError` exceptions.

A :exc:`ValueError` will be raised if :class:`Popen` is called with invalid
arguments.

check_call() will raise :exc:`CalledProcessError`, if the called process returns
a non-zero return code.


Security
^^^^^^^^

Unlike some other popen functions, this implementation will never call /bin/sh
implicitly.  This means that all characters, including shell metacharacters, can
safely be passed to child processes.


Popen Objects
-------------

Instances of the :class:`Popen` class have the following methods:


.. method:: Popen.poll()

   Check if child process has terminated.  Set and return :attr:`returncode`
   attribute.


.. method:: Popen.wait()

   Wait for child process to terminate.  Set and return :attr:`returncode`
   attribute.

   .. warning::

      This will deadlock if the child process generates enough output to a
      stdout or stderr pipe such that it blocks waiting for the OS pipe buffer
      to accept more data.  Use :meth:`communicate` to avoid that.


.. method:: Popen.recv(maxsize=None)

   Non-blocking, asynchronous reading of stdout from the child process. Since
   this method is non-blocking, data will not always be available to be read and
   calls done in quick succession will just return empty strings. When
   *maxsize*, the greatest number of bytes to be read from the child process, is
   *None* specified, 1024 bytes will be read. If the value given is less than
   one, one byte will be returned.

   .. note::
      It is recommended that you use :meth:`asyncread` instead of this method.


.. method:: Popen.recv_err(maxsize=None)
   
   Functions in the exact same manner as :meth:`recv` but instead of reading
   from stdout, it reads from stderr.


.. method:: Popen.send(input)

   Write the given bytes to the subprocess in a non-blocking manner. If the
   function is unable to communicate with the process, *None* is returned. It is
   recommended that you use :meth`asyncwrite`.


.. method:: Popen.listen(self, input='', maxsize=None)

   Sends input and returns a tuple containing the number of bytes written to
   the child process, and the output of the child process. *maxsize* represents 
   the greatest number of bytes to read from stdout and stderr separately. If it
   is *None*, data will be read until a specified timeout is reached or no more
   data can be read.


.. method:: Popen.asyncread(timeout=.1, raiseonnone=False, timeresolution=5, stderr=False, maxsize=None, chunksize=None)

   Read data from the child process using the asnychronous methods. This method
   provides more control over reading the data than ::meth`recv` and is
   especially useful if you expect that a program may not have data available to
   read immediately but more than likely will in a known timeframe. Data will be
   read until one of the following three conditions is met:
   
   * The specified timeout has expired
   
   * The process disconnected
   
   * The maximum number of bytes specified has been read

   The number of seconds to attempt to read data is specified by *timeout*. The
   *timeresolution* determines how many times during the duration specified by
   *timeout* to check to see if the subprocess has any data to be siphoned off.
   
   If *stderr* is *True*, this method will read from the stderr produced by the
   subprocess instead of the stdout.
   
   The number maximum number of bytes to read per timeout is determined by
   *maxsize* . Data will be read in chunks of bytes specified by *chunksize*
   when it is specified but otherwise 1024
   
   .. note::

      There is no guarantee that bytes will be read in chunks of the specified
      size since the method used will not block to attempt to read the given
      amount of data.
   
   When *raiseonnone* is *True*, an exception will be raised when it appears the
   child process has been disconnected. Otherwise, no exception will be raised
   and the method will return the data that it was able to obtain before the
   disconnect.

.. method:: Popen.asyncwrite

   Functions in the same manner as the :meth:`send` method but the data is
   written in chunks of 1024 bytes, and an *Exception* is raised if the child
   process disconnects. The exception string will contain the number of bytes
   that were successfully written to the child process.


.. method:: Popen.communicate(input=None)

   Interact with process: Send data to stdin.  Read data from stdout and stderr,
   until end-of-file is reached.  Wait for process to terminate. The optional
   *input* argument should be a byte string to be sent to the child process, or
   ``None``, if no data should be sent to the child.

   :meth:`communicate` returns a tuple ``(stdoutdata, stderrdata)``.

   Note that if you want to send data to the process's stdin, you need to create
   the Popen object with ``stdin=PIPE``.  Similarly, to get anything other than
   ``None`` in the result tuple, you need to give ``stdout=PIPE`` and/or
   ``stderr=PIPE`` too.

   .. note::

      The data read is buffered in memory, so do not use this method if the data
      size is large or unlimited.


.. method:: Popen.send_signal(signal)

   Sends the signal *signal* to the child.

   .. note::

      On Windows only SIGTERM is supported so far. It's an alias for
      :meth:`terminate`.


.. method:: Popen.terminate()

   Stop the child. On Posix OSs the method sends SIGTERM to the
   child. On Windows the Win32 API function :cfunc:`TerminateProcess` is called
   to stop the child.


.. method:: Popen.kill()

   Kills the child. On Posix OSs the function sends SIGKILL to the child.
   On Windows :meth:`kill` is an alias for :meth:`terminate`.


The following attributes are also available:

.. warning::

   Use :meth:`communicate` rather than :attr:`.stdin.write <stdin>`,
   :attr:`.stdout.read <stdout>` or :attr:`.stderr.read <stderr>` to avoid
   deadlocks due to any of the other OS pipe buffers filling up and blocking the
   child process.


.. attribute:: Popen.stdin

   If the *stdin* argument was :data:`PIPE`, this attribute is a file object
   that provides input to the child process.  Otherwise, it is ``None``.


.. attribute:: Popen.stdout

   If the *stdout* argument was :data:`PIPE`, this attribute is a file object
   that provides output from the child process.  Otherwise, it is ``None``.


.. attribute:: Popen.stderr

   If the *stderr* argument was :data:`PIPE`, this attribute is a file object
   that provides error output from the child process.  Otherwise, it is
   ``None``.


.. attribute:: Popen.pid

   The process ID of the child process.


.. attribute:: Popen.returncode

   The child return code, set by :meth:`poll` and :meth:`wait` (and indirectly
   by :meth:`communicate`).  A ``None`` value indicates that the process
   hasn't terminated yet.

   A negative value ``-N`` indicates that the child was terminated by signal
   ``N`` (Unix only).

.. _subprocess-asyncmeths:

Advantages Of Asynchronous Methods
-----------------------------------

The Popen.asyncread and Popen.asyncwrite methods are new to Python 3.1 and due
to their non-blocking nature, have a number of advantages over the older
methods, in particular :meth:`communicate`. 

communicate example::

   import sys
   import subprocess
   proc = subprocess.Popen([sys.executable, "-c",
       "factor=int(input());print(factor*1000**1000**1000**2448348)"],
       stdin = subprocess.PIPE, stdout = subprocess.PIPE)
   
   proc.communicate(b'456901092723\n')

The program will halt at the `proc.communicate` call until the program returns
something. Given the complexity of the expression, it will take most computers
quite some time to produce a result assuming there isn't a runtime error that
occurs in the mean time.

With :meth:`asyncwrite` and :meth:`asyncread`, you can fire off the child
process and continue to execute code in the parent process, regardless of
what the child process is doing or the output it returns (or does not return).

Asynchronous I/O example::

   import sys
   import subprocess
   import time
   import random
   proc = subprocess.Popen([sys.executable, "-c",
       "factor=int(input());print(factor*1000**1000**1000**2448348)"],
       stdin = subprocess.PIPE, stdout = subprocess.PIPE)
   
   # Communicate will block until the program produces some output or exits
   proc.asyncwrite('3242007\n')
   timerstart = time.time()
      
   print("Calculating...")
   pollresult = proc.asyncread(timeout=1.0)
   while not pollresult:
       print("Seconds elapsed: ", int(time.time() - timerstart))
       pollresult = proc.asyncread(timeout=random.randint(1,3))
   
   print('Done!\n', str(pollresult))

.. _subprocess-replacements:

Replacing Older Functions with the subprocess Module
----------------------------------------------------

In this section, "a ==> b" means that b can be used as a replacement for a.

.. note::

   All functions in this section fail (more or less) silently if the executed
   program cannot be found; this module raises an :exc:`OSError` exception.

In the following examples, we assume that the subprocess module is imported with
"from subprocess import \*".


Replacing /bin/sh shell backquote
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   output=`mycmd myarg`
   ==>
   output = Popen(["mycmd", "myarg"], stdout=PIPE).communicate()[0]


Replacing shell pipeline
^^^^^^^^^^^^^^^^^^^^^^^^

::

   output=`dmesg | grep hda`
   ==>
   p1 = Popen(["dmesg"], stdout=PIPE)
   p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
   output = p2.communicate()[0]


Replacing :func:`os.system`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   sts = os.system("mycmd" + " myarg")
   ==>
   p = Popen("mycmd" + " myarg", shell=True)
   sts = os.waitpid(p.pid, 0)

Notes:

* Calling the program through the shell is usually not required.

* It's easier to look at the :attr:`returncode` attribute than the exit status.

A more realistic example would look like this::

   try:
       retcode = call("mycmd" + " myarg", shell=True)
       if retcode < 0:
           print("Child was terminated by signal", -retcode, file=sys.stderr)
       else:
           print("Child returned", retcode, file=sys.stderr)
   except OSError as e:
       print("Execution failed:", e, file=sys.stderr)


Replacing the :func:`os.spawn <os.spawnl>` family
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

P_NOWAIT example::

   pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
   ==>
   pid = Popen(["/bin/mycmd", "myarg"]).pid

P_WAIT example::

   retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
   ==>
   retcode = call(["/bin/mycmd", "myarg"])

Vector example::

   os.spawnvp(os.P_NOWAIT, path, args)
   ==>
   Popen([path] + args[1:])

Environment example::

   os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)
   ==>
   Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})



Replacing :func:`os.popen`, :func:`os.popen2`, :func:`os.popen3`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   (child_stdin, child_stdout) = os.popen2(cmd, mode, bufsize)
   ==>
   p = Popen(cmd, shell=True, bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, close_fds=True)
   (child_stdin, child_stdout) = (p.stdin, p.stdout)

::

   (child_stdin,
    child_stdout,
    child_stderr) = os.popen3(cmd, mode, bufsize)
   ==>
   p = Popen(cmd, shell=True, bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
   (child_stdin,
    child_stdout,
    child_stderr) = (p.stdin, p.stdout, p.stderr)

::

   (child_stdin, child_stdout_and_stderr) = os.popen4(cmd, mode, bufsize)
   ==>
   p = Popen(cmd, shell=True, bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
   (child_stdin, child_stdout_and_stderr) = (p.stdin, p.stdout)

Return code handling translates as follows::

   pipe = os.popen(cmd, 'w')
   ...
   rc = pipe.close()
   if  rc != None and rc % 256:
       print "There were some errors"
   ==>
   process = Popen(cmd, 'w', stdin=PIPE)
   ...
   process.stdin.close()
   if process.wait() != 0:
       print "There were some errors"


Replacing functions from the :mod:`popen2` module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

   If the cmd argument to popen2 functions is a string, the command is executed
   through /bin/sh.  If it is a list, the command is directly executed.

::

   (child_stdout, child_stdin) = popen2.popen2("somestring", bufsize, mode)
   ==>
   p = Popen(["somestring"], shell=True, bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, close_fds=True)
   (child_stdout, child_stdin) = (p.stdout, p.stdin)

::

   (child_stdout, child_stdin) = popen2.popen2(["mycmd", "myarg"], bufsize, mode)
   ==>
   p = Popen(["mycmd", "myarg"], bufsize=bufsize,
             stdin=PIPE, stdout=PIPE, close_fds=True)
   (child_stdout, child_stdin) = (p.stdout, p.stdin)

:class:`popen2.Popen3` and :class:`popen2.Popen4` basically work as
:class:`subprocess.Popen`, except that:

* :class:`Popen` raises an exception if the execution fails.

* the *capturestderr* argument is replaced with the *stderr* argument.

* ``stdin=PIPE`` and ``stdout=PIPE`` must be specified.

* popen2 closes all file descriptors by default, but you have to specify
  ``close_fds=True`` with :class:`Popen`.
