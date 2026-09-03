function saveEvent(event){
    let q = JSON.parse(localStorage.getItem("queue") || "[]");
    q.push(event);
    localStorage.setItem("queue", JSON.stringify(q));
}

async function flushQueue(){
    let q = JSON.parse(localStorage.getItem("queue") || "[]");

    let remaining = [];

    for (let e of q){
        try{
            let r = await fetch("http://HEADTABLE_IP:8000/heat",{
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify(e)
            });

            let j = await r.json();
            if(j.status !== "accepted") remaining.push(e);

        }catch{
            remaining.push(e);
        }
    }

    localStorage.setItem("queue", JSON.stringify(remaining));
}

setInterval(flushQueue, 3000);