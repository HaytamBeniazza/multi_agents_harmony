"""
Simple Example: AI Research & Content Creation Team
"""
import asyncio
import json
from orchestrator import AgentOrchestrator

async def basic_example():
    """Basic example of using the AI agent system"""
    print("🤖 AI Research & Content Creation Team - Basic Example")
    print("=" * 55)
    
    # Initialize the orchestrator
    print("\n1. Initializing agent orchestrator...")
    orchestrator = AgentOrchestrator()
    
    # Define research topic
    topic = "Machine Learning in Cybersecurity"
    print(f"\n2. Research Topic: {topic}")
    
    # Execute the workflow
    print("\n3. Executing multi-agent workflow...")
    print("   🔍 Research Agent → 📊 Analysis Agent → 📝 Content Agent → ✅ Quality Agent")
    
    try:
        result = await orchestrator.execute_research_workflow(
            topic=topic,
            depth="medium",
            content_type="comprehensive_report"
        )
        
        # Display results
        print(f"\n4. ✅ Workflow completed successfully!")
        print(f"   ⏱️  Execution time: {result.total_execution_time:.2f} seconds")
        
        # Extract key metrics
        final_output = result.final_output
        metadata = final_output.get('workflow_metadata', {})
        
        print(f"\n5. 📊 Results Summary:")
        print(f"   • Sources analyzed: {metadata.get('total_sources_analyzed', 0)}")
        print(f"   • Recommendations: {metadata.get('total_recommendations', 0)}")
        print(f"   • Word count: {metadata.get('final_word_count', 0)}")
        print(f"   • Quality score: {metadata.get('overall_quality_score', 0):.2f}/1.00")
        
        # Show a sample of the generated content
        content_phase = final_output.get('content_phase', {})
        final_content = content_phase.get('final_content', {})
        exec_summary = final_content.get('executive_summary', {})
        
        if exec_summary.get('content'):
            print(f"\n6. 📝 Executive Summary Preview:")
            preview = exec_summary['content'][:200] + "..." if len(exec_summary['content']) > 200 else exec_summary['content']
            print(f"   {preview}")
        
        # Show top recommendations
        analysis_phase = final_output.get('analysis_phase', {})
        recommendations = analysis_phase.get('recommendations', [])
        
        if recommendations:
            print(f"\n7. 💡 Top Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec.get('action', 'N/A')} (Priority: {rec.get('priority', 'Medium')})")
        
        print(f"\n8. 🎉 Example completed successfully!")
        
        # Optional: Save results to file
        save_results = input("\nWould you like to save results to file? (y/n): ").lower().startswith('y')
        if save_results:
            filename = f"example_results_{topic.replace(' ', '_').lower()}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'topic': topic,
                    'execution_time': result.total_execution_time,
                    'final_output': final_output,
                    'timestamp': result.timestamp.isoformat()
                }, f, indent=2, default=str)
            
            print(f"✅ Results saved to: {filename}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure you have:")
        print("   1. Set OPENAI_API_KEY in your environment")
        print("   2. Installed all dependencies (pip install -r requirements.txt)")

if __name__ == "__main__":
    asyncio.run(basic_example()) 