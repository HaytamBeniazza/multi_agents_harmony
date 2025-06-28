"""
Agent Orchestrator - Multi-Agent Collaboration System
"""

import asyncio
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, cast
from dataclasses import dataclass
from enum import Enum

from agents import (
    ResearchAgent,
    AnalysisAgent,
    ContentAgent,
    QualityAgent,
    AgentStatus,
    AgentMessage,
    AgentResult,
)
from core.config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status"""

    INITIALIZED = "initialized"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class WorkflowResult:
    """Complete workflow result"""

    workflow_id: str
    status: WorkflowStatus
    topic: str
    final_output: Dict[str, Any]
    agent_results: Dict[str, AgentResult]
    execution_summary: Dict[str, Any]
    total_execution_time: float
    timestamp: datetime


class AgentOrchestrator:
    """Orchestrates collaboration between multiple agents"""

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.content_agent = ContentAgent()
        self.quality_agent = QualityAgent()

        self.agents = {
            "research": self.research_agent,
            "analysis": self.analysis_agent,
            "content": self.content_agent,
            "quality": self.quality_agent,
        }

        self.active_workflows: Dict[str, Dict[str, Any]] = {}

    async def execute_research_workflow(self, topic: str, **kwargs) -> WorkflowResult:
        """
        Execute the complete research and content creation workflow
        """
        workflow_id = kwargs.get("workflow_id", str(uuid.uuid4()))
        start_time = time.time()

        logger.info(f"Starting research workflow {workflow_id} for topic: {topic}")

        workflow_data: Dict[str, Any] = {
            "id": workflow_id,
            "topic": topic,
            "status": WorkflowStatus.INITIALIZED,
            "start_time": start_time,
            "agent_results": {},
            "current_step": 0,
            "total_steps": 4,
        }

        self.active_workflows[workflow_id] = workflow_data

        try:
            # Step 1: Research Phase
            workflow_data["status"] = WorkflowStatus.RUNNING
            workflow_data["current_step"] = 1
            logger.info(f"Workflow {workflow_id}: Starting research phase")

            research_input = {
                "topic": topic,
                "depth": kwargs.get("depth", "medium"),
                "focus_areas": kwargs.get("focus_areas", []),
            }

            research_result = await self.research_agent.process(research_input)
            agent_results = cast(Dict[str, AgentResult], workflow_data["agent_results"])
            agent_results["research"] = research_result

            if research_result.status != AgentStatus.COMPLETED:
                raise Exception(
                    f"Research phase failed: {research_result.output.get('error', 'Unknown error')}"
                )

            # Step 2: Analysis Phase
            workflow_data["current_step"] = 2
            logger.info(f"Workflow {workflow_id}: Starting analysis phase")

            analysis_input = {
                "topic": topic,
                "research_findings": research_result.output["research_findings"],
                "analysis_type": kwargs.get("analysis_type", "comprehensive"),
            }

            analysis_result = await self.analysis_agent.process(analysis_input)
            agent_results["analysis"] = analysis_result

            if analysis_result.status != AgentStatus.COMPLETED:
                raise Exception(
                    f"Analysis phase failed: {analysis_result.output.get('error', 'Unknown error')}"
                )

            # Step 3: Content Creation Phase
            workflow_data["current_step"] = 3
            logger.info(f"Workflow {workflow_id}: Starting content creation phase")

            content_input = {
                "topic": topic,
                "research_findings": research_result.output["research_findings"],
                "analysis_results": analysis_result.output,
                "content_type": kwargs.get("content_type", "comprehensive_report"),
                "target_audience": kwargs.get("target_audience", "general"),
            }

            content_result = await self.content_agent.process(content_input)
            agent_results["content"] = content_result

            if content_result.status != AgentStatus.COMPLETED:
                raise Exception(
                    f"Content creation phase failed: {content_result.output.get('error', 'Unknown error')}"
                )

            # Step 4: Quality Review Phase
            workflow_data["current_step"] = 4
            logger.info(f"Workflow {workflow_id}: Starting quality review phase")

            quality_input = {
                "topic": topic,
                "content": content_result.output.get("report_content", content_result.output.get("final_content", {})),
                "review_criteria": kwargs.get("review_criteria", "comprehensive"),
            }

            quality_result = await self.quality_agent.process(quality_input)
            agent_results["quality"] = quality_result

            if quality_result.status != AgentStatus.COMPLETED:
                raise Exception(
                    f"Quality review phase failed: {quality_result.output.get('error', 'Unknown error')}"
                )

            # Check if content meets quality threshold
            quality_score = quality_result.output.get("overall_score", quality_result.output.get("overall_quality_score", 0))
            if quality_score < config.QUALITY_THRESHOLD:
                logger.warning(
                    f"Workflow {workflow_id}: Content quality below threshold, considering revision"
                )

                # In a production system, you might implement automatic revision here
                # For now, we'll include the quality feedback in the final output

            # Compile final output
            final_output = self._compile_final_output(
                topic, research_result, analysis_result, content_result, quality_result
            )

            # Generate execution summary
            execution_summary = self._generate_execution_summary(workflow_data)

            workflow_result = WorkflowResult(
                workflow_id=workflow_id,
                status=WorkflowStatus.COMPLETED,
                topic=topic,
                final_output=final_output,
                agent_results=cast(Dict[str, AgentResult], workflow_data["agent_results"]),
                execution_summary=execution_summary,
                total_execution_time=time.time() - start_time,
                timestamp=datetime.now(),
            )

            workflow_data["status"] = WorkflowStatus.COMPLETED
            logger.info(
                f"Workflow {workflow_id} completed successfully in {workflow_result.total_execution_time:.2f} seconds"
            )

            return workflow_result

        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            workflow_data["status"] = WorkflowStatus.FAILED

            # Return partial results if available
            partial_output = self._compile_partial_output(
                cast(Dict[str, AgentResult], workflow_data.get("agent_results", {})), str(e)
            )

            return WorkflowResult(
                workflow_id=workflow_id,
                status=WorkflowStatus.FAILED,
                topic=topic,
                final_output=partial_output,
                agent_results=cast(Dict[str, AgentResult], workflow_data.get("agent_results", {})),
                execution_summary={
                    "error": str(e),
                    "failed_at_step": workflow_data.get("current_step", 0),
                },
                total_execution_time=time.time() - start_time,
                timestamp=datetime.now(),
            )

    def _compile_final_output(
        self,
        topic: str,
        research_result: AgentResult,
        analysis_result: AgentResult,
        content_result: AgentResult,
        quality_result: AgentResult,
    ) -> Dict[str, Any]:
        """Compile final comprehensive output - compatible with both old and new agent structures"""
        return {
            "topic": topic,
            "research_phase": {
                "findings": research_result.output.get("research_findings", {}),
                "sources": research_result.output.get("sources", []),
                "execution_time": research_result.execution_time,
            },
            "analysis_phase": {
                "insights": analysis_result.output.get("analysis_results", {}).get("insights", analysis_result.output.get("analytical_insights", [])),
                "trends": analysis_result.output.get("analysis_results", {}).get("key_trends", analysis_result.output.get("trend_analysis", [])),
                "recommendations": analysis_result.output.get("analysis_results", {}).get("recommendations", analysis_result.output.get("recommendations", [])),
                "confidence_score": analysis_result.output.get("analysis_results", {}).get("confidence_score", analysis_result.output.get("confidence_score", 0.8)),
                "execution_time": analysis_result.execution_time,
            },
            "content_phase": {
                "report_content": content_result.output.get("report_content", content_result.output.get("final_content", {})),
                "metadata": content_result.output.get("metadata", {"word_count": content_result.output.get("word_count", 0)}),
                "execution_time": content_result.execution_time,
            },
            "quality_phase": {
                "quality_score": quality_result.output.get("overall_score", quality_result.output.get("overall_quality_score", 0)),
                "quality_assessment": quality_result.output.get("quality_assessment", quality_result.output.get("quality_report", {})),
                "quality_grade": quality_result.output.get("quality_grade", "B+"),
                "improvement_suggestions": quality_result.output.get("quality_assessment", {}).get("improvements", quality_result.output.get("improvement_suggestions", [])),
                "execution_time": quality_result.execution_time,
            },
            "workflow_metadata": {
                "total_sources_analyzed": len(research_result.output.get("sources", [])),
                "total_recommendations": len(analysis_result.output.get("analysis_results", {}).get("recommendations", analysis_result.output.get("recommendations", []))),
                "final_word_count": content_result.output.get("word_count", content_result.output.get("metadata", {}).get("word_count", 0)),
                "overall_quality_score": quality_result.output.get("overall_score", quality_result.output.get("overall_quality_score", 0)),
                "generated_timestamp": datetime.now().isoformat(),
            },
        }

    def _compile_partial_output(
        self, agent_results: Dict[str, AgentResult], error: str
    ) -> Dict[str, Any]:
        """Compile partial output when workflow fails"""
        output: Dict[str, Any] = {
            "status": "failed",
            "error": error,
            "completed_phases": list(agent_results.keys()),
            "partial_results": {},
        }

        partial_results = cast(Dict[str, Dict[str, Any]], output["partial_results"])
        for phase, result in agent_results.items():
            if result.status == AgentStatus.COMPLETED:
                partial_results[phase] = {
                    "output": result.output,
                    "execution_time": result.execution_time,
                }

        return output

    def _generate_execution_summary(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate execution summary with metrics"""
        agent_results = cast(Dict[str, AgentResult], workflow_data["agent_results"])

        return {
            "workflow_id": workflow_data["id"],
            "topic": workflow_data["topic"],
            "total_steps_completed": len(agent_results),
            "total_execution_time": time.time() - workflow_data["start_time"],
            "agent_performance": {
                agent_name: {
                    "execution_time": result.execution_time,
                    "status": result.status.value,
                    "output_size": len(str(result.output)),
                }
                for agent_name, result in agent_results.items()
            },
            "success_rate": (
                len([r for r in agent_results.values() if r.status == AgentStatus.COMPLETED])
                / len(agent_results)
                if agent_results
                else 0
            ),
            "quality_metrics": {
                "research_sources": len(
                    agent_results.get(
                        "research", AgentResult("", AgentStatus.ERROR, {}, {}, 0, datetime.now())
                    ).output.get("sources", [])
                ),
                "analysis_insights": len(
                    str(
                        agent_results.get(
                            "analysis",
                            AgentResult("", AgentStatus.ERROR, {}, {}, 0, datetime.now()),
                        ).output.get("analytical_insights", {})
                    )
                ),
                "content_word_count": agent_results.get(
                    "content", AgentResult("", AgentStatus.ERROR, {}, {}, 0, datetime.now())
                )
                .output.get("metadata", {})
                .get("word_count", 0),
                "final_quality_score": agent_results.get(
                    "quality", AgentResult("", AgentStatus.ERROR, {}, {}, 0, datetime.now())
                ).output.get("overall_score", 
                    agent_results.get(
                        "quality", AgentResult("", AgentStatus.ERROR, {}, {}, 0, datetime.now())
                    ).output.get("overall_quality_score", 0)
                ),
            },
        }

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a workflow"""
        return self.active_workflows.get(workflow_id)

    def get_agent_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Get capabilities of all agents"""
        return {agent_name: agent.get_capabilities() for agent_name, agent in self.agents.items()}

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get overall system performance metrics"""
        return {
            "total_workflows_executed": len(self.active_workflows),
            "agent_metrics": {
                agent_name: agent.get_metrics() for agent_name, agent in self.agents.items()
            },
            "system_status": "operational",
            "last_updated": datetime.now().isoformat(),
        }
