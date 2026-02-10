"""Research Agent using LangGraph workflow orchestration.

This module defines the main research agent that uses LangGraph to orchestrate
the research workflow with planning, searching, citation tracking, and report generation.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from research_agent.state import ResearchState
from research_agent.nodes import (
    planning_node,
    search_node,
    synthesis_node,
    should_continue
)


class ResearchAgent:
    """Autonomous Research Agent using LangGraph.
    
    This agent can autonomously:
    - Plan research steps
    - Search for information using multiple tools
    - Track and manage citations
    - Generate comprehensive reports with proper citations
    """
    
    def __init__(self):
        """Initialize the Research Agent with LangGraph workflow."""
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow.
        
        The workflow consists of:
        1. Planning: Analyze query and create research plan
        2. Search: Execute searches and collect information (repeats)
        3. Synthesis: Generate final report with citations
        
        Returns:
            Compiled LangGraph workflow
        """
        # Create the graph
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("plan", planning_node)
        workflow.add_node("search", search_node)
        workflow.add_node("synthesize", synthesis_node)
        
        # Define the flow
        # Start with planning
        workflow.set_entry_point("plan")
        
        # After planning, go to search
        workflow.add_edge("plan", "search")
        
        # After search, decide whether to continue searching or synthesize
        workflow.add_conditional_edges(
            "search",
            should_continue,
            {
                "search": "search",  # Continue searching
                "synthesize": "synthesize"  # Move to synthesis
            }
        )
        
        # After synthesis, end the workflow
        workflow.add_edge("synthesize", END)
        
        # Compile the graph
        return workflow.compile()
    
    def research(self, query: str) -> Dict[str, Any]:
        """Conduct research on a given query.
        
        Args:
            query: The research question or topic
            
        Returns:
            Dictionary containing the final report and metadata
        """
        # Initialize state
        initial_state = {
            "query": query,
            "plan": [],
            "current_step": 0,
            "messages": [],
            "collected_info": [],
            "citations": [],
            "report": "",
            "is_complete": False
        }
        
        # Run the workflow
        final_state = self.graph.invoke(initial_state)
        
        # Return results
        return {
            "query": query,
            "report": final_state["report"],
            "citations": final_state["citations"],
            "plan": final_state["plan"],
            "messages": final_state["messages"]
        }
    
    async def research_async(self, query: str) -> Dict[str, Any]:
        """Conduct research asynchronously.
        
        Args:
            query: The research question or topic
            
        Returns:
            Dictionary containing the final report and metadata
        """
        # Initialize state
        initial_state = {
            "query": query,
            "plan": [],
            "current_step": 0,
            "messages": [],
            "collected_info": [],
            "citations": [],
            "report": "",
            "is_complete": False
        }
        
        # Run the workflow asynchronously
        final_state = await self.graph.ainvoke(initial_state)
        
        # Return results
        return {
            "query": query,
            "report": final_state["report"],
            "citations": final_state["citations"],
            "plan": final_state["plan"],
            "messages": final_state["messages"]
        }
    
    def visualize(self, output_path: str = "research_workflow.png"):
        """Visualize the research workflow graph.
        
        Args:
            output_path: Path to save the visualization
        """
        try:
            from IPython.display import Image, display
            display(Image(self.graph.get_graph().draw_mermaid_png()))
        except ImportError:
            print("To visualize the graph, install: pip install pygraphviz")
        except Exception as e:
            print(f"Visualization error: {e}")


def create_research_agent() -> ResearchAgent:
    """Factory function to create a Research Agent instance.
    
    Returns:
        Configured ResearchAgent instance
    """
    return ResearchAgent()
