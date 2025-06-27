"""
Web Interface for AI Research & Content Creation Team
"""
from flask import Flask, render_template_string, request, jsonify, session
from flask_cors import CORS
import asyncio
import json
from datetime import datetime
import threading
import time

from ...core.orchestrator import AgentOrchestrator, WorkflowStatus
from ...core.config import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'ai_agent_demo_key_2024'
CORS(app)

# Global orchestrator instance  
orchestrator = AgentOrchestrator()

# Store active workflows
active_workflows = {}

# HTML Templates
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Research & Content Creation Team</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; border-radius: 12px; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .agent-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .agent-card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 4px solid #667eea; }
        .agent-card h3 { color: #333; margin-bottom: 10px; font-size: 1.3em; }
        .agent-card p { color: #666; line-height: 1.6; }
        .demo-section { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 2px solid #e1e5e9; border-radius: 8px; font-size: 16px; }
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus { outline: none; border-color: #667eea; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: transform 0.2s; }
        .btn:hover { transform: translateY(-2px); }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
        .status-section { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .status-item { display: flex; align-items: center; margin-bottom: 10px; }
        .status-icon { width: 20px; height: 20px; border-radius: 50%; margin-right: 10px; }
        .status-pending { background: #ffc107; }
        .status-running { background: #007bff; animation: pulse 2s infinite; }
        .status-completed { background: #28a745; }
        .status-error { background: #dc3545; }
        .results-section { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 30px; display: none; }
        .tab-container { display: flex; border-bottom: 2px solid #e1e5e9; margin-bottom: 20px; }
        .tab { padding: 12px 24px; cursor: pointer; border-bottom: 2px solid transparent; transition: all 0.3s; }
        .tab.active { border-bottom-color: #667eea; color: #667eea; font-weight: 600; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .metric-card { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        .metric-value { font-size: 1.5em; font-weight: bold; color: #667eea; }
        .metric-label { color: #666; font-size: 0.9em; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        .example-topics { background: #e3f2fd; padding: 15px; border-radius: 8px; margin-top: 10px; }
        .example-topics h4 { margin-bottom: 10px; color: #1976d2; }
        .topic-tag { display: inline-block; background: #1976d2; color: white; padding: 4px 8px; margin: 2px; border-radius: 4px; font-size: 0.8em; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI Research & Content Creation Team</h1>
            <p>Level 4 Multi-Agent System for Collaborative Research and Analysis</p>
        </div>

        <div class="agent-grid">
            <div class="agent-card">
                <h3>🔍 Research Agent</h3>
                <p>Searches web for information and gathers relevant data on specified topics using intelligent query generation and content extraction.</p>
            </div>
            <div class="agent-card">
                <h3>📊 Analysis Agent</h3>
                <p>Performs deep analytical thinking on research findings, identifies trends, and generates strategic insights with critical reasoning.</p>
            </div>
            <div class="agent-card">
                <h3>📝 Content Agent</h3>
                <p>Creates structured reports and comprehensive content from analyzed data, generating professional documentation.</p>
            </div>
            <div class="agent-card">
                <h3>✅ Quality Agent</h3>
                <p>Reviews content quality, identifies issues, and provides improvement suggestions to ensure high standards.</p>
            </div>
        </div>

        <div class="demo-section">
            <h2>Generate Research Report</h2>
            <form id="researchForm">
                <div class="form-group">
                    <label for="topic">Research Topic</label>
                    <input type="text" id="topic" name="topic" placeholder="Enter your research topic..." required>
                    <div class="example-topics">
                        <h4>Example Topics:</h4>
                        <span class="topic-tag" onclick="setTopic('Artificial Intelligence in Healthcare')">AI in Healthcare</span>
                        <span class="topic-tag" onclick="setTopic('Future of Remote Work')">Future of Remote Work</span>
                        <span class="topic-tag" onclick="setTopic('Sustainable Energy Technologies')">Sustainable Energy</span>
                        <span class="topic-tag" onclick="setTopic('Blockchain Applications in Finance')">Blockchain in Finance</span>
                        <span class="topic-tag" onclick="setTopic('Machine Learning Ethics')">ML Ethics</span>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="depth">Research Depth</label>
                    <select id="depth" name="depth">
                        <option value="light">Light Research (Quick Overview)</option>
                        <option value="medium" selected>Medium Research (Balanced Analysis)</option>
                        <option value="deep">Deep Research (Comprehensive Investigation)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="content_type">Report Type</label>
                    <select id="content_type" name="content_type">
                        <option value="comprehensive_report" selected>Comprehensive Report</option>
                        <option value="executive_briefing">Executive Briefing</option>
                        <option value="research_summary">Research Summary</option>
                    </select>
                </div>

                <button type="submit" class="btn" id="submitBtn">Start Research Workflow</button>
            </form>

            <div class="status-section" id="statusSection" style="display: none;">
                <h3>Workflow Progress</h3>
                <div id="workflowStatus"></div>
            </div>
        </div>

        <div class="results-section" id="resultsSection">
            <h2>Research Results</h2>
            <div class="tab-container">
                <div class="tab active" onclick="showTab('summary')">Summary</div>
                <div class="tab" onclick="showTab('research')">Research</div>
                <div class="tab" onclick="showTab('analysis')">Analysis</div>
                <div class="tab" onclick="showTab('content')">Content</div>
                <div class="tab" onclick="showTab('quality')">Quality</div>
            </div>
            <div id="tabContent"></div>
        </div>
    </div>

    <script>
        let currentWorkflowId = null;
        let currentResults = null;

        function setTopic(topic) {
            document.getElementById('topic').value = topic;
        }

        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');
            
            const content = document.getElementById('tabContent');
            if (!currentResults) return;
            
            let html = '';
            switch(tabName) {
                case 'summary':
                    html = generateSummaryTab(currentResults);
                    break;
                case 'research':
                    html = generateResearchTab(currentResults);
                    break;
                case 'analysis':
                    html = generateAnalysisTab(currentResults);
                    break;
                case 'content':
                    html = generateContentTab(currentResults);
                    break;
                case 'quality':
                    html = generateQualityTab(currentResults);
                    break;
            }
            content.innerHTML = html;
        }

        function generateSummaryTab(results) {
            const metadata = results.workflow_metadata || {};
            return `
                <div class="metric-card">
                    <div class="metric-value">${metadata.total_sources_analyzed || 0}</div>
                    <div class="metric-label">Sources Analyzed</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${metadata.total_recommendations || 0}</div>
                    <div class="metric-label">Recommendations Generated</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${metadata.final_word_count || 0}</div>
                    <div class="metric-label">Final Word Count</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${(metadata.overall_quality_score || 0).toFixed(2)}</div>
                    <div class="metric-label">Quality Score</div>
                </div>
            `;
        }

        function generateResearchTab(results) {
            const research = results.research_phase || {};
            const findings = research.findings || {};
            return `
                <h3>Research Findings</h3>
                <h4>Main Findings:</h4>
                <ul>${(findings.main_findings || []).map(f => `<li>${f}</li>`).join('')}</ul>
                <h4>Current Trends:</h4>
                <ul>${(findings.current_trends || []).map(t => `<li>${t}</li>`).join('')}</ul>
                <h4>Sources:</h4>
                <ul>${(research.sources || []).map(s => `<li>${s}</li>`).join('')}</ul>
            `;
        }

        function generateAnalysisTab(results) {
            const analysis = results.analysis_phase || {};
            const recommendations = analysis.recommendations || [];
            return `
                <h3>Analysis Results</h3>
                <h4>Key Insights:</h4>
                <ul>${(analysis.insights?.key_insights || []).map(i => `<li>${i}</li>`).join('')}</ul>
                <h4>Recommendations:</h4>
                ${recommendations.map(rec => `
                    <div class="metric-card">
                        <strong>${rec.action}</strong><br>
                        <em>Priority: ${rec.priority}</em><br>
                        ${rec.rationale}
                    </div>
                `).join('')}
            `;
        }

        function generateContentTab(results) {
            const content = results.content_phase || {};
            const finalContent = content.final_content || {};
            const execSummary = finalContent.executive_summary || {};
            return `
                <h3>Generated Content</h3>
                <h4>${execSummary.title || 'Executive Summary'}</h4>
                <p>${execSummary.content || 'No content available'}</p>
                <h4>Document Structure:</h4>
                <ul>
                    ${(finalContent.main_sections || []).map(section => `
                        <li><strong>${section.title}</strong> - ${section.content.substring(0, 100)}...</li>
                    `).join('')}
                </ul>
            `;
        }

        function generateQualityTab(results) {
            const quality = results.quality_phase || {};
            const report = quality.quality_report || {};
            return `
                <h3>Quality Assessment</h3>
                <div class="metric-card">
                    <div class="metric-value">${quality.quality_score || 0}</div>
                    <div class="metric-label">Overall Quality Score</div>
                </div>
                <h4>Approval Status: ${quality.approval_status || 'Unknown'}</h4>
                <h4>Strengths:</h4>
                <ul>${(report.strengths || []).map(s => `<li>${s}</li>`).join('')}</ul>
                <h4>Areas for Improvement:</h4>
                <ul>${(report.areas_for_improvement || []).map(a => `<li>${a}</li>`).join('')}</ul>
            `;
        }

        document.getElementById('researchForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const topic = document.getElementById('topic').value;
            const depth = document.getElementById('depth').value;
            const contentType = document.getElementById('content_type').value;
            
            const submitBtn = document.getElementById('submitBtn');
            const statusSection = document.getElementById('statusSection');
            const resultsSection = document.getElementById('resultsSection');
            
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            statusSection.style.display = 'block';
            resultsSection.style.display = 'none';
            
            try {
                const response = await fetch('/api/start_workflow', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic, depth, content_type: contentType })
                });
                
                const data = await response.json();
                if (data.success) {
                    currentWorkflowId = data.workflow_id;
                    pollWorkflowStatus();
                } else {
                    alert('Error starting workflow: ' + data.error);
                    resetUI();
                }
            } catch (error) {
                alert('Error: ' + error.message);
                resetUI();
            }
        });

        function pollWorkflowStatus() {
            const statusDiv = document.getElementById('workflowStatus');
            const interval = setInterval(async () => {
                try {
                    const response = await fetch(`/api/workflow_status/${currentWorkflowId}`);
                    const data = await response.json();
                    
                    if (data.success) {
                        updateStatusDisplay(data.status);
                        
                        if (data.status.status === 'completed') {
                            clearInterval(interval);
                            await loadResults();
                            resetUI();
                            document.getElementById('resultsSection').style.display = 'block';
                        } else if (data.status.status === 'failed') {
                            clearInterval(interval);
                            alert('Workflow failed: ' + (data.status.error || 'Unknown error'));
                            resetUI();
                        }
                    }
                } catch (error) {
                    console.error('Error polling status:', error);
                }
            }, 2000);
        }

        function updateStatusDisplay(status) {
            const steps = ['Research', 'Analysis', 'Content Creation', 'Quality Review'];
            const currentStep = status.current_step || 0;
            
            let html = '';
            for (let i = 0; i < steps.length; i++) {
                let statusClass = 'status-pending';
                if (i < currentStep - 1) statusClass = 'status-completed';
                else if (i === currentStep - 1) statusClass = 'status-running';
                
                html += `
                    <div class="status-item">
                        <div class="status-icon ${statusClass}"></div>
                        <span>${steps[i]}</span>
                    </div>
                `;
            }
            
            document.getElementById('workflowStatus').innerHTML = html;
        }

        async function loadResults() {
            try {
                const response = await fetch(`/api/workflow_results/${currentWorkflowId}`);
                const data = await response.json();
                
                if (data.success) {
                    currentResults = data.results.final_output;
                    showTab('summary');
                }
            } catch (error) {
                console.error('Error loading results:', error);
            }
        }

        function resetUI() {
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Start Research Workflow';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return render_template_string(INDEX_TEMPLATE)

@app.route('/api/start_workflow', methods=['POST'])
def start_workflow():
    """Start a new research workflow"""
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        depth = data.get('depth', 'medium')
        content_type = data.get('content_type', 'comprehensive_report')
        
        if not topic:
            return jsonify({'success': False, 'error': 'Topic is required'})
        
        # Start workflow in background thread
        def run_workflow():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    orchestrator.execute_research_workflow(
                        topic=topic,
                        depth=depth,
                        content_type=content_type
                    )
                )
                active_workflows[result.workflow_id] = result
            except Exception as e:
                logger.error(f"Workflow failed: {str(e)}")
            finally:
                loop.close()
        
        # Create a temporary workflow entry
        import uuid
        workflow_id = str(uuid.uuid4())
        active_workflows[workflow_id] = {
            'status': 'running',
            'topic': topic,
            'current_step': 1,
            'start_time': time.time()
        }
        
        # Start workflow thread
        thread = threading.Thread(target=run_workflow)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'workflow_id': workflow_id,
            'message': 'Workflow started successfully'
        })
        
    except Exception as e:
        logger.error(f"Error starting workflow: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/workflow_status/<workflow_id>')
def get_workflow_status(workflow_id):
    """Get workflow status"""
    try:
        if workflow_id in active_workflows:
            workflow = active_workflows[workflow_id]
            
            # If it's a WorkflowResult object
            if hasattr(workflow, 'status'):
                return jsonify({
                    'success': True,
                    'status': {
                        'status': workflow.status.value,
                        'current_step': 4 if workflow.status.value == 'completed' else 4,
                        'topic': workflow.topic
                    }
                })
            # If it's a dict (temporary entry)
            else:
                return jsonify({
                    'success': True,
                    'status': workflow
                })
        else:
            return jsonify({'success': False, 'error': 'Workflow not found'})
            
    except Exception as e:
        logger.error(f"Error getting workflow status: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/workflow_results/<workflow_id>')
def get_workflow_results(workflow_id):
    """Get workflow results"""
    try:
        if workflow_id in active_workflows:
            workflow = active_workflows[workflow_id]
            
            if hasattr(workflow, 'final_output'):
                return jsonify({
                    'success': True,
                    'results': {
                        'workflow_id': workflow.workflow_id,
                        'status': workflow.status.value,
                        'topic': workflow.topic,
                        'final_output': workflow.final_output,
                        'execution_time': workflow.total_execution_time
                    }
                })
            else:
                return jsonify({'success': False, 'error': 'Results not ready yet'})
        else:
            return jsonify({'success': False, 'error': 'Workflow not found'})
            
    except Exception as e:
        logger.error(f"Error getting workflow results: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/agent_capabilities')
def get_agent_capabilities():
    """Get agent capabilities"""
    try:
        capabilities = orchestrator.get_agent_capabilities()
        return jsonify({'success': True, 'capabilities': capabilities})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/system_metrics')
def get_system_metrics():
    """Get system metrics"""
    try:
        metrics = orchestrator.get_system_metrics()
        return jsonify({'success': True, 'metrics': metrics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print(f"""
    🚀 AI Research & Content Creation Team - Web Interface
    
    🌐 Access the system at: http://{config.FLASK_HOST}:{config.FLASK_PORT}
    
    📋 System Features:
    • Multi-agent collaboration and reasoning
    • Intelligent research and analysis
    • Professional content generation  
    • Quality assurance and review
    
    ⚡ Ready to demonstrate Level 4 AI capabilities!
    """)
    
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    ) 