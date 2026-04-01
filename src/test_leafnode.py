import unittest
from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode(value="Hello, world!", tag="p")
        self.assertEqual(node.to_html(), node2.to_html())


if __name__ == "__main__":
    unittest.main()