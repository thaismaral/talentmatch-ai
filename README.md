# TalentMatch AI

Sistema inteligente de apoio à triagem de currículos. O projeto combina **Machine Learning** para classificar a área profissional provável do currículo e um **LLM** para analisar a aderência entre o currículo e uma vaga informada.

A decisão final de contratação permanece **sempre humana**; o sistema é apenas uma ferramenta de apoio.

## Funcionalidades

- Upload de currículo em PDF ou TXT, ou colagem direta do texto.
- Classificação da área profissional com modelo de Machine Learning.
- Exibição das três áreas mais prováveis e suas probabilidades.
- Análise do currículo frente à vaga por LLM.
- Nota de aderência de 0 a 100.
- Identificação de habilidades, pontos fortes, lacunas e justificativa.
- Sugestão de perguntas para entrevista.
- Download do relatório gerado.

## Arquitetura

```text
Entrada
  Currículo (PDF/TXT) + descrição da vaga
        |
        v
Processamento
  Extração de texto -> limpeza -> TF-IDF -> classificador ML
  Texto + vaga + previsão do ML -> LLM
        |
        v
Saída
  Área prevista, probabilidades, nota de aderência,
  análise estruturada e relatório para download
```

## Requisitos do TDE2

| Critério | Implementação |
|---|---|
| Machine Learning | `train.py` compara Logistic Regression, Random Forest e MLP com TF-IDF; seleciona o melhor modelo pelo F1 macro. |
| LLM | `llm.py` envia currículo, vaga e previsão do ML para um modelo de linguagem e retorna análise estruturada em JSON. |
| Entrada, processamento e saída | `app.py` recebe os arquivos/textos, processa os dados e gera análise, gráfico, métricas e relatório. |
| Ética e responsabilidade | `ETICA.md` e avisos na interface abordam privacidade, segurança, transparência, vieses e limitações. |

## Estrutura do projeto

```text
app.py               Interface Streamlit e fluxo completo
llm.py               Integração com LLM
preprocess.py        Limpeza do texto
train.py             Treinamento e comparação dos modelos
models/              Modelo treinado, métricas e matriz de confusão
data/                Dataset (não versionado)
ETICA.md             Aspectos éticos e limitações
requirements.txt     Dependências
```

## Instalação

```bash
git clone [https://github.com/thaismaral/talentmatch-ai.git](https://github.com/thaismaral/talentmatch-ai.git)
cd talentmatch-ai
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuração do LLM

Crie um arquivo `.env` na raiz do projeto, com base no `.env.example`:

```env
LLM_API_KEY=sua_chave_aqui
LLM_BASE_URL=[https://api.openai.com/v1](https://api.openai.com/v1)
LLM_MODEL=gpt-4o-mini
```

Não versione o arquivo `.env` nem compartilhe chaves de API.

## Dataset

O treinamento utiliza o dataset **Resume Dataset**, disponível no Kaggle:

https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset

Após baixar o arquivo, crie a pasta `data/` e salve o CSV como:

```text
data/Resume.csv
```

O código espera as colunas `Resume_str` e `Category`. Caso o arquivo use `Resume` em vez de `Resume_str`, o próprio `train.py` identifica a coluna correta.

## Treinar o modelo

```bash
python train.py
```

O script:

1. Lê `data/Resume.csv`.
2. Remove duplicatas e valores nulos.
3. Limpa o texto dos currículos.
4. Divide os dados em treino e teste, com estratificação por categoria.
5. Treina Logistic Regression, Random Forest e MLP.
6. Calcula acurácia e F1 macro.
7. Salva o melhor modelo em `models/classificador.joblib`.
8. Gera `models/comparacao_modelos.csv` e `models/matriz_confusao.png`.

## Executar a aplicação

```bash
streamlit run app.py
```

A aplicação abrirá no navegador, normalmente em:

```text
http://localhost:8501
```

## Demonstração

1. Execute `streamlit run app.py`.
2. Faça upload de um currículo em PDF/TXT ou cole o texto.
3. Informe a descrição da vaga.
4. Clique em **Analisar**.
5. Verifique a área prevista, a nota de aderência, a análise do LLM e baixe o relatório.

## Limitações

- O modelo foi treinado com um dataset em inglês e pode ter desempenho reduzido com currículos em português.
- PDFs digitalizados ou com layout complexo podem exigir OCR.
- O LLM pode cometer alucinações ou interpretar informações de forma imprecisa.
- A nota de aderência é uma estimativa de apoio à decisão, não uma avaliação definitiva do candidato.
- O sistema não deve ser usado para decisão automatizada de contratação ou exclusão de candidatos.