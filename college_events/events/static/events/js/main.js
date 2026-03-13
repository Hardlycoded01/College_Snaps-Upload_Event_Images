/**
 * main.js — Client-side enhancements
 * 
 * 1. Image preview before upload (shows thumbnail instantly)
 * 2. Drag-and-drop on upload zone
 * 3. File validation (size + type) before submit
 * 4. Auto-dismiss flash messages
 */

document.addEventListener('DOMContentLoaded', function () {

  // ── 1. Image Preview ──────────────────────────────────────────
  // When user selects a file, show a preview before they submit.
  // This reads the file locally using FileReader API (no server needed).

  const fileInput = document.getElementById('id_image');
  const previewContainer = document.getElementById('upload-preview');
  const previewImg = document.getElementById('preview-img');
  const uploadZone = document.querySelector('.upload-zone');

  if (fileInput) {
    fileInput.addEventListener('change', function (e) {
      const file = e.target.files[0];
      if (!file) return;

      // Validate on the client side first
      if (!validateFile(file)) return;

      // Use FileReader to read file as a data URL (base64)
      const reader = new FileReader();
      reader.onload = function (event) {
        previewImg.src = event.target.result;
        previewContainer.style.display = 'block';

        // Update the upload zone text
        const zoneText = uploadZone.querySelector('.upload-zone-text');
        if (zoneText) zoneText.textContent = file.name;
      };
      reader.readAsDataURL(file);
    });
  }

  // ── 2. Drag and Drop ──────────────────────────────────────────
  if (uploadZone) {
    // Prevent browser default (would open the file in a new tab)
    uploadZone.addEventListener('dragover', function (e) {
      e.preventDefault();
      uploadZone.classList.add('drag-over');
    });

    uploadZone.addEventListener('dragleave', function () {
      uploadZone.classList.remove('drag-over');
    });

    uploadZone.addEventListener('drop', function (e) {
      e.preventDefault();
      uploadZone.classList.remove('drag-over');

      const file = e.dataTransfer.files[0];
      if (!file || !validateFile(file)) return;

      // Assign the dropped file to the input element
      // We create a new DataTransfer to set files on the input
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      fileInput.files = dataTransfer.files;

      // Trigger the change event manually to show preview
      fileInput.dispatchEvent(new Event('change'));
    });
  }

  // ── 3. File Validation ────────────────────────────────────────
  function validateFile(file) {
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

    if (file.size > maxSize) {
      showAlert('File is too large. Maximum size is 10MB.', 'error');
      return false;
    }

    if (!allowedTypes.includes(file.type)) {
      showAlert('Invalid file type. Please upload JPEG, PNG, GIF, or WebP.', 'error');
      return false;
    }

    return true;
  }

  // ── 4. Auto-dismiss Messages ─────────────────────────────────
  const messages = document.querySelectorAll('.message');
  messages.forEach(function (msg) {
    setTimeout(function () {
      msg.style.transition = 'opacity 0.5s';
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 500);
    }, 4000); // disappear after 4 seconds
  });

  // ── Helper: Show alert ────────────────────────────────────────
  function showAlert(text, type) {
    const container = document.getElementById('messages-container');
    if (!container) return;

    const div = document.createElement('div');
    div.className = `message message-${type}`;
    div.textContent = text;
    container.appendChild(div);

    setTimeout(() => {
      div.style.transition = 'opacity 0.5s';
      div.style.opacity = '0';
      setTimeout(() => div.remove(), 500);
    }, 4000);
  }

});
