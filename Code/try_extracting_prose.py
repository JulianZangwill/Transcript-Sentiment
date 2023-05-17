from pathlib import Path
from typing import Iterable, Any
import finbert
import pandas as pd

from pdfminer.high_level import extract_pages


def show_ltitem_hierarchy(o: Any, input):
    """Show location and text of LTItem and all its descendants"""  
    result = input
    if o.__class__.__name__ == 'LTTextLineHorizontal':
        result += '\n'

    if o.__class__.__name__ == 'LTChar':
        if hasattr(o, 'fontname') and o.fontname == 'EAAAAA+Verdana':
            if hasattr(o, 'size') and round(o.size) == 10:
                result += o.get_text()

    if isinstance(o, Iterable):

        for i in o:
            result += show_ltitem_hierarchy(i, input)

 
    return result


