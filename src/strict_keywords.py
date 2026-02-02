"""
STRICT Topic Keywords for GCSE Maths OCR Detection
VETTED BY USER - These keywords are HIGHLY SPECIFIC to each topic to avoid false positives.
Each topic has PRIMARY keywords (must match) and CONTEXT keywords (supporting evidence).
"""

STRICT_TOPIC_KEYWORDS = {
    # 1 - Number
    "number": {
        "primary": ["hcf", "lcm", "prime factor", "prime factorisation", "highest common factor",
                   "lowest common multiple", "product of primes", "factor tree",
                   "venn diagram for factors", "express as product of primes"],
        "context": ["prime", "factor", "multiple", "divisible", "integer", "index", "indices"],
        "exclude": ["probability", "tree diagram", "frequency"]
    },

    # 2 - Angles
    "angles": {
        "primary": ["angles in a triangle", "angles in a polygon", "interior angle", "exterior angle", "angle",
                   "parallel lines", "alternate angles", "corresponding angles", "co-interior angles",
                   "vertically opposite", "bearing", "three-figure bearing", "angles on a straight line",
                   "angles around a point", "isosceles triangle angles"],
        "context": ["degree", "polygon", "triangle", "parallel", "perpendicular", "protractor"],
        "exclude": ["angle of elevation", "angle of depression", "trigonometry", "sin", "cos", "tan"]
    },

    # 3 - Scatter Graphs
    "scatter graphs": {
        "primary": ["scatter graph", "scatter diagram", "scatter plot", "line of best fit", "scatter",
                   "correlation", "positive correlation", "negative correlation", "no correlation",
                   "strong correlation", "weak correlation"],
        "context": ["outlier", "trend", "relationship", "bivariate", "plot the points"],
        "exclude": []
    },

    # 4 - Fractions
    "fractions": {
        "primary": ["fraction", "mixed number", "improper fraction", "numerator", "denominator",
                   "equivalent fraction", "simplify the fraction", "common denominator",
                   "add fractions", "subtract fractions", "multiply fractions", "divide fractions",
                   "reciprocal of a fraction", "fraction of an amount"],
        "context": ["simplest form", "top-heavy", "cancel", "lowest terms"],
        "exclude": ["algebraic fraction"]
    },

    # 5 - Expressions and Sequences
    "expressions and sequences": {
        "primary": ["nth term", "sequence", "arithmetic sequence", "geometric sequence",
                   "term-to-term", "position-to-term", "common difference", "common ratio",
                   "next term", "find an expression for the nth term", "linear sequence",
                   "quadratic sequence", "first term", "second difference"],
        "context": ["pattern", "algebra", "expression", "term"],
        "exclude": []
    },

    # 6 - Coordinates
    "coordinates": {
        "primary": ["coordinate", "coordinates", "midpoint", "distance between two points",
                   "x-coordinate", "y-coordinate", "plot the point", "midpoint formula",
                   "distance formula"],
        "context": ["axis", "origin", "quadrant", "grid"],
        "exclude": ["gradient", "equation of a line", "y = mx + c"]
    },

    # 7 - Percentages
    "percentages": {
        "primary": ["percentage", "percent", "percentage increase", "percentage decrease",
                   "percentage change", "compound interest", "simple interest", "reverse percentage",
                   "original amount", "multiplier", "percentage profit", "percentage loss",
                   "express as a percentage", "percentage of"],
        "context": ["increase by", "decrease by", "vat", "discount", "deposit", "depreciation"],
        "exclude": []
    },

    # 8 - Graphs (Linear/Straight Line)
    "graphs": {
        "primary": ["y = mx + c", "gradient", "y-intercept", "equation of a line", "straight line", "straight-line",
                   "equation of the line", "straight line graph", "parallel lines gradient",
                   "perpendicular gradient", "negative reciprocal", "find the equation of"],
        "context": ["slope", "intercept", "linear", "passes through"],
        "exclude": ["quadratic", "parabola", "curve", "exponential", "reciprocal graph", "turning point"]
    },

    # 9 - Perimeter and Area
    "perimeter and area": {
        "primary": ["perimeter", "area of", "circumference", "area of a circle", "area",
                   "area of a triangle", "area of a trapezium", "area of a parallelogram",
                   "area of a sector", "arc length", "compound shape", "shaded region",
                   "area of a rectangle", "semicircle"],
        "context": ["cm²", "m²", "square units", "rectangle", "circle", "radius", "diameter"],
        "exclude": ["surface area", "volume"]
    },

    # 10 - Transformations
    "transformations": {
        "primary": ["transformation", "translation", "rotation", "reflection", "enlargement", "translation vector",
                   "describe fully the transformation", "single transformation",
                   "centre of rotation", "centre of enlargement", "scale factor",
                   "line of reflection", "mirror line", "column vector for translation",
                   "invariant point"],
        "context": ["image", "object", "clockwise", "anticlockwise"],
        "exclude": []
    },

    # 11 - Ratio
    "ratio": {
        "primary": ["ratio", "share in the ratio", "simplify the ratio", "equivalent ratio",
                   "divide in the ratio", "in the ratio", "ratio of", "simplest form ratio",
                   "parts", "unitary ratio"],
        "context": ["share", "proportion", "parts", "divide"],
        "exclude": ["trigonometric ratio"]
    },

    # 12 - Right-angled Triangles
    "right-angled triangles": {
        "primary": ["pythagoras", "pythagorean", "hypotenuse", "right-angled triangle",
                   "sin", "cos", "tan", "opposite", "adjacent", "sohcahtoa",
                   "trigonometry in right-angled triangles"],
        "context": ["angle", "triangle", "right angle"],
        "exclude": ["sine rule", "cosine rule", "area = 1/2 ab sin c"]
    },

    # 13 - Statistics
    "statistics": {
        "primary": ["mean", "median", "mode", "range", "frequency table", "grouped frequency",
                   "cumulative frequency", "box plot", "histogram", "frequency polygon",
                   "interquartile range", "quartile", "stem and leaf", "estimate the mean",
                   "frequency density", "class interval", "modal class"],
        "context": ["average", "data", "midpoint", "tally"],
        "exclude": ["probability", "tree diagram", "at random", "likely", "chance"]
    },

    # 14 - Congruence and Similarity
    "congruence and similarity": {
        "primary": ["similar", "congruent", "congruence", "similarity", "similar triangles",
                   "similar shapes", "congruent triangles", "prove congruent", "prove similar",
                   "sss", "sas", "asa", "aas", "rhs", "scale factor for area", "scale factor for volume",
                   "corresponding sides", "corresponding angles"],
        "context": ["proportional", "enlargement", "ratio of areas"],
        "exclude": []
    },

    # 15 - Equations (Linear)
    "equations": {
        "primary": ["solve the equation", "solve", "linear equation", "forming equations",
                   "rearrange", "make x the subject", "change the subject", "solve for x",
                   "unknowns on both sides"],
        "context": ["unknown", "variable", "balance"],
        "exclude": ["quadratic equation", "simultaneous", "x²"]
    },

    # 16 - Inequalities
    "inequalities": {
        "primary": ["inequality", "inequalities", "solve the inequality", "integer values",
                   "number line", "represent on a number line", "shade the region",
                   "region satisfying", "less than", "greater than", "≤", "≥", "<", ">",
                   "list the integers", "satisfy"],
        "context": ["solution set", "region"],
        "exclude": []
    },

    # 17 - Circles (Properties, not theorems)
    "circles": {
        "primary": ["radius", "diameter", "circumference", "area of a circle", "sector",
                   "arc", "arc length", "chord", "tangent to a circle", "segment",
                   "area of a sector", "perimeter of a sector", "pi", "π"],
        "context": ["circle", "semicircle", "quarter circle"],
        "exclude": ["circle theorem", "angle at centre", "cyclic quadrilateral", "angle in a semicircle"]
    },

    # 18 - Indices and Surds
    "indices and surds": {
        "primary": ["surd", "surds", "rationalise", "rationalise the denominator", "simplify the surd",
                   "index", "indices", "negative index", "fractional index", "index laws",
                   "standard form", "scientific notation", "rules of indices",
                   "simplify fully", "√"],
        "context": ["power", "root", "square root", "cube root"],
        "exclude": []
    },

    # 19 - Pythagoras Theorem
    "pythagoras theorem": {
        "primary": ["pythagoras", "pythagorean", "pythagoras' theorem", "pythagorean theorem",
                   "hypotenuse", "a² + b² = c²", "right-angled triangle",
                   "find the length", "shortest distance", "diagonal of a rectangle",
                   "3d pythagoras"],
        "context": ["right angle", "squared", "square root"],
        "exclude": []
    },

    # 20 - Trigonometry (Including Sine/Cosine Rule)
    "trigonometry": {
        "primary": ["sin", "cos", "tan", "sine", "cosine", "tangent", "trigonometry",
                   "sohcahtoa", "sine rule", "cosine rule", "area = ½ab sin c",
                   "angle of elevation", "angle of depression", "exact trigonometric values",
                   "sin⁻¹", "cos⁻¹", "tan⁻¹", "inverse trig"],
        "context": ["opposite", "adjacent", "hypotenuse", "bearing", "triangle"],
        "exclude": []
    },

    # 21 - Bounds
    "bounds": {
        "primary": ["upper bound", "lower bound", "bounds", "error interval", "truncation",
                   "truncated", "degree of accuracy", "maximum value", "minimum value",
                   "limits of accuracy", "upper and lower bounds"],
        "context": ["rounded", "accuracy", "nearest", "continuous"],
        "exclude": []
    },

    # 22 - Vectors
    "vectors": {
        "primary": ["vector", "vectors", "column vector", "magnitude", "resultant vector",
                   "position vector", "parallel vectors", "in terms of a and b",
                   "scalar multiple", "vector addition", "vector subtraction",
                   "OA", "OB", "AB", "magnitude of a vector"],
        "context": ["displacement", "direction", "parallelogram"],
        "exclude": ["translation vector"]
    },

    # 23 - Reciprocal and Exponential Graphs
    "reciprocal and exponential graphs": {
        "primary": ["reciprocal graph", "exponential graph", "y = 1/x", "y = a^x",
                   "exponential growth", "exponential decay", "asymptote",
                   "y = k/x", "hyperbola"],
        "context": ["curve", "approaches"],
        "exclude": []
    },

    # 24 - 3D Shapes and Volume
    "3d shapes and volume": {
        "primary": ["volume", "surface area", "prism", "cylinder", "cone", "sphere",
                   "pyramid", "frustum", "hemisphere", "cuboid", "volume of", "surface area of",
                   "cross-section", "cross-sectional area", "capacity"],
        "context": ["cm³", "m³", "litres", "3d", "solid", "net"],
        "exclude": []
    },

    # 25 - Probability
    "probability": {
        "primary": ["probability", "tree diagram", "probability tree", "sample space",
                   "venn diagram probability", "conditional probability", "independent events",
                   "mutually exclusive", "relative frequency", "expected frequency",
                   "P(", "at random", "picked at random", "chosen at random",
                   "without replacement", "with replacement", "probability of"],
        "context": ["bag", "counter", "counters", "marble", "marbles", "dice", "die",
                   "coin", "spinner", "card", "cards", "ball", "balls", "biased", "fair",
                   "likely", "unlikely", "certain", "impossible", "chance", "random",
                   "red", "blue", "sweets", "beads"],
        "exclude": ["frequency table", "frequency polygon", "cumulative frequency",
                   "estimate the mean", "histogram", "box plot", "median"]
    },

    # 26 - Proportion (Direct and Inverse)
    "proportion": {
        "primary": ["direct proportion", "inverse proportion", "directly proportional",
                   "inversely proportional", "constant of proportionality", "y ∝ x",
                   "y varies", "varies directly", "varies inversely", "y = kx", "y = k/x",
                   "y is proportional to"],
        "context": ["proportional", "constant", "k"],
        "exclude": []
    },

    # 27 - Loci and Constructions
    "loci and constructions": {
        "primary": ["locus", "loci", "construction", "construct", "perpendicular bisector",
                   "angle bisector", "equidistant", "compass", "compasses",
                   "construct a triangle", "bisect an angle", "perpendicular from a point",
                   "ruler and compasses"],
        "context": ["bisector", "arc", "accurately"],
        "exclude": []
    },

    # 28 - Algebraic Fractions
    "algebraic fractions": {
        "primary": ["algebraic fraction", "algebraic fractions", "simplify the algebraic fraction",
                   "single fraction", "write as a single fraction", "add algebraic fractions",
                   "subtract algebraic fractions", "multiply algebraic fractions",
                   "divide algebraic fractions"],
        "context": ["numerator", "denominator", "factorise", "common factor"],
        "exclude": []
    },

    # 29 - Quadratic Graphs
    "quadratic graphs": {
        "primary": ["quadratic graph", "parabola", "turning point", "vertex",
                   "minimum point", "maximum point", "line of symmetry", "axis of symmetry",
                   "sketch the graph of y = x²", "roots from graph", "u-shape", "n-shape",
                   "y = ax² + bx + c graph"],
        "context": ["curve", "quadratic", "intercept"],
        "exclude": ["solve the quadratic", "quadratic formula", "factorise the quadratic"]
    },

    # 30 - Circle Theorems
    "circle theorems": {
        "primary": ["circle theorem", "circle theorems", "angle at the centre",
                   "angle in a semicircle", "angles in the same segment", "cyclic quadrilateral",
                   "tangent radius", "alternate segment", "alternate segment theorem",
                   "chord perpendicular bisector", "subtended", "angle subtended"],
        "context": ["circumference", "centre", "diameter", "tangent"],
        "exclude": ["area of a circle", "circumference formula"]
    },

    # 31 - Quadratic Equations
    "quadratic equations": {
        "primary": ["quadratic equation", "solve the quadratic", "quadratic formula", "quadratic",
                   "factorise the quadratic", "completing the square", "discriminant",
                   "roots of the equation", "x² + bx + c = 0", "solutions of",
                   "factorising quadratics"],
        "context": ["factorise", "formula", "roots", "solutions"],
        "exclude": ["quadratic graph", "turning point", "sketch"]
    },

    # 32 - Simultaneous Equations
    "simultaneous equations": {
        "primary": ["simultaneous equations", "solve simultaneously", "pair of equations",
                   "elimination", "substitution method", "solve these simultaneous equations",
                   "two equations", "linear simultaneous", "one linear one quadratic"],
        "context": ["two unknowns", "x and y"],
        "exclude": []
    },

    # 33 - Functions
    "functions": {
        "primary": ["function", "f(x)", "g(x)", "composite function", "inverse function",
                   "fg(x)", "gf(x)", "f⁻¹", "f inverse", "domain", "range",
                   "composite", "inverse"],
        "context": ["input", "output", "mapping"],
        "exclude": []
    },

    # 34 - Iteration
    "iteration": {
        "primary": ["iteration", "iterative formula", "iterative method", "xₙ₊₁", "x_{n+1}",
                   "recurrence relation", "converge", "starting value", "x₀", "x₁",
                   "use iteration", "iterative process"],
        "context": ["approximate", "root", "decimal places"],
        "exclude": []
    },

    # 35 - Proof
    "proof": {
        "primary": ["prove", "proof", "show that", "hence prove", "algebraic proof",
                   "counter example", "counterexample", "prove algebraically",
                   "prove that", "always true", "never true", "sometimes true"],
        "context": ["therefore", "hence", "qed", "even", "odd", "consecutive", "integer"],
        "exclude": ["prove similar", "prove congruent"]
    },

    # 36 - Gradients and Rate of Change
    "gradients and rate of change": {
        "primary": ["rate of change", "gradient of the curve", "tangent to the curve",
                   "instantaneous rate", "average rate of change", "area under the curve",
                   "area under the graph", "estimate the gradient", "draw a tangent",
                   "gradient at a point"],
        "context": ["velocity", "acceleration", "speed-time", "distance-time"],
        "exclude": ["y = mx + c", "equation of a line"]
    },

    # 37 - Pre-calculus / Differentiation
    "pre-calculus": {
        "primary": ["differentiate", "differentiation", "derivative", "dy/dx", "d/dx",
                   "f'(x)", "gradient function", "turning point", "stationary point",
                   "find dy/dx", "rate of change"],
        "context": ["maximum", "minimum", "increasing", "decreasing"],
        "exclude": []
    },

    # 38 - Trigonometric Graphs
    "trigonometric graphs": {
        "primary": ["sin graph", "cos graph", "tan graph", "y = sin", "y = cos", "y = tan",
                   "sine graph", "cosine graph", "tangent graph", "sketch the graph of sin",
                   "sketch the graph of cos", "trig graph", "trigonometric graph",
                   "graph of y = sin x", "graph of y = cos x", "graph of y = tan x",
                   "period of sin", "period of cos", "amplitude", "y = a sin", "y = a cos",
                   "y = sin(x + ", "y = cos(x + ", "transformation of trig", "asymptote tan"],
        "context": ["periodic", "cycle", "period", "wave", "oscillation", "180", "360", "90"],
        "exclude": ["sine rule", "cosine rule", "sohcahtoa", "right-angled triangle"]
    },
}

# Mapping topic names to numbers
TOPIC_NAME_TO_NUMBER = {
    "number": 1, "angles": 2, "scatter graphs": 3, "fractions": 4,
    "expressions and sequences": 5, "coordinates": 6, "percentages": 7,
    "graphs": 8, "perimeter and area": 9, "transformations": 10,
    "ratio": 11, "right-angled triangles": 12, "statistics": 13,
    "congruence and similarity": 14, "equations": 15, "inequalities": 16,
    "circles": 17, "indices and surds": 18, "pythagoras theorem": 19,
    "trigonometry": 20, "bounds": 21, "vectors": 22,
    "reciprocal and exponential graphs": 23, "3d shapes and volume": 24,
    "probability": 25, "proportion": 26, "loci and constructions": 27,
    "algebraic fractions": 28, "quadratic graphs": 29, "circle theorems": 30,
    "quadratic equations": 31, "simultaneous equations": 32, "functions": 33,
    "iteration": 34, "proof": 35, "gradients and rate of change": 36,
    "pre-calculus": 37, "trigonometric graphs": 38
}

# Also add aliases for common topic name variations
TOPIC_ALIASES = {
    "loci": "loci and constructions",
    "constructions": "loci and constructions",
    "sine and cosine rule": "trigonometry",
    "sine rule": "trigonometry",
    "cosine rule": "trigonometry",
    "pythagoras": "pythagoras theorem",
    "differentiation": "pre-calculus",
    "volume": "3d shapes and volume",
    "surface area": "3d shapes and volume",
    "linear graphs": "graphs",
    "straight line graphs": "graphs",
    "area": "perimeter and area",
    "sequences": "expressions and sequences",
    "nth term": "expressions and sequences",
    "trig graphs": "trigonometric graphs",
    "sin cos tan graphs": "trigonometric graphs",
    "sine cosine graphs": "trigonometric graphs",
}


def get_strict_keywords(topic_name: str) -> dict:
    """Get strict keywords for a topic"""
    # Normalize topic name
    topic_lower = topic_name.lower()

    # Handle "25 - Probability" format
    if ' - ' in topic_lower:
        topic_lower = topic_lower.split(' - ', 1)[1].strip()

    # Check aliases first
    if topic_lower in TOPIC_ALIASES:
        topic_lower = TOPIC_ALIASES[topic_lower]

    # Direct match
    if topic_lower in STRICT_TOPIC_KEYWORDS:
        return STRICT_TOPIC_KEYWORDS[topic_lower]

    # Partial match
    for key in STRICT_TOPIC_KEYWORDS:
        if key in topic_lower or topic_lower in key:
            return STRICT_TOPIC_KEYWORDS[key]

    return {"primary": [], "context": [], "exclude": []}


def page_matches_topic(page_text: str, topic_name: str, debug: bool = False) -> tuple:
    """
    Check if a page matches a topic using strict keyword matching.
    Returns (matches: bool, score: int, matched_keywords: list)
    """
    text_lower = page_text.lower()
    keywords = get_strict_keywords(topic_name)

    if not keywords["primary"]:
        return (False, 0, [])

    # Count primary keyword matches (these are essential)
    primary_matches = []
    for kw in keywords["primary"]:
        if kw.lower() in text_lower:
            primary_matches.append(kw)

    # Count context keyword matches (supporting evidence)
    context_matches = []
    for kw in keywords.get("context", []):
        if kw.lower() in text_lower:
            context_matches.append(kw)

    # Scoring: Need at least 1 primary keyword to match
    # Score = (primary_matches * 3) + context_matches
    if len(primary_matches) == 0:
        return (False, 0, [])

    # Check for exclusions that should prevent matching
    excluded_count = 0
    excluded_terms = []
    for exclude in keywords.get("exclude", []):
        if exclude.lower() in text_lower:
            excluded_count += 1
            excluded_terms.append(exclude)
            if debug:
                print(f"      Found exclude term: {exclude}")

    # If more exclusions than primary matches, probably wrong topic
    if excluded_count > len(primary_matches):
        if debug:
            print(f"      REJECTED: {excluded_count} excludes > {len(primary_matches)} primary matches")
        return (False, 0, [])

    score = (len(primary_matches) * 3) + len(context_matches) - (excluded_count * 2)
    all_matches = primary_matches + context_matches

    # Minimum score threshold
    if score >= 3:
        return (True, score, all_matches)

    return (False, score, all_matches)
