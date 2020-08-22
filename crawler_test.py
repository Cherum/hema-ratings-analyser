import unittest
import crawler

class TestCrawler(unittest.TestCase):

    def test_isValidConfidence(self):
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.HIGH, "nonsense"), False)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.HIGH, "High"), True)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.HIGH, "Medium"), False)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.HIGH, "Low"), False)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.HIGH, "Inactive"), False)

        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.MEDIUM, "nonsense"), False)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.MEDIUM, "High"), True)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.MEDIUM, "Medium"), True)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.MEDIUM, "Low"), False)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.MEDIUM, "Inactive"), False)

        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.ALL, "nonsense"), False)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.ALL, "High"), True)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.ALL, "Medium"), True)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.ALL, "Low"), True)
        self.assertEqual(crawler.isValidConfidence(crawler.ConfidenceLevel.ALL, "Inactive"), True)

if __name__ == '__main__':
    unittest.main()
