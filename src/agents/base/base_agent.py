"""
Base Agent Class for AI Research & Content Creation Team
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
from enum import Enum

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class AgentMessage:
    """Message structure for agent communication"""
    sender: str
    recipient: str
    content: Dict[str, Any]
    message_type: str
    timestamp: datetime
    message_id: str

@dataclass
class AgentResult:
    """Result structure for agent outputs"""
    agent_name: str
    status: AgentStatus
    output: Dict[str, Any]
    metadata: Dict[str, Any]
    execution_time: float
    timestamp: datetime

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = AgentStatus.IDLE
        self.messages: List[AgentMessage] = []
        self.results: List[AgentResult] = []
        self.logger = logging.getLogger(f"Agent.{name}")
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Main processing method - must be implemented by each agent
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Return agent capabilities and requirements
        """
        pass
    
    def update_status(self, status: AgentStatus):
        """Update agent status"""
        self.status = status
        self.logger.info(f"Agent {self.name} status updated to {status.value}")
    
    def add_message(self, message: AgentMessage):
        """Add a message to the agent's message queue"""
        self.messages.append(message)
        self.logger.info(f"Agent {self.name} received message from {message.sender}")
    
    def get_last_result(self) -> Optional[AgentResult]:
        """Get the last result produced by this agent"""
        return self.results[-1] if self.results else None
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data structure"""
        required_fields = self.get_required_fields()
        for field in required_fields:
            if field not in input_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        return True
    
    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """Return list of required input fields"""
        pass
    
    def log_result(self, result: AgentResult):
        """Log and store agent result"""
        self.results.append(result)
        self.logger.info(f"Agent {self.name} completed task with status {result.status.value}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        if not self.results:
            return {"total_tasks": 0, "success_rate": 0, "avg_execution_time": 0}
        
        successful_tasks = sum(1 for r in self.results if r.status == AgentStatus.COMPLETED)
        total_tasks = len(self.results)
        avg_time = sum(r.execution_time for r in self.results) / total_tasks
        
        return {
            "total_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "success_rate": successful_tasks / total_tasks if total_tasks > 0 else 0,
            "avg_execution_time": avg_time,
            "last_execution": self.results[-1].timestamp if self.results else None
        } 