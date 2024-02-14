from filer.models.filemodels import File
from markdown import Extension
from markdown.inlinepatterns import IMAGE_LINK_RE, ImageInlineProcessor
from markdown.util import etree


class FilerExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add(
            "filer_image_link",
            FilerImagePattern(IMAGE_LINK_RE, md),
            "<image_link",
        )


class FilerImagePattern(ImageInlineProcessor):
    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        if not src.startswith("filer:"):
            return None, None, None

        filer_id = src.split(":")[1]
        filer_file = File.objects.filter(pk=filer_id, is_public=True).first()
        if not filer_file or not filer_file.file:
            return None, None, None

        src = filer_file.canonical_url
        if not src:
            return None, None, None

        el = etree.Element("img")

        el.set("src", src)

        if title is not None:
            el.set("title", title)

        el.set("alt", self.unescape(text))
        return el, m.start(0), index


def makeExtension(**kwargs):
    return FilerExtension(**kwargs)
