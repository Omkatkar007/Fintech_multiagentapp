"""Prompt templates used by optional LLM-backed agents."""

REVIEW_PROMPT = """You are the {role} reviewer for a business proposal.
Focus: {focus}
Use only the supplied proposal evidence. Return concise JSON with keys:
summary, strengths (array), concerns (array), questions (array), risk_level.

Proposal evidence:
{context}
"""
