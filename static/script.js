document.addEventListener('DOMContentLoaded', function() {
  const generateButton = document.getElementById('generateButton');
  const videoUrlInput = document.getElementById('videoUrl');
  const languageSelect = document.getElementById('language');
  const summaryDiv = document.getElementById('summary');

  generateButton.addEventListener('click', async function() {
    const videoUrl = videoUrlInput.value;
    const language = languageSelect.value;

    // Log video URL and language for debugging purposes
    console.log('videoUrl:', videoUrl);
    console.log('language:', language);

    if (!videoUrl) {
      alert('Please enter a YouTube video URL.');
      return;
    }

    summaryDiv.textContent = 'Generating summary...';

    try {
      // Fetch data from the server
      const response = await fetch(`/summarize?url=${encodeURIComponent(videoUrl)}&language=${encodeURIComponent(language)}`);
      
      // Check if the response is OK (status code 200-299)
      if (!response.ok) {
        throw new Error('Failed to generate summary');
      }

      // Parse the summary text from the response
      const summary = await response.text();
      summaryDiv.textContent = summary;

    } catch (error) {
      // Handle errors
      summaryDiv.textContent = 'An error occurred while generating the summary. Please try again.';
      console.error('Error:', error.message);
    }
  });
});
