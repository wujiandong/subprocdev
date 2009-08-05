from test import support
import os, site, unittest
site.addsitedir(os.path.join('..'))
#Import classes and methods to test after this point.
import subprocess, sys, time
class ProcessTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_recv(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; sys.stdout.write("Scout McCreary")'],
                        stdout=subprocess.PIPE)
        time.sleep(1)
        got, expect = p.recv(), b"Scout McCreary"
        self.assertEqual(got, expect)

    def test_send(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.exit(sys.stdin.readline() == "kitty\n")'],
                         stdin=subprocess.PIPE)
        p.send("kitty\n")
        p.wait()
        got, expect = p.returncode, 1
        self.assertEqual(got, expect)

    def test_longrunning(self):
        program = r"""
            import sys
            import time
            letters = 'Mamie'
            while letters:
                try:
                    letters = letters[0:int(sys.stdin.readline())]
                    sys.stdout.write(letters+'\n')
                    sys.stdout.flush()
                except ValueError:
                    continue
            exit(True)
        """.replace(' ' * 12, '') #Removes the extra whitespace on the left
        p = subprocess.Popen([sys.executable, "-c", program],
            stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        letters = b"Mamie"
        n = len(letters)
        # We send a number to the program and we then make sure it returns
        # letters[0:numbers_we_sent]. If we read the output of the program
        # and it matches what we want, we ask the program to send one less
        # letter
        nl = b'\n'
        if subprocess.mswindows:
            nl = b'\r\n'
        while n >= 0:
            p.asyncwrite(bytes(str(n)+'\n', 'UTF-8'))
            n -= (p.asyncread() == letters[0:n]+nl)
        p.wait()
        self.assertEqual(1, p.returncode)

    def test_asyncwrite(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.exit(sys.stdin.readline() == "Lauren\n")'],
                         stdin=subprocess.PIPE)
        p.asyncwrite(b"Lauren\n")
        p.wait()
        got, expect = p.returncode, 1
        self.assertEqual(got, expect)

    def test_asyncread_stdout(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.stdout.write("Chuck")'],
                         stdout=subprocess.PIPE)
        got, expect = p.asyncread(timeout=1), b"Chuck"
        self.assertEqual(got, expect)

    def test_asyncread_stderr(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.stderr.write("JC")'],
                         stderr=subprocess.PIPE)
        got, expect = p.asyncread(timeout=1, stderr = True), b"JC"
        self.assertEqual(got, expect)

    def test_listen(self):
        # On Python 3.0, is not passed consistently... :/ changed listen delay
        # to .25 seconds. because of it.
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; x=sys.stdin.readline();sys.stderr.write("X_X\n");sys.stdout.write(x.capitalize());sys.exit()'],
                        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = False)
        got = p.listen('sam\n')
        if subprocess.mswindows:
            self.assertEqual(got, (4, b"Sam\r\n", b"X_X\r\n"))
        else:
            self.assertEqual(got, (4, b"Sam\n", b"X_X\n"))

    def tearDown(self):
        pass

def test_suite():
    support.run_unittest(ProcessTestCase)
    support.reap_children()

if __name__ == "__main__":

    test_suite()
    exit()
