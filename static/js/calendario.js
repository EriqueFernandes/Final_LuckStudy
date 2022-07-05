const containerCalendario = document.querySelector(".container_calendario");
const btn_past = document.querySelector("#past_btn");
const btn_future = document.querySelector("#future_btn")
const btn_home = document.querySelector("#homepage");

const data_main = new Date()

const mes = data_main.getMonth();
const ano = data_main.getFullYear();

let controleAno = ano;
let controleMes = mes;

const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

const criaDias = (pai) => {
    const dia = document.createElement("div")
    dia.classList.add("day")
    pai.appendChild(dia)
}

const nDias = (mess) => {
    if (mess % 2 == 1) {
        if (mess == 1) {

            if (controleAno % 4 == 0) {

                if (controleAno % 100 == 0 && !controleAno % 400 == 0) {
                    return 28;
                }

                return 29;
            }

            return 28;
        }

        else if (mess == 7) {
            return 31;
        }

        return 30;
    }

    return 31;
}

const descobreDiaDaSemana = (numero) => {
    switch (numero) {
        case 0:
            return "Dom"
        case 1:
            return "Seg"
        case 2:
            return "Ter"
        case 3:
            return "Qua"
        case 4:
            return "Qui"
        case 5:
            return "Sex"
        case 6:
            return "Sab"
        default:
            break;

    }
}

const descobreDiaPrimeiro = (diaDoMes, diaDaSemana) => {
    while (diaDoMes > 1) {
        diaDaSemana -= 1
        diaDoMes -= 1;
    }

    return (diaDaSemana % 7) + 7
}

const dias = nDias(mes);

for (let i = 0; i < 7; i++) {
    const divRow = document.createElement("div");
    divRow.classList.add("div_row");
    for (let k = 0; k < 7; k++) {
        criaDias(divRow);
    }
    containerCalendario.appendChild(divRow);
}

for (let i = 0; i < 7; i++) {
    document.querySelectorAll(".day")[i].innerHTML = descobreDiaDaSemana(i)
}

const desenhandoDias = (firstDay) => {
    let count = 7;
    let countDay = 1;

    const allDias = document.querySelectorAll(".day");

    const limparDias = () => {
        for (let k = 7; k < 49; k++) {
            if (allDias[k].children.length == 0) continue;
            allDias[k].removeChild(allDias[k].lastChild);
        }
    }
    limparDias()

    while (count < 49 && countDay <= nDias(controleMes % 12)) {
        if (countDay == 1) {
            if (count % 7 == firstDay % 7) {
                const paragrafo = document.createElement("p");
                paragrafo.textContent = countDay;
                allDias[count].appendChild(paragrafo);
                countDay++;
            }
            else {
                count++
                continue;
            }
        }
        else {
            const paragrafo = document.createElement("p");
            paragrafo.textContent = countDay;
            allDias[count].appendChild(paragrafo);
            countDay++;
        }
        count++
    }
}

const primeiroDia = descobreDiaPrimeiro(data_main.getDate(), data_main.getDay())
let controlePrimeiroDia = primeiroDia;

const exibir_dia = (diaPassado, textoPassado) => {
    document.querySelector("#title_day").textContent = diaPassado + " de " + monthNames[controleMes % 12] + " de " + controleAno;

    document.querySelector("#text_of_day").innerHTML = textoPassado;

    document.querySelector(".day_exibition").style = "display : flex;";
    document.querySelector(".fundo_preto").style = "display : flex;";
    document.querySelector(".fundo_preto").onclick = () => {
        document.querySelector(".day_exibition").style = "display : none;";
        document.querySelector(".fundo_preto").style = "display : none;";
    }
}

document.querySelector("#show_month").textContent = monthNames[controleMes]
document.querySelector("#show_year").textContent = ano;

desenhandoDias(primeiroDia)

btn_past.onclick = () => {
    let lastDay = controlePrimeiroDia - 1;

    controleMes -= 1;

    if (controleMes < 0) {
        controleMes += 12;
    }

    if (lastDay < 0) {
        lastDay += 7;
    }

    if (controleMes % 12 == 11) {
        controleAno -= 1;
    }

    controlePrimeiroDia = descobreDiaPrimeiro(nDias(controleMes), lastDay);

    document.querySelector("#show_year").textContent = controleAno;
    document.querySelector("#show_month").textContent = monthNames[controleMes % 12];

    desenhandoDias(controlePrimeiroDia);
}

btn_future.onclick = () => {
    controlePrimeiroDia = (controlePrimeiroDia + nDias(controleMes)) % 7;

    controleMes += 1;

    if (controleMes % 12 == 0) {
        controleAno += 1;
    }

    document.querySelector("#show_year").textContent = controleAno;
    document.querySelector("#show_month").textContent = monthNames[controleMes % 12];

    desenhandoDias(controlePrimeiroDia);
}

btn_home.onclick = () => {
    window.location.href="/"
}

document.querySelectorAll(".day").forEach(($dia) => {
    $dia.onclick = () => {
        if ($dia.children.length == 0) return;

        $.post("", {
            info_dia: $dia.children[0].textContent,
            info_ano: controleAno,
            info_mes: controleMes % 12
        })
            .then(response => {
                exibir_dia($dia.children[0].textContent, response)
            })

    }
})
