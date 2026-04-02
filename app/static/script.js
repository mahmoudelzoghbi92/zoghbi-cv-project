// Load counts from the backend when the page opens
async function loadCounts() {
    const response = await fetch('/api/counts');
    const data = await response.json();
    document.getElementById('likeCount').textContent = data.likes;
    document.getElementById('dislikeCount').textContent = data.dislikes;
}

// Send a vote to the backend and update the display
async function vote(type) {
    const response = await fetch(`/api/${type}`, { method: 'POST' });
    const data = await response.json();
    document.getElementById('likeCount').textContent = data.likes;
    document.getElementById('dislikeCount').textContent = data.dislikes;
}

// Run on page load
loadCounts();