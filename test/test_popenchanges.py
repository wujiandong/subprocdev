import os, site, unittest
site.addsitedir(os.path.join('..'))
#Import classes and methods to test after this point.
import subprocess, sys
from time import sleep
class test_module(unittest.TestCase):
    def setUp(self):
        pass

    def test_recv(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; sys.stdout.write("scout")'],
                        stdout=subprocess.PIPE)
        sleep(1)
        got, expect = p.recv(), b"scout"
        self.assertEqual(got, expect)

    def test_send(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.exit(sys.stdin.readline() == "kitty\n")'],
                         stdin=subprocess.PIPE)
        p.send("kitty\n")
        p.wait()
        got, expect = p.returncode, 1
        self.assertEqual(got, expect)

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
                         r'import sys; sys.stdout.write("Charles McCreary")'],
                         stdout=subprocess.PIPE)
        got, expect = p.asyncread(timeout=1,raiseerror=0), b"Charles McCreary"
        self.assertEqual(got, expect)

    def test_asyncread_stderr(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.stderr.write("Josiah Carlson")'],
                         stderr=subprocess.PIPE)
        got, expect = p.asyncread(timeout=1,raiseerror=0), b"Josiah Carlson"
        self.assertEqual(got, expect)

    def test_listen(self):
        # On Python 3.0, is not passed consistently... :/ changed listen delay
        # to .25 seconds.
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; x=sys.stdin.readline();sys.stderr.write("X_X");sys.stdout.write(x.capitalize());sys.exit()'],
                        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        got = p.listen('sam\n')
        self.assertEqual(got, (4, b"Sam\n", b"X_X"))

    def tearDown(self):
        pass

def suite():

    s = unittest.makeSuite(test_module)
    return unittest.TestSuite([s])

if __name__ == "__main__":

    unittest.main()
