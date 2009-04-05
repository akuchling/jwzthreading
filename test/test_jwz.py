#!/www/python/bin/python

"""
Test script for jwzthreading.

$Id: test_jwz.py,v 1.1 2003/03/26 13:09:56 akuchling Exp $
"""

from sancho.unittest import TestScenario, parse_args, run_scenarios
import jwzthreading, rfc822, StringIO

tested_modules = ["jwzthreading"]

def make_rfc822_message (S):
    input = StringIO.StringIO(S)
    return rfc822.Message(input)


class JWZTest (TestScenario):

    def setup (self):
        pass
    
    def shutdown (self):
        pass

    def check_container (self):
        self.test_stmt('jwzthreading.Container()')
        c = jwzthreading.Container()
        c2 = jwzthreading.Container()
        self.test_true('c.is_dummy()')
        self.test_seq('c.children', [])
        self.test_val('c.parent', None)
        self.test_false('c.has_descendant(c2)')

        # Add a child
        c3 = jwzthreading.Container()
        self.test_stmt('c.add_child(c2)')
        self.test_stmt('c2.add_child(c3)')
        self.test_seq('c.children', [c2])
        self.test_val('c2.parent', c)
        self.test_true('c.has_descendant(c2)')
        self.test_true('c.has_descendant(c3)')

        # Remove a child
        self.test_stmt('c.remove_child(c2)')
        self.test_seq('c.children', [])
        self.test_val('c2.parent', None)
        self.test_false('c.has_descendant(c3)')
        self.test_true('c2.has_descendant(c3)')

    def check_make_message (self):
        msg_templ = """Subject: %(subject)s
Message-ID: %(msg_id)s

Message body
"""
        m = make_rfc822_message("""Subject: random

Body.""")        
        self.test_exc('jwzthreading.make_message(m)', ValueError)
        
# class JWZTest


if __name__ == "__main__":
    (scenarios, options) = parse_args()
    run_scenarios(scenarios, options)
