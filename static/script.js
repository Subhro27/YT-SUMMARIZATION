async function summarizeVideo() {
      const urlInput = document.getElementById('youtube-url').value;
      const loading = document.getElementById('loading');
      const error = document.getElementById('error');
      const result = document.getElementById('result');
      const videoId = document.getElementById('video-id');
      const source = document.getElementById('source');
      const summary = document.getElementById('summary');

      // Reset UI
      loading.classList.remove('hidden');
      error.classList.add('hidden');
      result.classList.add('hidden');

      try {
          const response = await fetch('/summarize', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ url: urlInput })
          });

          if (!response.ok) {
              const errorData = await response.json();
              throw new Error(errorData.detail || 'Failed to summarize video');
          }

          const data = await response.json();
          videoId.textContent = data.video_id;
          source.textContent = data.source === 'transcript' ? 'Transcript' : 'Title and Description';
          summary.textContent = data.summary;
          result.classList.remove('hidden');
      } catch (err) {
          error.textContent = err.message;
          error.classList.remove('hidden');
      } finally {
          loading.classList.add('hidden');
      }
  }