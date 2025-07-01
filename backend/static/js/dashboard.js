// Dashboard-specific JavaScript functionality

// Initialize sentiment chart for manager dashboard
function initSentimentChart(sentimentData) {
    const ctx = document.getElementById('sentimentChart');
    if (!ctx) return;
    
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [
                    sentimentData.positive || 0,
                    sentimentData.neutral || 0,
                    sentimentData.negative || 0
                ],
                backgroundColor: [
                    '#28a745', // Success green
                    '#6c757d', // Secondary gray
                    '#ffc107'  // Warning yellow
                ],
                borderColor: [
                    '#1e7e34',
                    '#545b62',
                    '#e0a800'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        color: '#ffffff'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? Math.round((context.parsed / total) * 100) : 0;
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
    
    return chart;
}

// Initialize feedback timeline chart for employee dashboard
function initTimelineChart(feedbackData) {
    const ctx = document.getElementById('timelineChart');
    if (!ctx || !feedbackData || feedbackData.length === 0) return;
    
    // Prepare data for timeline
    const sortedData = feedbackData.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    const labels = sortedData.map(feedback => {
        const date = new Date(feedback.created_at);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    
    const sentimentValues = sortedData.map(feedback => {
        switch(feedback.sentiment) {
            case 'positive': return 1;
            case 'neutral': return 0;
            case 'negative': return -1;
            default: return 0;
        }
    });
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Feedback Sentiment',
                data: sentimentValues,
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: sentimentValues.map(value => {
                    if (value > 0) return '#28a745';
                    if (value < 0) return '#ffc107';
                    return '#6c757d';
                }),
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: -1.2,
                    max: 1.2,
                    ticks: {
                        callback: function(value) {
                            if (value > 0.5) return 'Positive';
                            if (value < -0.5) return 'Negative';
                            return 'Neutral';
                        },
                        color: '#ffffff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#ffffff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const feedback = sortedData[context.dataIndex];
                            const sentiment = feedback.sentiment.charAt(0).toUpperCase() + feedback.sentiment.slice(1);
                            return `Sentiment: ${sentiment}`;
                        },
                        afterLabel: function(context) {
                            const feedback = sortedData[context.dataIndex];
                            return [
                                `Acknowledged: ${feedback.acknowledged ? 'Yes' : 'No'}`,
                                `Date: ${new Date(feedback.created_at).toLocaleDateString()}`
                            ];
                        }
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
    
    return chart;
}

// Dashboard statistics animation
function animateStatistics() {
    const statCards = document.querySelectorAll('.card h4');
    
    statCards.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        let currentValue = 0;
        const increment = Math.ceil(finalValue / 20);
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                stat.textContent = finalValue;
                clearInterval(timer);
            } else {
                stat.textContent = currentValue;
            }
        }, 50);
    });
}

// Real-time updates for dashboard (placeholder for future WebSocket implementation)
function initRealTimeUpdates() {
    // This would be implemented with WebSockets in a production environment
    // For now, we can simulate with periodic polling
    
    function checkForUpdates() {
        // Placeholder for checking new feedback or acknowledgments
        console.log('Checking for updates...');
    }
    
    // Check for updates every 30 seconds
    setInterval(checkForUpdates, 30000);
}

// Initialize dashboard features when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Animate statistics on page load
    setTimeout(animateStatistics, 500);
    
    // Initialize real-time updates
    initRealTimeUpdates();
    
    // Add hover effects to stat cards
    const statCards = document.querySelectorAll('.card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Handle feedback acknowledgment (employee dashboard)
    const acknowledgeBtns = document.querySelectorAll('.acknowledge-btn');
    acknowledgeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const feedbackId = this.getAttribute('data-feedback-id');
            const originalText = this.innerHTML;
            
            // Add loading state
            utils.addLoadingState(this, 'Acknowledging...');
            
            fetch(`/feedback/${feedbackId}/acknowledge`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update UI to show acknowledged state
                    this.closest('.card-footer').innerHTML = `
                        <div>
                            <span class="text-success">
                                <i class="fas fa-check-circle me-2"></i>
                                Acknowledged just now
                            </span>
                        </div>
                    `;
                    
                    utils.showToast('Feedback acknowledged successfully!', 'success');
                } else {
                    utils.removeLoadingState(this, originalText);
                    utils.showToast(data.message || 'Error acknowledging feedback', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                utils.removeLoadingState(this, originalText);
                utils.showToast('Error acknowledging feedback', 'danger');
            });
        });
    });
});

// Export functions for use in templates
window.dashboardUtils = {
    initSentimentChart,
    initTimelineChart,
    animateStatistics
};
