import os
import shutil
import os.path
from subprocess import Popen
from tempfile import mkdtemp

import html2text
from lxml import etree
from elasticsearch_dsl import Index

from django.core.management.base import BaseCommand
from django.conf import settings

from finder.elastic_models import VisnykDocument


class ConvertException(Exception):
    def __init__(self, stdout, stderr, *args, **kwargs):
        super(ConvertException, self).__init__(*args, **kwargs)

        self.stderr = stderr
        self.stdout = stdout


class Command(BaseCommand):
    args = "<path path ...>"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.html2text = html2text.HTML2Text()
        self.html2text.ignore_images = True
        self.html2text.ignore_links = True

    def convert_to_json_doc(self, doc, ext):
        xml = etree.parse(doc + ".xml")
        out_doc = {el.tag.lower(): el.text for el in xml.getroot()}

        try:
            dr = mkdtemp()
            outfile = os.path.join(dr, os.path.basename(doc) + ".html")

            if ext == ".pdf":
                pr = Popen([settings.PDF_TO_HTML_BIN, "-s", "-noframes",
                            "{0}{1}".format(doc, ext), outfile])
            else:
                pr = Popen([settings.SOFFICE_BIN, "--headless", "--convert-to",
                            "html", "--outdir", dr, "{0}{1}".format(doc, ext)])

            stdout, stderr = pr.communicate()

            if not os.path.exists(outfile):
                raise ConvertException(stdout=stdout, stderr=stderr)

            with open(outfile, "r") as fp:
                content = fp.read()

            plain_content = self.html2text.handle(content)

            if len(plain_content) < 100:
                self.stderr.write(
                    "{0}{1} looks like a scan".format(doc, ext))
                return False

            out_doc["content"] = content
            return out_doc
        finally:
            shutil.rmtree(dr)

    def handle(self, *args, **options):
        VisnykDocument.init()

        for arg in args:
            for root, _, files in os.walk(arg, topdown=True):
                for fl in files:
                    fname, ext = os.path.splitext(fl)

                    if ext.lower() in [".xml", ""]:
                        continue

                    basename = os.path.join(root, fname)

                    if not os.path.exists(basename + ".xml"):
                        self.stderr.write(
                            'Cannot find "{0}.xml", skipping'.format(basename))
                        continue

                    try:
                        doc = self.convert_to_json_doc(basename, ext)
                        if doc:
                            doc["_id"] = fname

                            el_doc = VisnykDocument(**doc)
                            el_doc.save()

                    except ConvertException:
                        self.stderr.write("Cannot convert {0}".format(fl))
