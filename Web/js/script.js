var serverIP = '192.168.1.7'


class MessageQueue {
    constructor(sendInterval = 2000) 
    {
        this.queue = [];
        this.sending = false;
        this.sendInterval = sendInterval;
    }

    // Adaugă un mesaj in coada
    enqueue(message) 
    {
        this.queue.push(message);
        this.processQueue();
    }

    // Procesează coada de mesaje
    async processQueue() 
    {
        if (this.sending) return;
        this.sending = true;

        while (this.queue.length > 0) {
            const message = this.queue.shift();
            await this.sendMessage(message);
            await this.delay(this.sendInterval);
        }

        this.sending = false;
    }

    // Functie de trimitere a mesajului
    sendMessage(message) 
    {
        return new Promise((resolve, reject) => {
            const xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (xhttp.readyState == 4) {
                    if (xhttp.status == 200) {
                        document.getElementById("result").innerHTML = xhttp.responseText;
                        console.log('Message sent successfully:', xhttp.responseText);
                        resolve();
                    } else {
                        console.error('Failed to send message:', xhttp.statusText);
                        reject();
                    }
                }
            };
            xhttp.open('POST', message.url, true);
            xhttp.send(message.data);
        });
    }

    // Functie de intarziere
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

const messageQueue = new MessageQueue(2000); // Trimite mesaje la fiecare 1 secundă

function schimbaContinut(nume_resursa)
{
    var resursa = 'http://' + serverIP + ':5678/'+nume_resursa+'.html';
    var xhttp;
    if (window.XMLHttpRequest) 
    {
        xhttp = new XMLHttpRequest();
        /* onreadystatechange, onload, onerror */
        xhttp.onreadystatechange =
        function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) 
            {
                document.getElementById("continut").innerHTML = xhttp.responseText;
                //let myJson = JSON.parse(xhttp.responseText);
                console.log(xhttp.responseText);
            }
        }
        xhttp.open("GET", resursa, true);
        xhttp.send();
    }
}

function uploadFile()
{
    var resursa = 'http://' + serverIP + ':5678/'
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const formData = new FormData();

    formData.append('file', file, file.name);

    var xhttp;
    if (window.XMLHttpRequest) 
    {
        xhttp = new XMLHttpRequest();
        /* onreadystatechange, onload, onerror */
        xhttp.onreadystatechange =
        function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) 
            {
                document.getElementById("result").innerHTML = xhttp.responseText;
                //let myJson = JSON.parse(xhttp.responseText);
                console.log(xhttp.responseText);
            }
        }
        
        xhttp.open('POST', resursa + file.name, true);
        xhttp.send(formData);
    }
    /*messageQueue.enqueue({
        url: resursa + file.name,
        data: formData
    });*/
}

function displayImage(input)
{
    const file = input.files[0];
    if(file)
    {
        const reader = new FileReader();
        reader.onload = function(e){
            const imageContainer = document.getElementById('imageContainer');
            imageContainer.innerHTML = '';
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '250px';
            imageContainer.appendChild(img);
        }
        reader.readAsDataURL(file);
    }
}