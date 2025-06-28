// Fixed JavaScript functions for the web interface

// Fixed setTopic function
function setTopic(topic) {
    console.log('setTopic called with:', topic);
    const topicInput = document.getElementById('topic');
    if (topicInput) {
        topicInput.value = topic;
        console.log('Topic set successfully:', topic);
    } else {
        console.error('Topic input field not found');
    }
}

// Fixed formatReportContent function without problematic regex
function formatReportContent(text) {
    if (!text) return '<p>No content available</p>';
    
    // Simple text cleaning without regex - just remove backticks
    while (text.indexOf('```') !== -1) {
        text = text.replace('```', '');
    }
    
    // Convert newlines to HTML paragraphs  
    const paragraphs = text.split('\\n\\n');
    let formatted = '';
    
    for (let i = 0; i < paragraphs.length; i++) {
        const para = paragraphs[i].trim();
        if (para) {
            formatted += '<p style="margin: 15px 0; text-align: justify; line-height: 1.6; color: #374151;">' + para + '</p>';
        }
    }
    
    return formatted || '<p>Content formatting in progress...</p>';
}

// Make setTopic globally available
window.setTopic = setTopic; 