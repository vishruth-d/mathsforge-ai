"""
GCSE Maths Topic Keywords for Question Classification

Each topic contains 25-40 keywords including:
- Topic name and variations
- Common question phrases
- Mathematical terms specific to that topic
- Context words often used in exam questions
- Units and symbols commonly seen
"""

TOPIC_KEYWORDS = {
    # 1 - Number
    "number": [
        "number", "integer", "integers", "whole number", "natural number",
        "prime", "primes", "prime number", "prime factor", "prime factorisation",
        "factor", "factors", "multiple", "multiples", "divisible", "divisibility",
        "hcf", "highest common factor", "lcm", "lowest common multiple", "least common multiple",
        "product", "quotient", "remainder", "divide", "divisor",
        "bidmas", "bodmas", "order of operations", "brackets",
        "positive", "negative", "odd", "even", "square number", "cube number",
        "work out", "calculate", "find", "write down", "list",
        "ascending", "descending", "between", "consecutive",
        "digit", "place value", "powers of 10",
    ],

    # 2 - Angles
    "angles": [
        "angle", "angles", "degree", "degrees", "protractor",
        "acute", "obtuse", "reflex", "right angle", "straight line",
        "triangle", "triangles", "equilateral", "isosceles", "scalene",
        "quadrilateral", "quadrilaterals", "parallelogram", "trapezium", "rhombus", "kite",
        "polygon", "polygons", "pentagon", "hexagon", "octagon", "regular", "irregular",
        "interior angle", "exterior angle", "sum of angles",
        "parallel", "parallel lines", "transversal", "corresponding", "alternate", "co-interior",
        "bearing", "bearings", "north", "clockwise", "three-figure bearing",
        "vertically opposite", "supplementary", "complementary",
        "calculate", "find", "work out", "measure", "marked",
    ],

    # 3 - Scatter graphs
    "scatter graphs": [
        "scatter", "scatter graph", "scatter diagram", "scatter plot",
        "correlation", "positive correlation", "negative correlation", "no correlation",
        "strong", "weak", "moderate",
        "line of best fit", "best fit", "trend line",
        "outlier", "outliers", "anomaly",
        "estimate", "predict", "prediction", "interpolation", "extrapolation",
        "relationship", "data", "points", "plotted", "plot",
        "describe", "draw", "comment", "reliability",
        "height", "weight", "age", "temperature", "distance", "time",
        "variable", "independent", "dependent",
        "bivariate", "data set",
    ],

    # 4 - Fractions
    "fractions": [
        "fraction", "fractions", "numerator", "denominator",
        "mixed number", "mixed numbers", "improper fraction", "improper fractions",
        "proper fraction", "top-heavy",
        "equivalent", "equivalent fraction", "simplify", "simplest form", "lowest terms",
        "common denominator", "lcd",
        "add", "subtract", "multiply", "divide", "of",
        "reciprocal", "invert",
        "convert", "write as", "express",
        "half", "quarter", "third", "fifth", "eighth", "tenth",
        "work out", "calculate", "give your answer as",
        "pizza", "cake", "pie", "share", "parts", "whole",
        "cancel", "cancelling",
    ],

    # 5 - Expressions and sequences
    "expressions and sequences": [
        "expression", "expressions", "algebraic", "algebra",
        "term", "terms", "like terms", "collect", "simplify",
        "coefficient", "constant", "variable",
        "sequence", "sequences", "pattern", "patterns",
        "nth term", "general term", "position-to-term", "term-to-term",
        "arithmetic", "arithmetic sequence", "common difference",
        "geometric", "geometric sequence", "common ratio",
        "linear", "quadratic", "fibonacci",
        "next term", "previous term", "first term",
        "write an expression", "find the nth term", "work out",
        "substitute", "substitution", "when", "given that",
        "increasing", "decreasing",
        "matchsticks", "tiles", "dots", "shapes",
    ],

    # 6 - Coordinates
    "coordinates": [
        "coordinate", "coordinates", "coordinate plane", "coordinate grid",
        "x-axis", "y-axis", "axes", "origin",
        "x-coordinate", "y-coordinate", "ordered pair",
        "plot", "plotting", "point", "points", "position",
        "quadrant", "quadrants", "first quadrant",
        "midpoint", "midpoint formula",
        "distance", "distance between", "length",
        "horizontal", "vertical",
        "positive", "negative",
        "grid", "graph paper",
        "write down", "find", "calculate", "state",
        "line segment", "join",
        "translation", "move",
    ],

    # 7 - Percentages
    "percentages": [
        "percent", "percentage", "percentages", "%",
        "percentage change", "percentage increase", "percentage decrease",
        "percentage profit", "percentage loss",
        "reverse percentage", "original amount", "original value",
        "compound interest", "simple interest", "interest rate",
        "depreciation", "appreciation", "growth", "decay",
        "multiplier", "decimal multiplier",
        "vat", "tax", "discount", "sale", "reduction",
        "deposit", "loan", "savings", "investment",
        "calculate", "work out", "find", "express as",
        "convert", "write as",
        "increase", "decrease", "by", "of",
        "profit", "loss", "cost price", "selling price",
        "population", "salary", "price",
    ],

    # 8 - Graphs
    "graphs": [
        "graph", "graphs", "graphing", "plot", "sketch",
        "straight line", "linear", "y = mx + c", "y=mx+c",
        "gradient", "slope", "steepness", "rate of change",
        "intercept", "y-intercept", "x-intercept", "crosses",
        "parallel", "perpendicular",
        "equation of a line", "equation of the line",
        "coordinate", "coordinates", "point", "points",
        "passes through", "through the point",
        "horizontal", "vertical", "diagonal",
        "positive gradient", "negative gradient",
        "draw", "sketch", "plot", "label",
        "find the equation", "work out", "calculate",
        "distance-time", "speed-time", "conversion graph",
        "real-life", "travel graph",
    ],

    # 9 - Perimeter and area
    "perimeter and area": [
        "perimeter", "area", "surface area",
        "rectangle", "rectangular", "square", "triangle", "triangular",
        "parallelogram", "trapezium", "rhombus", "kite",
        "circle", "circular", "semicircle", "quarter circle",
        "radius", "diameter", "circumference", "pi",
        "sector", "arc", "arc length", "segment",
        "compound shape", "composite shape", "l-shape", "t-shape",
        "length", "width", "height", "base",
        "calculate", "find", "work out", "measure",
        "cm", "m", "mm", "km", "cm2", "m2", "mm2",
        "square units", "squared",
        "garden", "field", "floor", "wall", "room", "fence", "lawn",
        "grass", "paint", "carpet", "tiles",
    ],

    # 10 - Transformations
    "transformations": [
        "transformation", "transformations", "transform",
        "translation", "translate", "vector", "column vector", "movement",
        "rotation", "rotate", "turn", "clockwise", "anticlockwise", "centre of rotation",
        "reflection", "reflect", "mirror line", "line of reflection", "symmetry",
        "enlargement", "enlarge", "scale factor", "centre of enlargement",
        "congruent", "similar", "image", "object",
        "describe", "describe fully", "single transformation",
        "invariant", "invariant point",
        "negative scale factor", "fractional scale factor",
        "coordinate", "coordinates", "grid",
        "shape", "triangle", "quadrilateral",
        "map", "maps onto",
    ],

    # 11 - Ratio
    "ratio": [
        "ratio", "ratios", "proportion", "proportional",
        "simplify", "simplest form", "equivalent ratio",
        "share", "sharing", "divide", "split",
        "parts", "part", "in the ratio",
        "unitary method", "unit ratio",
        "scale", "scale drawing", "map scale",
        "recipe", "ingredients", "mixture", "mix",
        "convert", "comparison", "compare",
        "red", "blue", "boys", "girls", "men", "women",
        "sweets", "counters", "marbles", "coins",
        "work out", "calculate", "find", "give your answer",
        "increased", "decreased", "total",
        "amount", "quantity",
    ],

    # 12 - Right-angled triangles
    "right-angled triangles": [
        "right-angled", "right angle", "right-angled triangle",
        "hypotenuse", "opposite", "adjacent",
        "pythagoras", "pythagorean", "pythagoras theorem",
        "trigonometry", "trig", "sohcahtoa",
        "sin", "cos", "tan", "sine", "cosine", "tangent",
        "angle", "side", "length",
        "find", "calculate", "work out",
        "ladder", "wall", "ground", "roof", "ramp",
        "distance", "height", "horizontal", "vertical",
        "cm", "m", "mm", "km",
        "decimal places", "significant figures",
        "exact", "exact value", "surd form",
    ],

    # 13 - Statistics
    "statistics": [
        "statistics", "statistical", "data", "data set",
        "mean", "average", "median", "mode", "modal",
        "range", "spread", "interquartile range", "iqr",
        "frequency", "frequency table", "grouped frequency",
        "class interval", "class width", "midpoint",
        "cumulative frequency", "cumulative frequency diagram",
        "box plot", "box and whisker", "quartile", "lower quartile", "upper quartile",
        "histogram", "frequency density", "bar chart", "pie chart",
        "stem and leaf", "stem-and-leaf",
        "sample", "sampling", "population", "bias", "random",
        "survey", "questionnaire",
        "calculate", "find", "estimate", "compare",
        "table", "tally", "total",
    ],

    # 14 - Congruence and similarity
    "congruence and similarity": [
        "congruent", "congruence", "congruent triangles",
        "similar", "similarity", "similar shapes", "similar triangles",
        "scale factor", "linear scale factor",
        "area scale factor", "volume scale factor",
        "corresponding", "corresponding sides", "corresponding angles",
        "proportion", "proportional",
        "ratio", "ratio of areas", "ratio of volumes",
        "prove", "proof", "show that", "explain",
        "sss", "sas", "asa", "aas", "rhs",
        "length", "side", "angle",
        "calculate", "find", "work out",
        "enlargement", "reduction",
        "squared", "cubed",
    ],

    # 15 - Equations
    "equations": [
        "equation", "equations", "solve", "solving",
        "linear equation", "linear equations",
        "unknown", "variable", "x", "y",
        "rearrange", "rearranging", "make the subject",
        "balance", "balancing", "inverse operations",
        "expand", "simplify", "collect like terms",
        "brackets", "both sides",
        "solution", "solutions", "root", "roots",
        "substitute", "substitution", "check",
        "form an equation", "set up an equation",
        "work out", "find", "calculate", "solve for",
        "equals", "equal to", "is equal",
        "word problem", "consecutive", "sum", "difference",
        "perimeter", "angles", "age",
    ],

    # 16 - Inequalities
    "inequalities": [
        "inequality", "inequalities", "inequation",
        "less than", "greater than", "less than or equal", "greater than or equal",
        "< ", "> ", "<=", ">=", "leq", "geq",
        "solve", "solving", "solution", "solution set",
        "number line", "represent", "show", "indicate",
        "integer", "integers", "integer values",
        "region", "shade", "shading", "unshaded",
        "satisfy", "satisfies", "values that satisfy",
        "boundary", "boundary line", "dashed", "solid",
        "list", "write down", "state",
        "range", "interval", "between",
        "simultaneously", "system of inequalities",
        "n", "x", "y",
    ],

    # 17 - Circles
    "circles": [
        "circle", "circles", "circular",
        "radius", "radii", "diameter", "centre", "center",
        "circumference", "perimeter of a circle",
        "area of a circle", "area of circle",
        "pi", "3.14", "3.142",
        "arc", "arc length", "sector", "sector area",
        "segment", "chord", "tangent",
        "semicircle", "quarter circle", "quadrant",
        "angle at centre", "angle at circumference",
        "calculate", "find", "work out",
        "give your answer in terms of pi", "exact", "leave in terms of",
        "cm", "m", "mm", "cm2", "m2",
        "round", "decimal places", "significant figures",
        "wheel", "pizza", "clock", "coin",
    ],

    # 18 - Indices and surds
    "indices and surds": [
        "index", "indices", "power", "powers", "exponent",
        "square", "squared", "cube", "cubed",
        "square root", "cube root", "nth root", "root",
        "surd", "surds", "radical", "irrational",
        "simplify", "rationalise", "rationalise the denominator",
        "standard form", "scientific notation",
        "negative index", "negative indices", "fractional index", "fractional indices",
        "laws of indices", "index laws", "rules of indices",
        "multiply", "divide", "add", "subtract",
        "calculate", "work out", "find", "evaluate",
        "write in standard form", "write as a power",
        "express", "give your answer", "simplest form",
        "10^", "a^n", "x^",
    ],

    # 19 - Pythagoras theorem
    "pythagoras theorem": [
        "pythagoras", "pythagorean", "pythagoras theorem",
        "hypotenuse", "longest side", "opposite the right angle",
        "right-angled triangle", "right angle", "right-angled",
        "a squared plus b squared", "a^2 + b^2 = c^2",
        "square", "squared", "square root",
        "length", "side", "distance",
        "find", "calculate", "work out",
        "ladder", "wall", "ground", "diagonal",
        "horizontal", "vertical",
        "3d", "three-dimensional", "cuboid", "pyramid",
        "cm", "m", "mm", "km",
        "decimal places", "significant figures",
        "exact", "surd", "leave your answer",
        "isosceles triangle", "equilateral triangle",
        "coordinate", "coordinates", "distance between points",
    ],

    # 20 - Trigonometry
    "trigonometry": [
        "trigonometry", "trig", "trigonometric", "trigonometrical",
        "sin", "cos", "tan", "sine", "cosine", "tangent",
        "sohcahtoa", "opposite", "adjacent", "hypotenuse",
        "angle", "find the angle", "calculate the angle",
        "side", "find the length", "calculate the length",
        "inverse", "sin^-1", "cos^-1", "tan^-1", "arcsin", "arccos", "arctan",
        "right-angled triangle", "right angle",
        "sine rule", "cosine rule", "area formula",
        "3d trigonometry", "three-dimensional",
        "bearing", "angle of elevation", "angle of depression",
        "degree", "degrees",
        "calculator", "decimal places", "significant figures",
        "exact value", "surd form",
        "ladder", "tower", "cliff", "tree", "building",
    ],

    # 21 - Bounds
    "bounds": [
        "bounds", "bound", "upper bound", "lower bound",
        "error interval", "truncation", "truncated",
        "rounding", "rounded", "nearest",
        "accuracy", "accurate", "degree of accuracy",
        "significant figures", "decimal places",
        "maximum", "minimum", "greatest", "least",
        "upper limit", "lower limit",
        "tolerance", "error",
        "calculate", "find", "work out", "state",
        "distance", "time", "speed", "area", "volume",
        "measurement", "measured", "correct to",
        "nearest cm", "nearest m", "nearest 10",
        "continuous", "discrete",
        "interval", "range",
    ],

    # 22 - Vectors
    "vectors": [
        "vector", "vectors", "column vector",
        "magnitude", "direction", "length of vector",
        "position vector", "displacement",
        "add", "addition", "subtract", "subtraction",
        "scalar", "scalar multiple", "multiply",
        "parallel", "parallel vectors",
        "equal vectors", "resultant", "resultant vector",
        "i", "j", "unit vector",
        "midpoint", "ratio",
        "prove", "show that", "explain",
        "find", "calculate", "work out", "express",
        "in terms of", "a", "b",
        "point", "points", "line segment",
        "triangle", "parallelogram", "quadrilateral",
        "oa", "ob", "ab", "ba",
    ],

    # 23 - Reciprocal and exponential graphs
    "reciprocal and exponential graphs": [
        "reciprocal", "reciprocal graph", "1/x", "y = 1/x", "y = k/x",
        "exponential", "exponential graph", "exponential growth", "exponential decay",
        "y = a^x", "y = e^x", "y = 2^x", "y = 10^x",
        "asymptote", "asymptotes", "approaches",
        "hyperbola", "curve", "curves",
        "sketch", "draw", "plot",
        "shape", "describe", "features",
        "horizontal asymptote", "vertical asymptote",
        "x-axis", "y-axis", "origin",
        "positive", "negative", "quadrant",
        "growth rate", "decay rate", "half-life",
        "population", "bacteria", "compound interest",
        "recognise", "identify", "match",
        "transformation", "translate", "reflect",
    ],

    # 24 - 3D shapes and volume
    "3d shapes and volume": [
        "3d", "three-dimensional", "solid", "solids",
        "volume", "capacity",
        "surface area", "total surface area",
        "cube", "cuboid", "rectangular prism",
        "prism", "prisms", "cross-section", "cross-sectional area",
        "cylinder", "cylindrical",
        "pyramid", "cone", "conical",
        "sphere", "spherical", "hemisphere",
        "frustum",
        "edge", "edges", "face", "faces", "vertex", "vertices",
        "net", "nets",
        "calculate", "find", "work out",
        "cm3", "m3", "mm3", "litres", "ml",
        "height", "length", "width", "radius", "diameter",
        "slant height", "perpendicular height",
        "exact", "terms of pi",
    ],

    # 25 - Probability
    "probability": [
        "probability", "probable", "likelihood", "chance",
        "certain", "likely", "unlikely", "impossible", "even chance",
        "fair", "unfair", "biased", "unbiased",
        "random", "randomly", "at random",
        "event", "events", "outcome", "outcomes",
        "independent", "dependent", "mutually exclusive",
        "conditional", "conditional probability", "given that",
        "tree diagram", "tree diagrams", "branches",
        "sample space", "sample space diagram",
        "venn diagram", "intersection", "union",
        "relative frequency", "experimental", "theoretical",
        "expected", "expected frequency", "expected number",
        "bag", "bags", "counter", "counters", "marble", "marbles",
        "spinner", "spinners", "dice", "die", "coin", "coins", "card", "cards",
        "without replacement", "with replacement",
        "calculate", "find", "work out",
    ],

    # 26 - Proportion
    "proportion": [
        "proportion", "proportional", "proportionality",
        "direct proportion", "directly proportional",
        "inverse proportion", "inversely proportional",
        "constant", "constant of proportionality", "k",
        "y is proportional to x", "y varies as x", "varies directly",
        "y is inversely proportional", "y varies inversely",
        "y = kx", "y = k/x", "y = kx^2", "y = k/x^2",
        "graph", "straight line through origin", "curve",
        "double", "halve", "triple", "quadruple",
        "find the value", "calculate", "work out",
        "when", "given that", "if",
        "equation", "formula", "relationship",
        "speed", "distance", "time", "pressure", "volume",
        "currency", "exchange rate",
    ],

    # 27 - Loci
    "loci": [
        "locus", "loci", "path",
        "construction", "constructions", "construct",
        "compass", "compasses", "ruler", "straight edge",
        "bisector", "perpendicular bisector", "angle bisector",
        "perpendicular", "perpendicular line",
        "equidistant", "equal distance",
        "arc", "arcs", "circle",
        "fixed point", "fixed distance",
        "region", "shade", "shading",
        "describe", "draw", "show",
        "all points", "set of points",
        "constraint", "constraints",
        "treasure", "dog", "goat", "rope", "fence",
        "cm", "m", "accurately", "scale",
        "construction lines", "show your construction lines",
    ],

    # 28 - Algebraic fractions
    "algebraic fractions": [
        "algebraic fraction", "algebraic fractions",
        "simplify", "simplest form", "cancel",
        "common factor", "common denominator",
        "add", "subtract", "multiply", "divide",
        "numerator", "denominator",
        "factorise", "factorising", "factor",
        "quadratic", "linear", "expression",
        "expand", "brackets",
        "single fraction", "write as a single fraction",
        "solve", "equation", "equations",
        "partial fractions",
        "work out", "calculate", "give your answer",
        "fully simplified", "in its simplest form",
        "x", "y", "a", "b",
        "difference of two squares", "common factor",
    ],

    # 29 - Quadratic graphs
    "quadratic graphs": [
        "quadratic", "quadratic graph", "quadratic function",
        "parabola", "u-shape", "n-shape",
        "y = x^2", "y = ax^2 + bx + c", "x squared",
        "turning point", "vertex", "maximum", "minimum",
        "line of symmetry", "axis of symmetry",
        "roots", "solutions", "x-intercepts", "crosses the x-axis",
        "y-intercept", "crosses the y-axis",
        "sketch", "draw", "plot",
        "coefficient", "positive", "negative",
        "completing the square",
        "table of values",
        "estimate", "read off", "from your graph",
        "intersect", "intersection", "meets",
        "discriminant",
        "shape", "describe",
    ],

    # 30 - Circle theorems
    "circle theorems": [
        "circle theorem", "circle theorems",
        "angle at centre", "angle at circumference",
        "angle in semicircle", "diameter", "90 degrees",
        "angles in same segment", "angles subtended",
        "cyclic quadrilateral", "opposite angles",
        "tangent", "tangent to a circle", "radius tangent",
        "chord", "perpendicular bisector of chord",
        "alternate segment", "alternate segment theorem",
        "arc", "subtended", "subtend",
        "prove", "proof", "show that", "give reasons",
        "find", "calculate", "work out",
        "marked", "diagram", "not drawn accurately",
        "centre", "circumference", "point on circle",
        "isosceles triangle", "radius",
    ],

    # 31 - Quadratic equations
    "quadratic equations": [
        "quadratic", "quadratic equation", "quadratic equations",
        "solve", "solving", "solution", "solutions",
        "root", "roots", "x =",
        "factorise", "factorising", "factorisation",
        "quadratic formula", "formula",
        "completing the square",
        "discriminant", "b^2 - 4ac", "b squared minus 4ac",
        "real roots", "no real roots", "equal roots", "distinct roots",
        "expand", "brackets",
        "x^2", "x squared", "ax^2 + bx + c = 0",
        "give your answers to", "decimal places", "significant figures",
        "exact", "surd form", "simplest form",
        "form an equation", "show that",
        "positive", "negative", "integer",
        "product", "sum",
    ],

    # 32 - Simultaneous equations
    "simultaneous equations": [
        "simultaneous", "simultaneous equations",
        "solve", "solving", "solution", "solutions",
        "pair of equations", "system of equations",
        "linear", "linear simultaneous", "both linear",
        "quadratic", "one linear one quadratic",
        "elimination", "eliminate",
        "substitution", "substitute",
        "x and y", "find x and y", "values of x and y",
        "graphically", "point of intersection", "intersect",
        "add", "subtract", "multiply",
        "coefficient", "coefficients",
        "check", "verify",
        "word problem", "form two equations",
        "cost", "number of", "total",
        "adult", "child", "ticket", "tickets",
    ],

    # 33 - Functions
    "functions": [
        "function", "functions", "f(x)", "g(x)", "h(x)",
        "input", "output", "domain", "range",
        "composite", "composite function", "fg(x)", "gf(x)",
        "inverse", "inverse function", "f^-1", "f inverse",
        "mapping", "maps to", "arrow",
        "evaluate", "find", "calculate", "work out",
        "when x =", "given that", "if",
        "solve", "f(x) =", "equation",
        "graph", "sketch", "transformation",
        "self-inverse", "one-to-one", "many-to-one",
        "undefined", "not defined",
        "notation", "function notation",
        "machine", "function machine",
        "order", "order of operations",
    ],

    # 34 - Iteration
    "iteration": [
        "iteration", "iterative", "iterate",
        "formula", "iterative formula", "recurrence relation",
        "x(n+1)", "x sub n", "x subscript",
        "starting value", "initial value", "x0", "x1",
        "converge", "convergence", "converges to",
        "root", "solution", "approximate",
        "decimal places", "significant figures",
        "rearrange", "rearranging",
        "show that", "can be rearranged",
        "estimate", "approximation",
        "calculate", "find", "work out",
        "continue", "iterations", "times",
        "accurate", "accuracy",
        "between", "lies between", "interval",
        "trial and improvement",
    ],

    # 35 - Proof
    "proof": [
        "proof", "prove", "proving",
        "show that", "explain why", "justify",
        "algebraic proof", "algebraic", "algebra",
        "geometric proof", "geometrically",
        "counter-example", "counterexample", "disprove",
        "always", "sometimes", "never",
        "even", "odd", "consecutive", "integer",
        "divisible", "divisibility", "multiple",
        "prime", "square number", "cube number",
        "n", "n+1", "n+2", "2n", "2n+1",
        "therefore", "hence", "thus", "so",
        "qed", "as required",
        "let", "assume", "suppose",
        "congruent", "similar",
        "logical", "reasoning", "deduce",
    ],

    # 36 - Gradients and rate of change
    "gradients and rate of change": [
        "gradient", "slope", "steepness",
        "rate of change", "rate", "change",
        "tangent", "tangent to the curve",
        "instantaneous", "instantaneous rate",
        "average rate", "average gradient",
        "speed", "velocity", "acceleration",
        "distance-time", "speed-time", "velocity-time",
        "area under", "area under the curve", "area under graph",
        "estimate", "approximation",
        "draw a tangent", "at the point",
        "derivative", "differentiation",
        "increase", "decrease", "positive", "negative",
        "turning point", "stationary point",
        "units", "per second", "per hour", "m/s",
        "curve", "graph", "non-linear",
    ],

    # 37 - Pre-calculus
    "pre-calculus": [
        "derivative", "differentiate", "differentiation",
        "dy/dx", "d/dx", "f'(x)", "f dash x",
        "gradient function", "derived function",
        "power rule", "chain rule",
        "tangent", "normal", "equation of tangent", "equation of normal",
        "turning point", "stationary point", "maximum", "minimum",
        "increasing", "decreasing",
        "second derivative", "d2y/dx2",
        "rate of change", "instantaneous",
        "area under curve", "integration", "integrate",
        "find", "calculate", "work out", "determine",
        "curve", "y =", "given that",
        "at the point", "when x =",
        "optimisation", "optimization",
    ],
}


# Mapping from config.py topic numbers to keyword dictionary keys
TOPIC_NUMBER_TO_KEY = {
    1: "number",
    2: "angles",
    3: "scatter graphs",
    4: "fractions",
    5: "expressions and sequences",
    6: "coordinates",
    7: "percentages",
    8: "graphs",
    9: "perimeter and area",
    10: "transformations",
    11: "ratio",
    12: "right-angled triangles",
    13: "statistics",
    14: "congruence and similarity",
    15: "equations",
    16: "inequalities",
    17: "circles",
    18: "indices and surds",
    19: "pythagoras theorem",
    20: "trigonometry",
    21: "bounds",
    22: "vectors",
    23: "reciprocal and exponential graphs",
    24: "3d shapes and volume",
    25: "probability",
    26: "proportion",
    27: "loci",
    28: "algebraic fractions",
    29: "quadratic graphs",
    30: "circle theorems",
    31: "quadratic equations",
    32: "simultaneous equations",
    33: "functions",
    34: "iteration",
    35: "proof",
    36: "gradients and rate of change",
    37: "pre-calculus",
}


def get_keywords_for_topic(topic_number):
    """
    Get keywords for a topic by its number.

    Args:
        topic_number: Integer 1-37 corresponding to the topic

    Returns:
        List of keywords or empty list if topic not found
    """
    key = TOPIC_NUMBER_TO_KEY.get(topic_number)
    if key:
        return TOPIC_KEYWORDS.get(key, [])
    return []


def get_all_keywords():
    """
    Get a flat list of all keywords across all topics.

    Returns:
        List of all unique keywords
    """
    all_keywords = set()
    for keywords in TOPIC_KEYWORDS.values():
        all_keywords.update(keywords)
    return list(all_keywords)


def find_topics_by_keyword(keyword):
    """
    Find all topics that contain a given keyword.

    Args:
        keyword: String to search for (case-insensitive)

    Returns:
        List of topic names that contain the keyword
    """
    keyword_lower = keyword.lower()
    matching_topics = []
    for topic_name, keywords in TOPIC_KEYWORDS.items():
        if any(keyword_lower in kw.lower() for kw in keywords):
            matching_topics.append(topic_name)
    return matching_topics
