#!/usr/bin/env python3
"""
MathsForge AI - Apply Learned Keywords
Merges learned keywords with existing strict_keywords.py
"""

import json
from pathlib import Path

LEARNED_FILE = Path(__file__).parent / "learned_keywords.json"
STRICT_KEYWORDS_FILE = Path(__file__).parent / "strict_keywords.py"

# Topic name mapping (folder name -> strict_keywords key)
FOLDER_TO_TOPIC = {
    "01_number": "number",
    "02_angles": "angles",
    "03_scatter_graphs": "scatter graphs",
    "04_fractions": "fractions",
    "05_expressions_and_sequences": "expressions and sequences",
    "06_coordinates": "coordinates",
    "07_percentages": "percentages",
    "08_graphs": "graphs",
    "09_perimeter_and_area": "perimeter and area",
    "10_transformations": "transformations",
    "11_ratio": "ratio",
    "12_right_angled_triangles": "right-angled triangles",
    "13_statistics": "statistics",
    "14_congruence_and_similarity": "congruence and similarity",
    "15_equations": "equations",
    "16_inequalities": "inequalities",
    "17_circles": "circles",
    "18_indices_and_surds": "indices and surds",
    "19_pythagoras_theorem": "pythagoras theorem",
    "20_trigonometry": "trigonometry",
    "21_bounds": "bounds",
    "22_vectors": "vectors",
    "23_reciprocal_and_exponential_graphs": "reciprocal and exponential graphs",
    "24_3d_shapes_and_volume": "3d shapes and volume",
    "25_probability": "probability",
    "26_proportion": "proportion",
    "27_loci_and_constructions": "loci and constructions",
    "28_algebraic_fractions": "algebraic fractions",
    "29_quadratic_graphs": "quadratic graphs",
    "30_circle_theorems": "circle theorems",
    "31_quadratic_equations": "quadratic equations",
    "32_simultaneous_equations": "simultaneous equations",
    "33_functions": "functions",
    "34_iteration": "iteration",
    "35_proof": "proof",
    "36_gradients_and_rate_of_change": "gradients and rate of change",
    "37_pre_calculus": "pre-calculus",
}


def load_learned_keywords():
    """Load learned keywords from JSON file"""
    if not LEARNED_FILE.exists():
        print(f"Error: {LEARNED_FILE} not found. Run train_keywords.py first.")
        return None

    with open(LEARNED_FILE) as f:
        return json.load(f)


def load_current_keywords():
    """Load current strict keywords by importing the module"""
    import strict_keywords
    return strict_keywords.STRICT_TOPIC_KEYWORDS.copy()


def merge_keywords(current: dict, learned: dict) -> dict:
    """Merge learned keywords into current keywords"""
    merged = {}

    for folder_name, topic_key in FOLDER_TO_TOPIC.items():
        if topic_key not in current:
            print(f"Warning: Topic '{topic_key}' not in current keywords")
            continue

        current_topic = current[topic_key].copy()
        merged[topic_key] = current_topic

        # Check if we have learned data for this folder
        if folder_name not in learned.get('suggestions', {}):
            continue

        suggestions = learned['suggestions'][folder_name]

        # Add new primary keywords (avoiding duplicates)
        current_primary = set(kw.lower() for kw in current_topic.get('primary', []))
        new_primary = []
        for kw in suggestions.get('primary_suggestions', []):
            if kw.lower() not in current_primary:
                new_primary.append(kw)

        if new_primary:
            print(f"\n{topic_key}:")
            print(f"  + Primary: {new_primary[:5]}")

        # Add new context keywords
        current_context = set(kw.lower() for kw in current_topic.get('context', []))
        new_context = []
        for kw in suggestions.get('context_suggestions', []):
            if kw.lower() not in current_context and kw.lower() not in current_primary:
                new_context.append(kw)

        if new_context:
            print(f"  + Context: {new_context[:5]}")

        # Update the merged dictionary
        merged[topic_key]['primary'] = current_topic.get('primary', []) + new_primary
        merged[topic_key]['context'] = current_topic.get('context', []) + new_context

    return merged


def generate_new_keywords_file(merged: dict) -> str:
    """Generate Python code for the updated strict_keywords.py"""

    lines = [
        '"""',
        'STRICT Topic Keywords for GCSE Maths OCR Detection',
        'AUTO-GENERATED with learned keywords from training data',
        'Each topic has PRIMARY keywords (must match) and CONTEXT keywords (supporting evidence).',
        '"""',
        '',
        'STRICT_TOPIC_KEYWORDS = {'
    ]

    for topic_key, data in sorted(merged.items()):
        lines.append(f'    # {topic_key.title()}')
        lines.append(f'    "{topic_key}": {{')

        # Primary keywords
        primary = data.get('primary', [])
        primary_str = ', '.join(f'"{kw}"' for kw in primary)
        lines.append(f'        "primary": [{primary_str}],')

        # Context keywords
        context = data.get('context', [])
        context_str = ', '.join(f'"{kw}"' for kw in context)
        lines.append(f'        "context": [{context_str}],')

        # Exclude keywords
        exclude = data.get('exclude', [])
        exclude_str = ', '.join(f'"{kw}"' for kw in exclude)
        lines.append(f'        "exclude": [{exclude_str}]')

        lines.append('    },')
        lines.append('')

    lines.append('}')

    return '\n'.join(lines)


def main():
    print("=" * 60)
    print("MathsForge AI - Apply Learned Keywords")
    print("=" * 60)

    # Load learned keywords
    learned = load_learned_keywords()
    if not learned:
        return

    # Load current keywords
    current = load_current_keywords()
    print(f"\nLoaded {len(current)} existing topic keyword sets")

    # Check how many topics have training data
    topics_with_data = learned.get('metadata', {}).get('topics_with_data', 0)
    print(f"Topics with training data: {topics_with_data}")

    if topics_with_data == 0:
        print("\nNo training data found. Please add PDFs to training folders first.")
        print("Then run: python train_keywords.py")
        return

    # Merge keywords
    print("\n" + "=" * 60)
    print("Merging learned keywords with existing...")
    print("=" * 60)

    merged = merge_keywords(current, learned)

    # Generate new file content
    new_content = generate_new_keywords_file(merged)

    # Save backup
    backup_file = STRICT_KEYWORDS_FILE.with_suffix('.py.backup')
    if STRICT_KEYWORDS_FILE.exists():
        import shutil
        shutil.copy(STRICT_KEYWORDS_FILE, backup_file)
        print(f"\n✅ Backup saved to: {backup_file}")

    # Preview mode - don't overwrite yet
    preview_file = Path(__file__).parent / "strict_keywords_preview.py"
    with open(preview_file, 'w') as f:
        f.write(new_content)

    print(f"✅ Preview saved to: {preview_file}")
    print("\nTo apply changes:")
    print(f"  cp {preview_file} {STRICT_KEYWORDS_FILE}")


if __name__ == "__main__":
    main()
