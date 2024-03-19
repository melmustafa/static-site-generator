class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        html_props = ""
        for attribute in self.props:
            html_props += f' {attribute}="{self.props[attribute]}"'
        return html_props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None) -> None:
        if value is None:
            raise ValueError("Invalid HTML: value is required")
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str = None, children: list = None, props: dict = None
    ) -> None:
        if tag is None:
            raise ValueError("Invalid HTML: tag is required")
        if children is None:
            raise ValueError("Invalid HTML: children is required")
        if len(children) == 0:
            raise ValueError("Invalid HTML: children is empty")
        super().__init__(tag, None, children, props)

    def to_html(self):
        try:
            raw_html = ""
            for child in self.children:
                raw_html += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{raw_html}</{self.tag}>"
        except Exception:
            raise TypeError("Invalid HTML: children type must be of LeafNode")
