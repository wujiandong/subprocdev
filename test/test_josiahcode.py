import os, site, unittest
site.addsitedir(os.path.join('..'))
#Import classes and methods to test after this point.
import subprocess, sys

class test_module(unittest.TestCase):
    def setUp(self):
        pass

    def test_recv_universal(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; sys.stdout.write("scout")'],
                        stdout=subprocess.PIPE)
        p.wait()
        got, expect = p.recv(), "scout"
        self.assertEqual(got, expect)

    def test_send_universal_out(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; sys.exit(sys.stdin.read() == "digimon.en_US-8.14.97")'],
                         stdin=subprocess.PIPE)
        p.send("digimon.en_US-8.14.97")
        got, expect = p.returncode, 1
        self.assertEqual(got, expect)
    
    def test_recv_err_universal(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; sys.stderr.write("josiah carlson")'],
                         stderr=subprocess.PIPE)
        got, expect = p.recv_err(), "josiah carlson"
        self.assertEqual(got, expect)

    def DISABLED_test_send_recv(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; x=stdin.read();sys.stderr.write("X_X");sys.stdout.write(x.upper());sys.exit()'],
                        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        got = p.send_recv('god')
        self.assertEqual(got, (3, "GOD", "X_X"))
        
    def tearDown(self):
        pass

def suite():
    s = unittest.makeSuite(test_module)
    return unittest.TestSuite([s])

if __name__ == "__main__":

    unittest.main()
