"""
AI Research & Content Creation Team - Demonstration Script
"""
import asyncio
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.json import JSON

from ...core.orchestrator import AgentOrchestrator
from ...core.config import config

console = Console()

async def main():
    """Main demonstration function"""
    
    # Display welcome message
    console.print(Panel.fit(
        "[bold blue]AI Research & Content Creation Team[/bold blue]\n"
        "[dim]Level 4 Multi-Agent Collaboration System[/dim]\n\n"
        "🔍 Research Agent → 📊 Analysis Agent → 📝 Content Agent → ✅ Quality Agent",
        title="🤖 AI Agent System Demo",
        border_style="blue"
    ))
    
    # Check configuration
    console.print("\n[yellow]⚙️  Checking system configuration...[/yellow]")
    
    config_status = config.validate_config()
    if not config_status['valid']:
        console.print("[red]❌ Configuration issues found:[/red]")
        for issue in config_status['issues']:
            console.print(f"   • {issue}")
        console.print("\n[yellow]💡 Please set up your environment variables (especially OPENAI_API_KEY)[/yellow]")
        return
    
    console.print("[green]✅ Configuration validated successfully[/green]")
    
    # Initialize orchestrator
    console.print("\n[yellow]🚀 Initializing agent orchestrator...[/yellow]")
    orchestrator = AgentOrchestrator()
    
    # Display agent capabilities
    console.print("\n[bold]🤖 Agent Capabilities:[/bold]")
    capabilities = orchestrator.get_agent_capabilities()
    
    capabilities_table = Table(title="Agent System Capabilities")
    capabilities_table.add_column("Agent", style="cyan", no_wrap=True)
    capabilities_table.add_column("Capabilities", style="green")
    
    for agent_name, caps in capabilities.items():
        cap_list = []
        for key, value in caps.items():
            if isinstance(value, bool) and value:
                cap_list.append(key.replace('can_', '').replace('_', ' ').title())
            elif isinstance(value, list):
                cap_list.append(f"{key}: {len(value)} types")
        
        capabilities_table.add_row(
            agent_name.title(),
            ", ".join(cap_list[:3]) + ("..." if len(cap_list) > 3 else "")
        )
    
    console.print(capabilities_table)
    
    # Demo topics
    demo_topics = [
        {
            'topic': 'Artificial Intelligence in Healthcare',
            'description': 'Comprehensive analysis of AI applications in healthcare industry'
        },
        {
            'topic': 'Future of Remote Work',
            'description': 'Research on remote work trends and future implications'
        },
        {
            'topic': 'Sustainable Energy Technologies',
            'description': 'Analysis of renewable energy innovations and market trends'
        }
    ]
    
    console.print(f"\n[bold]📋 Available Demo Topics:[/bold]")
    for i, topic_info in enumerate(demo_topics, 1):
        console.print(f"  {i}. [cyan]{topic_info['topic']}[/cyan]")
        console.print(f"     {topic_info['description']}")
    
    # Get user choice
    while True:
        try:
            choice = console.input("\n[yellow]Select a topic (1-3) or enter your own topic: [/yellow]")
            
            if choice.isdigit() and 1 <= int(choice) <= 3:
                selected_topic = demo_topics[int(choice) - 1]['topic']
                break
            elif choice.strip():
                selected_topic = choice.strip()
                break
            else:
                console.print("[red]Please enter a valid choice or topic[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Demo cancelled by user[/yellow]")
            return
    
    console.print(f"\n[green]✅ Selected topic: {selected_topic}[/green]")
    
    # Execute workflow with progress tracking
    console.print("\n[bold blue]🚀 Starting Multi-Agent Workflow...[/bold blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Add progress tasks
        task1 = progress.add_task("🔍 Research Agent - Gathering information...", total=None)
        task2 = progress.add_task("📊 Analysis Agent - Processing data...", total=None)
        task3 = progress.add_task("📝 Content Agent - Creating content...", total=None)
        task4 = progress.add_task("✅ Quality Agent - Reviewing output...", total=None)
        
        try:
            # Execute the workflow
            result = await orchestrator.execute_research_workflow(
                topic=selected_topic,
                depth='medium',
                content_type='comprehensive_report'
            )
            
            # Update progress as complete
            progress.update(task1, completed=True, description="🔍 Research Agent - ✅ Complete")
            progress.update(task2, completed=True, description="📊 Analysis Agent - ✅ Complete")
            progress.update(task3, completed=True, description="📝 Content Agent - ✅ Complete")
            progress.update(task4, completed=True, description="✅ Quality Agent - ✅ Complete")
            
        except Exception as e:
            console.print(f"\n[red]❌ Workflow failed: {str(e)}[/red]")
            return
    
    # Display results
    console.print(f"\n[bold green]🎉 Workflow Completed Successfully![/bold green]")
    console.print(f"⏱️  Total execution time: {result.total_execution_time:.2f} seconds")
    
    # Results summary
    final_output = result.final_output
    metadata = final_output.get('workflow_metadata', {})
    
    summary_table = Table(title="📊 Workflow Results Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green")
    
    summary_table.add_row("Sources Analyzed", str(metadata.get('total_sources_analyzed', 0)))
    summary_table.add_row("Recommendations Generated", str(metadata.get('total_recommendations', 0)))
    summary_table.add_row("Final Word Count", str(metadata.get('final_word_count', 0)))
    summary_table.add_row("Quality Score", f"{metadata.get('overall_quality_score', 0):.2f}/1.00")
    summary_table.add_row("Content Status", final_output.get('quality_phase', {}).get('approval_status', 'Unknown'))
    
    console.print(summary_table)
    
    # Show detailed results
    show_details = console.input("\n[yellow]Would you like to see detailed results? (y/n): [/yellow]").lower().startswith('y')
    
    if show_details:
        console.print("\n[bold]📋 Detailed Results:[/bold]")
        
        # Research findings
        research_phase = final_output.get('research_phase', {})
        research_findings = research_phase.get('findings', {})
        
        console.print(Panel(
            "\n".join([f"• {finding}" for finding in research_findings.get('main_findings', [])[:3]]),
            title="🔍 Key Research Findings",
            border_style="blue"
        ))
        
        # Analysis insights
        analysis_phase = final_output.get('analysis_phase', {})
        insights = analysis_phase.get('insights', {})
        
        console.print(Panel(
            "\n".join([f"• {insight}" for insight in insights.get('key_insights', [])[:3]]),
            title="📊 Analysis Insights",
            border_style="green"
        ))
        
        # Recommendations
        recommendations = analysis_phase.get('recommendations', [])
        if recommendations:
            rec_text = []
            for i, rec in enumerate(recommendations[:3], 1):
                rec_text.append(f"{i}. {rec.get('action', 'N/A')} (Priority: {rec.get('priority', 'Medium')})")
            
            console.print(Panel(
                "\n".join(rec_text),
                title="💡 Strategic Recommendations",
                border_style="yellow"
            ))
        
        # Content preview
        content_phase = final_output.get('content_phase', {})
        final_content = content_phase.get('final_content', {})
        exec_summary = final_content.get('executive_summary', {})
        
        if exec_summary.get('content'):
            preview = exec_summary['content'][:300] + "..." if len(exec_summary['content']) > 300 else exec_summary['content']
            console.print(Panel(
                preview,
                title="📝 Executive Summary Preview",
                border_style="magenta"
            ))
    
    # System metrics
    console.print("\n[bold]📈 System Performance Metrics:[/bold]")
    metrics = orchestrator.get_system_metrics()
    
    metrics_table = Table(title="Agent Performance")
    metrics_table.add_column("Agent", style="cyan")
    metrics_table.add_column("Tasks", style="green")
    metrics_table.add_column("Success Rate", style="yellow")
    metrics_table.add_column("Avg Time", style="blue")
    
    for agent_name, agent_metrics in metrics.get('agent_metrics', {}).items():
        success_rate = f"{agent_metrics.get('success_rate', 0)*100:.1f}%"
        avg_time = f"{agent_metrics.get('avg_execution_time', 0):.2f}s"
        
        metrics_table.add_row(
            agent_name.title(),
            str(agent_metrics.get('total_tasks', 0)),
            success_rate,
            avg_time
        )
    
    console.print(metrics_table)
    
    # Export option
    export_results = console.input("\n[yellow]Would you like to export results to JSON? (y/n): [/yellow]").lower().startswith('y')
    
    if export_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_agent_results_{timestamp}.json"
        
        export_data = {
            'workflow_id': result.workflow_id,
            'topic': selected_topic,
            'execution_time': result.total_execution_time,
            'results': result.final_output,
            'execution_summary': result.execution_summary,
            'timestamp': result.timestamp.isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        console.print(f"[green]✅ Results exported to: {filename}[/green]")
    
    console.print(Panel.fit(
        "[bold green]Demo Completed Successfully! 🎉[/bold green]\n\n"
        "[dim]This demonstration showcased:[/dim]\n"
        "• Multi-agent collaboration and reasoning\n"
        "• Intelligent research and data gathering\n"  
        "• Advanced analysis and insight generation\n"
        "• Professional content creation\n"
        "• Quality assurance and review processes\n\n"
        "[yellow]Ready for production use and further development![/yellow]",
        title="✨ AI Agent System Demo Summary",
        border_style="green"
    ))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user. Goodbye! 👋[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Demo failed with error: {str(e)}[/red]")
        console.print("[dim]Please check your configuration and try again.[/dim]") 