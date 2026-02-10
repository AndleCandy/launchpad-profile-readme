"""Tests for citation management utilities."""

from research_agent.utils.citation import CitationManager, create_citation


class TestCitationManager:
    def test_init_default(self):
        manager = CitationManager()
        assert manager.citations == []
        assert manager.citation_counter == 0

    def test_init_with_start_index(self):
        manager = CitationManager(start_index=5)
        assert manager.citation_counter == 5

    def test_add_citation_returns_id(self):
        manager = CitationManager()
        citation_id = manager.add_citation("Title", "http://example.com", "excerpt")
        assert citation_id == "[1]"

    def test_add_multiple_citations_sequential_ids(self):
        manager = CitationManager()
        id1 = manager.add_citation("Title 1", "http://example.com/1", "excerpt 1")
        id2 = manager.add_citation("Title 2", "http://example.com/2", "excerpt 2")
        id3 = manager.add_citation("Title 3", "http://example.com/3", "excerpt 3")
        assert id1 == "[1]"
        assert id2 == "[2]"
        assert id3 == "[3]"

    def test_add_citation_with_start_index(self):
        manager = CitationManager(start_index=3)
        citation_id = manager.add_citation("Title", "http://example.com", "excerpt")
        assert citation_id == "[4]"

    def test_add_citation_stored_correctly(self):
        manager = CitationManager()
        manager.add_citation("My Title", "http://example.com", "my excerpt")
        assert len(manager.citations) == 1
        citation = manager.citations[0]
        assert citation["title"] == "My Title"
        assert citation["url"] == "http://example.com"
        assert citation["excerpt"] == "my excerpt"
        assert citation["source_id"] == "[1]"
        assert "timestamp" in citation

    def test_get_citations_returns_copy(self):
        manager = CitationManager()
        manager.add_citation("Title", "http://example.com", "excerpt")
        citations = manager.get_citations()
        citations.clear()
        assert len(manager.citations) == 1  # original unaffected

    def test_get_citations_empty(self):
        manager = CitationManager()
        assert manager.get_citations() == []

    def test_format_citations_empty(self):
        manager = CitationManager()
        assert manager.format_citations() == ""

    def test_format_citations_non_empty(self):
        manager = CitationManager()
        manager.add_citation("Title 1", "http://example.com/1", "excerpt 1")
        manager.add_citation("Title 2", "http://example.com/2", "excerpt 2")
        formatted = manager.format_citations()
        assert "## References" in formatted
        assert "[1] Title 1" in formatted
        assert "[2] Title 2" in formatted
        assert "http://example.com/1" in formatted
        assert "http://example.com/2" in formatted

    def test_format_citation_inline(self):
        manager = CitationManager()
        result = manager.format_citation_inline("[1]")
        assert result == "[1]"


class TestCreateCitation:
    def test_basic_creation(self):
        source_info = {
            "title": "Test Article",
            "url": "http://example.com",
            "snippet": "A test snippet"
        }
        citation = create_citation(source_info)
        assert citation["title"] == "Test Article"
        assert citation["url"] == "http://example.com"
        assert citation["excerpt"] == "A test snippet"
        assert "timestamp" in citation

    def test_with_explicit_excerpt(self):
        source_info = {
            "title": "Test",
            "url": "http://example.com",
            "snippet": "default snippet"
        }
        citation = create_citation(source_info, excerpt="custom excerpt")
        assert citation["excerpt"] == "custom excerpt"

    def test_missing_title_uses_default(self):
        citation = create_citation({})
        assert citation["title"] == "Unknown Source"

    def test_missing_url_uses_empty(self):
        citation = create_citation({})
        assert citation["url"] == ""

    def test_summary_fallback(self):
        source_info = {
            "title": "Wiki Article",
            "url": "http://example.com",
            "summary": "A wiki summary"
        }
        citation = create_citation(source_info)
        assert citation["excerpt"] == "A wiki summary"
