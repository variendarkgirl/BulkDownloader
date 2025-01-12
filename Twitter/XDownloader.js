async function downloadTwitterImagesHD() {
    // Create status display
    const status = document.createElement('div');
    status.style = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0,0,0,0.9);
        color: white;
        padding: 20px;
        border-radius: 10px;
        z-index: 9999;
        font-family: Arial;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    `;
    document.body.appendChild(status);

    const downloadedUrls = new Set();
    const imageData = []; // Store image data for batch download
    let imageCount = 0;
    let scrollCount = 0;
    let consecutiveEmptyScrolls = 0;
    let isDownloading = true;

    // Add download buttons
    const buttonStyle = `
        background: #1DA1F2;
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
    batchDownloadButton.innerHTML = 'Download All Images';
    batchDownloadButton.style.cssText = buttonStyle;
    batchDownloadButton.onclick = () => downloadAllImages();
    
    const stopButton = document.createElement('button');
    stopButton.innerHTML = 'Stop Download';
    stopButton.style.cssText = buttonStyle;
    stopButton.onclick = () => { isDownloading = false; };

    controlsDiv.appendChild(batchDownloadButton);
    controlsDiv.appendChild(stopButton);
    status.appendChild(controlsDiv);

    function updateStatus(message) {
        const statusContent = `
            Images Found: ${imageCount}<br>
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

    // Function to trigger multiple downloads with delay
    async function downloadAllImages() {
        updateStatus('Starting batch download...');
        
        for (let i = 0; i < imageData.length; i++) {
            const { blob, filename } = imageData[i];
            const blobUrl = URL.createObjectURL(blob);
            
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);
            
            // Add delay between downloads to prevent browser throttling
            await sleep(500);
            updateStatus(`Downloading image ${i + 1} of ${imageData.length}`);
        }
        
        updateStatus('Batch download complete!');
    }

    async function downloadImage(imageUrl) {
        try {
            if (downloadedUrls.has(imageUrl)) return false;
            
            // Convert to HD URL
            let hdUrl = imageUrl.replace(/&name=\w+/, '&name=orig');
            
            // Fetch the image
            const response = await fetch(hdUrl);
            const blob = await response.blob();
            
            // Store image data for batch download
            const filename = `twitter_${Date.now()}_${Math.random().toString(36).substr(2, 5)}.jpg`;
            imageData.push({ blob, filename });
            
            downloadedUrls.add(imageUrl);
            imageCount++;
            
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

    async function processVisibleImages() {
        const images = Array.from(document.querySelectorAll('img[src*="media"]'))
            .filter(img => {
                const rect = img.getBoundingClientRect();
                return !img.src.includes('profile') &&
                       !img.src.includes('emoji') &&
                       !img.src.includes('video_thumb') &&
                       img.src.includes('media') &&
                       img.width > 100;
            })
            .map(img => img.src);

        let downloadedAny = false;
        
        for (const imgUrl of images) {
            if (!isDownloading) {
                updateStatus('Download stopped by user');
                return false;
            }
            const success = await downloadImage(imgUrl);
            if (success) downloadedAny = true;
            updateStatus('Finding media images...');
        }

        return downloadedAny;
    }

    async function waitForImages() {
        const delay = 2000;
        await sleep(delay);
        
        return new Promise(resolve => {
            let checkCount = 0;
            const maxChecks = 5;
            
            const checkImages = () => {
                const images = document.querySelectorAll('img[src*="media"]');
                const allLoaded = Array.from(images).every(img => img.complete);
                
                if (allLoaded || checkCount >= maxChecks) {
                    resolve();
                } else {
                    checkCount++;
                    setTimeout(checkImages, 1000);
                }
            };
            
            checkImages();
        });
    }

    function isInMediaTab() {
        return window.location.href.includes('/media') || 
               document.querySelector('[href$="/media"][aria-selected="true"]') !== null;
    }

    async function startDownload() {
        if (!isInMediaTab()) {
            updateStatus('Please run this script in the Media tab of the profile');
            return;
        }

        while (isDownloading) {
            try {
                const foundNew = await processVisibleImages();
                
                if (!isNearBottom()) {
                    await smoothScroll();
                    await waitForImages();
                    consecutiveEmptyScrolls = foundNew ? 0 : consecutiveEmptyScrolls + 1;
                } else {
                    await sleep(2000);
                    consecutiveEmptyScrolls++;
                }

                if (consecutiveEmptyScrolls >= 5) {
                    updateStatus('No new images found after multiple attempts. Scanning complete!');
                    break;
                }

            } catch (error) {
                console.error('Error during scan:', error);
                await sleep(2000);
            }
        }

        updateStatus(`Scan complete! Found ${imageCount} images. Click "Download All Images" to start downloading.`);
    }

    try {
        await startDownload();
    } catch (error) {
        updateStatus(`Error: ${error.message}`);
        console.error('Script error:', error);
    }
}

// Add manual trigger function
window.startImageDownload = () => {
    downloadTwitterImagesHD().catch(console.error);
};

// Run immediately
startImageDownload();
