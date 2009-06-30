import os, site, unittest, sys
import subprocess
class test_module(unittest.TestCase):
    def setUp(self):
        pass

    def test_read(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("Kitty")'])
        got, expect = p.read(), "Kitty"
        self.assertEqual(got, expect)
    
    def test_read_length_X(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("live love laf")'])
        got, expect = p.read(6), "live l"
        self.assertEqual(got, expect)

    def test_seekzero(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("charles ayudo")'])
        p.seek(4, 0)
        got, expect = p.read(), "les ayudo"
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
                                    r'import sys; sys.stdout.write("chipman\nlikes\nle cafe.\n")'])
        got, expect = p.readline(), "chipman\n"
        self.assertEqual(got, expect)
    # Need to make sure cursor is in the right place.
    def test_readlines(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("eric\np\r\n:")'])
        got, expect = p.readlines(7), ["eric\n", "p\r\n"]
        self.assertEqual(got, expect)

    def test_readlines_universal_newlines(self):
        p = subprocess.FileWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("Funciona!\nPlease?\r\n:")'],
                                    mode = 'U')
        got, expect = p.readlines(), ["Funciona!\n", "Please?\n", ":"]
        self.assertEqual(got, expect)
        self.assertTrue('\r\n' in p.newlines)
        self.assertTrue('\n' in p.newlines)
    
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
