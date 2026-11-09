# Aspectos eticos e responsabilidade (TDE2)

- **Privacidade (LGPD):** curriculos tem dados pessoais. O app nao grava arquivos nem texto em disco; o conteudo e enviado ao LLM apenas durante a analise. Recomenda-se obter consentimento do candidato e usar modelo local (ex.: Llama via Ollama) em producao.
- **Seguranca:** chave da API em `.env` (fora do Git); minimizar o dado enviado (o prompt orienta a ignorar nome, genero, idade, foto).
- **Transparencia:** o sistema mostra a area prevista com probabilidade, a nota com justificativa e os criterios usados; o usuario sabe que ha IA envolvida.
- **Vieses:** o dataset (Kaggle, em ingles, poucos perfis) pode refletir vieses historicos de genero, instituicao e area. O modelo de ML aprende o que e frequente no dataset, e o LLM pode herdar vieses do pre-treino. Mitigacao: instrucao para ignorar atributos sensiveis, auditoria por amostragem e comparacao de notas entre perfis equivalentes.
- **Impacto nos usuarios:** uma nota baixa pode excluir candidatos injustamente. O sistema e apenas apoio; a decisao final e humana, com direito a revisao (LGPD art. 20).
- **Limitacoes:** alucinacoes do LLM; PDFs com layout complexo ou imagem (sem OCR) perdem texto; dataset em ingles; categorias fixas; curriculos atipicos sao mal classificados; custo e latencia da API.
