async function downloadInstagramImagesHD() {
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
    const imageData = [];
    let imageCount = 0;
    let scrollCount = 0;
    let consecutiveEmptyScrolls = 0;
    let isDownloading = true;

    const buttonStyle = `
        background: #E1306C;
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
        status.innerHTML = `
            Images Found: ${imageCount}<br>
            Scroll Count: ${scrollCount}<br>
            Consecutive Empty Scrolls: ${consecutiveEmptyScrolls}/5<br>
            ${message}
        `;
        status.appendChild(controlsDiv);
        console.log(message);
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

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
            await sleep(500);
            updateStatus(`Downloading image ${i + 1} of ${imageData.length}`);
        }
        updateStatus('Batch download complete!');
    }

    async function downloadImage(imageUrl) {
        if (downloadedUrls.has(imageUrl)) return false;
        const response = await fetch(imageUrl);
        const blob = await response.blob();
        const filename = `instagram_${Date.now()}_${Math.random().toString(36).substr(2, 5)}.jpg`;
        imageData.push({ blob, filename });
        downloadedUrls.add(imageUrl);
        imageCount++;
        return true;
    }

    function isNearBottom() {
        return window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 1000;
    }

    async function smoothScroll() {
        scrollCount++;
        window.scrollBy(0, 1000);
        await sleep(1000);
    }

    async function processVisibleImages() {
        const images = Array.from(document.querySelectorAll('img[srcset]'))
            .map(img => img.srcset.split(' ')[0])
            .filter(url => !downloadedUrls.has(url));

        let downloadedAny = false;
        for (const imgUrl of images) {
            if (!isDownloading) {
                updateStatus('Download stopped by user');
                return false;
            }
            if (await downloadImage(imgUrl)) downloadedAny = true;
            updateStatus('Finding images...');
        }
        return downloadedAny;
    }

    async function waitForImages() {
        await sleep(2000);
        const images = Array.from(document.querySelectorAll('img[srcset]'));
        if (images.length) return true;
        await sleep(1000);
    }

    async function startDownload() {
        while (isDownloading) {
            const foundNew = await processVisibleImages();
            if (!isNearBottom()) {
                await smoothScroll();
                await waitForImages();
                consecutiveEmptyScrolls = foundNew ? 0 : consecutiveEmptyScrolls + 1;
            } else {
                await sleep(2000);
                consecutiveEmptyScrolls++;
            }
            if (consecutiveEmptyScrolls >= 5) break;
        }
        updateStatus(`Scan complete! Found ${imageCount} images.`);
    }

    startDownload();
}

window.startInstagramImageDownload = downloadInstagramImagesHD;
startInstagramImageDownload();
