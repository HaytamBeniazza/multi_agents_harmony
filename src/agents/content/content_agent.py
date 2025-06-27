"""
Content Agent - Report and Article Generation
"""
import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from ..base.base_agent import BaseAgent, AgentResult, AgentStatus
from ...core.config import config

class ContentAgent(BaseAgent):
    """Agent responsible for creating structured content from analyzed data"""
    
    def __init__(self):
        super().__init__(
            name="ContentAgent",
            description="Creates structured reports, articles, and content from research and analysis"
        )
        self.llm = ChatOpenAI(
            temperature=config.OPENAI_TEMPERATURE,
            model_name=config.OPENAI_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )
        
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Generate structured content from research and analysis"""
        start_time = time.time()
        self.update_status(AgentStatus.WORKING)
        
        try:
            if not self.validate_input(input_data):
                raise ValueError("Invalid input data")
            
            topic = input_data['topic']
            research_findings = input_data['research_findings']
            analysis_results = input_data['analysis_results']
            content_type = input_data.get('content_type', 'comprehensive_report')
            
            # Generate content sections
            executive_summary = await self._create_executive_summary(topic, research_findings, analysis_results)
            main_content = await self._create_main_content(topic, research_findings, analysis_results)
            recommendations_section = await self._create_recommendations_section(analysis_results)
            
            # Assemble final content
            final_content = self._assemble_content(
                topic, executive_summary, main_content, recommendations_section, content_type
            )
            
            # Generate metadata
            content_metadata = self._generate_content_metadata(final_content, topic, content_type)
            
            result = AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output={
                    'topic': topic,
                    'content_type': content_type,
                    'final_content': final_content,
                    'executive_summary': executive_summary,
                    'main_sections': main_content,
                    'recommendations': recommendations_section,
                    'metadata': content_metadata
                },
                metadata={
                    'content_type': content_type,
                    'word_count': content_metadata['word_count'],
                    'sections_count': len(main_content),
                    'recommendations_count': len(recommendations_section.get('recommendations', []))
                },
                execution_time=time.time() - start_time,
                timestamp=datetime.now()
            )
            
            self.update_status(AgentStatus.COMPLETED)
            self.log_result(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Content generation failed: {str(e)}")
            result = AgentResult(
                agent_name=self.name,
                status=AgentStatus.ERROR,
                output={'error': str(e)},
                metadata={'error_type': type(e).__name__},
                execution_time=time.time() - start_time,
                timestamp=datetime.now()
            )
            self.update_status(AgentStatus.ERROR)
            self.log_result(result)
            return result
    
    async def _create_executive_summary(self, topic: str, research_findings: Dict[str, Any], 
                                        analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary section"""
        return {
            'title': f"Executive Summary: {topic}",
            'content': f"This comprehensive analysis of {topic} provides valuable insights based on extensive research and expert analysis. Key findings reveal significant opportunities and strategic implications for stakeholders.",
            'key_points': research_findings.get('main_findings', [])[:3],
            'word_count': 200
        }
    
    async def _create_main_content(self, topic: str, research_findings: Dict[str, Any], 
                                   analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create main content sections"""
        sections = []
        
        # Introduction section
        intro = {
            'title': f"Introduction to {topic}",
            'content': f"This comprehensive report examines {topic}, providing in-depth analysis based on current research and industry insights.",
            'subsections': []
        }
        sections.append(intro)
        
        # Research findings section
        research_section = {
            'title': f"Research Findings on {topic}",
            'content': f"Our comprehensive research on {topic} reveals several key findings.",
            'subsections': [
                {
                    'title': 'Key Findings',
                    'content': '\n'.join([f"• {finding}" for finding in research_findings.get('main_findings', [])])
                },
                {
                    'title': 'Current Trends',
                    'content': '\n'.join([f"• {trend}" for trend in research_findings.get('current_trends', [])])
                }
            ]
        }
        sections.append(research_section)
        
        # Analysis section
        analysis_section = {
            'title': f"Analysis and Insights on {topic}",
            'content': f"Deep analysis of the research findings reveals important patterns and implications for {topic}.",
            'subsections': [
                {
                    'title': 'Key Insights', 
                    'content': '\n'.join([f"• {insight}" for insight in analysis_results.get('synthesis', {}).get('key_insights', [])])
                },
                {
                    'title': 'Strategic Implications',
                    'content': '\n'.join([f"• {implication}" for implication in analysis_results.get('synthesis', {}).get('strategic_implications', [])])
                }
            ]
        }
        sections.append(analysis_section)
        
        return sections
    
    async def _create_recommendations_section(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create recommendations section"""
        recommendations = analysis_results.get('recommendations', [])
        
        return {
            'title': 'Strategic Recommendations',
            'content': 'Based on our comprehensive analysis, we recommend the following strategic actions:',
            'recommendations': [
                {
                    'priority': rec.get('priority', 'Medium'),
                    'action': rec.get('action', ''),
                    'rationale': rec.get('rationale', ''),
                    'expected_impact': rec.get('expected_impact', ''),
                    'time_horizon': rec.get('time_horizon', '')
                }
                for rec in recommendations
            ]
        }
    
    def _assemble_content(self, topic: str, executive_summary: Dict[str, Any], 
                          main_content: List[Dict[str, Any]], recommendations: Dict[str, Any], 
                          content_type: str) -> Dict[str, Any]:
        """Assemble all content into final structure"""
        return {
            'title': f"Comprehensive Analysis: {topic}",
            'subtitle': f"Research, Analysis, and Strategic Recommendations",
            'executive_summary': executive_summary,
            'main_sections': main_content,
            'recommendations': recommendations,
            'document_info': {
                'generated_date': datetime.now().strftime('%Y-%m-%d'),
                'content_type': content_type,
                'total_sections': len(main_content) + 2
            }
        }
    
    def _generate_content_metadata(self, content: Dict[str, Any], topic: str, content_type: str) -> Dict[str, Any]:
        """Generate content metadata"""
        word_count = 0
        if content.get('executive_summary', {}).get('content'):
            word_count += len(content['executive_summary']['content'].split())
        
        for section in content.get('main_sections', []):
            if section.get('content'):
                word_count += len(section['content'].split())
        
        return {
            'word_count': word_count,
            'estimated_reading_time': max(1, word_count // 200),
            'content_type': content_type,
            'topic': topic,
            'sections_count': len(content.get('main_sections', [])),
            'generated_date': datetime.now().isoformat(),
            'quality_indicators': {
                'comprehensive': word_count > config.MIN_CONTENT_LENGTH,
                'structured': len(content.get('main_sections', [])) >= 3,
                'actionable': len(content.get('recommendations', {}).get('recommendations', [])) > 0
            }
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities"""
        return {
            'content_types': ['comprehensive_report', 'executive_briefing', 'research_summary'],
            'output_formats': ['structured_text', 'markdown', 'html'],
            'max_length': 10000,
            'languages': ['en']
        }
    
    def get_required_fields(self) -> List[str]:
        """Return required input fields"""
        return ['topic', 'research_findings', 'analysis_results'] 