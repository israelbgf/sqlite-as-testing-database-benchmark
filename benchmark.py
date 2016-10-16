import sys
import unittest
import os
from datetime import datetime
from unittest import TestCase, TextTestRunner

from sqlalchemy import create_engine, select

from schema import metadata


class SQLiteTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        if not hasattr(cls, 'engine'):
            cls.engine = create_engine('sqlite:///:memory:')
            metadata.create_all(bind=cls.engine)

    def setUp(self):
        self.conn = self.engine.connect()
        self.transaction = self.conn.begin()

    def tearDown(self):
        self.transaction.rollback()


NOW = datetime.today()


class SampleTest(SQLiteTestCase):
    def test_foo(self):
        for i in range(0, os.environ.get('NUMBER_OF_OPERATIONS', 10)):
            table = metadata.tables['sample_table_{}'.format(i)]
            self.conn.execute(table.insert().values({
                'a1': 'foo',
                'a2': 'foo',
                'a3': 'foo',
                'a4': 'foo',
                'a5': 'foo',
                'a6': 'foo',
                'a7': 'foo',
                'a8': 'foo',
                'a9': 'foo',
                'date': NOW,
            }))

            self.assertEqual(1, len(self.conn.execute(select([table])).fetchall()))


def run_benchmark():
    suite = unittest.TestSuite()
    number_of_tests = sys.argv[1]
    for i in range(int(number_of_tests)):
        suite.addTest(SampleTest('test_foo'))
    TextTestRunner().run(suite)


if __name__ == '__main__':
    run_benchmark()
