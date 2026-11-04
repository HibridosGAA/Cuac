
document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const input = document.getElementById("user-input");
    const btn = document.getElementById("send-btn");
    const robotModel = document.getElementById("robot-model");
    let silenceTimer = 0;
    
    // Si el input está deshabilitado, la IA está apagada
    if (input && input.disabled) {
        if(robotModel) robotModel.classList.add("offline");
        return;
    }

    function addMessage(text, sender) {
        const div = document.createElement("div");
        div.className = `message ${sender}`;
        div.innerText = text;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
        if (input.disabled) return;
        const msg = input.value.trim();
        if (!msg) return;
        
        addMessage(msg, "usuario");
        input.value = "";
        silenceTimer = 0; 

        if(robotModel) robotModel.classList.add("thinking");

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mensaje: msg })
            });
            const data = await res.json();
            
            if(robotModel) robotModel.classList.remove("thinking");
            
            if (data.activo) {
                if(robotModel) robotModel.classList.add("talking");
                addMessage(data.respuesta, "pato");
                setTimeout(() => { if(robotModel) robotModel.classList.remove("talking"); }, 2000);
            } else {
                addMessage("Sistema apagado.", "system");
                input.disabled = true;
                btn.disabled = true;
                if(robotModel) robotModel.classList.add("offline");
            }
            
            // Actualizar panel izquierdo si existe (recarga básica para simplicidad)
            // Se podría hacer con JS puro para no recargar, pero por ahora mostramos en el stream central.
            
        } catch (e) {
            console.error(e);
            if(robotModel) robotModel.classList.remove("thinking");
        }
    }

    if(btn) btn.addEventListener("click", sendMessage);
    if(input) {
        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") sendMessage();
        });
        input.addEventListener("input", () => { silenceTimer = 0; });
    }

    // Autonomía
    setInterval(async () => {
        if (!input || input.disabled) return;
        
        silenceTimer++;
        if (silenceTimer > 20) { 
            silenceTimer = 0;
            try {
                const res = await fetch("/api/impulso");
                const data = await res.json();
                if (data.impulso) {
                    if(robotModel) robotModel.classList.add("talking");
                    addMessage(data.impulso, "pato");
                    setTimeout(() => { if(robotModel) robotModel.classList.remove("talking"); }, 2000);
                }
            } catch (e) {}
        }
    }, 1000);
});
