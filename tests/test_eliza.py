# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2021 Neongecko.com Inc.
# BSD-3
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import unittest
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from eliza import Eliza


class ElizaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.eliza = Eliza()
        cls.eliza.load(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'eliza', 'doctor.txt'))

    def test_decomp_1(self):
        self.assertEqual([], self.eliza._match_decomp(['a'], ['a']))
        self.assertEqual([], self.eliza._match_decomp(['a', 'b'], ['a', 'b']))

    def test_decomp_2(self):
        self.assertIsNone(self.eliza._match_decomp(['a'], ['b']))
        self.assertIsNone(self.eliza._match_decomp(['a'], ['a', 'b']))
        self.assertIsNone(self.eliza._match_decomp(['a', 'b'], ['a']))
        self.assertIsNone(self.eliza._match_decomp(['a', 'b'], ['b', 'a']))

    def test_decomp_3(self):
        self.assertEqual([['a']], self.eliza._match_decomp(['*'], ['a']))
        self.assertEqual([['a', 'b']], self.eliza._match_decomp(['*'], ['a', 'b']))
        self.assertEqual([['a', 'b', 'c']],
                         self.eliza._match_decomp(['*'], ['a', 'b', 'c']))

    def test_decomp_4(self):
        self.assertEqual([], self.eliza._match_decomp([], []))
        self.assertEqual([[]], self.eliza._match_decomp(['*'], []))

    def test_decomp_5(self):
        self.assertIsNone(self.eliza._match_decomp(['a'], []))
        self.assertIsNone(self.eliza._match_decomp([], ['a']))

    def test_decomp_6(self):
        self.assertEqual([['0']], self.eliza._match_decomp(['*', 'a'], ['0', 'a']))
        self.assertEqual([['0', 'a']],
                         self.eliza._match_decomp(['*', 'a'], ['0', 'a', 'a']))
        self.assertEqual([['0', 'a', 'b']],
                         self.eliza._match_decomp(['*', 'a'], ['0', 'a', 'b', 'a']))
        self.assertEqual([['0', '1']],
                         self.eliza._match_decomp(['*', 'a'], ['0', '1', 'a']))

    def test_decomp_7(self):
        self.assertEqual([[]], self.eliza._match_decomp(['*', 'a'], ['a']))

    def test_decomp_8(self):
        self.assertIsNone(self.eliza._match_decomp(['*', 'a'], ['a', 'b']))
        self.assertIsNone(self.eliza._match_decomp(['*', 'a'], ['0', 'a', 'b']))
        self.assertIsNone(self.eliza._match_decomp(['*', 'a'], ['0', '1', 'a', 'b']))

    def test_decomp_9(self):
        self.assertEqual([['0'], ['b']],
                         self.eliza._match_decomp(['*', 'a', '*'], ['0', 'a', 'b']))
        self.assertEqual([['0'], ['b', 'c']],
                         self.eliza._match_decomp(['*', 'a', '*'],
                                          ['0', 'a', 'b', 'c']))

    def test_decomp_10(self):
        self.assertEqual([['0'], []],
                         self.eliza._match_decomp(['*', 'a', '*'], ['0', 'a']))
        self.assertEqual([[], []], self.eliza._match_decomp(['*', 'a', '*'], ['a']))
        self.assertEqual([[], ['b']],
                         self.eliza._match_decomp(['*', 'a', '*'], ['a', 'b']))

    def test_syn_1(self):
        self.assertEqual([['am']], self.eliza._match_decomp(['@be'], ['am']))
        self.assertEqual([['am']], self.eliza._match_decomp(['@be', 'a'], ['am', 'a']))
        self.assertEqual([['am']],
                         self.eliza._match_decomp(['a', '@be', 'b'], ['a', 'am', 'b']))

    def test_syn_2(self):
        self.assertIsNone(self.eliza._match_decomp(['@be'], ['a']))

    def test_syn_3(self):
        self.assertIsNotNone(
            self.eliza._match_decomp(['*', 'i', 'am', '@sad', '*'],
                             ['its', 'true', 'i', 'am', 'unhappy']))

    def test_response_1(self):
        self.assertEqual('In what way ?', self.eliza.respond('Men are all alike.'))
        self.assertEqual(
            'Can you think of a specific example ?',
            self.eliza.respond('They\'re always bugging us about something or other.'))
        self.assertEqual('Your boyfriend made you come here ?',
                         self.eliza.respond('Well, my boyfriend made me come here.'))
        self.assertEqual(
            'I am sorry to hear that you are depressed .',
            self.eliza.respond('He says I\'m depressed much of the time.'))
        self.assertEqual(
            'Do you think that coming here will help you not to be unhappy ?',
            self.eliza.respond('It\'s true. I am unhappy.'))
        self.assertEqual(
            'What would it mean to you if you got some help ?',
            self.eliza.respond('I need some help, that much seems certain.'))
        self.assertEqual(
            'Tell me more about your family.',
            self.eliza.respond('Perhaps I could learn to get along with my mother.'))
        self.assertEqual('Who else in your family takes care of you ?',
                         self.eliza.respond('My mother takes care of me.'))
        self.assertEqual('Your father ?', self.eliza.respond('My father.'))
        self.assertEqual('What resemblence do you see ?',
                         self.eliza.respond('You are like my father in some ways.'))
        self.assertEqual(
            'What makes you think I am not very aggressive ?',
            self.eliza.respond(
                'You are not very aggressive, but I think you don\'t want me to notice that.'
            ))
        self.assertEqual('Why do you think I don\'t argue with you ?',
                         self.eliza.respond('You don\'t argue with me.'))
        self.assertEqual('Does it please you to believe I am afraid of you ?',
                         self.eliza.respond('You are afraid of me.'))
        self.assertEqual(
            'What else comes to mind when you think of your father ?',
            self.eliza.respond('My father is afraid of everybody.'))
        self.assertIn(
            self.eliza.respond('Bullies.'), [
                'Lets discuss further why your boyfriend made you come here .',
                'Earlier you said your mother .',
                'But your mother takes care of you .',
                'Does that have anything to do with the fact that your boyfriend made you come here ?',
                'Does that have anything to do with the fact that your father ?',
                'Lets discuss further why your father is afraid of everybody .',
            ])

    def test_response_2(self):
        self.assertEqual(self.eliza.initial(), 'How do you do.  Please tell me your problem.')
        self.assertIn(self.eliza.respond('Hello'), [
            'How do you do. Please state your problem.',
            'Hi. What seems to be your problem ?'])
        self.assertEqual(self.eliza.final(), 'Goodbye.  Thank you for talking to me.')


if __name__ == '__main__':
    unittest.main()
