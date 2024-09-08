document.addEventListener('DOMContentLoaded', function() {
    const minutesOfMeeting = document.getElementById('minutes-of-meeting');
    
    console.log('Side panel DOM fully loaded');
  
    if (minutesOfMeeting) {
        console.log('Minutes of meeting element found');
        
        minutesOfMeeting.addEventListener('click', function() {
            console.log('Minutes of meeting clicked');
            chrome.runtime.sendMessage('bkmhfgbiemlmokjfbbijkckanjhepina', {action: 'open_popup'}, (response) => {
                if (chrome.runtime.lastError) {
                    console.error('Error:', chrome.runtime.lastError.message);
                } else if (!response || response.status !== 'Popup opened') {
                    console.error('Unexpected response:', response);
                } else {
                    console.log('Message sent, response:', response);
                }
            });
        });
    } else {
        console.error('Minutes of meeting element not found');
    }
});
