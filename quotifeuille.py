"""Automatic generation of tables in latex allowing one to enforce its habits.

"""


import argparse


def parse_cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--columns', '-c', nargs='+', default=('work', 'read', 'code'),
                        help='columns to show in each table')
    parser.add_argument('--tables', '-t', help='number of table per page', default=3)
    parser.add_argument('--lines', '-l', help='number of lines per table', default=56)
    parser.add_argument('--padding', '-p', default=0.05,
                        help='ratio of the page dedicated to space between tables')
    parser.add_argument('--output', '-o', help='name of the output tex file',
                        default='tables.tex')
    return parser.parse_args()


LATEX_TEMPLATE = r"""
\documentclass[10pt]{{article}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{fca}}
\usepackage[top=0.25in, bottom=.2in, left=.2in, right=.2in]{{geometry}}
\pagenumbering{{gobble}}

\begin{{document}}
\begin{{center}}
{content}
\end{{center}}
\end{{document}}
"""
LATEX_TEMPLATE_COLUMN = r"""\begin{{minipage}}{{{col_width}\textwidth}}
\begin{{center}}
\begin{{cxt}}%
    \cxtName{{{name}}}%
    {attributes}
    {objects}
\end{{cxt}}
\end{{center}}
\end{{minipage}}%"""
LATEX_TEMPLATE_OBJECT = r"""\obj{{{points}}}{{\quad/\quad/\quad}}"""
LATEX_TEMPLATE_ATTR = r"""\atr{{{attr}}}"""


DEFAULT_CONTEXT_NAME = ['\quad\quad\quad\quad']


def build_page(columns, line_per_page, context_names=DEFAULT_CONTEXT_NAME,
               col_padding:float=0.05) -> str:
    """Return latex code describing a page"""
    col_joiner = '\n    '
    col_width=round(100 // len(context_names) + col_padding / 2) / 100
    return LATEX_TEMPLATE.format(
        content=col_joiner.join(build_column(context_name, columns, line_per_page, col_width)
                                for context_name in context_names)
    )


def build_column(context_name, columns, line_per_page, col_width):
    line_joiner = '\n    '
    return LATEX_TEMPLATE_COLUMN.format(
        name=context_name,
        attributes=line_joiner + line_joiner.join(build_attributes(columns)),
        objects=line_joiner + line_joiner.join(build_objects(line_per_page, len(columns))),
        col_width=col_width,
    )

def build_objects(count:int, nb_attr:int) -> str:
    for _ in range(count):
        yield LATEX_TEMPLATE_OBJECT.format(points='.' * nb_attr)

def build_attributes(attrs:tuple) -> str:
    for attr in attrs:
        yield LATEX_TEMPLATE_ATTR.format(attr=attr)


def write_page(outfile:str, columns, line_per_page, context_names, col_padding):
    with open(outfile, 'w') as fd:
        fd.write(build_page(
            columns=columns,
            line_per_page=line_per_page,
            context_names=context_names,
            col_padding=col_padding,
        ))


if __name__ == "__main__":
    args = parse_cli()
    write_page(args.output, args.columns, args.lines, DEFAULT_CONTEXT_NAME * args.tables, args.padding)
