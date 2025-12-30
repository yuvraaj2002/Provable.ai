from pydantic import BaseModel, Field, field_validator
from typing import Dict
from app.core.config import settings
import tiktoken
from concurrent.futures import ThreadPoolExecutor, as_completed

class ContextChunk(BaseModel):
    """Simple model for a retrieved context chunk"""
    content: str = Field(...)
    chunk_id: str = Field(...)
    score: float = Field(..., ge=0.0, le=1.0)

class EvaluateGeneratorRequest(BaseModel):
    """Simple request model for evaluation of the Generator part of the RAG architecture"""
    query: str = Field(..., min_length=1)
    context_retrieved: Dict[str, ContextChunk] = Field(...)
    llm_response: str = Field(..., min_length=1)
    
    @field_validator('context_retrieved')
    @classmethod
    def validate_context_chunks(cls, v: Dict[str, ContextChunk]) -> Dict[str, ContextChunk]:
        """
        Validate context chunks:
        1. Check that the number of chunks does not exceed the maximum allowed count
        2. Check that no chunk exceeds 1000 tokens using parallel token counting
        """
        # First validation: Check chunk count
        max_chunks = settings.MAX_CHUNKS
        if len(v) > max_chunks:
            raise ValueError(
                f"The number of context chunks ({len(v)}) exceeds the maximum allowed count of {max_chunks}. "
                f"Please provide no more than {max_chunks} context chunks."
            )
        
        # Second validation: Check token count for each chunk (parallelized)
        # Get encoding for GPT-4 model (gpt-4.1 uses the same encoding as gpt-4)
        try:
            encoding = tiktoken.encoding_for_model("gpt-4")
        except KeyError:
            # Fallback to cl100k_base encoding if model not found
            encoding = tiktoken.get_encoding("cl100k_base")
        
        max_tokens_per_chunk = settings.MAX_TOKEN_PER_CHUNK
        max_workers = min(len(v), 10)  # Limit to 10 workers max
        
        def count_tokens(chunk_id: str, content: str) -> tuple[str, int]:
            """Count tokens for a single chunk"""
            token_count = len(encoding.encode(content))
            return chunk_id, token_count
        
        # Parallelize token counting using ThreadPoolExecutor
        invalid_chunks = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all token counting tasks
            future_to_chunk = {
                executor.submit(count_tokens, chunk_id, chunk.content): chunk_id
                for chunk_id, chunk in v.items()
            }
            
            # Collect results
            for future in as_completed(future_to_chunk):
                chunk_id, token_count = future.result()
                if token_count > max_tokens_per_chunk:
                    invalid_chunks.append((chunk_id, token_count))
        
        # Raise error if any chunk exceeds the limit
        if invalid_chunks:
            error_messages = [
                f"Chunk '{chunk_id}' has {token_count} tokens (exceeds limit of {max_tokens_per_chunk})"
                for chunk_id, token_count in invalid_chunks
            ]
            raise ValueError(
                f"One or more context chunks exceed the maximum token limit of {max_tokens_per_chunk}:\n"
                + "\n".join(error_messages)
            )
        
        return v