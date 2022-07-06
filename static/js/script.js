const up_btn = document.querySelector("#btn_up");
const down_btn = document.querySelector("#btn_down");
const box_names = document.querySelector("#lista_users");

const submit_btn = document.querySelector("#submit_btn");
const box_info = document.querySelector("#show_this");
const btn_home = document.querySelector("#home");

const totalNomes = document.querySelectorAll("li").length

let pixels = 1;

submit_btn.onclick = (event) => {
    event.preventDefault()

    if(document.querySelector("#username").value == ""){
        document.querySelector("#show_this").style = "display: flex;"
        document.querySelector("#segundo_plano").style = "display: flex;"
        setTimeout(()=>{
            document.querySelector("#show_this").style = "display: none;"
            document.querySelector("#segundo_plano").style = "display: none;"
        },1000)
        return
    }

    document.querySelector("form").submit();
}

up_btn.onclick = () => {
    if(pixels > 15 * (totalNomes - 1)) return
    pixels += 15;
    box_names.style = `transform: translateY(${pixels}px);`;
}

down_btn.onclick = () => {
    if(pixels < -15 * (totalNomes - 1)) return
    pixels -= 15;
    box_names.style = `transform: translateY(${pixels}px);`;
}

btn_home.onclick = () => {
    window.location.href = "/"
}