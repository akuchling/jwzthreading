#!/www/python/bin/python

"""
Test script for jwzthreading.

"""

import unittest
import jwzthreading
from email import message_from_string

try:
    import rfc822
except ImportError:
    rfc822 = None

tested_modules = ["jwzthreading"]

def make_message (S):
    return message_from_string(S)


class JWZTest (unittest.TestCase):

    def test_container (self):
        c = jwzthreading.Container()
        repr(c)

        c2 = jwzthreading.Container()
        self.assertTrue(c.is_dummy())
        self.assertEquals(c.children, [])
        self.assertEquals(c.parent, None)
        self.assertFalse(c.has_descendant(c2))

        # Add a child
        c3 = jwzthreading.Container()
        c.add_child(c2)
        c2.add_child(c3)
        self.assertEquals(c.children, [c2])
        self.assertEquals(c2.parent, c)
        self.assertTrue(c.has_descendant(c2))
        self.assertTrue(c.has_descendant(c3))
        self.assertTrue(c.has_descendant(c))

        # Remove a child
        c.remove_child(c2)
        self.assertEquals(c.children, [])
        self.assertEquals(c2.parent, None)
        self.assertFalse(c.has_descendant(c3))
        self.assertTrue(c2.has_descendant(c3))

        # Add child of one container to another
        c3 = jwzthreading.Container()
        c.add_child(c3)
        c2.add_child(c3)
        self.assertEquals(c3.parent, c2)

    def test_deep_container(self):
        # Build a 50000-deep list of nested Containers.
        parent = jwzthreading.Container()
        L = [parent]
        for i in range(50000):
            child = jwzthreading.Container()
            parent.add_child(child)
            L.append(child)
            parent = child

        # Test finding the last child
        self.assertTrue(L[0].has_descendant(L[-1]))

        # Test a search that fails
        self.assertFalse(L[0].has_descendant(jwzthreading.Container()))
        
    def test_uniq(self):
        self.assertEquals(jwzthreading.uniq((1,2,3,1,2,3)), [1,2,3])

    def test_rfc822_make_message (self):
        if rfc822 is None:
            return
        from StringIO import StringIO

        msg_templ = """Subject: %(subject)s
Message-ID: %(msg_id)s

Message body
"""
        f = StringIO("""Subject: random

Body.""")
        m = rfc822.Message(f)
        self.assertRaises(ValueError, jwzthreading.make_message, m)

    def test_email_make_message (self):
        msg_templ = """Subject: %(subject)s
Message-ID: %(msg_id)s

Message body
"""
        m = message_from_string("""Subject: random

Body.""")
        self.assertRaises(ValueError, jwzthreading.make_message, m)

    def test_basic_message(self):
        msg = message_from_string("""Subject: random
Message-ID: <message1>
References: <ref1> <ref2> <ref1>
In-Reply-To: <reply>

Body.""")
        m = jwzthreading.make_message(msg)
        self.assertTrue(repr(m))
        self.assertEquals(m.subject, 'random')
        self.assertEquals(sorted(m.references),
                          ['ref1', 'ref2', 'reply'])

        # Verify that repr() works
        repr(m)

    def test_prune_empty(self):
        c = jwzthreading.Container()
        self.assertEquals(jwzthreading.prune_container(c), [])

    def test_prune_promote(self):
        p = jwzthreading.Container()
        c1 = jwzthreading.Container()
        c1.message = jwzthreading.Message()
        p.add_child(c1)
        self.assertEquals(jwzthreading.prune_container(p), [c1])

    def test_thread_single(self):
        "Thread a single message"
        m = jwzthreading.Message(None)
        m.subject = m.message_id = 'Single'
        self.assertEqual(jwzthreading.thread([m])['Single'].message, m)

    def test_thread_unrelated(self):
        "Thread two unconnected messages"
        m1 = jwzthreading.Message(None)
        m1.subject = m1.message_id = 'First'
        m2 = jwzthreading.Message(None)
        m2.subject = m2.message_id = 'Second'
        d = jwzthreading.thread([m1, m2])
        self.assertEqual(d['First'].message, m1)
        self.assertEqual(d['Second'].children, [])
        self.assertEqual(d['Second'].message, m2)

    def test_thread_two(self):
        "Thread two messages together."
        m1 = jwzthreading.Message(None)
        m1.subject = m1.message_id = 'First'
        m2 = jwzthreading.Message(None)
        m2.subject = m2.message_id = 'Second'
        m2.references = ['First']
        d = jwzthreading.thread([m1, m2])
        self.assertEqual(d['First'].message, m1)
        self.assertEqual(len(d['First'].children), 1)
        self.assertEqual(d['First'].children[0].message, m2)

    def test_thread_two_reverse(self):
        "Thread two messages together, with the child message listed first."
        m1 = jwzthreading.Message(None)
        m1.subject = m1.message_id = 'First'
        m2 = jwzthreading.Message(None)
        m2.subject = m2.message_id = 'Second'
        m2.references = ['First']
        d = jwzthreading.thread([m2, m1])
        self.assertEqual(d['First'].message, m1)
        self.assertEqual(len(d['First'].children), 1)
        self.assertEqual(d['First'].children[0].message, m2)

    def test_thread_lying_message(self):
        "Thread three messages together, with other messages lying in their references."
        dummy_parent_m = jwzthreading.Message(None)
        dummy_parent_m.subject = dummy_parent_m.message_id = 'Dummy parent'
        lying_before_m = jwzthreading.Message(None)
        lying_before_m.subject = lying_before_m.message_id = 'Lying before'
        lying_before_m.references = ['Dummy parent', 'Second', 'First', 'Third']
        m1 = jwzthreading.Message(None)
        m1.subject = m1.message_id = 'First'
        m2 = jwzthreading.Message(None)
        m2.subject = m2.message_id = 'Second'
        m2.references = ['First']
        m3 = jwzthreading.Message(None)
        m3.subject = m3.message_id = 'Third'
        m3.references = ['First', 'Second']
        lying_after_m = jwzthreading.Message(None)
        lying_after_m.subject = lying_after_m.message_id = 'Lying after'
        #lying_after_m.references = ['Dummy parent','Third', 'Second', 'First']
        d = jwzthreading.thread([dummy_parent_m, lying_before_m, m1, m2, m3, lying_after_m])
        self.assertEqual(d['First'].message, m1)
        self.assertEqual(len(d['First'].children), 1)
        self.assertEqual(d['First'].children[0].message, m2)
        self.assertEqual(len(d['First'].children[0].children), 1)
        self.assertEqual(d['First'].children[0].children[0].message, m3)
        
    def test_thread_two_missing_parent(self):
        "Thread two messages, both children of a missing parent."
        m1 = jwzthreading.Message(None)
        m1.subject = 'Child'
        m1.message_id = 'First'
        m1.references = ['parent']
        m2 = jwzthreading.Message(None)
        m2.subject = 'Child'
        m2.message_id = 'Second'
        m2.references = ['parent']
        d = jwzthreading.thread([m1, m2])
        self.assertEqual(d['Child'].message, None)
        self.assertEqual(len(d['Child'].children), 2)
        self.assertEqual(d['Child'].children[0].message, m1)


if __name__ == "__main__":
    unittest.main()
