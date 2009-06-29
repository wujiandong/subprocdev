import os, site, unittest
site.addsitedir(os.path.join('..'))
#Import classes and methods to test after this point.
import subprocess, sys, time
from subprocess import PIPE

class test_module(unittest.TestCase):
    def setUp(self):
        pass

    def test_recv_universal(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; sys.stdout.write("scout")'],
                        stdout=PIPE)
        time.sleep(1)
        got, expect = p.recv(), "scout"
        self.assertEqual(got, expect)

    def test_send_universal(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.exit(sys.stdin.readline() == "kitty\n")'],
                         stdin=PIPE)
        p.send("kitty\n")
        p.wait()
        got, expect = p.returncode, 1
        self.assertEqual(got, expect)

    def test_recv_err_universal(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.stderr.write("josiah carlson")'],
                         stderr=PIPE)
        got, expect = p.asyncread(timeout = 1, stderr = True), "josiah carlson"
        self.assertEqual(got, expect)

    def test_listen(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; x=sys.stdin.readline();sys.stderr.write("X_X");sys.stdout.write(x.upper());sys.exit()'],
                        stdout=PIPE, stdin=PIPE, stderr=PIPE)
        got = p.listen('xxx\n')
        self.assertEqual(got, (4, "XXX\n", "X_X"))

    def test_longrunning(self):
        program = '\n'.join([
            "import sys", "import time", "letters = 'abcd'", "while letters:",
            "\ttry:", "\t\tletters = letters[0:int(sys.stdin.readline())]",
            "\t\tsys.stdout.write(letters+'\\n')", "\t\tsys.stdout.flush()",
            "\texcept ValueError:", "\t\tcontinue", "exit(True)" ])
        p = subprocess.Popen([sys.executable, "-c", program],
            stdout=PIPE, stdin=PIPE)
        letters = "abcd"
        n = len(letters)
        while n >= 0:
            p.asyncwrite(str(n)+'\n')
            n -= (p.asyncread() == letters[0:n]+'\n')
        p.wait()
        self.assertEqual(1, p.returncode)

    def tearDown(self):
        pass

def suite():
    s = unittest.makeSuite(test_module)
    return unittest.TestSuite([s])

if __name__ == "__main__":

    unittest.main()
