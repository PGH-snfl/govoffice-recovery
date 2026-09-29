"""Shared table paragraph metrics for layout and size estimates (HWP units)."""
import re
import unicodedata

LIST_PREFIX=re.compile(r'^(?:[-•·○▪]|\d{1,2}[.)]|[가-힣][.)])\s+')


def paragraph_gap(font_height,review=False):
    # A small gap, not an extra blank line in a size-limited cell.
    return min(80,int(font_height*.06)) if review else min(200,int(font_height*.16))


def list_indent(value,font_height):
    match=LIST_PREFIX.match(value)
    if not match:return 0
    units=sum(1 if unicodedata.east_asian_width(c) in 'WF' else .6 for c in match.group())
    return int(units*font_height)
