"""Citation management utilities."""

from typing import List, Dict, Any
from datetime import datetime


class CitationManager:
    """Manages citations throughout the research process."""
    
    def __init__(self):
        self.citations: List[Dict[str, Any]] = []
        self.citation_counter = 0
    
    def add_citation(self, title: str, url: str, excerpt: str) -> str:
        """Add a new citation and return its ID.
        
        Args:
            title: Title of the source
            url: URL of the source
            excerpt: Relevant excerpt from the source
            
        Returns:
            Citation ID (e.g., "[1]")
        """
        self.citation_counter += 1
        citation_id = f"[{self.citation_counter}]"
        
        citation = {
            "source_id": citation_id,
            "title": title,
            "url": url,
            "excerpt": excerpt,
            "timestamp": datetime.now().isoformat()
        }
        
        self.citations.append(citation)
        return citation_id
    
    def get_citations(self) -> List[Dict[str, Any]]:
        """Get all citations.
        
        Returns:
            List of all citations
        """
        return self.citations.copy()
    
    def format_citations(self) -> str:
        """Format all citations for inclusion in a report.
        
        Returns:
            Formatted citation list as string
        """
        if not self.citations:
            return ""
        
        formatted = "\n## References\n\n"
        for citation in self.citations:
            formatted += f"{citation['source_id']} {citation['title']}\n"
            formatted += f"   URL: {citation['url']}\n"
            if citation['excerpt']:
                formatted += f"   Excerpt: {citation['excerpt'][:200]}...\n"
            formatted += "\n"
        
        return formatted
    
    def format_citation_inline(self, citation_id: str) -> str:
        """Format a citation for inline use.
        
        Args:
            citation_id: The citation ID
            
        Returns:
            Formatted inline citation
        """
        return citation_id


def create_citation(source_info: Dict[str, Any], excerpt: str = "") -> Dict[str, Any]:
    """Create a citation object from source information.
    
    Args:
        source_info: Dictionary with source metadata (title, url, etc.)
        excerpt: Optional excerpt from the source
        
    Returns:
        Citation dictionary
    """
    return {
        "title": source_info.get("title", "Unknown Source"),
        "url": source_info.get("url", ""),
        "excerpt": excerpt or source_info.get("snippet", source_info.get("summary", "")),
        "timestamp": datetime.now().isoformat()
    }
