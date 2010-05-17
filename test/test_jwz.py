#!/www/python/bin/python

"""
Test script for jwzthreading.

"""

import unittest
import jwzthreading, rfc822, StringIO

tested_modules = ["jwzthreading"]

def make_rfc822_message (S):
    input = StringIO.StringIO(S)
    return rfc822.Message(input)


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

    def test_uniq(self):
        self.assertEquals(jwzthreading.uniq((1,2,3,1,2,3)), [1,2,3])

    def test_make_message (self):
        msg_templ = """Subject: %(subject)s
Message-ID: %(msg_id)s

Message body
"""
        m = make_rfc822_message("""Subject: random

Body.""")
        self.assertRaises(ValueError, jwzthreading.make_message, m)

    def test_basic_message(self):
        msg = make_rfc822_message("""Subject: random
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
