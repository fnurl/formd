# coding=utf8
"""formd is a tool for conversion between inline and referenced markdown style.

formd is a tool for (for)matting (M)ark(d)own that allows rapid conversion
between the two styles of Markdown links and images--inline and referenced.

Author: Seth Brown
Date: 2012-02-24
"""
from sys import stdin, stdout
from collections import OrderedDict
import argparse
import re


class ForMd(object):
    """Format Markdown text."""

    def __init__(self, text):
        """Initialize ForMd object."""
        super(ForMd, self).__init__()
        self.text = text
        self.match_links = re.compile(r"""(\[[^^\[\]:]*?\])\s?? # text
                                      (\[[^\[\]:]*?\]|          # ref
                                      \(.*?\r?\n?.*?\)\)?)      # url
                                      """, re.MULTILINE | re.X)
        self.match_refs = re.compile(r'(?<=\n)\s?.*\[[^^\r?\n]*?\]:\s?.*')
        self.data = []

    def _links(self):
        """Find Markdown links."""
        links = re.findall(self.match_links, self.text)
        for (text, ref) in links:
            ref = ref.replace('\n', '').replace('\r', '')
            yield (text, ref)

    def _refs(self):
        """Find Markdown references."""
        refs = re.findall(self.match_refs, self.text)
        refs = sorted([_.lstrip().replace('\n', '').replace('\r', '')
                      for _ in refs])
        refs = OrderedDict(i.split(":", 1) for i in refs)
        return refs

    def _format(self):
        """Process text."""
        links = (i for i in self._links())
        refs = self._refs()
        for n, link in enumerate(links):
            text, ref = link
            ref_num = ''.join(("[", str(n+1), "]: "))
            if ref in refs.keys():
                url = refs.get(ref).strip()
                formd_ref = ''.join((ref_num, url))
                formd_text = ''.join((text, ref_num))
                self.data.append([formd_text, formd_ref])
            elif text in refs.keys():
                url = refs.get(text).strip()
                formd_ref = ''.join((ref_num, url))
                formd_text = ''.join((text, ref_num))
                self.data.append([formd_text, formd_ref])
            elif ref not in refs.keys():
                # remove the leading/training parens
                parse_ref = ref[1:-1]
                formd_ref = ''.join((ref_num, parse_ref))
                formd_text = ''.join((text, ref_num))
                self.data.append([formd_text, formd_ref])

    def inline_md(self):
        """Generate inline Markdown."""
        self._format()
        text_link = iter([''.join((_[0].split(
                            "][", 1)[0],
                            "](",
                            _[1].split(":", 1)[1].strip(), ")")
                        ) for _ in self.data])
        formd_text = self.match_links.sub(lambda _: next(text_link), self.text)
        formd_md = self.match_refs.sub('', formd_text).strip()
        yield formd_md

    def ref_md(self):
        """Generate referenced Markdown."""
        self._format()
        ref_nums = iter([_[0].rstrip(" :") for _ in self.data])
        formd_text = self.match_links.sub(lambda _: next(ref_nums), self.text)
        formd_refs = self.match_refs.sub('', formd_text).strip()
        references = (i[1] for i in self.data)
        formd_md = '\n'.join((formd_refs,
                              '\n', '\n'.join(i for i in references)))
        yield formd_md

    def flip(self):
        """Convert Markdown to the opposite style of the first text link."""
        try:
            first_match = re.search(self.match_links, self.text).group(0)
            if first_match is None or first_match == []:
                formd_md = self.text
            elif '(' and ')' in first_match:
                formd_md = self.ref_md()
            else:
                formd_md = self.inline_md()
        except AttributeError:
            formd_md = self.text
        return formd_md
