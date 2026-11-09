# Aspectos éticos e responsabilidade no uso da IA

O TalentMatch AI é uma ferramenta de **apoio à triagem de currículos**, e não um sistema de decisão autônoma. A análise gerada deve ser sempre revisada por uma pessoa responsável pelo processo seletivo.

## Privacidade e LGPD

Currículos podem conter dados pessoais sensíveis, como nome, contato, idade, gênero, nacionalidade, estado civil e informações sobre saúde. Por isso, o sistema deve tratar esses dados com cuidado.

* O candidato deve ser informado sobre o uso do currículo e, quando aplicável, consentir com o tratamento dos dados.
* O sistema não deve armazenar currículos, textos extraídos ou relatórios sem uma finalidade clara, base legal e período de retenção definido.
* Em produção, recomenda-se o uso de modelo local, como Llama via Ollama, para reduzir o envio de dados pessoais a serviços externos.
* O acesso aos currículos e às análises deve ser restrito às pessoas autorizadas do processo seletivo.

## Segurança dos dados

* A chave da API do LLM deve ser mantida em variáveis de ambiente, no arquivo `.env`, que não deve ser enviado ao Git.
* O repositório inclui `.env.example` apenas como modelo de configuração; nenhuma chave real deve ser commitada.
* O texto enviado ao LLM deve ser minimizado ao necessário para a análise.
* Recomenda-se criptografia em trânsito e em repouso, controle de acesso, registros de auditoria e política de retenção e exclusão de dados.

## Transparência

A interface informa que a análise é automática e que o resultado está sujeito a erros e vieses. O usuário consegue visualizar:

* A área profissional prevista pelo modelo de Machine Learning.
* As probabilidades das áreas mais prováveis.
* A nota de aderência à vaga.
* A justificativa da análise.
* Os pontos fortes e lacunas identificados.
* A necessidade de revisão humana antes de qualquer decisão.

## Vieses algorítmicos

O dataset utilizado pode refletir vieses históricos de gênero, raça, idade, instituição de ensino, região, idioma e área profissional. O modelo de Machine Learning aprende padrões presentes nos dados e pode reproduzi-los ou ampliá-los.

O LLM também pode herdar vieses presentes em seus dados de pré-treinamento. Por isso, o prompt instrui o modelo a ignorar nome, gênero, idade, foto, estado civil e nacionalidade, mas essa instrução não elimina completamente o risco de viés.

Mitigações recomendadas:

* Auditoria periódica das previsões por gênero, idade, região e outros grupos relevantes, quando esses dados estiverem disponíveis de forma ética e legal.
* Comparação das notas atribuídas a currículos equivalentes, mas com características demográficas diferentes.
* Revisão humana obrigatória de todas as decisões com impacto no candidato.
* Monitoramento de falsos negativos e falsos positivos.
* Atualização e diversificação do dataset de treinamento.

## Impacto sobre os usuários

Uma nota baixa ou uma classificação incorreta pode prejudicar injustamente a oportunidade de um candidato. Por isso, o sistema não deve eliminar automaticamente pessoas do processo seletivo.

A decisão final deve considerar o contexto completo da candidatura, entrevistas, provas técnicas, experiências e critérios definidos pela organização. O candidato também deve poder solicitar revisão, correção ou explicação sobre decisões automatizadas que o afetem, conforme os princípios da LGPD.

## Limitações da tecnologia

* O modelo de classificação depende da qualidade, representatividade e atualidade do dataset.
* O dataset utilizado é majoritariamente em inglês, o que pode reduzir a qualidade da análise para currículos em português.
* Currículos com layout complexo, imagens, tabelas ou digitalização de baixa qualidade podem perder informações durante a extração de texto.
* O sistema não realiza OCR; portanto, PDFs baseados em imagem podem não ser analisados corretamente.
* O LLM pode alucinar informações, atribuir habilidades inexistentes ou interpretar experiências de forma imprecisa.
* A nota de aderência é uma estimativa probabilística e não uma medida objetiva de competência.
* O uso de APIs comerciais envolve custo, latência, dependência de provedor externo e possível alteração de políticas ou modelos.

## Uso responsável

O TalentMatch AI deve ser utilizado apenas como apoio à triagem inicial. Ele não substitui análise humana, entrevista, avaliação técnica, verificação de referências nem decisão final de contratação.

