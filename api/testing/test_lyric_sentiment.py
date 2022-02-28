import unittest

from sentiment.sentiment_analyser import calc


class TestLyricSentiment(unittest.TestCase):

    def test_sample(self):
        result = calc(10, 5)
        self.assertEqual(result, 15)


if __name__ == '__main__':
    unittest.main()

# Use below to run code in terminal
# python -m unittest test_sentiment_analyser.py
