from xml.etree.ElementTree import Element
from filer.models.filemodels import File
from markdown import Extension
from markdown.inlinepatterns import IMAGE_LINK_RE, ImageInlineProcessor

class FilerExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            FilerImagePattern(IMAGE_LINK_RE, md), "filer_image_link", 151
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

        img = Element("img")
        img.set("src", src)
        img.set("alt", self.unescape(text))
        if title is not None:
            img.set("title", title)

        return img, m.start(0), index


def makeExtension(**kwargs):
    return FilerExtension(**kwargs)
