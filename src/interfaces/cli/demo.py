"""
CLI Demo for AI Research & Content Creation Team
"""

import asyncio
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...core.orchestrator import AgentOrchestrator
from ...core.config import config

console = Console()


def display_welcome():
    """Display welcome message"""
    console.print(
        Panel.fit(
            "[bold blue]AI Research & Content Creation Team[/bold blue]\n"
            "[dim]Level 4 Multi-Agent Collaboration System[/dim]\n\n"
            "Research Agent → Analysis Agent → Content Agent → Quality Agent",
            title="AI Agent System Demo",
            border_style="blue",
        )
    )


def check_configuration():
    """Check and validate system configuration"""
    console.print("\n[yellow]Checking system configuration...[/yellow]")

    config_status = config.validate_config()
    if not config_status["valid"]:
        console.print("[red]Configuration issues found:[/red]")
        for issue in config_status["issues"]:
            console.print(f"   • {issue}")
        console.print("\n[yellow]Please set up your environment variables[/yellow]")
        return False

    console.print("[green]Configuration validated successfully[/green]")
    return True


def display_agent_capabilities(orchestrator):
    """Display agent capabilities table"""
    console.print("\n[bold]Agent Capabilities:[/bold]")
    capabilities = orchestrator.get_agent_capabilities()

    capabilities_table = Table(title="Agent System Capabilities")
    capabilities_table.add_column("Agent", style="cyan", no_wrap=True)
    capabilities_table.add_column("Capabilities", style="green")

    for agent_name, caps in capabilities.items():
        cap_list = []
        for key, value in caps.items():
            if isinstance(value, bool) and value:
                cap_list.append(key.replace("can_", "").replace("_", " ").title())
            elif isinstance(value, list):
                cap_list.append(f"{key}: {len(value)} types")

        capabilities_table.add_row(
            agent_name.title(),
            ", ".join(cap_list[:3]) + ("..." if len(cap_list) > 3 else ""),
        )

    console.print(capabilities_table)


def get_demo_topics():
    """Return demo topics list"""
    return [
        {
            "topic": "Artificial Intelligence in Healthcare",
            "description": "Comprehensive analysis of AI applications in healthcare",
        },
        {
            "topic": "Future of Remote Work",
            "description": "Research on remote work trends and future implications",
        },
        {
            "topic": "Sustainable Energy Technologies",
            "description": "Analysis of renewable energy innovations and market trends",
        },
    ]


def select_topic():
    """Handle topic selection from user"""
    demo_topics = get_demo_topics()

    console.print("\n[bold]Available Demo Topics:[/bold]")
    for i, topic_info in enumerate(demo_topics, 1):
        console.print(f"  {i}. [cyan]{topic_info['topic']}[/cyan]")
        console.print(f"     {topic_info['description']}")

    while True:
        try:
            choice = console.input("\n[yellow]Select a topic (1-3) or enter your own: [/yellow]")

            if choice.isdigit() and 1 <= int(choice) <= 3:
                return demo_topics[int(choice) - 1]["topic"]
            elif choice.strip():
                return choice.strip()
            else:
                console.print("[red]Please enter a valid choice or topic[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Demo cancelled by user[/yellow]")
            return None


async def execute_workflow(orchestrator, topic):
    """Execute the research workflow with progress tracking"""
    console.print("\n[bold blue]Starting Multi-Agent Workflow...[/bold blue]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Add progress tasks
        task1 = progress.add_task("Research Agent - Gathering information...", total=None)
        task2 = progress.add_task("Analysis Agent - Processing data...", total=None)
        task3 = progress.add_task("Content Agent - Creating content...", total=None)
        task4 = progress.add_task("Quality Agent - Reviewing output...", total=None)

        try:
            result = await orchestrator.execute_research_workflow(
                topic=topic, depth="medium", content_type="comprehensive_report"
            )

            # Update progress as complete
            progress.update(task1, completed=True, description="Research Agent - Complete")
            progress.update(task2, completed=True, description="Analysis Agent - Complete")
            progress.update(task3, completed=True, description="Content Agent - Complete")
            progress.update(task4, completed=True, description="Quality Agent - Complete")

            return result

        except Exception as e:
            console.print(f"\n[red]Workflow failed: {str(e)}[/red]")
            return None


def display_results_summary(result):
    """Display workflow results summary"""
    console.print("\n[bold green]Workflow Completed Successfully![/bold green]")
    console.print(f"Total execution time: {result.total_execution_time:.2f} seconds")

    final_output = result.final_output
    metadata = final_output.get("workflow_metadata", {})

    summary_table = Table(title="Workflow Results Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green")

    summary_table.add_row("Sources Analyzed", str(metadata.get("total_sources_analyzed", 0)))
    summary_table.add_row("Recommendations Generated", str(metadata.get("total_recommendations", 0)))
    summary_table.add_row("Final Word Count", str(metadata.get("final_word_count", 0)))
    summary_table.add_row("Quality Score", f"{metadata.get('overall_quality_score', 0):.2f}/1.00")
    summary_table.add_row("Content Status", final_output.get("quality_phase", {}).get("approval_status", "Unknown"))

    console.print(summary_table)


def display_detailed_results(result):
    """Display detailed workflow results"""
    final_output = result.final_output

    # Research findings
    research_phase = final_output.get("research_phase", {})
    research_findings = research_phase.get("findings", {})

    console.print(
        Panel(
            "\n".join([f"• {finding}" for finding in research_findings.get("main_findings", [])[:3]]),
            title="Key Research Findings",
            border_style="blue",
        )
    )

    # Analysis insights
    analysis_phase = final_output.get("analysis_phase", {})
    insights = analysis_phase.get("insights", {})

    console.print(
        Panel(
            "\n".join([f"• {insight}" for insight in insights.get("key_insights", [])[:3]]),
            title="Analysis Insights",
            border_style="green",
        )
    )


async def main():
    """Main demonstration function"""
    display_welcome()

    if not check_configuration():
        return

    # Initialize orchestrator
    console.print("\n[yellow]Initializing agent orchestrator...[/yellow]")
    orchestrator = AgentOrchestrator()

    display_agent_capabilities(orchestrator)

    selected_topic = select_topic()
    if not selected_topic:
        return

    console.print(f"\n[green]Selected topic: {selected_topic}[/green]")

    # Execute workflow
    result = await execute_workflow(orchestrator, selected_topic)
    if not result:
        return

    # Display results
    display_results_summary(result)

    # Show detailed results if requested
    show_details = console.input("\n[yellow]Would you like to see detailed results? (y/n): [/yellow]").lower().startswith("y")

    if show_details:
        console.print("\n[bold]Detailed Results:[/bold]")
        display_detailed_results(result)

    console.print("\n[bold blue]Demo completed successfully![/bold blue]")


if __name__ == "__main__":
    asyncio.run(main())
