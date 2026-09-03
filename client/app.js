function normalize(v){
    if(v.toUpperCase() === "N") return "NF";
    return v;
}

function submitHeat(){

    let event = {
        event_id: crypto.randomUUID(),
        match_id: document.getElementById("match").value,
        heat_number: document.getElementById("heat").value,
        lane: "left",
        teamA_time: normalize(document.getElementById("a").value),
        teamB_time: normalize(document.getElementById("b").value),
        source_tablet: navigator.userAgent
    };

    saveEvent(event);
}