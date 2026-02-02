# MathsForge AI - Topic Training Data

## How to Use

1. **Download topic-specific papers** from these sources:
   - [Corbett Maths](https://corbettmaths.com/contents/) - Textbook exercises by topic
   - [Maths Genie](https://www.mathsgenie.co.uk/gcse.html) - Exam questions by topic
   - [Physics & Maths Tutor](https://www.physicsandmathstutor.com/maths-revision/gcse-edexcel/) - Topic papers
   - [Dr Frost Maths](https://www.drfrostmaths.com/) - Worksheets (free account needed)

2. **Place PDFs in the correct folder** based on topic

3. **Run the training script** (coming soon):
   ```bash
   python train_keywords.py
   ```

## Folder Structure

| Folder | Topic |
|--------|-------|
| 01_number | HCF, LCM, Prime Factors |
| 02_angles | Angles in polygons, parallel lines |
| 03_scatter_graphs | Correlation, line of best fit |
| 04_fractions | Operations with fractions |
| 05_expressions_and_sequences | nth term, sequences |
| 06_coordinates | Midpoint, distance |
| 07_percentages | Compound interest, reverse % |
| 08_graphs | y = mx + c, linear graphs |
| 09_perimeter_and_area | Area, circumference, sectors |
| 10_transformations | Translation, rotation, enlargement |
| 11_ratio | Share in ratio, simplify |
| 12_right_angled_triangles | Pythagoras + basic trig |
| 13_statistics | Mean, median, histograms |
| 14_congruence_and_similarity | Similar shapes, proofs |
| 15_equations | Solve linear equations |
| 16_inequalities | Solve and represent |
| 17_circles | Properties (not theorems) |
| 18_indices_and_surds | Index laws, rationalise |
| 19_pythagoras_theorem | Pythagoras specifically |
| 20_trigonometry | Sin/cos/tan, sine/cosine rule |
| 21_bounds | Upper/lower bounds |
| 22_vectors | Column vectors, magnitude |
| 23_reciprocal_and_exponential_graphs | y=1/x, y=a^x |
| 24_3d_shapes_and_volume | Volume, surface area |
| 25_probability | Tree diagrams, Venn diagrams |
| 26_proportion | Direct/inverse proportion |
| 27_loci_and_constructions | Compass constructions |
| 28_algebraic_fractions | Simplify, add/subtract |
| 29_quadratic_graphs | Parabolas, turning points |
| 30_circle_theorems | Angle theorems |
| 31_quadratic_equations | Factorise, formula, complete square |
| 32_simultaneous_equations | Elimination, substitution |
| 33_functions | f(x), composite, inverse |
| 34_iteration | Iterative methods |
| 35_proof | Algebraic proof |
| 36_gradients_and_rate_of_change | Tangent to curve, area under |
| 37_pre_calculus | Differentiation basics |

## Priority Topics (suggested to start with)

These are commonly tested and benefit most from better detection:
1. **25_probability** - Very common, lots of specific vocabulary
2. **20_trigonometry** - Distinct formulas and terms
3. **22_vectors** - Unique notation
4. **31_quadratic_equations** - High frequency topic
5. **13_statistics** - Many sub-topics
