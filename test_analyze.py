import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from analyze import load_orders, summarize


class SalesTests(unittest.TestCase):
    def load(self, rows):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'orders.json'
            path.write_text(json.dumps(rows))
            return load_orders(path)

    def order(self, **changes):
        return dict(order_id='O1', date='2026-01-10', product='Notebook',
                    region='East', quantity=3, unit_price='0.10', **changes)

    def test_exact_money_and_grouping(self):
        first = self.order()
        second = dict(first, order_id='O2', date='2026-02-01', quantity=2)
        total, groups = summarize(self.load([first, second]))
        self.assertEqual(total, Decimal('0.50'))
        self.assertEqual(groups['month']['2026-01'], Decimal('0.30'))
        self.assertEqual(groups['region']['East'], total)

    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.load([self.order(), self.order()])

    def test_bad_inputs_rejected(self):
        for changes in ({'quantity': -1}, {'unit_price': 'NaN'},
                        {'unit_price': '1.001'}, {'date': 'bad'}, {'product': ''}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.load([dict(self.order(), **changes)])
        with self.assertRaises(ValueError):
            self.load([])


if __name__ == '__main__':
    unittest.main()
