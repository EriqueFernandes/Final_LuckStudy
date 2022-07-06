const btn_home = document.querySelector("#home");

btn_home.onclick = () => {
    window.location.href = "/login"
}

document.querySelectorAll(".butoes").forEach((btn) => {
    btn.onclick = () => {
        let url_dividida = location.href.split("/");
        const nome = url_dividida[4];
        let materia = null;

        switch (btn.textContent) {
            case "Geometria analítica":
                materia = "ga"
                break
            case "Introdução à modelagem matemática":
                materia = "imm"
                break
            case "Calculo em uma variável":
                materia = "calc"
                break
            case "Introdução à computação":
                materia = "ic"
                break
            case "Fundamentos da matemática":
                materia = "fun"
                break
            default:
                break
        }

        url_dividida = url_dividida.splice(0, url_dividida.length - 1)
        url_dividida[url_dividida.length - 1] = `teste/${nome}/${materia}`
        location.href = url_dividida.join("/")
    }
})