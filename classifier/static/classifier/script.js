// Get DOM elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const submitBtn = document.getElementById('submitBtn');
const uploadForm = document.getElementById('uploadForm');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        imageInput.files = files;
        handleImageSelect(files[0]);
    }
});

// Handle file input change
imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleImageSelect(file);
    }
});

// Handle image selection
function handleImageSelect(file) {
    // Validate file type
    if (!file.type.match('image/(jpeg|jpg|png)')) {
        alert('Please select a JPG or PNG image.');
        return;
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        alert('Image size must be less than 10MB.');
        return;
    }

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        previewContainer.style.display = 'block';
        uploadArea.style.display = 'none';
        submitBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

// Remove image
function removeImage() {
    imageInput.value = '';
    previewContainer.style.display = 'none';
    uploadArea.style.display = 'block';
    submitBtn.disabled = true;
}

// Handle form submission
uploadForm.addEventListener('submit', (e) => {
    // Show loading state
    submitBtn.disabled = true;
    btnText.textContent = 'Processing...';
    btnLoader.style.display = 'inline-block';
});
