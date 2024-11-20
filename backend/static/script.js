async function handleUpload() {
    const fileInput = document.getElementById("resumeUpload");
    const file = fileInput.files[0];
    
    if (file) {
      const formData = new FormData();
      formData.append("resume", file);
  
      try {
        const response = await fetch("/upload", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
  
        // Display keywords on the right side
        displayResults(data.keywords);
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    } else {
      alert("Please select a file to upload.");
    }
  }
  
  function displayResults(keywords) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";  // Clear previous results
    
    keywords.forEach(keyword => {
      const keywordElement = document.createElement("div");
      keywordElement.className = "keyword";
      keywordElement.innerText = keyword;
      resultsDiv.appendChild(keywordElement);
    });
  }
  