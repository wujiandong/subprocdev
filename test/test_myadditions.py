import os, site, unittest, sys
import subprocess
class test_module(unittest.TestCase):
    def setUp(self):
        pass

    def test_read(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            'import sys; sys.stdout.write("kitty")'])
        got, expect = p.read(), "kitty"
        self.assertEqual(got, expect)
    
    def test_read_length_X(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            'import sys; sys.stdout.write("live love laf")'])
        got, expect = p.read(6), "live l"
        self.assertEqual(got, expect)

    def test_seekzero(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            'import sys; sys.stdout.write("charles ayuda")'])
        p.seek(0, 4)
        got, expect = p.read(), "les ayuda"
        self.assertEqual(got, expect)

    def test_seekone(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            'import sys; sys.stdout.write("thinears")'])
        p.seek(0, 2)
        p.seek(1, 2)
        got, expect = p.read(), "ears"
        self.assertEqual(got, expect)

    def test_tell(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    'import sys; sys.stdout.write("0123456")'])
        p.seek(0, 2)
        p.seek(1, 2)
        got, expect = p.tell(), 4
        self.assertEqual(got, expect)

    def test_seektwo(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    'import sys; sys.stdout.write("Lauren")'])
        self.assertRaises(IOError, lambda : p.seek(2, -12))
    
    def test_readline(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    'import sys; sys.stdout.write("j\np\nn")'])
        got, expect = p.readline(), "j\n"
        self.assertEqual(got, expect)
    
    def test_readlines(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    'import sys; sys.stdout.write("eric\np\n:)")'])
        got, expect = p.readlines(7), "eric\np\n"
        self.assertEqual(got, expect)
    
    def test_close(self):
        p = subprocess.FileWrapper([sys.executable, "-c", "input()"])
        p.close()
        self.assertRaises(ValueError, lambda : p.write("This should fizail righ-chyhea."))

    def test_josaih_recv_universal(self):
        p = subprocess.Popen([sys.executable, "-c",
                         'import sys; sys.stdout.write("scout")'],
                        stdout=subprocess.PIPE)
        got, expect = subprocess.recv_some(p,t=1,e=0), "scout"
        self.assertEqual(got, expect)

    def test_send_universal(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.exit(sys.stdin.readline() == "digimon.en_US-8.14.97\n")'],
                         stdin=subprocess.PIPE)
        p.send("digimon.en_US-8.14.97\n")
        p.wait()
        got, expect = p.returncode, 1
        self.assertEqual(got, expect)

    def test_send_universal(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.exit(sys.stdin.readline() == "charles\n")'],
                         stdin=subprocess.PIPE)
        p.asyncwrite("charles\n")
        got, expect = p.returncode, 1
        self.assertEqual(got, expect)
    
    def test_recv_err_universal(self):
        p = subprocess.Popen([sys.executable, "-c",
                         r'import sys; sys.stderr.write("josiah carlson")'],
                         stderr=subprocess.PIPE)
        got, expect = p.asyncread(t=1,e=0,stderr=1), "josiah carlson"
        self.assertEqual(got, expect)

    def test_send_recv(self):
        p = subprocess.Popen([sys.executable, "-c",
                        'import sys; x=sys.stdin.readline();sys.stderr.write("X_X");sys.stdout.write(x.upper());sys.exit()'],
                        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        got = p.send_recv('spam\n')
        self.assertEqual(got, (5, "SPAM\n", "X_X"))

    def tearDown(self):
        pass

def suite():
    s = unittest.makeSuite(test_module)
    return unittest.TestSuite([s])

if __name__ == "__main__":

    unittest.main()
