import os, site, unittest, sys
import subprocess
import time
from test import support
class ProcessTestCase(unittest.TestCase):
    def setUp(self):
        if hasattr(support, "reap_children"):
            support.reap_children()

    def test_read(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("Kitty")'], mode = 'rU')
        got, expect = p.read(), "Kitty"
        self.assertEqual(got, expect)
    
    def test_read_length_X(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("live love laf")'], mode = 'rU')
        got, expect = p.read(6), "live l"
        self.assertEqual(got, expect)

    def test_seekzero(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("charles ayudo")'])
        p.seek(4, 0)
        got, expect = p.read(), "les ayudo"
        self.assertEqual(got, expect)

    def test_seekone(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
                            r'import sys; sys.stdout.write("thinears")'])
        p.seek(2, 0)
        p.seek(2, 1)
        got, expect = p.read(), "ears"
        self.assertEqual(got, expect)

    def test_tell(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("0123456")'])
        p.seek(2, 0)
        p.seek(2, 1)
        got, expect = p.tell(), 4
        self.assertEqual(got, expect)

    def test_seektwo(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("evil")'])
        self.assertRaises(IOError, lambda : p.seek(-12,2))
    
    def test_readline(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("chipman\nlikes\nle cafe.\n")'], mode = 'rU')
        got, expect = p.readline(), "chipman\n"
        self.assertEqual(got, expect)
    # Need to make sure cursor is in the right place.
    def test_readlines(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("eric\np\r\n:")'])
        got, expect = p.readlines(7), ["eric\n", "p\r\n"]
        self.assertEqual(got, expect)

    def test_readlines_universal_newlines(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
                                    r'import sys; sys.stdout.write("Funciona!\nPlease?\r\n:")'],
                                    mode = 'rU')
        got, expect = p.readlines(), ["Funciona!\n", "Please?\n", ":"]
        self.assertEqual(got, expect)
        self.assertTrue('\r\n' in p.newlines)
        self.assertTrue('\n' in p.newlines)
    
    def test_close(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c", "input()"], mode = 'r+')
        p.close()
        self.assertRaises(ValueError, lambda : p.write("This should fizail righ-chyhea."))
    
    def test_write(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
            r'import sys; sys.stdout.write(str(sys.stdin.readline() == ".hach//SIGN\n"))'], 
            mode = 'r+')
        p.write(".hach//SIGN\n")
        self.assertEqual("True", p.read())
        p.close()
    
    def test_readonly(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c", r'input()'], mode = 'rb')
        try:
            p.write("Can you dig it?")
            self.fail("Was able to write to process.")
        except IOError as why:
            if why.errno != 9:
                raise why
        p.close()
    
    def test_writeonly(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c", r'input()'], mode = 'wt')
        try:
            p.read()
            self.fail("Was able to read from the process.")
        except IOError as why:
            if why.errno != 9:
                raise why
        p.close()

    def test_writeonly_appendcheck(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c", r'input()'], mode = 'aU')
        try:
            p.read()
            self.fail("Was able to read from the process.")
        except IOError as why:
            if why.errno != 9:
                raise why
        p.close()

    def test_readwriteok(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c", r'print(input())'], mode = 'r+U')
        p.write('Zonk\n')
        self.assertEqual(p.read(), 'Zonk\n')
        p.close()
        
        p = subprocess.ProcessIOWrapper([sys.executable, "-c", r'print(input())'], mode = 'w+U')
        p.write('Woosh\n')
        self.assertEqual(p.read(), 'Woosh\n')
        p.close()

    def test_filemodefuzzing(self):
        brokenmodes = ['r++', 'w++', 'a+r', 'rw', 'xxx']
        for mode in brokenmodes:
            try:
                p = subprocess.ProcessIOWrapper([sys.executable, "-c", r'print("...")'], mode = mode)
                self.fail("Mode was considered valid; " + mode)
            except ValueError:
                pass

    def test_stdoutonlywrapper(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
            r'import sys; print("you dont see this", file = sys.stderr); print("do you?")'], mode = 'rU')
        self.assertEqual(p.read(), "do you?\n")

    def test_stderronlywrapper(self):
        p = subprocess.ProcessIOWrapperStdErr([sys.executable, "-c",
            r'import sys; print("you dont see this"); print("do you?", file=sys.stderr)'], mode = 'rU')
        self.assertEqual(p.read(), "do you?\n")

    def test_stderronlywrapper(self):
        p = subprocess.ProcessIOWrapper2([sys.executable, "-c",
            r'import sys; print("we are"); print("one!", file=sys.stderr)'], mode = 'rU')
        self.assertEqual(p.read(), "we are\none!\n")

    def DISABLED_UNTIL_I_FIX_TEST_test_writelines(self):
        lineset = ['.hach//SIGN\n', '2\n', '3\n']
        p = subprocess.ProcessIOWrapper([sys.executable, "-c",
            r'import sys; l=sys.stdin.readlines();sys.stderr.write(l);sys.stdout.write(str(l == ".hach//SIGN\n"))'])
        p.writelines(lineset)
        p.writelines(lineset)
        self.assertEqual("True", p.read())
        p.close()
    
    def test_simplebools(self):
        p = subprocess.ProcessIOWrapper([sys.executable, "-c", r'import sys; input()'], mode = 'rU')
        self.assertFalse(p.isatty())
        self.assertFalse(p.closed)
        self.assertEqual(p.popenobject.pid, p.fileno())
        self.assertTrue(p.seekable())
        p.close()
        self.assertTrue(p.closed)

    def tearDown(self):
        if hasattr(support, "reap_children"):
            support.reap_children()

def test_suite():
    support.run_unittest(ProcessTestCase)
    support.reap_children()

if __name__ == "__main__":

    test_suite()
    exit()
