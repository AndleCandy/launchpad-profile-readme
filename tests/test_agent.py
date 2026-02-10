"""Tests for the Research Agent."""

from research_agent.agent import ResearchAgent, create_research_agent


class TestResearchAgent:
    def test_init(self):
        agent = ResearchAgent()
        assert agent.graph is not None

    def test_research_returns_dict(self):
        agent = ResearchAgent()
        result = agent.research("test query")
        assert isinstance(result, dict)

    def test_research_contains_expected_keys(self):
        agent = ResearchAgent()
        result = agent.research("test query")
        assert "query" in result
        assert "report" in result
        assert "citations" in result
        assert "plan" in result
        assert "messages" in result

    def test_research_query_preserved(self):
        agent = ResearchAgent()
        result = agent.research("my specific query")
        assert result["query"] == "my specific query"

    def test_research_generates_plan(self):
        agent = ResearchAgent()
        result = agent.research("test query")
        assert len(result["plan"]) > 0

    def test_research_generates_report(self):
        agent = ResearchAgent()
        result = agent.research("test query")
        assert len(result["report"]) > 0
        assert "test query" in result["report"]

    def test_research_collects_citations(self):
        agent = ResearchAgent()
        result = agent.research("test query")
        assert len(result["citations"]) > 0

    def test_citation_ids_are_unique(self):
        agent = ResearchAgent()
        result = agent.research("test query")
        source_ids = [c["source_id"] for c in result["citations"]]
        assert len(source_ids) == len(set(source_ids))

    def test_report_has_proper_structure(self):
        agent = ResearchAgent()
        result = agent.research("test query")
        report = result["report"]
        assert "# Research Report" in report
        assert "## Executive Summary" in report
        assert "## Main Findings" in report
        assert "## References" in report
        assert "## Conclusion" in report

    def test_citations_have_required_fields(self):
        agent = ResearchAgent()
        result = agent.research("test query")
        for citation in result["citations"]:
            assert "source_id" in citation
            assert "title" in citation
            assert "url" in citation
            assert "excerpt" in citation
            assert "timestamp" in citation

    def test_uses_multiple_tools(self):
        """Verify that different tool types are used across steps."""
        agent = ResearchAgent()
        result = agent.research("test query")
        citations = result["citations"]
        # Should have Wikipedia citation from step 2
        wiki_citations = [c for c in citations if "Wikipedia" in c["title"]]
        assert len(wiki_citations) >= 1


class TestCreateResearchAgent:
    def test_returns_agent_instance(self):
        agent = create_research_agent()
        assert isinstance(agent, ResearchAgent)

    def test_agent_is_functional(self):
        agent = create_research_agent()
        result = agent.research("quick test")
        assert result["report"]
