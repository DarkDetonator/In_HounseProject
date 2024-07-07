// Function to control audio playback
function togglePlayback() {
  const audioPlayer = document.getElementById('audioPlayer');
  if (audioPlayer.paused) {
    audioPlayer.play();
  } else {
    audioPlayer.pause();
  }
}
function repeat() {
  const audioPlayer = document.getElementById('audioPlayer');
  audioPlayer.currentTime = 0;
  audioPlayer.play();
}
function restart() {
  const audioPlayer = document.getElementById('audioPlayer');
  audioPlayer.currentTime = 0;
}

// Function to send command to server and process response
function sendCommand(command) {
  fetch('/command', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ command: command }),
  })
  .then(response => response.json())
  .then(result => {
    if (result.action === 'navigate') {
      window.location.href = result.url; // Navigate to URL returned by server
    } else if (result.action === 'response') {
      speak(result.message); // Speak the response message
    }
  })
  .catch(error => {
    console.error('Error sending command:', error);
  });
}

// Speech recognition setup
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.interimResults = false;
recognition.lang = 'en-US';
recognition.start();

recognition.addEventListener('result', event => {
  const transcript = Array.from(event.results)
    .map(result => result[0])
    .map(result => result.transcript)
    .join('');
  sendCommand(transcript.toLowerCase());
});

recognition.addEventListener('end', recognition.start);

// Function to speak a message using Speech Synthesis
function speak(message) {
  const speech = new SpeechSynthesisUtterance(message);
  speechSynthesis.speak(speech);
}

// Initial greeting
window.addEventListener('load', () => {
  speak('Welcome to our website. How can I assist you today?');
});
