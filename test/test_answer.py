#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals
import unittest
import os

from zhihu import Answer
from zhihu.common import BeautifulSoup
from test_utils import TEST_DATA_PATH


class AnswerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url = 'http://www.zhihu.com/question/24825703/answer/30975949'
        file_path = os.path.join(TEST_DATA_PATH, 'answer.html')
        with open(file_path, 'rb') as f:
            html = f.read()
        soup = BeautifulSoup(html)

        answer_saved_path = os.path.join(TEST_DATA_PATH, 'answer.md')
        with open(answer_saved_path, 'rb') as f:
            cls.answer_saved = f.read()

        cls.answer = Answer(url)
        cls.answer._session = None
        cls.answer.soup = soup
        cls.expected = {'id': 30975949, 'aid': 7775236,
                        'xsrf': 'cfd489623d34ca03adfdc125368c6426',
                        'html': soup.prettify(), 'author_id': 'tian-ge-xia',
                        'author_name': '甜阁下', 'question_id': 24825703,
                        'question_title': '关系亲密的人之间要说「谢谢」吗？',
                        'upvote_num': 1164}

    def test_id(self):
        self.assertEqual(self.expected['id'], self.answer.id)

    def test_aid(self):
        self.assertEqual(self.expected['aid'], self.answer.aid)

    def test_xsrf(self):
        self.assertEqual(self.expected['xsrf'], self.answer.xsrf)

    def test_html(self):
        self.assertEqual(self.expected['html'], self.answer.html)

    def test_upvote_num(self):
        self.assertEqual(self.expected['upvote_num'], self.answer.upvote_num)

    def test_author(self):
        self.assertEqual(self.expected['author_id'], self.answer.author.id)
        self.assertEqual(self.expected['author_name'], self.answer.author.name)

    def test_question(self):
        self.assertEqual(self.expected['question_id'], self.answer.question.id)
        self.assertEqual(self.expected['question_title'],
                         self.answer.question.title)

    def test_content(self):
        path = os.path.join(TEST_DATA_PATH, 'answer_content.html')
        with open(path, 'rb') as f:
            content = f.read()
        self.assertEqual(content.decode('utf-8'), self.answer.content)

    def test_save(self):
        save_name = 'answer_save'
        self.answer.save(filepath=TEST_DATA_PATH, filename=save_name,
                         mode='md')
        answer_saved_path = os.path.join(TEST_DATA_PATH, save_name + '.md')
        with open(answer_saved_path, 'rb') as f:
            answer_saved = f.read()
        os.remove(answer_saved_path)
        self.assertEqual(self.answer_saved, answer_saved)
