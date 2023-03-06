class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };
        this.state = false;
        this.messages = [];
    }

    display() {
        const {chatBox, sendButton} = this.args;

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    onSendButton(chatbox) {
        
        const {sendButton} = this.args;
        const pid = document.getElementById("chatID").getAttribute("PID");

        var textField = chatbox.querySelector('input');
        let text1 = textField.value

        if (text1 === "") {
            return;
        }

        textField.disabled = true;
        sendButton.disabled = true;

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);

        fetch('http://www.aizinga.com/predict/'+ pid, {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
            textField.disabled = false;
            sendButton.disabled = false;
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            textField.disabled = false;
            sendButton.disabled = false;
            this.updateChatText(chatbox)
            textField.value = ''
          });
    
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += 
                '<div class="user-icon"> <img src="static/images/baberuthai.jpg" alt="user icon" align="right" width=40 hight=40 style= border-radius:50%> </div>' +
                '<div class="messages__item messages__item--operator">' +         
                item.message + '</div>'
            }
            else
            {
                
                html += 
                '<div class=user-icon width=10px hight=10px> <img src="https://img.icons8.com/color/48/000000/circled-user-male-skin-type-5--v1.png" alt="user icon" align="left"> </div>' +
                '<div class="messages__item messages__item--visitor">' +         
                item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}


const chatbox = new Chatbox();
chatbox.display();