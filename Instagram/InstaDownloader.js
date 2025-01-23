// Google Developer Console Script for Bulk Downloading Instagram Media
// Run this script in the console while viewing an Instagram profile page.

async function downloadInstagramMedia() {
    // Create status display
    const status = document.createElement('div');
    status.style = `
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
    document.body.appendChild(status);

    const downloadedUrls = new Set();
    const mediaData = [];
    let mediaCount = 0;
    let scrollCount = 0;
    let consecutiveEmptyScrolls = 0;
    let isDownloading = true;

    // Add download controls
    const buttonStyle = `
        background: #3897f0;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        margin: 5px;
        cursor: pointer;
    `;

    const controlsDiv = document.createElement('div');
    controlsDiv.style.marginTop = '10px';

    const batchDownloadButton = document.createElement('button');
    batchDownloadButton.innerHTML = 'Download All Media';
    batchDownloadButton.style.cssText = buttonStyle;
    batchDownloadButton.onclick = () => downloadAllMedia();

    const stopButton = document.createElement('button');
    stopButton.innerHTML = 'Stop Download';
    stopButton.style.cssText = buttonStyle;
    stopButton.onclick = () => { isDownloading = false; };

    controlsDiv.appendChild(batchDownloadButton);
    controlsDiv.appendChild(stopButton);
    status.appendChild(controlsDiv);

    function updateStatus(message) {
        const statusContent = `
            Media Found: ${mediaCount}<br>
            Scroll Count: ${scrollCount}<br>
            Consecutive Empty Scrolls: ${consecutiveEmptyScrolls}/5<br>
            ${message}
        `;
        status.innerHTML = statusContent;
        status.appendChild(controlsDiv);
        console.log(message);
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function downloadAllMedia() {
        updateStatus('Starting batch download...');

        for (let i = 0; i < mediaData.length; i++) {
            const { blob, filename } = mediaData[i];
            const blobUrl = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);

            await sleep(500);
            updateStatus(`Downloading media ${i + 1} of ${mediaData.length}`);
        }

        updateStatus('Batch download complete!');
    }

    async function downloadMedia(mediaUrl, type) {
        try {
            if (downloadedUrls.has(mediaUrl)) return false;

            const response = await fetch(mediaUrl);
            const blob = await response.blob();

            const filename = `instagram_${Date.now()}_${Math.random().toString(36).substr(2, 5)}.${type}`;
            mediaData.push({ blob, filename });

            downloadedUrls.add(mediaUrl);
            mediaCount++;

            return true;
        } catch (error) {
            console.error('Download error:', error);
            return false;
        }
    }

    function isNearBottom() {
        return window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 1000;
    }

    async function smoothScroll() {
        scrollCount++;
        const scrollAmount = 1000;
        const duration = 1000;
        const start = window.scrollY;
        const end = start + scrollAmount;
        const startTime = performance.now();

        function ease(t) {
            return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
        }

        return new Promise(resolve => {
            function step(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                window.scrollTo(0, start + (end - start) * ease(progress));

                if (progress < 1) {
                    requestAnimationFrame(step);
                } else {
                    resolve();
                }
            }

            requestAnimationFrame(step);
        });
    }

    async function processVisibleMedia() {
        const mediaElements = Array.from(document.querySelectorAll('img, video'))
            .filter(media => {
                const rect = media.getBoundingClientRect();
                return rect.height > 100 && rect.width > 100 && !downloadedUrls.has(media.src);
            });

        let downloadedAny = false;

        for (const mediaElement of mediaElements) {
            if (!isDownloading) {
                updateStatus('Download stopped by user');
                return false;
            }

            const mediaUrl = mediaElement.src;
            const type = mediaElement.tagName === 'IMG' ? 'jpg' : 'mp4';

            const success = await downloadMedia(mediaUrl, type);
            if (success) downloadedAny = true;

            updateStatus('Finding media...');
        }

        return downloadedAny;
    }

    async function startDownload() {
        while (isDownloading) {
            try {
                const foundNew = await processVisibleMedia();

                if (!isNearBottom()) {
                    await smoothScroll();
                    await sleep(2000);
                    consecutiveEmptyScrolls = foundNew ? 0 : consecutiveEmptyScrolls + 1;
                } else {
                    await sleep(2000);
                    consecutiveEmptyScrolls++;
                }

                if (consecutiveEmptyScrolls >= 5) {
                    updateStatus('No new media found after multiple attempts. Scanning complete!');
                    break;
                }

            } catch (error) {
                console.error('Error during scan:', error);
                await sleep(2000);
            }
        }

        updateStatus(`Scan complete! Found ${mediaCount} media items. Click "Download All Media" to start downloading.`);
    }

    try {
        await startDownload();
    } catch (error) {
        updateStatus(`Error: ${error.message}`);
        console.error('Script error:', error);
    }
}

// Add manual trigger function
window.startInstagramDownload = () => {
    downloadInstagramMedia().catch(console.error);
};

// Run immediately
startInstagramDownload();

