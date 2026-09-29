"""Turn unambiguous generated formulas into editable HWP equation controls.

Only compact algebraic assignments are inferred from prose. Fixed template text,
ordinary comparisons such as Q=10, and expressions too wide for their cell stay
as text. The equation script can be mapped back to the input for verification.
"""
import re
import xml.etree.ElementTree as ET


FORMULA = re.compile(
    r'(?<![A-Za-z0-9_/])(?:[A-Za-zΑ-Ωα-ω][A-Za-z0-9Α-Ωα-ω]*_[A-Za-z0-9]+'
    r'(?:[+\-*/×÷=][A-Za-z0-9Α-Ωα-ω_]+)+)(?![A-Za-z0-9_/(×÷+\-=])'
)
SUBSCRIPT = re.compile(r'_([A-Za-z0-9]+)')
SCRIPT_SUBSCRIPT = re.compile(r'_\{([A-Za-z0-9]+)\}')


def equation_script(source):
    return SUBSCRIPT.sub(r'_{\1}', source)


def equation_source(script):
    return SCRIPT_SUBSCRIPT.sub(r'_\1', script)


def logical_paragraph_text(paragraph):
    """Read generated equation scripts as the source text they replaced."""
    parts = []
    for run in paragraph.findall('TEXT'):
        for child in run:
            if child.tag == 'CHAR':
                parts.append(child.text or '')
            elif child.tag == 'EQUATION':
                parts.append(equation_source(child.findtext('SCRIPT') or ''))
    return ''.join(parts)


def _available_width(root, paragraph, parents):
    node = paragraph
    while id(node) in parents:
        node = parents[id(node)]
        if node.tag == 'CELL':
            width = int(node.get('Width', '0') or 0)
            margin = node.find('CELLMARGIN')
            if margin is not None:
                width -= sum(int(margin.get(side, '0')) for side in ('Left', 'Right'))
            return max(0, width)
    page = root.find('.//PAGEDEF')
    if page is None:
        return 0
    width = int(page.get('Width', '0') or 0)
    margin = page.find('PAGEMARGIN')
    if margin is not None:
        width -= sum(int(margin.get(side, '0')) for side in ('Left', 'Right', 'Gutter'))
    return max(0, width)


def format_equations(root, refs):
    """Replace equation spans only in paragraphs written by this job."""
    parents = {id(child): parent for parent in root.iter() for child in parent}
    shapes = {shape.get('Id'): shape for shape in root.iter('CHARSHAPE')}
    instance_ids = [int(node.get('InstId')) for node in root.iter()
                    if (node.get('InstId') or '').isdigit()]
    next_id = max(instance_ids, default=0) + 1
    counts = {}
    for _, paragraphs, _ in refs:
        for paragraph in paragraphs:
            count = 0
            available = _available_width(root, paragraph, parents)
            for run in paragraph.findall('TEXT'):
                shape = shapes.get(run.get('CharShape'))
                height = int(shape.get('Height', '1000')) if shape is not None else 1000
                for char in list(run):
                    if char.tag != 'CHAR' or not char.text:
                        continue
                    value = char.text
                    replacements = []
                    offset = 0
                    for match in FORMULA.finditer(value):
                        source = match.group()
                        # Equation objects cannot wrap inside narrow cells. Keep
                        # the original text when the estimated object would clip.
                        width = max(height * 2, int(len(source) * height * .66))
                        if not available or width > available * .85:
                            continue
                        if match.start() > offset:
                            replacements.append(ET.Element('CHAR'))
                            replacements[-1].text = value[offset:match.start()]
                        equation = ET.Element('EQUATION', {
                            'LineMode': 'false', 'BaseUnit': str(height),
                            'TextColor': '0', 'BaseLine': '61',
                            'Version': 'Equation Version 60',
                        })
                        obj = ET.SubElement(equation, 'SHAPEOBJECT', {
                            'InstId': str(next_id), 'ZOrder': '0',
                            'NumberingType': 'Equation', 'Lock': 'false',
                        })
                        ET.SubElement(obj, 'SIZE', {
                            'Width': str(width), 'Height': str(int(height * 1.5)),
                            'WidthRelTo': 'Absolute', 'HeightRelTo': 'Absolute',
                            'Protect': 'false',
                        })
                        ET.SubElement(obj, 'POSITION', {
                            'TreatAsChar': 'true', 'AffectLSpacing': 'true',
                            'FlowWithText': 'true', 'AllowOverlap': 'false',
                            'VertRelTo': 'Para', 'VertAlign': 'Center',
                            'VertOffset': '0',
                        })
                        ET.SubElement(obj, 'OUTSIDEMARGIN', {
                            'Left': '0', 'Right': '0', 'Top': '0', 'Bottom': '0',
                        })
                        ET.SubElement(equation, 'SCRIPT').text = equation_script(source)
                        replacements.append(equation)
                        next_id += 1
                        count += 1
                        offset = match.end()
                    if not replacements:
                        continue
                    if offset < len(value):
                        tail = ET.Element('CHAR')
                        tail.text = value[offset:]
                        replacements.append(tail)
                    position = list(run).index(char)
                    run.remove(char)
                    for index, replacement in enumerate(replacements):
                        run.insert(position + index, replacement)
            counts[id(paragraph)] = count
    return counts
