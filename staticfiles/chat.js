function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// Function to scroll to the bottom of the chat messages
function scrollToBottom() {
    var chatMessages = document.getElementById("chat-messages");
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Scroll to the bottom when the page loads
window.onload = scrollToBottom;

// Function to add a new message
let form = document.getElementById("myform")
form.addEventListener("submit", sendChat)

function sendChat(e){
    e.preventDefault()
    let chatMessage = document.getElementById("id_body").value

    const data = {'msg' : chatMessage}
    let url = "{% url 'sent_msg' friend.profile.id %}"

    fetch(url, {
        method: 'POST',
        headers : {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    }).then(response => response.json()).then(data => {
        let mainch = document.getElementById("chat-messages")
        let chatMessageBox = document.createElement("div")
        chatMessageBox.classList.add("chat-message", "sender")
        let chatmsgchild = document.createElement("div")
        chatmsgchild.classList.add("message-text")
        chatmsgchild.textContent = data
        chatMessageBox.appendChild(chatmsgchild)
        mainch.appendChild(chatMessageBox)
        document.getElementById("id_body").value = ""
        scrollToBottom()
    }).catch((error) => {
        console.error('Error: ', error)
    })

}

const eventSource = new EventSource(
    "{% url 'sse_chat' friend.profile.id %}"
);



eventSource.onmessage = function (event){
    console.log("chala")
    receiveMessages();
}


let counter = {{num}}

function receiveMessages(){

    let url = "{% url 'receive_msg' friend.profile.id %}"
    
    fetch(url).then(response => response.json()).then(data => {
        console.log('Success: ', data);
        if(data.length == 0){}
        else{
            let lastmsg = data[data.length-1]
            if (counter == data.length){}
            else{
                let mainch = document.getElementById("chat-messages")
                let chatMessageBox = document.createElement("div")
                chatMessageBox.classList.add("chat-message")
                let chatmsgchild = document.createElement("div")
                chatmsgchild.classList.add("message-text")
                chatmsgchild.textContent = lastmsg
                chatMessageBox.appendChild(chatmsgchild)
                mainch.appendChild(chatMessageBox)
                scrollToBottom()
            }
        }
        counter = data.length
    }).catch((error) => {
        console.error('Error: ', error)
    })


}