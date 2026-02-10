"""Tests for research tools."""

from research_agent.tools import (
    WebSearchTool,
    DocumentReaderTool,
    WikipediaTool,
    get_available_tools,
)


class TestWebSearchTool:
    def test_init(self):
        tool = WebSearchTool()
        assert tool.name == "web_search"
        assert tool.description

    def test_search_returns_list(self):
        tool = WebSearchTool()
        results = tool.search("test query")
        assert isinstance(results, list)
        assert len(results) == 5  # default num_results

    def test_search_custom_num_results(self):
        tool = WebSearchTool()
        results = tool.search("test query", num_results=3)
        assert len(results) == 3

    def test_search_result_fields(self):
        tool = WebSearchTool()
        results = tool.search("test query", num_results=1)
        result = results[0]
        assert "title" in result
        assert "url" in result
        assert "snippet" in result
        assert "timestamp" in result

    def test_search_query_in_results(self):
        tool = WebSearchTool()
        results = tool.search("artificial intelligence", num_results=1)
        assert "artificial intelligence" in results[0]["title"]
        assert "artificial intelligence" in results[0]["snippet"]


class TestDocumentReaderTool:
    def test_init(self):
        tool = DocumentReaderTool()
        assert tool.name == "document_reader"
        assert tool.description

    def test_read_returns_dict(self):
        tool = DocumentReaderTool()
        result = tool.read("https://example.com")
        assert isinstance(result, dict)

    def test_read_result_fields(self):
        tool = DocumentReaderTool()
        result = tool.read("https://example.com")
        assert "url" in result
        assert "title" in result
        assert "content" in result
        assert "word_count" in result
        assert "timestamp" in result

    def test_read_url_preserved(self):
        url = "https://example.com/article"
        tool = DocumentReaderTool()
        result = tool.read(url)
        assert result["url"] == url


class TestWikipediaTool:
    def test_init(self):
        tool = WikipediaTool()
        assert tool.name == "wikipedia"
        assert tool.description

    def test_search_returns_dict(self):
        tool = WikipediaTool()
        result = tool.search("Python programming")
        assert isinstance(result, dict)

    def test_search_result_fields(self):
        tool = WikipediaTool()
        result = tool.search("Python programming")
        assert "title" in result
        assert "url" in result
        assert "summary" in result
        assert "timestamp" in result

    def test_search_url_format(self):
        tool = WikipediaTool()
        result = tool.search("Python programming")
        assert "en.wikipedia.org/wiki/" in result["url"]
        assert "Python_programming" in result["url"]


class TestGetAvailableTools:
    def test_returns_dict(self):
        tools = get_available_tools()
        assert isinstance(tools, dict)

    def test_contains_all_tools(self):
        tools = get_available_tools()
        assert "web_search" in tools
        assert "document_reader" in tools
        assert "wikipedia" in tools

    def test_tool_types(self):
        tools = get_available_tools()
        assert isinstance(tools["web_search"], WebSearchTool)
        assert isinstance(tools["document_reader"], DocumentReaderTool)
        assert isinstance(tools["wikipedia"], WikipediaTool)
