
  document.addEventListener('DOMContentLoaded', function () {
      const messageContainer = document.getElementById('message-container');

      // Function to hide and remove the message container
      const hideMessageContainer = () => {
          if (messageContainer) {
              messageContainer.style.transition = 'opacity 1s ease';
              messageContainer.style.opacity = '0'; // Fade out
              setTimeout(() => {
                  messageContainer.style.display = 'none'; // Remove from view
              }, 1000); // Wait for fade-out to complete
          }
      };

      // Hide the message after 3 seconds
      setTimeout(hideMessageContainer, 3000);
  });
