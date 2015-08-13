from elasticsearch_dsl import DocType, Index, String

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
