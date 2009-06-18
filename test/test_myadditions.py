import os, site, unittest, sys
site.addsitedir(os.path.join('..'))
import subprocess
class test_module(unittest.TestCase):
    def setUp(self):
        pass

    def test_read(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            'import sys; sys.stdout.write("kitty")'],
                            stdout=subprocess.PIPE)
        got, expect = p.read(), "kitty"
        self.assertEqual(got, expect)
    
    def test_read_length_X(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            'import sys; sys.stdout.write("live love laf")'],
                            stdout=subprocess.PIPE)
        got, expect = p.read(6), "live l"
        self.assertEqual(got, expect)

    def test_seekzero(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            'import sys; sys.stdout.write("charles ayuda")'],
                            stdout=subprocess.PIPE)
        p.seek(0, 4)
        got, expect = p.read(), "les ayuda"
        self.assertEqual(got, expect)
#ok issue with my code is that we shouldn't need all the std out additons; fix
#so that it can be just run without declaring the PIPE
    def test_seekone(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            'import sys; sys.stdout.write("thinears")'],
                            stdout=subprocess.PIPE)
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

    def tearDown(self):
        pass

def suite():
    s = unittest.makeSuite(test_module)
    return unittest.TestSuite([s])

if __name__ == "__main__":

    unittest.main()
