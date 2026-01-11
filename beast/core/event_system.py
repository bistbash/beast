"""
Event System for Dynamic Communication
Enables departments and automations to communicate via events
"""

from typing import Dict, List, Callable, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class EventType(Enum):
    """Built-in event types"""
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    CLASS_CREATED = "class_created"
    CLASS_UPDATED = "class_updated"
    AUTOMATION_TRIGGERED = "automation_triggered"
    DEPARTMENT_LOADED = "department_loaded"
    CUSTOM = "custom"


@dataclass
class Event:
    """Event data structure"""
    event_type: str
    source: str  # Department or component that emitted the event
    data: Dict[str, Any]
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class EventSystem:
    """
    Event-driven communication system
    Supports pub/sub pattern for inter-department communication
    """
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[Event] = []
        self._max_history: int = 1000
    
    def subscribe(self, event_type: str, callback: Callable[[Event], None]):
        """
        Subscribe to an event type
        
        Args:
            event_type: Type of event to listen for
            callback: Function to call when event is emitted
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]):
        """Unsubscribe from an event type"""
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
    
    def emit(self, event_type: str, source: str, data: Dict[str, Any], 
             metadata: Optional[Dict[str, Any]] = None):
        """
        Emit an event
        
        Args:
            event_type: Type of event
            source: Component emitting the event
            data: Event data
            metadata: Additional metadata
        """
        event = Event(
            event_type=event_type,
            source=source,
            data=data,
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        # Store in history
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
        
        # Notify subscribers
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    # Log error but don't stop event propagation
                    print(f"Error in event callback for {event_type}: {e}")
        
        # Also notify wildcard subscribers (*)
        if "*" in self._subscribers:
            for callback in self._subscribers["*"]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in wildcard event callback: {e}")
    
    def get_event_history(self, event_type: Optional[str] = None, 
                         limit: int = 100) -> List[Event]:
        """
        Get event history, optionally filtered by type
        
        Args:
            event_type: Filter by event type (None for all)
            limit: Maximum number of events to return
        
        Returns:
            List of events
        """
        events = self._event_history
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events[-limit:]
    
    def clear_history(self):
        """Clear event history"""
        self._event_history.clear()
