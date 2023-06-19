import re


def pretty_print(node, indent=0):
    print("  " * indent + str(node.type) + " " + str(node.field))
    for child in node.nodes:
        pretty_print(child, indent + 1)


def get_text(ast):
    if ast.type == "CONTENT":
        return ast.field
    return ''.join([get_text(child) for child in ast.nodes])


def get_title(ast):
    if (ast.type == "OP") and (ast.field == "title"):
        return get_text(ast)
    if (ast.type == "CONTENT"):
        return None

    for child in ast.nodes:
        found = get_title(child)
        if found:
            return found


def get_offset(text):
    try:
        match_divider = re.search(r'---\s*\n*', text)
        start_index = match_divider.end()
        lines_before = text[:start_index].count('\n')
        return lines_before
    except:
        raise SyntaxError("No --- found!")


def separate(text):
    try:
        match = re.search(r'^(.*?)---(.*?)$', text, re.DOTALL)
        header, body = match.group(1), match.group(2)
        offset = get_offset(text)
        return header, body, offset
    except:
        raise SyntaxError(
            "There must be a header and a body, separated by ---")
