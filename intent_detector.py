"""
Intent Detection Module - Classifies user queries as information or action requests
"""
import logging
from typing import Dict, Any
from config import ACTION_KEYWORDS


class IntentDetector:
    """Detects intent from user queries using keyword scoring."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.action_keywords = ACTION_KEYWORDS
    
    def detect_intent(self, query: str) -> Dict[str, Any]:
        """
        Detect intent using keyword matching with scoring.
        More specific matches get higher priority.
        """
        query_lower = query.lower().strip()
        
        # Score each action type
        action_scores = {}
        
        for action_type, keywords in self.action_keywords.items():
            score = 0
            matched = []
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # Exact match - highest priority
                if query_lower == keyword_lower:
                    score += 20
                    matched.append(keyword)
                # Starts with keyword - high priority
                elif query_lower.startswith(keyword_lower):
                    score += 10
                    matched.append(keyword)
                # Contains keyword - medium priority
                elif keyword_lower in query_lower:
                    # Give more weight to longer, more specific keywords
                    keyword_weight = len(keyword.split())
                    score += (2 * keyword_weight)
                    matched.append(keyword)
            
            if score > 0:
                action_scores[action_type] = {
                    'score': score,
                    'matched': matched
                }
        
        # If we have action matches, return the highest scoring one
        if action_scores:
            # Sort by score descending
            sorted_actions = sorted(
                action_scores.items(), 
                key=lambda x: x[1]['score'], 
                reverse=True
            )
            
            best_action = sorted_actions[0]
            action_type = best_action[0]
            score = best_action[1]['score']
            matched_keywords = best_action[1]['matched']
            
            # Calculate confidence based on score
            # Higher scores = higher confidence
            confidence = min(0.95, 0.6 + (score * 0.02))
            
            self.logger.info(
                f"Action detected: {action_type} "
                f"(score: {score}, keywords: {matched_keywords[:3]}...)"
            )
            
            return {
                "intent_type": "action",
                "action_type": action_type,
                "confidence": round(confidence, 2),
                "matched_keywords": matched_keywords[:5]  # Limit to top 5
            }
        
        # No action keywords found - information query
        self.logger.info("Information intent detected (no action keywords)")
        return {
            "intent_type": "information",
            "action_type": None,
            "confidence": 0.9,
            "matched_keywords": []
        }
    
    def is_action_query(self, query: str) -> bool:
        """Quick check if query is an action request."""
        intent = self.detect_intent(query)
        return intent["intent_type"] == "action"
    
    def get_action_type(self, query: str) -> str:
        """Get the action type from query."""
        intent = self.detect_intent(query)
        return intent.get("action_type")
    
    def get_all_action_types(self) -> list:
        """Get list of all available action types."""
        return list(self.action_keywords.keys())
    
    def add_keyword(self, action_type: str, keyword: str):
        """Add a new keyword for an action type."""
        if action_type in self.action_keywords:
            if keyword.lower() not in [k.lower() for k in self.action_keywords[action_type]]:
                self.action_keywords[action_type].append(keyword)
                self.logger.info(f"Added keyword '{keyword}' to action '{action_type}'")
        else:
            self.logger.warning(f"Action type '{action_type}' not found")