from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode

def main():
    test_text = TextNode("Let me Google that for you", TextType.LINK, "https://google.com")
    print(TextType.LINK.value)
    print(test_text)
    test_childnode = HTMLNode("b", "HTML")
    test_HTML = HTMLNode("p", "This is a paragraph of HTML Text.", [test_childnode])
    print(test_HTML)
    test_HTML2 = HTMLNode("a", "A link to Google", None, { "href" : "https://google.com" })
    print(test_HTML2)
    print(test_HTML2.props_to_html())

main()
