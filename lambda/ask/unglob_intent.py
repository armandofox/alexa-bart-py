import sys
import re
import pdb

class Unglobber(object):

    def __init__(self, string):
        self.string = string.rstrip()
        self.unglobbed = []

    def unglob(self):
        glob = r'\(([^\)]+)\)'
        res = re.match(r'\A([^(]*)' + glob + r'(.*)\Z', self.string)
        if res == None:
            # no glob patterns in string
            self.unglobbed = [re.sub(r'\s+', ' ', self.string)]
        else:
            prefix = res.group(1)
            globs = res.group(2).split('|')
            suffix = res.group(3)
            for choice in globs:
                self.unglobbed += Unglobber(prefix+choice+suffix).unglob()
        return self.unglobbed

out = sys.stdout
with open(sys.argv[1]) as f:
    for line in f:
        if re.match(r'\A\s*\Z', line):
            out.write("\n")
            continue
        unglobber = Unglobber(line)
        unglobber.unglob()
        out.write("\n".join(unglobber.unglobbed) + "\n")
