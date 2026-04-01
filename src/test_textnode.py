import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("test", TextType.ITALIC, None)
        node4 = TextNode("test", TextType.ITALIC)
        self.assertEqual(node3, node4)
        self.assertNotEqual(node, node3)

        node5 = TextNode("test", TextType.BOLD)
        self.assertNotEqual(node4, node5)

    def test_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()