class PhotoBrowser {
    constructor() {
        this.baseUrl = '';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadImageCount();
    }

    bindEvents() {
        document.getElementById('refreshCount').addEventListener('click', () => {
            this.loadImageCount();
        });

        document.getElementById('scanImages').addEventListener('click', () => {
            this.scanImages();
        });

        document.getElementById('loadImages').addEventListener('click', () => {
            this.loadImages();
        });
    }

    async loadImageCount() {
        try {
            const response = await fetch('/api/images/count');
            const data = await response.json();
            document.getElementById('imageCount').textContent = data.count;
        } catch (error) {
            console.error('Error loading image count:', error);
            document.getElementById('imageCount').textContent = 'Error';
        }
    }

    async scanImages() {
        const button = document.getElementById('scanImages');
        const result = document.getElementById('scanResult');
        const resultText = document.getElementById('scanResultText');

        button.disabled = true;
        button.textContent = 'Scanning...';
        result.classList.add('hidden');

        try {
            const response = await fetch('/api/images/scan', {
                method: 'POST'
            });
            const data = await response.json();
            
            resultText.textContent = `Found ${data.scanned} new images and added them to the database.`;
            result.classList.remove('hidden');
            
            this.loadImageCount();
        } catch (error) {
            console.error('Error scanning images:', error);
            resultText.textContent = 'Error scanning images. Please try again.';
            result.classList.remove('hidden');
            result.querySelector('div').className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded';
        } finally {
            button.disabled = false;
            button.textContent = 'Scan for New Images';
        }
    }

    async loadImages() {
        const button = document.getElementById('loadImages');
        const grid = document.getElementById('imageGrid');

        button.disabled = true;
        button.textContent = 'Loading...';
        grid.innerHTML = '<div class="col-span-full text-center text-gray-500">Loading images...</div>';

        try {
            const response = await fetch('/api/images');
            const data = await response.json();
            
            if (data.images.length === 0) {
                grid.innerHTML = '<div class="col-span-full text-center text-gray-500">No images found in database. Try scanning for images first.</div>';
                return;
            }

            grid.innerHTML = data.images.map(image => `
                <div class="bg-gray-50 rounded-lg p-4">
                    <div class="aspect-square bg-gray-200 rounded mb-3 overflow-hidden">
                        ${image.width && image.height ? 
                            `<img src="/api/images/${image.id}/thumbnail" 
                                 alt="${image.filename}" 
                                 class="w-full h-full object-cover"
                                 onerror="this.parentElement.innerHTML='<span class=\\"text-gray-400 text-sm flex items-center justify-center h-full\\">Preview unavailable</span>'">` :
                            `<div class="flex items-center justify-center h-full"><span class="text-gray-400 text-sm">No preview</span></div>`
                        }
                    </div>
                    <h3 class="font-semibold text-sm truncate" title="${image.filename}">${image.filename}</h3>
                    <p class="text-xs text-gray-500">${image.width && image.height ? `${image.width} × ${image.height}` : 'Dimensions unavailable'}</p>
                    <p class="text-xs text-gray-500">${this.formatFileSize(image.file_size)}</p>
                    <p class="text-xs text-gray-500">${image.format}</p>
                </div>
            `).join('');

        } catch (error) {
            console.error('Error loading images:', error);
            grid.innerHTML = '<div class="col-span-full text-center text-red-500">Error loading images. Please try again.</div>';
        } finally {
            button.disabled = false;
            button.textContent = 'Load Images';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

new PhotoBrowser();