"""Tests for research agent workflow nodes."""

from research_agent.nodes import planning_node, search_node, synthesis_node, should_continue


def _make_initial_state():
    """Create a minimal initial state for testing."""
    return {
        "query": "test topic",
        "plan": [],
        "current_step": 0,
        "messages": [],
        "collected_info": [],
        "citations": [],
        "report": "",
        "is_complete": False
    }


class TestPlanningNode:
    def test_returns_plan(self):
        state = _make_initial_state()
        result = planning_node(state)
        assert "plan" in result
        assert isinstance(result["plan"], list)
        assert len(result["plan"]) > 0

    def test_plan_references_query(self):
        state = _make_initial_state()
        state["query"] = "artificial intelligence"
        result = planning_node(state)
        for step in result["plan"][:-1]:  # last step is synthesis
            assert "artificial intelligence" in step

    def test_current_step_reset(self):
        state = _make_initial_state()
        state["current_step"] = 5
        result = planning_node(state)
        assert result["current_step"] == 0

    def test_message_added(self):
        state = _make_initial_state()
        result = planning_node(state)
        assert len(result["messages"]) == 1
        assert "plan" in result["messages"][0]["content"].lower()


class TestSearchNode:
    def test_returns_citations(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "synthesize"]
        state["current_step"] = 0
        result = search_node(state)
        assert "citations" in result
        assert isinstance(result["citations"], list)
        assert len(result["citations"]) > 0

    def test_returns_collected_info(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "synthesize"]
        state["current_step"] = 0
        result = search_node(state)
        assert "collected_info" in result
        assert isinstance(result["collected_info"], list)
        assert len(result["collected_info"]) > 0

    def test_increments_step(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "synthesize"]
        state["current_step"] = 0
        result = search_node(state)
        assert result["current_step"] == 1

    def test_step0_uses_web_search(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "step3", "step4", "synthesize"]
        state["current_step"] = 0
        result = search_node(state)
        # Web search produces 3 results by default
        assert len(result["citations"]) == 3

    def test_step2_uses_wikipedia(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "step3", "step4", "synthesize"]
        state["current_step"] = 2
        state["citations"] = [{"source_id": f"[{i}]"} for i in range(1, 7)]
        result = search_node(state)
        # Wikipedia produces 1 result
        assert len(result["citations"]) == 1
        assert "Wikipedia" in result["citations"][0]["title"]

    def test_step3_uses_doc_reader(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "step3", "step4", "synthesize"]
        state["current_step"] = 3
        state["citations"] = [{"source_id": f"[{i}]"} for i in range(1, 8)]
        result = search_node(state)
        # Doc reader processes 2 search results
        assert len(result["citations"]) == 2

    def test_citation_ids_unique_across_steps(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "step3", "step4", "synthesize"]
        state["current_step"] = 0

        # Step 0
        result0 = search_node(state)
        ids0 = [c["source_id"] for c in result0["citations"]]
        assert ids0 == ["[1]", "[2]", "[3]"]

        # Step 1 (simulate accumulated state)
        state["current_step"] = 1
        state["citations"] = result0["citations"]
        result1 = search_node(state)
        ids1 = [c["source_id"] for c in result1["citations"]]
        assert ids1 == ["[4]", "[5]", "[6]"]

    def test_last_step_returns_empty(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "synthesize"]
        state["current_step"] = 1  # At synthesis step
        result = search_node(state)
        assert result == {}

    def test_message_added(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "synthesize"]
        state["current_step"] = 0
        result = search_node(state)
        assert len(result["messages"]) >= 1


class TestSynthesisNode:
    def test_generates_report(self):
        state = _make_initial_state()
        state["query"] = "test topic"
        state["collected_info"] = ["info1 [1]", "info2 [2]"]
        state["citations"] = [
            {"source_id": "[1]", "title": "Source 1", "url": "http://example.com/1", "excerpt": "excerpt 1", "timestamp": "2026-01-01"},
            {"source_id": "[2]", "title": "Source 2", "url": "http://example.com/2", "excerpt": "excerpt 2", "timestamp": "2026-01-01"},
        ]
        result = synthesis_node(state)
        assert "report" in result
        assert "test topic" in result["report"]

    def test_report_contains_sections(self):
        state = _make_initial_state()
        state["collected_info"] = ["finding 1 [1]"]
        state["citations"] = [
            {"source_id": "[1]", "title": "Source", "url": "http://example.com", "excerpt": "excerpt", "timestamp": "2026-01-01"},
        ]
        result = synthesis_node(state)
        report = result["report"]
        assert "# Research Report" in report
        assert "## Executive Summary" in report
        assert "## Main Findings" in report
        assert "## References" in report
        assert "## Conclusion" in report

    def test_report_includes_all_findings(self):
        state = _make_initial_state()
        state["collected_info"] = ["alpha [1]", "beta [2]", "gamma [3]"]
        state["citations"] = []
        result = synthesis_node(state)
        assert "alpha" in result["report"]
        assert "beta" in result["report"]
        assert "gamma" in result["report"]

    def test_is_complete_set(self):
        state = _make_initial_state()
        result = synthesis_node(state)
        assert result["is_complete"] is True

    def test_empty_citations_no_references(self):
        state = _make_initial_state()
        state["collected_info"] = []
        state["citations"] = []
        result = synthesis_node(state)
        assert "## References" not in result["report"]

    def test_message_added(self):
        state = _make_initial_state()
        result = synthesis_node(state)
        assert len(result["messages"]) == 1
        assert "completed" in result["messages"][0]["content"].lower()


class TestShouldContinue:
    def test_continue_searching(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "synthesize"]
        state["current_step"] = 0
        assert should_continue(state) == "search"

    def test_continue_searching_middle(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "step3", "synthesize"]
        state["current_step"] = 1
        assert should_continue(state) == "search"

    def test_move_to_synthesis(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "step2", "synthesize"]
        state["current_step"] = 2
        assert should_continue(state) == "synthesize"

    def test_past_end_synthesize(self):
        state = _make_initial_state()
        state["plan"] = ["step1", "synthesize"]
        state["current_step"] = 5
        assert should_continue(state) == "synthesize"
