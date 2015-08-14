from elasticsearch_dsl import DocType, Index, String
from django.core.urlresolvers import reverse

visnyk_index = Index('visnyk')

visnyk_index.settings(
    index={
        "analysis": {
            "filter": {
                "lemmagen_filter_uk": {
                    "type": "lemmagen",
                    "lexicon": "uk"
                }
            },
            "analyzer": {
                "html_uk_analyzer": {
                    "type": "custom",
                    "tokenizer": "uax_url_email",
                    "filter": ["lemmagen_filter_uk", "lowercase", "stop"],
                    "char_filter": ["html_strip"]
                }
            }
        }
    }
)


@visnyk_index.doc_type
class VisnykDocument(DocType):
    """Visnyk document."""
    plain_content = String(analyzer="html_uk_analyzer")
    goods_name = String(analyzer="html_uk_analyzer")
    cust_name = String(analyzer="html_uk_analyzer")

    def get_absolute_url(self):
        return reverse("preview", kwargs={"doc_id": self._id})
