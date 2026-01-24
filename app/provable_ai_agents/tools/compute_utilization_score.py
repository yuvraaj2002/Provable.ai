class ComputeChunkUtilizationScore():
    def __init__(self):
        pass
    
    @staticmethod
    def compute_chunk_utilization_score(utilized_chunks: int, total_chunks: int) -> float:
        """
        Computes the chunk utilization score by dividing utilized chunks by total chunks.
        """
        if total_chunks == 0:
            return 0.0
        return utilized_chunks / total_chunks
