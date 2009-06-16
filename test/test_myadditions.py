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
        
    #def test_filelike_noerror1(self): #eventually, make it so we can chose wether we read from stderr or stdin
        #newproc = lambda : subprocess.FileWrapper([sys.executable,
                        #"-c", ';'.join(codelines)])
        #codelines = [
            #"from os import sys",
            #"outstream, instream = sys.stdout, sys.stdin",
            #"a = instream.read()"
            #"outstream.write(a)"
            #"outstream.flush()"
            #"input()" ]
        #p = newproc()
        #p.write("japan1\nwhat a\nneat place.\n")
        ##implement seek in positive directions? simply discards skipped data
        ##valid cases:   x.seek(offset, 1) where offset > 0
        ##               x.seek(absolute, [0]) where absolute > x.tell()
        ##               x.seek(any, 2) returns an error or something
        #self.assertEqual(p.read(8),"what a \nn")
        #self.assertEqual(p.readline(), "japan1\n")
        #self.assertEqual(p.read(8),"what a \nn")
        #p.seek(17, 0)
        #p.seek(2, 1)
        #self.assertEqual(p.read(),"place.\n")
        #p.close()
        #p = newproc()
        #p.write("line1/nline2/nline3/n")
        #self.assertEqual(p.readlines(12), ["line1/n", "line2/n"])
        #self.assertEqual(p.readlines(1), ["line3/n"])
        #p.close()

    def tearDown(self):
        pass

def suite():
    s = unittest.makeSuite(test_module)
    return unittest.TestSuite([s])

if __name__ == "__main__":

    unittest.main()
