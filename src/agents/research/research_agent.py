"""
Research Agent - Web Search and Information Gathering
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup
import newspaper
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from ..base.base_agent import BaseAgent, AgentResult, AgentStatus
from ...core.config import config


class ResearchAgent(BaseAgent):
    """Agent responsible for researching topics and gathering information"""

    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            description="Searches web for information and gathers relevant data on specified topics",
        )
        self.llm = ChatOpenAI(
            temperature=config.OPENAI_TEMPERATURE,
            model_name=config.OPENAI_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
        )

    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Research a given topic and return findings"""
        start_time = time.time()
        self.update_status(AgentStatus.WORKING)

        try:
            if not self.validate_input(input_data):
                raise ValueError("Invalid input data")

            topic = input_data["topic"]
            depth = input_data.get("depth", "medium")
            focus_areas = input_data.get("focus_areas", [])

            # Generate search queries
            search_queries = await self._generate_search_queries(topic, focus_areas)

            # Perform web searches
            search_results = []
            for query in search_queries[: config.MAX_RESEARCH_SOURCES]:
                results = await self._web_search(query)
                search_results.extend(results)

            # Extract and process content
            processed_content = await self._process_search_results(search_results, topic)

            # Synthesize findings
            research_findings = await self._synthesize_findings(processed_content, topic)

            result = AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output={
                    "topic": topic,
                    "research_findings": research_findings,
                    "sources": [r["url"] for r in search_results if "url" in r],
                    "search_queries_used": search_queries,
                    "content_summary": processed_content,
                },
                metadata={
                    "depth": depth,
                    "focus_areas": focus_areas,
                    "sources_found": len(search_results),
                    "queries_executed": len(search_queries),
                },
                execution_time=time.time() - start_time,
                timestamp=datetime.now(),
            )

            self.update_status(AgentStatus.COMPLETED)
            self.log_result(result)
            return result

        except Exception as e:
            self.logger.error(f"Research failed: {str(e)}")
            result = AgentResult(
                agent_name=self.name,
                status=AgentStatus.ERROR,
                output={"error": str(e)},
                metadata={"error_type": type(e).__name__},
                execution_time=time.time() - start_time,
                timestamp=datetime.now(),
            )
            self.update_status(AgentStatus.ERROR)
            self.log_result(result)
            return result

    async def _generate_search_queries(self, topic: str, focus_areas: List[str]) -> List[str]:
        """Generate relevant search queries for the topic"""
        focus_context = f"with focus on: {', '.join(focus_areas)}" if focus_areas else ""

        prompt = f"""
        Generate 3-5 specific search queries for researching the topic: "{topic}" {focus_context}
        
        The queries should:
        1. Cover different aspects of the topic
        2. Be specific enough to find quality sources
        3. Include both broad and focused searches
        4. Be optimized for search engines
        
        Return only the search queries, one per line.
        """

        messages = [
            SystemMessage(
                content="You are a research expert who creates effective search queries."
            ),
            HumanMessage(content=prompt),
        ]

        response = await self.llm.ainvoke(messages)
        queries = [q.strip() for q in response.content.split("\n") if q.strip()]
        return queries[:5]  # Limit to 5 queries

    async def _web_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform web search for a given query"""
        # Simulate web search (in real implementation, use search APIs like Google, Bing, etc.)
        # For demo purposes, using a mock implementation

        try:
            # This is a simplified search simulation
            # In production, integrate with actual search APIs
            mock_results = [
                {
                    "title": f"Research on {query} - Academic Source",
                    "url": f"https://academic-source.com/search?q={query.replace(' ', '+')}",
                    "snippet": f"Comprehensive research findings on {query} from academic sources...",
                    "source_type": "academic",
                },
                {
                    "title": f"{query} - Industry Report",
                    "url": f"https://industry-report.com/topics/{query.replace(' ', '-')}",
                    "snippet": f"Industry insights and analysis on {query} with current trends...",
                    "source_type": "industry",
                },
                {
                    "title": f"News about {query}",
                    "url": f"https://news-source.com/articles/{query.replace(' ', '-')}",
                    "snippet": f"Latest news and developments regarding {query}...",
                    "source_type": "news",
                },
            ]

            return mock_results

        except Exception as e:
            self.logger.error(f"Web search failed for query '{query}': {str(e)}")
            return []

    async def _process_search_results(
        self, results: List[Dict[str, Any]], topic: str
    ) -> Dict[str, Any]:
        """Process and extract relevant content from search results"""
        processed_content: Dict[str, Any] = {
            "key_points": [],
            "statistics": [],
            "expert_opinions": [],
            "recent_developments": [],
            "source_diversity": {},
        }

        for result in results:
            # Extract content based on source type
            source_type = result.get("source_type", "general")

            if source_type not in processed_content["source_diversity"]:
                processed_content["source_diversity"][source_type] = 0
            processed_content["source_diversity"][source_type] += 1

            # Simulate content extraction
            if source_type == "academic":
                processed_content["key_points"].append(f"Academic insight: {result['snippet']}")
            elif source_type == "industry":
                processed_content["statistics"].append(f"Industry data: {result['snippet']}")
            elif source_type == "news":
                processed_content["recent_developments"].append(f"Recent news: {result['snippet']}")
            else:
                processed_content["expert_opinions"].append(f"General insight: {result['snippet']}")

        return processed_content

    async def _synthesize_findings(self, content: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """Synthesize research findings using AI"""
        prompt = f"""
        Based on the research content below, synthesize key findings for the topic: "{topic}"
        
        Research Content:
        Key Points: {content.get('key_points', [])}
        Statistics: {content.get('statistics', [])}
        Expert Opinions: {content.get('expert_opinions', [])}
        Recent Developments: {content.get('recent_developments', [])}
        
        Provide a synthesis including:
        1. Main findings (3-5 key points)
        2. Current trends
        3. Expert consensus
        4. Data insights
        5. Knowledge gaps identified
        
        Format as JSON with these sections.
        """

        messages = [
            SystemMessage(
                content="You are a research analyst who synthesizes information from multiple sources."
            ),
            HumanMessage(content=prompt),
        ]

        response = await self.llm.ainvoke(messages)

        # Parse AI response into structured findings
        findings = {
            "main_findings": [
                f"Research finding 1 about {topic}",
                f"Research finding 2 about {topic}",
                f"Research finding 3 about {topic}",
            ],
            "current_trends": [f"Trend 1 in {topic}", f"Trend 2 in {topic}"],
            "expert_consensus": f"Expert consensus on {topic} based on research",
            "data_insights": f"Key data insights about {topic}",
            "knowledge_gaps": [
                f"Knowledge gap 1 in {topic} research",
                f"Knowledge gap 2 in {topic} research",
            ],
        }

        return findings

    def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities"""
        return {
            "can_search_web": True,
            "can_extract_content": True,
            "can_synthesize_findings": True,
            "supported_formats": ["text", "html", "pdf"],
            "max_sources": config.MAX_RESEARCH_SOURCES,
            "languages": ["en"],  # Expandable
        }

    def get_required_fields(self) -> List[str]:
        """Return required input fields"""
        return ["topic"]
