
import sys
import json
from config import AgentConfig
from agent import AgenticRAGAssistant


def run_demo_queries():
    """Run a set of demo queries to showcase the system."""
    
    config = AgentConfig.from_env()
    assistant = AgenticRAGAssistant(config)
    
    if not assistant.initialize():
        print("Failed to initialize assistant. Please check logs.")
        return
    
    print("\n" + "="*70)
    print(" "*15 + "HCLTech Agentic Enterprise Assistant Demo")
    print("="*70)
    
    demo_queries = [
        {
            "category": "Financial Information",
            "query": "What is HCLTech's revenue growth in 2024-25?"
        },
        {
            "category": "IT Service Desk - Action",
            "query": "File a ticket for laptop not connecting to VPN"
        },
        {
            "category": "Strategic Information",
            "query": "What are the key strategic initiatives mentioned in the annual report?"
        },
        {
            "category": "HR Operations - Action",
            "query": "Apply for 3 days of casual leave next week"
        },
        {
            "category": "Developer Support",
            "query": "What technologies is HCLTech investing in?"
        },
        {
            "category": "IT Service Desk - Action",
            "query": "Schedule a meeting with IT team to discuss cloud migration"
        }
    ]
    
    results = []
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n\n{'='*70}")
        print(f"Demo Query {i}/{len(demo_queries)}: {demo['category']}")
        print("="*70)
        print(f"Query: {demo['query']}")
        print("-"*70)
        
        result = assistant.process_query(demo['query'])
        results.append(result)
        
        if result.get("error"):
            print(f" Error: {result['error']}")
        else:
            print(f"\n Intent: {result['intent']['intent_type'].upper()}")
            if result['retrieval']['pages']:
                print(f" Sources: Pages {result['retrieval']['pages']}")
            print(f" Confidence: {result['retrieval']['confidence']}")
            
            if result.get('response_type') == 'action':
                print(f"\n ACTION EXECUTED")
                print(f"   Type: {result['action']['action_type']}")
                print(f"   Status: {result['action']['status']}")
                print(f"   ID: {result['action']['action_id']}")
                print(f"\n Response:")
                print(f"   {result['explanation'][:200]}...")
            else:
                print(f"\n Answer:")
                print(f"   {result['answer'][:400]}...")
    
    print("\n\n" + "="*70)
    print(" "*25 + "Demo Complete!")
    print("="*70)
    
    stats = assistant.get_statistics()
    print(f"\n Session Statistics:")
    print(f"   Total Actions Executed: {stats['total_actions']}")
    print(f"   Actions by Type: {stats['actions_by_type']}")
    
    assistant.export_session_log("demo_session_log.json")
    print(f"\n Session log saved to: demo_session_log.json")
    print(f" Full logs available in: agent.log")
    
    return results


def run_single_query(query: str):
    """Run a single query and display results."""
    
    config = AgentConfig.from_env()
    assistant = AgenticRAGAssistant(config)
    
    if not assistant.initialize():
        print("Failed to initialize assistant.")
        return None
    
    print(f"\nProcessing query: {query}")
    print("-"*70)
    
    result = assistant.process_query(query)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))
    
    return result


def run_interactive():
    """Run in interactive mode."""
    
    config = AgentConfig.from_env()
    assistant = AgenticRAGAssistant(config)
    
    if not assistant.initialize():
        print("Failed to initialize assistant.")
        return
    
    assistant.interactive_mode()


def print_usage():
    """Print usage information."""
    print("""
HCLTech Agentic Enterprise Assistant

Usage:
    python main.py [mode] [options]

Modes:
    demo        - Run demo queries showcasing different capabilities
    interactive - Run in interactive CLI mode (default)
    query       - Process a single query
    help        - Show this help message

Examples:
    python main.py demo
    python main.py interactive
    python main.py query "What is HCLTech's revenue?"
    python main.py help
    """)


def main():
    """Main entry point."""
    
    if len(sys.argv) < 2:
        run_interactive()
        return
    
    mode = sys.argv[1].lower()
    
    if mode == "demo":
        run_demo_queries()
    elif mode == "interactive":
        run_interactive()
    elif mode == "query":
        if len(sys.argv) < 3:
            print("Error: Please provide a query")
            print("Usage: python main.py query 'Your question here'")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        run_single_query(query)
    elif mode in ["help", "-h", "--help"]:
        print_usage()
    else:
        print(f"Unknown mode: {mode}")
        print("Use 'python main.py help' for usage information")
        sys.exit(1)


if __name__ == "__main__":
    main()