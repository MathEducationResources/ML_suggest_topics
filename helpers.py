def find_math_words(text):
    math_words = ''
    if '\\int' in text:
        math_words += ' integral'
    if '\\lim' in text:
        math_words += ' limit'
    if '\\sum' in text:
        math_words += ' sum'
    if '\\infty' in text:
        math_words += ' infinity'
    if '{matrix}' in text or '{pmatrix}' in text or '{bmatrix}' in text:
        math_words += ' matrix'
    if '{array}' in text:
        math_words += ' array'
    if '\\exp' in text or 'e^' in text:
        math_words += ' exponential'
    if 'ln(' in text or 'log(' in text:
        math_words += ' log'
    if '\\sqrt' in text:
        math_words += ' square root'
    if '\\frac' in text:
        math_words += ' fraction'
    if '\\sin' in text:
        math_words += ' sine'
    if '\\cos' in text:
        math_words += ' cosine'
    if '\\tan' in text:
        math_words += ' tangent'
    if '\\arctan' in text:
        math_words += ' arctangent'
    if '\\pi' in text:
        math_words += ' pi'
    if '\\partial' in text:
        math_words += ' partial'
    if '\\Delta' in text:
        math_words += ' delta'
    if '\\geq' in text or '\\leq':
        math_words += ' greater than'
    if '\\cdot' in text:
        math_words += ' cdot'
    if '\\subset' in text or '\\subseteq' in text:
        math_words += ' subset'
    if ('\\cup' in text or '\\cap' in text
            or '\\bigcup' in text or '\\bigcap' in text):
        math_words += ' cup'
    if '\\epsilon' in text or '\\varepsilon' in text:
        math_words += ' epsilon'
    if '\\inf' in text:
        math_words += ' infimum'
    if '\\sup' in text:
        math_words += ' supremum'
    if '\\min' in text:
        math_words += ' minimum'
    if '\\max' in text:
        math_words += ' maximum'
    if '\\det' in text:
        math_words += ' determinant'
    if '^T' in text:
        math_words += ' transpose'
    if '\\mod' in text:
        math_words += ' modulo'

    return math_words
