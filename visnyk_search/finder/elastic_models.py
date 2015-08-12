from elasticsearch_dsl import DocType


class VisnykDocument(DocType):
    """Visnyk document."""

    class Meta:
        index = 'visnyk'
