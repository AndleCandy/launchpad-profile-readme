"""Node functions for the Research Agent LangGraph workflow."""

from typing import Dict, Any, List
from research_agent.state import ResearchState, Citation
from research_agent.tools import get_available_tools
from research_agent.utils import CitationManager, create_citation


def planning_node(state: ResearchState) -> ResearchState:
    """Plan the research steps based on the query.
    
    This node analyzes the research query and creates a step-by-step plan.
    
    Args:
        state: Current research state
        
    Returns:
        Updated state with research plan
    """
    query = state["query"]
    
    # Create a research plan based on the query
    # In production, this would use an LLM to generate a sophisticated plan
    plan = [
        f"Search for general information about: {query}",
        f"Find specific details and examples related to: {query}",
        f"Look for expert opinions and analysis on: {query}",
        f"Gather recent developments and news about: {query}",
        "Synthesize findings into a comprehensive report"
    ]
    
    state["plan"] = plan
    state["current_step"] = 0
    state["messages"].append({
        "role": "system",
        "content": f"Created research plan with {len(plan)} steps"
    })
    
    return state


def search_node(state: ResearchState) -> ResearchState:
    """Execute search and gather information.
    
    This node performs searches using available tools and collects information.
    
    Args:
        state: Current research state
        
    Returns:
        Updated state with collected information and citations
    """
    current_step = state["current_step"]
    plan = state["plan"]
    
    if current_step >= len(plan) - 1:  # Last step is synthesis, not search
        state["is_complete"] = False  # Ready for report generation
        return state
    
    step_description = plan[current_step]
    tools = get_available_tools()
    citation_manager = CitationManager()
    
    # Use web search tool
    web_search = tools["web_search"]
    search_results = web_search.search(state["query"], num_results=3)
    
    collected_info = []
    citations = []
    
    for result in search_results:
        # Add citation
        citation = create_citation(result)
        citation_id = citation_manager.add_citation(
            citation["title"],
            citation["url"],
            citation["excerpt"]
        )
        
        # Store citation
        citations.append({
            "source_id": citation_id,
            "title": citation["title"],
            "url": citation["url"],
            "excerpt": citation["excerpt"],
            "timestamp": citation["timestamp"]
        })
        
        # Collect information
        info = f"{result['snippet']} {citation_id}"
        collected_info.append(info)
    
    # Update state
    state["collected_info"] = collected_info
    state["citations"] = citations
    state["current_step"] = current_step + 1
    state["messages"].append({
        "role": "system",
        "content": f"Completed step {current_step + 1}/{len(plan)}: {step_description}"
    })
    
    return state


def synthesis_node(state: ResearchState) -> ResearchState:
    """Synthesize collected information into a final report.
    
    This node takes all collected information and citations to generate
    a comprehensive research report.
    
    Args:
        state: Current research state
        
    Returns:
        Updated state with final report
    """
    query = state["query"]
    collected_info = state.get("collected_info", [])
    citations = state.get("citations", [])
    
    # Build the report
    report_sections = []
    
    # Title and introduction
    report_sections.append(f"# Research Report: {query}\n")
    report_sections.append(f"## Executive Summary\n")
    report_sections.append(
        f"This report presents comprehensive research findings on '{query}'. "
        f"The research was conducted using multiple sources and includes "
        f"{len(citations)} citations.\n"
    )
    
    # Main findings
    report_sections.append(f"## Main Findings\n")
    for i, info in enumerate(collected_info, 1):
        report_sections.append(f"{i}. {info}\n")
    
    # Add citations section
    if citations:
        report_sections.append("\n## References\n")
        for citation in citations:
            report_sections.append(
                f"{citation['source_id']} {citation['title']}\n"
                f"   - URL: {citation['url']}\n"
                f"   - Excerpt: {citation['excerpt'][:150]}...\n\n"
            )
    
    # Conclusion
    report_sections.append(f"## Conclusion\n")
    report_sections.append(
        f"This research on '{query}' has compiled information from {len(citations)} "
        f"sources, providing a comprehensive overview of the topic. "
        f"The findings demonstrate the current state of knowledge and "
        f"key perspectives on this subject.\n"
    )
    
    final_report = "\n".join(report_sections)
    
    state["report"] = final_report
    state["is_complete"] = True
    state["messages"].append({
        "role": "system",
        "content": "Report generation completed"
    })
    
    return state


def should_continue(state: ResearchState) -> str:
    """Determine if research should continue or move to synthesis.
    
    Args:
        state: Current research state
        
    Returns:
        Next node to execute: "search" or "synthesize"
    """
    current_step = state["current_step"]
    plan = state["plan"]
    
    # Continue searching until we reach the synthesis step
    if current_step < len(plan) - 1:
        return "search"
    else:
        return "synthesize"
