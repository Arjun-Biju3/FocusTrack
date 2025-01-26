  document.addEventListener('DOMContentLoaded', function () {
            const messageContainer = document.getElementById('message-box');
    
            if (messageContainer) {
                setTimeout(function () {
                    // Apply fade-out transition to the message container
                    messageContainer.style.transition = 'opacity 1s ease';
                    messageContainer.style.opacity = '0';
    
                    // Remove the element completely after the fade-out
                    setTimeout(function () {
                        messageContainer.style.display = 'none';
                    }, 1000); // 1000ms = 1 second fade-out duration
                }, 3000); // 3000ms = 3 seconds before starting the fade-out
            }
        });