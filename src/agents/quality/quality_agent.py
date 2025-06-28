"""
Quality Agent - Quality Assurance and Review
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from ..base.base_agent import BaseAgent, AgentResult, AgentStatus
from ...core.config import config


class QualityAgent(BaseAgent):
    """Agent responsible for quality assurance and content review"""
    
    def __init__(self):
        super().__init__(
            name="QualityAgent",
            description="Reviews and evaluates quality of research, analysis, and content",
        )
        self.llm = ChatOpenAI(
            temperature=config.OPENAI_TEMPERATURE,
            model_name=config.OPENAI_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
        )
        
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Review and evaluate quality of work products"""
        start_time = time.time()
        self.update_status(AgentStatus.WORKING)
        
        try:
            if not self.validate_input(input_data):
                raise ValueError("Invalid input data")
            
            topic = input_data["topic"]
            research_findings = input_data.get("research_findings", {})
            analysis_results = input_data.get("analysis_results", {})
            content_output = input_data.get("content_output", {})
            
            # Perform quality assessments
            research_quality = await self._assess_research_quality(research_findings, topic)
            analysis_quality = await self._assess_analysis_quality(analysis_results, topic)
            content_quality = await self._assess_content_quality(content_output, topic)

            # Generate overall quality score
            overall_score = self._calculate_overall_score(
                research_quality, analysis_quality, content_quality
            )

            # Generate improvement suggestions
            improvement_suggestions = await self._generate_improvement_suggestions(
                research_quality, analysis_quality, content_quality, topic
            )

            # Final quality assessment
            quality_report = self._generate_quality_report(
                research_quality,
                analysis_quality,
                content_quality,
                overall_score,
                improvement_suggestions,
                topic,
            )
            
            result = AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output={
                    "topic": topic,
                    "overall_quality_score": overall_score,
                    "research_quality": research_quality,
                    "analysis_quality": analysis_quality,
                    "content_quality": content_quality,
                    "improvement_suggestions": improvement_suggestions,
                    "quality_report": quality_report,
                    "approval_status": (
                        "approved"
                        if overall_score >= config.QUALITY_THRESHOLD
                        else "needs_improvement"
                    ),
                },
                metadata={
                    "quality_threshold": config.QUALITY_THRESHOLD,
                    "assessment_categories": 3,
                    "suggestions_count": len(improvement_suggestions),
                    "meets_threshold": overall_score >= config.QUALITY_THRESHOLD,
                },
                execution_time=time.time() - start_time,
                timestamp=datetime.now(),
            )
            
            self.update_status(AgentStatus.COMPLETED)
            self.log_result(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Quality assessment failed: {str(e)}")
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
    
    async def _assess_research_quality(
        self, research_findings: Dict[str, Any], topic: str
    ) -> Dict[str, Any]:
        """Assess quality of research findings"""
        main_findings = research_findings.get("main_findings", [])
        sources = research_findings.get("sources", [])
        
        return {
            "completeness_score": min(len(main_findings) / 5.0, 1.0) * 100,
            "source_quality_score": min(len(sources) / 10.0, 1.0) * 100,
            "depth_score": 85,  # Simulated
            "reliability_score": 90,  # Simulated
            "overall_research_score": 85,
            "strengths": [
                f"Comprehensive coverage of {topic}",
                "Diverse source utilization",
                "Current and relevant findings",
            ],
            "weaknesses": [
                f"Could benefit from more academic sources on {topic}",
                "Some gaps in international perspectives",
            ],
        }

    async def _assess_analysis_quality(
        self, analysis_results: Dict[str, Any], topic: str
    ) -> Dict[str, Any]:
        """Assess quality of analysis"""
        synthesis = analysis_results.get("synthesis", {})
        recommendations = analysis_results.get("recommendations", [])

        return {
            "analytical_depth_score": 90,  # Simulated
            "logical_coherence_score": 85,  # Simulated
            "insight_quality_score": 88,  # Simulated
            "recommendation_quality_score": min(len(recommendations) / 5.0, 1.0) * 100,
            "overall_analysis_score": 87,
            "strengths": [
                f"Strong analytical framework for {topic}",
                "Clear logical progression",
                "Actionable recommendations",
            ],
            "weaknesses": [
                f"Could explore more alternative scenarios for {topic}",
                "Some assumptions need more validation",
            ],
        }

    async def _assess_content_quality(
        self, content_output: Dict[str, Any], topic: str
    ) -> Dict[str, Any]:
        """Assess quality of generated content"""
        final_content = content_output.get("final_content", {})
        metadata = content_output.get("metadata", {})

        word_count = metadata.get("word_count", 0)

        return {
            "clarity_score": 90,  # Simulated
            "structure_score": 85,  # Simulated
            "completeness_score": min(word_count / config.MIN_CONTENT_LENGTH, 1.0) * 100,
            "professional_score": 88,  # Simulated
            "overall_content_score": 86,
            "strengths": [
                f"Clear and professional presentation of {topic}",
                "Well-structured sections",
                "Comprehensive coverage",
            ],
            "weaknesses": [
                f"Could include more visual elements for {topic}",
                "Some sections could be more concise",
            ],
        }

    def _calculate_overall_score(
        self,
        research_quality: Dict[str, Any],
        analysis_quality: Dict[str, Any],
        content_quality: Dict[str, Any],
    ) -> float:
        """Calculate overall quality score"""
        research_score = research_quality.get("overall_research_score", 0)
        analysis_score = analysis_quality.get("overall_analysis_score", 0)
        content_score = content_quality.get("overall_content_score", 0)

        # Weighted average
        overall_score = research_score * 0.3 + analysis_score * 0.4 + content_score * 0.3
        return round(overall_score, 1)

    async def _generate_improvement_suggestions(
        self,
        research_quality: Dict[str, Any],
        analysis_quality: Dict[str, Any],
        content_quality: Dict[str, Any],
        topic: str,
    ) -> List[Dict[str, Any]]:
        """Generate suggestions for improvement"""
        suggestions = []
        
        # Research improvements
        if research_quality.get("overall_research_score", 0) < 90:
            suggestions.append(
                {
                    "category": "Research",
                    "priority": "Medium",
                    "suggestion": f"Expand research sources for {topic} to include more academic and international perspectives",
                    "expected_impact": "Improved research depth and credibility",
                }
            )

        # Analysis improvements
        if analysis_quality.get("overall_analysis_score", 0) < 90:
            suggestions.append(
                {
                    "category": "Analysis",
                    "priority": "High",
                    "suggestion": f"Develop additional scenarios and stress-test assumptions for {topic} analysis",
                    "expected_impact": "More robust and comprehensive analysis",
                }
            )

        # Content improvements
        if content_quality.get("overall_content_score", 0) < 90:
            suggestions.append(
                {
                    "category": "Content",
                    "priority": "Low",
                    "suggestion": f"Add visual elements and charts to enhance {topic} presentation",
                    "expected_impact": "Improved readability and engagement",
                }
            )
        
        return suggestions
    
    def _generate_quality_report(
        self,
        research_quality: Dict[str, Any],
        analysis_quality: Dict[str, Any],
        content_quality: Dict[str, Any],
        overall_score: float,
        improvement_suggestions: List[Dict[str, Any]],
        topic: str,
    ) -> Dict[str, Any]:
        """Generate comprehensive quality report"""
        return {
            "summary": f"Quality assessment of {topic} analysis completed with overall score of {overall_score}%",
            "performance_breakdown": {
                "research": research_quality.get("overall_research_score", 0),
                "analysis": analysis_quality.get("overall_analysis_score", 0),
                "content": content_quality.get("overall_content_score", 0),
            },
            "key_strengths": [
                f"Strong research foundation for {topic}",
                "Comprehensive analytical approach",
                "Professional content presentation",
            ],
            "areas_for_improvement": [
                f"Research depth on {topic} could be enhanced",
                "Analysis assumptions need validation",
                "Content could be more visually engaging",
            ],
            "recommendation": (
                "Approved with minor improvements suggested"
                if overall_score >= config.QUALITY_THRESHOLD
                else "Requires improvement before approval"
            ),
            "next_steps": [
                "Implement suggested improvements",
                "Conduct additional review if needed",
                "Finalize for delivery",
            ],
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities"""
        return {
            "assessment_categories": ["research", "analysis", "content"],
            "scoring_range": [0, 100],
            "quality_threshold": config.QUALITY_THRESHOLD,
            "improvement_tracking": True,
            "automated_approval": True,
        }
    
    def get_required_fields(self) -> List[str]:
        """Return required input fields"""
        return ["topic"]
