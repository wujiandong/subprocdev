import os, site, unittest, sys
import subprocess
class test_module(unittest.TestCase):
    def setUp(self):
        pass

    def test_read(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("kitty")'])
        got, expect = p.read(), "kitty"
        self.assertEqual(got, expect)
    
    def test_read_length_X(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("live love laf")'])
        got, expect = p.read(6), "live l"
        self.assertEqual(got, expect)

    def test_seekzero(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("charles ayuda")'])
        p.seek(4, 0)
        got, expect = p.read(), "les ayuda"
        self.assertEqual(got, expect)

    def test_seekone(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("thinears")'])
        p.seek(2, 0)
        p.seek(2, 1)
        got, expect = p.read(), "ears"
        self.assertEqual(got, expect)

    def test_tell(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("0123456")'])
        p.seek(2, 0)
        p.seek(2, 1)
        got, expect = p.tell(), 4
        self.assertEqual(got, expect)

    def test_seektwo(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("evil")'])
        self.assertRaises(IOError, lambda : p.seek(-12,2))
    
    def test_readline(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("j\np\nn")'])
        got, expect = p.readline(), "j\n"
        self.assertEqual(got, expect)
    
    def test_readlines(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("eric\np\n:")'])
        got, expect = p.readlines(7), ["eric\n", "p\n"]
        self.assertEqual(got, expect)
    
    def test_close(self):
        p = subprocess.FileWrapper([sys.executable, "-c", "input()"])
        p.close()
        self.assertRaises(ValueError, lambda : p.write("This should fizail righ-chyhea."))

    def tearDown(self):
        pass

def suite():
    s = unittest.makeSuite(test_module)
    return unittest.TestSuite([s])

if __name__ == "__main__":

    unittest.main()
