function analyzeData() {
    const input = document.getElementById("postInput").value;
    const posts = input.split("\n").filter(p => p.trim() !== "");

    if (posts.length === 0) {
        alert("Please enter at least one post to analyze.");
        return;
    }

    fetch("http://localhost:5000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ posts })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";
        if (data.error) {
            resultsDiv.innerHTML = `<div>Error: ${data.error}</div>`;
        } else {
            data.forEach(item => {
                resultsDiv.innerHTML += `
                    <div>
                        <strong>Post:</strong> ${item.text}<br>
                        <strong>Sentiment:</strong> ${item.sentiment}<br>
                        <strong>Trend Score:</strong> ${item.trend_score}<br><hr>
                    </div>`;
            });
        }
    })
    .catch(err => {
        console.error("Error:", err);
        alert("Failed to fetch analysis. Please try again later.");
    });
}
