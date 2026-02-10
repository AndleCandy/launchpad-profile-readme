"""State model for the Research Agent."""

from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import add_messages
from operator import add


class Citation(TypedDict):
    """A citation with source information."""
    source_id: str
    title: str
    url: str
    excerpt: str
    timestamp: str


class ResearchState(TypedDict):
    """State for the research agent workflow.
    
    This state is passed between nodes in the LangGraph workflow.
    """
    # User's research query
    query: str
    
    # Research plan - list of steps to execute
    plan: List[str]
    
    # Current step being executed
    current_step: int
    
    # Messages exchanged during research
    messages: Annotated[List[Dict[str, Any]], add_messages]
    
    # Collected information from various sources
    collected_info: Annotated[List[str], add]
    
    # Citations tracking
    citations: Annotated[List[Citation], add]
    
    # Final report
    report: str
    
    # Whether research is complete
    is_complete: bool
