"""
Example usage of the Research Agent.

This script demonstrates how to use the autonomous research agent to:
1. Plan research on a topic
2. Search for information
3. Track citations
4. Generate a comprehensive report
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from research_agent.agent import create_research_agent


def main():
    """Run an example research query."""
    
    print("=" * 80)
    print("Research Agent - Example Usage")
    print("=" * 80)
    print()
    
    # Create the research agent
    print("Initializing Research Agent...")
    agent = create_research_agent()
    print("✓ Agent initialized with LangGraph workflow")
    print()
    
    # Define a research query
    query = "What is LangGraph and how does it work?"
    print(f"Research Query: {query}")
    print("-" * 80)
    print()
    
    # Conduct research
    print("Starting research process...")
    print()
    
    try:
        results = agent.research(query)
        
        # Display the research plan
        print("Research Plan:")
        for i, step in enumerate(results["plan"], 1):
            print(f"  {i}. {step}")
        print()
        
        # Display citations
        print(f"Citations Found: {len(results['citations'])}")
        print()
        
        # Display the final report
        print("=" * 80)
        print("FINAL RESEARCH REPORT")
        print("=" * 80)
        print()
        print(results["report"])
        print()
        
        # Save the report to a file
        output_file = "research_report.md"
        with open(output_file, "w") as f:
            f.write(results["report"])
        
        print("=" * 80)
        print(f"✓ Research completed successfully!")
        print(f"✓ Report saved to: {output_file}")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error during research: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
