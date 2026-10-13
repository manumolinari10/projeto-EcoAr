const ctx = document.getElementById('graficoHistorico').getContext('2d');

let meuGrafico = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
        datasets: [
            {
                label: 'AQI',
                data: [38, 42, 35, 45, 30, 38],
                borderColor: '#059669',
                tension: 0.4
            },
            {
                label: 'Temp. Max',
                data: [26, 27, 28, 27, 25, 24],
                borderColor: '#F97316',
                tension: 0.4
            },
            {
                label: 'Temp. Min',
                data: [20, 21, 22, 21, 19, 18],
                borderColor: '#3B82F6',
                tension: 0.4
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {display: false}
        },
        scales: {
            y: {beginAtZero: false}
        }
    }
});

const pagMedidor = document.getElementById('pag-medidor');
const pagDicas = document.getElementById('pag-dicas');
const pagPrevisao = document.getElementById('pag-previsao');

const pontos = document.querySelectorAll('.ponto');

function esconderTudo() {
    pagMedidor.style.display = 'none';
    pagDicas.style.display = 'none';
    pagPrevisao.style.display = 'none';

    pontos.forEach(ponto => {
        ponto.classList.remove('ativo');
    });
}

pontos[0].addEventListener('click', () => {
    esconderTudo();
    pagMedidor.style.display = 'block';
    pontos[0].classList.add('ativo');
});

pontos[1].addEventListener('click', () => {
    esconderTudo();
    pagDicas.style.display = 'block';
    pontos[1].classList.add('ativo');
});

pontos[2].addEventListener('click', () => {
    esconderTudo();
    pagPrevisao.style.display = 'block';
    pontos[2].classList.add('ativo');
});

const btnToggle = document.querySelector('.btn-toggle');
const bolinha = document.querySelector('.bolinha');
const iconeTema = btnToggle.querySelector('i');

function atualizarCoresGrafico(isEscuro) {
    if (isEscuro) {
        meuGrafico.options.scales.x.grid.color = 'rgba(255,255,255, 0.1)';
        meuGrafico.options.scales.y.grid.color = 'rgba(255,255,255, 0.1)';
        meuGrafico.options.scales.x.ticks.color = '#CBD5E1';
        meuGrafico.options.scales.y.ticks.color = '#CBD5E1';
    } else {
        meuGrafico.options.scales.x.grid.color = 'rgba(0, 0, 0, 0.1)';
        meuGrafico.options.scales.y.grid.color = 'rgba(0, 0, 0, 0.1)';
        meuGrafico.options.scales.x.ticks.color = '#64748B';
        meuGrafico.options.scales.y.ticks.color = '#64748B';
    }
    meuGrafico.update();
}

const temaSalvo = localStorage.getItem('tema');
if (temaSalvo === 'escuro') {
    document.body.classList.add('modo-escuro');
    bolinha.classList.add('deslizar');
    iconeTema.classList.remove('ph-moon');
    iconeTema.classList.add('ph-sun');
    atualizarCoresGrafico(true);
}

btnToggle.addEventListener('click', () => {
    bolinha.classList.toggle('deslizar');  //adiciona ou remove a classe que faz a bolinha ir para o lado
    const isEscuro = document.body.classList.toggle('modo-escuro');

    if (isEscuro) {  //verifica se a bolinha foi para a direita e troca o ícone
        iconeTema.classList.remove('ph-moon');
        iconeTema.classList.add('ph-sun');
        localStorage.setItem('tema', 'escuro');
        atualizarCoresGrafico(true);
    } else {
        iconeTema.classList.remove('ph-sun');
        iconeTema.classList.add('ph-moon');
        localStorage.setItem('tema', 'claro');
        atualizarCoresGrafico(false);
    }
});

const engrenagem = document.querySelector('.ph-gear');
const modal = document.querySelector('.modal-fundo');
const btnFechar = document.querySelector('.btn-fechar');

engrenagem.addEventListener('click', () => {  //abrir o modal
    modal.style.display = 'flex';
});

btnFechar.addEventListener('click', (evento) => {  //fechar o modal
        modal.style.display = 'none';
});

modal.addEventListener('click', (evento) => {
    if (evento.target === modal) {
        modal.style.display = 'none';
    }
});

const botoesMedida = document.querySelectorAll('.btn-medida');  //captura todos os botões de medida

botoesMedida.forEach(botao => {  //para cada botão, adiciona um "ouvinte" de cliques
    botao.addEventListener('click', () => {
        botoesMedida.forEach(b => b.classList.remove('ativo'));  //1. remove a classe 'ativo' de TODOS os botões

        botao.classList.add('ativo');  //2. adiviona a classe 'ativo' APENAS no botão que foi clicado
    });
});

const botoesPeriodo = document.querySelectorAll('.btn-periodo');

botoesPeriodo.forEach(botao => {
    botao.addEventListener('click', () => {
        botoesPeriodo.forEach(b => b.classList.remove('ativo'));

        botao.classList.add('ativo');
    });
});

const caixaDicas = document.getElementById('pag-dicas'); // 1. Seleciona a caixa onde as dicas vão aparecer

function atualizarDicasDeSaude(indiceAQI) {  // 2. Função que decide o que mostrar com base no nível de poluição (1 a 5)
    let dicasHTML = ''; // Começa vazio

    if (indiceAQI === 1 || indiceAQI === 2) { // Nível 1 e 2: Ar Bom ou Razoável
        dicasHTML = `
            <div class="dica-item">
                <i class="ph ph-tree"></i>
                <span>Ar perfeito para atividades ao ar livre!</span>
            </div>
            <div class="dica-item">
                <i class="ph ph-wind"></i>
                <span>Abra as janelas e renove o ar de casa.</span>
            </div>
        `;
    } else if (indiceAQI === 3) { // Nível 3: Moderado
        dicasHTML = `
            <div class="dica-item">
                <i class="ph ph-warning-circle"></i>
                <span>Qualidade aceitável. Pessoas sensíveis devem reduzir esforços.</span>
            </div>
        `;
    } else { // Nível 4 e 5: Ruim ou Muito Ruim
        dicasHTML = `
            <div class="dica-item">
                <i class="ph ph-mask-face"></i>
                <span>Use máscara em áreas externas.</span>
            </div>
            <div class="dica-item">
                <i class="ph ph-house-line"></i>
                <span>Mantenha as janelas fechadas. Evite exercícios fora de casa.</span>
            </div>
        `;
    }

    caixaDicas.innerHTML = dicasHTML;  // 3. Injeta as dicas criadas dentro da sua div no HTML
}

// PARA TESTAR AGORA MESMO:
// Mude este número de 1 a 5, guarde o ficheiro, e clique na bolinha das dicas no seu carrossel!
atualizarDicasDeSaude(1);