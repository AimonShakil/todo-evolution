"""
Metrics collection for observability and performance monitoring.

Tracks:
- Request latency (p50, p95, p99)
- Intent accuracy (successful task operations)
- Cost tracking (OpenAI token usage and API costs)
- Error rates
"""

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
import statistics


@dataclass
class LatencyMetric:
    """Latency measurement for a single request."""
    timestamp: datetime
    endpoint: str
    latency_ms: float
    user_id: int
    conversation_id: int


@dataclass
class CostMetric:
    """Cost measurement for OpenAI API usage."""
    timestamp: datetime
    user_id: int
    conversation_id: int
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float


@dataclass
class IntentMetric:
    """Intent accuracy measurement."""
    timestamp: datetime
    user_id: int
    conversation_id: int
    intent_detected: str  # e.g., "add_task", "list_tasks", etc.
    tool_executed: Optional[str]  # None if no tool called
    success: bool
    error: Optional[str] = None


class MetricsCollector:
    """
    In-memory metrics collector for observability.
    
    Stores recent metrics for analysis and monitoring.
    In production, this would push to Prometheus, CloudWatch, etc.
    """
    
    def __init__(self, retention_limit: int = 1000):
        """
        Initialize metrics collector.
        
        Args:
            retention_limit: Max number of metrics to retain per type
        """
        self.retention_limit = retention_limit
        
        # Metric storage
        self.latency_metrics: List[LatencyMetric] = []
        self.cost_metrics: List[CostMetric] = []
        self.intent_metrics: List[IntentMetric] = []
        
        # Counter storage
        self.counters: Dict[str, int] = defaultdict(int)
    
    def record_latency(
        self,
        endpoint: str,
        latency_ms: float,
        user_id: int,
        conversation_id: int
    ) -> None:
        """
        Record a latency measurement.
        
        Args:
            endpoint: API endpoint (e.g., "/api/chat")
            latency_ms: Latency in milliseconds
            user_id: User ID
            conversation_id: Conversation ID
        """
        metric = LatencyMetric(
            timestamp=datetime.utcnow(),
            endpoint=endpoint,
            latency_ms=latency_ms,
            user_id=user_id,
            conversation_id=conversation_id
        )
        self.latency_metrics.append(metric)
        
        # Trim old metrics
        if len(self.latency_metrics) > self.retention_limit:
            self.latency_metrics = self.latency_metrics[-self.retention_limit:]
    
    def record_cost(
        self,
        user_id: int,
        conversation_id: int,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> None:
        """
        Record OpenAI API cost.
        
        Args:
            user_id: User ID
            conversation_id: Conversation ID
            model: Model used (e.g., "gpt-4", "gpt-3.5-turbo")
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
        """
        # Pricing as of 2024 (update as needed)
        pricing = {
            "gpt-4": {"prompt": 0.03 / 1000, "completion": 0.06 / 1000},
            "gpt-3.5-turbo": {"prompt": 0.0015 / 1000, "completion": 0.002 / 1000},
        }
        
        rates = pricing.get(model, pricing["gpt-3.5-turbo"])
        estimated_cost = (
            prompt_tokens * rates["prompt"] +
            completion_tokens * rates["completion"]
        )
        
        metric = CostMetric(
            timestamp=datetime.utcnow(),
            user_id=user_id,
            conversation_id=conversation_id,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            estimated_cost_usd=estimated_cost
        )
        self.cost_metrics.append(metric)
        
        # Trim old metrics
        if len(self.cost_metrics) > self.retention_limit:
            self.cost_metrics = self.cost_metrics[-self.retention_limit:]
    
    def record_intent(
        self,
        user_id: int,
        conversation_id: int,
        intent_detected: str,
        tool_executed: Optional[str],
        success: bool,
        error: Optional[str] = None,
    ) -> None:
        """
        Record intent accuracy measurement.
        
        Args:
            user_id: User ID
            conversation_id: Conversation ID
            intent_detected: Detected intent
            tool_executed: Tool that was executed (None if no tool)
            success: Whether the intent was handled successfully
            error: Error message if failed
        """
        metric = IntentMetric(
            timestamp=datetime.utcnow(),
            user_id=user_id,
            conversation_id=conversation_id,
            intent_detected=intent_detected,
            tool_executed=tool_executed,
            success=success,
            error=error
        )
        self.intent_metrics.append(metric)
        
        # Trim old metrics
        if len(self.intent_metrics) > self.retention_limit:
            self.intent_metrics = self.intent_metrics[-self.retention_limit:]
    
    def increment_counter(self, counter_name: str, value: int = 1) -> None:
        """
        Increment a named counter.
        
        Args:
            counter_name: Counter name (e.g., "total_requests", "errors")
            value: Increment amount (default: 1)
        """
        self.counters[counter_name] += value
    
    def get_latency_percentiles(
        self,
        endpoint: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Calculate latency percentiles.
        
        Args:
            endpoint: Filter by specific endpoint (optional)
            
        Returns:
            Dict with p50, p95, p99 latencies in milliseconds
        """
        metrics = self.latency_metrics
        
        if endpoint:
            metrics = [m for m in metrics if m.endpoint == endpoint]
        
        if not metrics:
            return {"p50": 0.0, "p95": 0.0, "p99": 0.0, "count": 0}
        
        latencies = sorted([m.latency_ms for m in metrics])
        count = len(latencies)
        
        return {
            "p50": latencies[int(count * 0.5)] if count > 0 else 0.0,
            "p95": latencies[int(count * 0.95)] if count > 0 else 0.0,
            "p99": latencies[int(count * 0.99)] if count > 0 else 0.0,
            "count": count,
        }
    
    def get_average_cost_per_conversation(self) -> float:
        """
        Calculate average cost per conversation.
        
        Returns:
            Average cost in USD per conversation
        """
        if not self.cost_metrics:
            return 0.0
        
        # Group by conversation ID
        conversation_costs: Dict[int, float] = defaultdict(float)
        for metric in self.cost_metrics:
            conversation_costs[metric.conversation_id] += metric.estimated_cost_usd
        
        if not conversation_costs:
            return 0.0
        
        return statistics.mean(conversation_costs.values())
    
    def get_intent_accuracy(self) -> float:
        """
        Calculate intent accuracy rate.
        
        Returns:
            Percentage of successful intent handling (0.0 to 100.0)
        """
        if not self.intent_metrics:
            return 0.0
        
        successful = sum(1 for m in self.intent_metrics if m.success)
        total = len(self.intent_metrics)
        
        return (successful / total) * 100 if total > 0 else 0.0
    
    def get_error_rate(self) -> float:
        """
        Calculate error rate.
        
        Returns:
            Percentage of failed requests (0.0 to 100.0)
        """
        total = self.counters.get("total_requests", 0)
        errors = self.counters.get("total_errors", 0)
        
        return (errors / total) * 100 if total > 0 else 0.0
    
    def get_summary(self) -> Dict:
        """
        Get comprehensive metrics summary.
        
        Returns:
            Dict with all key metrics
        """
        return {
            "latency": self.get_latency_percentiles(),
            "intent_accuracy_pct": round(self.get_intent_accuracy(), 2),
            "avg_cost_per_conversation_usd": round(self.get_average_cost_per_conversation(), 4),
            "error_rate_pct": round(self.get_error_rate(), 2),
            "counters": dict(self.counters),
            "total_conversations_tracked": len(set(m.conversation_id for m in self.cost_metrics)),
        }


# Global metrics collector instance
metrics_collector = MetricsCollector()


class LatencyTimer:
    """
    Context manager for measuring latency.
    
    Example:
        >>> with LatencyTimer("chat_endpoint", user_id, conversation_id):
        ...     # Do work
        ...     pass
    """
    
    def __init__(
        self,
        endpoint: str,
        user_id: int,
        conversation_id: int,
        collector: Optional[MetricsCollector] = None
    ):
        """
        Initialize latency timer.
        
        Args:
            endpoint: Endpoint name
            user_id: User ID
            conversation_id: Conversation ID
            collector: MetricsCollector instance (uses global if None)
        """
        self.endpoint = endpoint
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.collector = collector or metrics_collector
        self.start_time = None
    
    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and record metric."""
        if self.start_time:
            latency_ms = (time.time() - self.start_time) * 1000
            self.collector.record_latency(
                endpoint=self.endpoint,
                latency_ms=latency_ms,
                user_id=self.user_id,
                conversation_id=self.conversation_id
            )
