class ComputeGroundness():
    def __init__(self):
        pass
    
    @staticmethod
    def compute_groundness_score(total_claims: int, supported_claims: int) -> float:
        """
        Computes the groundness score by dividing supported claims by total claims.
        Use this function only after you have finished verifying all individual claims.
        """
        if total_claims == 0:
            return 0.0
        return supported_claims / total_claims