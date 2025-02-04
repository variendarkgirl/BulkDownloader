// Run this script in the console while viewing a YouTube channel or playlist page.
 
(async function extractYouTubeMedia() {
    const statusDiv = document.createElement('div');
    statusDiv.style = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 20px;
        border-radius: 10px;
        z-index: 9999;
        font-family: Arial;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    `;
    document.body.appendChild(statusDiv);

    const videoData = [];
    const processedUrls = new Set();

    function updateStatus(message) {
        statusDiv.innerHTML = `
            <p>${message}</p>
            <p>Videos Extracted: ${videoData.length}</p>
        `;
        console.log(message);
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function extractVisibleVideos() {
        const videoElements = Array.from(document.querySelectorAll('ytd-grid-video-renderer, ytd-playlist-video-renderer'))
            .filter(el => !processedUrls.has(el.querySelector('a#thumbnail').href));

        for (const videoElement of videoElements) {
            const anchor = videoElement.querySelector('a#thumbnail');
            const titleElement = videoElement.querySelector('a#video-title');
            const thumbnailElement = videoElement.querySelector('img');

            const videoUrl = anchor?.href || '';
            const videoTitle = titleElement?.innerText.trim() || 'Untitled';
            const thumbnailUrl = thumbnailElement?.src || '';

            if (videoUrl && !processedUrls.has(videoUrl)) {
                videoData.push({ videoUrl, videoTitle, thumbnailUrl });
                processedUrls.add(videoUrl);
                updateStatus(`Extracted: ${videoTitle}`);
            }
        }
    }

    async function smoothScroll() {
        window.scrollBy(0, window.innerHeight);
        await sleep(2000);
    }

    async function startExtraction() {
        let consecutiveEmptyScrolls = 0;

        while (consecutiveEmptyScrolls < 5) {
            const previousCount = videoData.length;
            await extractVisibleVideos();
            await smoothScroll();

            if (videoData.length === previousCount) {
                consecutiveEmptyScrolls++;
            } else {
                consecutiveEmptyScrolls = 0;
            }
        }

        updateStatus('Extraction complete! Check the console for results.');
        console.table(videoData);
    }

    try {
        await startExtraction();
    } catch (error) {
        updateStatus(`Error: ${error.message}`);
        console.error('Script Error:', error);
    }
})();

// (function(){ const videoElement = document.querySelector('video'); if(videoElement) { const videoUrl = videoElement.src; const videoTitle = document.querySelector('h1.ytd-video-primary-info-renderer')?.textContent || 'youtube-video'; const a = document.createElement('a'); a.href = videoUrl; a.download = `${videoTitle}.mp4`; document.body.appendChild(a); a.click(); document.body.removeChild(a); } else { console.log('No video found on this page'); } })();//
