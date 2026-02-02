# Training Resources - Topic-Specific PDF Sources

Use these links to download topic-specific question papers for training the keyword system.

## Primary Sources

### Maths Genie (mathsgenie.co.uk)
Excellent topic-organised questions sorted by grade.

| Topic | Link |
|-------|------|
| 1. Number | https://www.mathsgenie.co.uk/gcse.html → Number section |
| 2. Angles | https://www.mathsgenie.co.uk/angles.html |
| 3. Scatter Graphs | https://www.mathsgenie.co.uk/scattergraphs.html |
| 4. Fractions | https://www.mathsgenie.co.uk/fractions.html |
| 5. Sequences | https://www.mathsgenie.co.uk/sequences.html |
| 6. Coordinates | https://www.mathsgenie.co.uk/coordinates.html |
| 7. Percentages | https://www.mathsgenie.co.uk/percentages.html |
| 8. Linear Graphs | https://www.mathsgenie.co.uk/lineargraphs.html |
| 9. Area & Perimeter | https://www.mathsgenie.co.uk/area.html |
| 10. Transformations | https://www.mathsgenie.co.uk/transformations.html |
| 11. Ratio | https://www.mathsgenie.co.uk/ratio.html |
| 12. Pythagoras & Trig | https://www.mathsgenie.co.uk/pythagoras.html |
| 13. Statistics | https://www.mathsgenie.co.uk/statistics.html |
| 14. Similarity | https://www.mathsgenie.co.uk/similarity.html |
| 15. Equations | https://www.mathsgenie.co.uk/equations.html |
| 16. Inequalities | https://www.mathsgenie.co.uk/inequalities.html |
| 17. Circles | https://www.mathsgenie.co.uk/circles.html |
| 18. Indices & Surds | https://www.mathsgenie.co.uk/surds.html |
| 19. Pythagoras | https://www.mathsgenie.co.uk/pythagoras.html |
| 20. Trigonometry | https://www.mathsgenie.co.uk/trigonometry.html |
| 21. Bounds | https://www.mathsgenie.co.uk/bounds.html |
| 22. Vectors | https://www.mathsgenie.co.uk/vectors.html |
| 23. Exponential Graphs | https://www.mathsgenie.co.uk/exponentialgraphs.html |
| 24. Volume | https://www.mathsgenie.co.uk/volume.html |
| 25. Probability | https://www.mathsgenie.co.uk/probability.html |
| 26. Proportion | https://www.mathsgenie.co.uk/proportion.html |
| 27. Constructions | https://www.mathsgenie.co.uk/constructions.html |
| 28. Algebraic Fractions | https://www.mathsgenie.co.uk/algebraicfractions.html |
| 29. Quadratic Graphs | https://www.mathsgenie.co.uk/quadraticgraphs.html |
| 30. Circle Theorems | https://www.mathsgenie.co.uk/circletheorems.html |
| 31. Quadratic Equations | https://www.mathsgenie.co.uk/quadratics.html |
| 32. Simultaneous Equations | https://www.mathsgenie.co.uk/simultaneous.html |
| 33. Functions | https://www.mathsgenie.co.uk/functions.html |
| 34. Iteration | https://www.mathsgenie.co.uk/iteration.html |
| 35. Proof | https://www.mathsgenie.co.uk/proof.html |
| 36. Gradients | https://www.mathsgenie.co.uk/gradients.html |
| 37. Differentiation | https://www.mathsgenie.co.uk/differentiation.html |
| 38. Trig Graphs | https://www.mathsgenie.co.uk/trigonometricgraphs.html |

---

### Physics & Maths Tutor (physicsandmathstutor.com)
Topic papers extracted from real Edexcel past papers.

**Base URL:** https://www.physicsandmathstutor.com/maths-revision/gcse-edexcel/

Navigate to topic → Download "Questions" PDF

---

### Corbett Maths (corbettmaths.com)
Textbook exercises and practice questions.

**Base URL:** https://corbettmaths.com/contents/

Each topic has:
- Video tutorial
- Textbook exercise (PDF)
- Practice questions
- Answers

---

### Dr Frost Maths (drfrostmaths.com)
Requires free account. Excellent structured worksheets.

**Base URL:** https://www.drfrostmaths.com/

---

## How to Use Training Data

1. Download PDFs from above sources
2. Place in correct `training/XX_topic_name/` folder
3. Run: `python src/train_keywords.py`
4. Review: `learned_keywords.json`
5. Apply: `python src/apply_learned_keywords.py`

## Priority Topics

Start with these high-value topics:

1. **25_probability** - Most distinct vocabulary
2. **22_vectors** - Unique notation (a, b, column vectors)
3. **20_trigonometry** - Specific formulas (sin, cos, tan)
4. **30_circle_theorems** - Very specific terms
5. **31_quadratic_equations** - High frequency in exams
6. **13_statistics** - Many sub-topics (mean, median, histograms)
7. **38_trigonometric_graphs** - Distinct from trig calculations

## File Naming

Any naming works, but suggested format:
```
mathsgenie_probability_grade5.pdf
pmt_vectors_higher.pdf
corbett_quadratics_exercise.pdf
```
