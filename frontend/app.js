// Cấu hình API URL — sửa lại khi deploy
const API_URL = 'https://jarvis-backend.onrender.com';

const chatBox = document.getElementById('chatBox');
const micBtn = document.getElementById('micBtn');
const status = document.getElementById('status');

let recognition = null;
let isListening = false;

// Khởi tạo SpeechRecognition (Google STT, free)
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = 'vi-VN';
    recognition.interimResults = false;
    recognition.continuous = false;
    
    recognition.onstart = () => {
        isListening = true;
        micBtn.classList.add('listening');
        status.textContent = '🔴 Jarvis đang lắng nghe... (nói chuyện)';
        status.style.color = '#ff4444';
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('Nghe được:', transcript);
        addMessage('user', transcript);
        status.textContent = '⏳ Jarvis đang xử lý...';
        status.style.color = '#00d4ff';
        
        fetch(`${API_URL}/api/process`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: transcript })
        })
        .then(res => res.json())
        .then(data => {
            addMessage('jarvis', data.response);
            status.textContent = '🔊 Jarvis nói đáp ứng...';
            
            if (data.audio_base64) {
                const audio = new Audio(`data:audio/mp3;base64,${data.audio_base64}`);
                audio.play();
                status.textContent = '🔊 Jarvis đang nói...';
            } else {
                status.textContent = '✅ Xong. Bạn nói tiếp nhé';
                status.style.color = '#aaa';
            }
        })
        .catch(err => {
            console.error('Lỗi:', err);
            addMessage('jarvis', 'Xin lỗi, Jarvis gặp sự cố. Bạn thử lại nhé.');
            status.textContent = '❌ Có lỗi xảy ra';
            status.style.color = '#ff4444';
        })
        .finally(() => {
            isListening = false;
            micBtn.classList.remove('listening');
        });
    };
    
    recognition.onerror = (event) => {
        console.error('STT lỗi:', event.error);
        isListening = false;
        micBtn.classList.remove('listening');
        status.textContent = `⚠️ Lỗi: ${event.error}`;
        status.style.color = '#ff4444';
    };
    
    recognition.onend = () => {
        isListening = false;
        micBtn.classList.remove('listening');
        if (!isListening) {
            status.textContent = 'Nhấn mic để nói';
            status.style.color = '#aaa';
        }
    };
} else {
    status.textContent = '⚠️ Browser không hỗ trợ voice recognition. Hãy dùng Chrome hoặc Edge.';
    status.style.color = '#ff4444';
    micBtn.disabled = true;
    micBtn.style.opacity = '0.5';
}

function addMessage(type, text) {
    const div = document.createElement('div');
    div.className = `message ${type}-msg`;
    div.textContent = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

micBtn.addEventListener('click', () => {
    if (isListening) {
        recognition.stop();
        isListening = false;
        micBtn.classList.remove('listening');
        status.textContent = 'Đã dừng lắng nghe';
        status.style.color = '#aaa';
    } else {
        if (recognition) {
            recognition.start();
        }
    }
});
