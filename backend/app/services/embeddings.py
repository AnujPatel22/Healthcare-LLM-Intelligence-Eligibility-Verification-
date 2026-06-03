import hashlib
import math
import re


TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


class DeterministicEmbedding:
    def __init__(self, dimensions: int = 16) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = TOKEN_RE.findall(text.lower())
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = digest[0] % self.dimensions
            sign = 1 if digest[1] % 2 == 0 else -1
            vector[idx] += sign * (1 + len(token) / 12)
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [round(value / norm, 6) for value in vector]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left)) or 1.0
    right_norm = math.sqrt(sum(b * b for b in right)) or 1.0
    return max(0.0, min(1.0, dot / (left_norm * right_norm)))
