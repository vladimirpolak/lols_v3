from ._scraper_base import ExtractorBase
from downloader.types import determine_content_type_, img_extensions
from utils import split_filename_ext
import re

# Regex Patterns
PATTERN_IMGBOX_IMAGE_TH = rf"((?:https?://)?thumbs\d+\.imgbox\.com/[a-z\d]+/[a-z\d]+/[\d\w]+_t(?:{'|'.join(img_extensions)}))"


class IMGBoxImageExtractor(ExtractorBase):
    NEXT_PAGE = None
    VALID_URL_RE = re.compile(PATTERN_IMGBOX_IMAGE_TH)
    PROTOCOL = "https"
    DOMAIN = "imgbox.com"
    DESC = "ImgBox Extract From Thumbnail"
    CONTENT_TYPE = "ITEM"
    SAMPLE_URLS = [
        "https://thumbs2.imgbox.com/76/51/0MgDRXNo_t.png",
        "https://thumbs2.imgbox.com/72/95/VL9wS1tI_t.jpeg",
        "https://thumbs2.imgbox.com/cf/a3/p807JSq5_t.jpeg",
        "https://thumbs2.imgbox.com/e1/24/f3rYiAMq_t.jpeg",
        "https://thumbs2.imgbox.com/f5/ed/a2m6ziVH_t.jpeg"
    ]

    def _extract_data(self, url):
        source = url.replace(
            "thumbs", "images", 1
        ).replace(
            "_t.", "_o.", 1
        )
        file = source.split("/")[-1]
        filename, extension = split_filename_ext(file)
        content_type = determine_content_type_(extension)

        self.add_item(
            source=source,
            content_type=content_type,
            filename=filename,
            extension=extension
        )

    @classmethod
    def _extract_from_html(cls, html):
        return [data for data in set(re.findall(cls.VALID_URL_RE, html))]
