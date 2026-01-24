class ComputeQueryAlignment():
    def __init__(self):
        pass

    @staticmethod
    def compute_alignment_score(verdict: str) -> float:
        """
        Converts the alignment verdict to a numerical score.
        ALIGNED = 1.0, PARTIALLY_ALIGNED = 0.5, NOT_ALIGNED = 0.0
        """
        score_map = {
            "ALIGNED": 1.0,
            "PARTIALLY_ALIGNED": 0.5,
            "NOT_ALIGNED": 0.0
        }
        return score_map.get(verdict, 0.0)