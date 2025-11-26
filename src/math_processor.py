"""
Math Processor Module
Handles mathematical content (LaTeX, formulas)
"""

import re
from typing import List

class MathProcessor:
    """Process mathematical content in PDFs"""

    def __init__(self):
        # Patterns to detect LaTeX math blocks
        self.latex_patterns = [
            r'\$\$.*?\$\$',                     # $$ display math $$
            r'\$.*?\$',                         # $ inline math $
            r'\\begin\{equation\}.*?\\end\{equation\}',
            r'\\begin\{align\}.*?\\end\{align\}',
            r'\\\[.*?\\\]',                     # \[ math \]
        ]

    # ------------------------------------------------------

    def detect_math_content(self, text: str) -> bool:
        """Check if text contains mathematical LaTeX notation"""
        for pattern in self.latex_patterns:
            if re.search(pattern, text, re.DOTALL):
                return True
        return False

    # ------------------------------------------------------

    def extract_formulas(self, text: str) -> List[str]:
        """Extract all mathematical expressions from the text"""
        formulas = []
        for pattern in self.latex_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            formulas.extend(matches)
        return formulas

    # ------------------------------------------------------

    def chunk_with_math_preservation(
        self,
        text: str,
        chunk_size: int = 500
    ) -> List[str]:
        """
        Split text into chunks while preserving complete math expressions.
        Math blocks should not be split across chunks.
        """

        chunks = []
        current_chunk = ""

        # Split by sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)

        for sentence in sentences:
            # If adding sentence exceeds chunk size → start new chunk
            if len(current_chunk) + len(sentence) > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = ""

            # If sentence contains math → keep entire sentence together
            if self.detect_math_content(sentence):
                current_chunk += " " + sentence
            else:
                current_chunk += " " + sentence

        # Add last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    # ------------------------------------------------------

    def add_math_context(self, text: str, formulas: List[str]) -> str:
        """
        Add tags around math formulas for better retrieval accuracy.
        Example: [MATH] formula [/MATH]
        """

        enhanced_text = text

        for formula in formulas:
            tagged_formula = f"[MATH]{formula}[/MATH]"
            enhanced_text = enhanced_text.replace(formula, tagged_formula)

        return enhanced_text
