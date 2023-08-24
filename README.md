# LuckStudy

## Repositório destinado ao site de banco de questões, inicialmente voltado para o estudo de matérias do primeiro período de Matemática Aplicada na FGV.
<br>

<p> LuckStudy é um site de banco de questões, inicialmente voltado para o estudo de matérias do primeiro período de Matemática Aplicada na FGV.
Sua ideia é gerar questões e suas possíveis respostas de maneira colaborativa, a partir de arquivos YAML e formatação Tex. Assim, nesse servidor cada um poderia elaborar questões e repostas nesses arquivos.</p>

# Método de construção do projeto.
<h6> Linguagens utilizadas: HTML, CSS, JavaScript(Bootstrap, MathJax, Jinja, Python(Flask, Yaml), arquivos .yaml. </h6>
<br>
<p> Inicialmente, a página inicial foi construída com a aplicação do Bootstrap 5, com intuito de gerar o padrão para o site. O site possui a página inicial com a apresentação geral e botões para todas as seções do site, que são: A própria página inicial, as páginas das questões de cada matéria, uma página para obter contatos com os administradores e outra página para entender para que foi criada.</p>
 
<p> Depois, foram criados vários arquivos no formato .yaml para o armazenamento do enunciado das questões. Para cada questão, um "texto:" representa o seu enunciado, que segue acompanhado de 4 respostas possíveis: A, B, C ou D, em que somente uma delas está correta. Cada alternativa é representada: por cada letra, como " - A :", seguido do seu enunciado; se é a alternativa correta ou não, pelo "correct:"; E uma razão ou dica apontada por "reason:". Segue-se um exemplo abaixo:</p>
 
<p> Posteriormente, para ler os arquivos YAML, foi criado um código em Python que importa a biblioteca PyYaml, executando um comando iterável em que se lê todas as questões, transformando em um dicionário propriamente de Pyhton.</p>
<p> Assim, para renderizar o HTML, foi usado Flask e Jinja, iterando novamente sobre o dicionário obtido de maneira conveniente. O resultado obtido é uma questao da seguinte maneira:</p>

<br>
<p> Para a exibição de fórmulas matemáticas, foi utilizado MathJax, que permite escrever em LaTex no HTML, e para a costumização do site, aplicou-se templates do Bootstrap 5.</p>
