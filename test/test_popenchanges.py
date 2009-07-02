import os, site, unittest
site.addsitedir(os.path.join('..'))
#Import classes and methods to test after this point.
import subprocess, sys
from subprocess import PIPE
from time import sleep
class test_module(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_recv(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; sys.stdout.write("Scout McCreary")'],
                        stdout=PIPE)
        sleep(1)
        got, expect = p.recv(), b"Scout McCreary"
        self.assertEqual(got, expect)

    def test_send(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.exit(sys.stdin.readline() == "kitty\n")'],
                         stdin=PIPE)
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
"""
        p = subprocess.Popen([sys.executable, "-c", program],
            stdout=PIPE, stdin=PIPE)
        letters = b"Mamie"
        n = len(letters)
        while n >= 0:
            p.asyncwrite(bytes(str(n)+'\n', 'UTF-8'))
            n -= (p.asyncread() == letters[0:n]+b'\n')
        p.wait()
        self.assertEqual(1, p.returncode)

    def test_asyncwrite(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.exit(sys.stdin.readline() == "Lauren\n")'],
                         stdin=PIPE)
        p.asyncwrite(b"Lauren\n")
        p.wait()
        got, expect = p.returncode, 1
        self.assertEqual(got, expect)

    def test_asyncread_stdout(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.stdout.write("Charles McCreary")'],
                         stdout=PIPE)
        got, expect = p.asyncread(timeout=1), b"Charles McCreary"
        self.assertEqual(got, expect)

    def test_asyncread_stderr(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.stderr.write("Josiah Carlson")'],
                         stderr=PIPE)
        got, expect = p.asyncread(timeout=1, stderr = True), b"Josiah Carlson"
        self.assertEqual(got, expect)

    def test_listen(self):
        # On Python 3.0, is not passed consistently... :/ changed listen delay
        # to .25 seconds. because of it.
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; x=sys.stdin.readline();sys.stderr.write("X_X");sys.stdout.write(x.capitalize());sys.exit()'],
                        stdout=PIPE, stdin=PIPE, stderr=PIPE)
        got = p.listen('sam\n')
        self.assertEqual(got, (4, b"Sam\n", b"X_X"))

    def tearDown(self):
        pass

def suite():
    s = unittest.makeSuite(test_module)
    return unittest.TestSuite([s])

if __name__ == "__main__":

    unittest.main()
    exit()
