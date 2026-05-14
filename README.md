# Resume-as-Code (RaC): The Reality Check Pipeline 🚀

Bem-vindo ao **Resume-as-Code (RaC)**. Este não é apenas um conjunto de scripts; é um manifesto sobre como tratar sua carreira e processos seletivos usando princípios de **Engenharia de Software, FinOps e Arquitetura**.

Em vez de disparar currículos genéricos, criamos uma esteira de Integração e Entrega Contínua (CI/CD) para o seu perfil profissional. Sem "Overselling", sem desperdício de energia. Apenas integridade técnica e foco no longo prazo.

---

## 🏗️ A Arquitetura (Componentes Core)

O projeto atualmente opera sobre três pilares de código puro e local (Stateless & Zero Custo):

### 1. The Single Source of Truth (`master_cv.yaml`)
A base de dados do projeto. Todas as suas experiências, formações e conquistas residem aqui. Em vez de editar dezenas de documentos `.docx`, você atualiza o YAML. Ele garante que não haja discrepâncias ou mentiras no seu perfil.

### 2. O Motor de Build (`generate_pdf.sh` & `cv_style.css`)
Nosso compilador. Ele pega os "Recortes de Realidade" que você desenha em Markdown a partir do YAML e "builda" um PDF elegante usando o `md-to-pdf` via npx. É rápido, auditável via Git e dispensa processadores de texto pesados.
- **Integração Visual (`cv_style.css`):** Um arquivo de CSS com padrão "Gold Standard". Ele contém regras estritas de Mídia Paginada (`page-break`) para impedir que seções do seu currículo quebrem no meio das páginas.
- **Observabilidade:** Diferente de scripts básicos, nosso motor não joga erros "no lixo". A saída de compilação do motor PDF é direcionada para um `pdf_generation.log`, permitindo debugar falhas do Puppeteer facilmente.
### 3. The Reality Check Filter (`cv_scanner.py`)
O nosso linter / SonarQube para vagas de emprego. Antes de você gastar energia mental adaptando seu CV para uma vaga, você joga a descrição dela neste CLI. Ele varre o texto aplicando expressões regulares e um sistema de "Tiers":
- **Tier 1 (The Dream):** AWS, Terraform, Cloud, IA (+ Pontos).
- **Tier 2 (The Sponsor):** APIs, SQL, Logs, Backend (+ Pontos Base).
- **Tier 3 (The Drainers):** Angular, Figma, Telas (- Pontos de Penalidade).

Se o script detectar que a vaga vai sugar sua energia (Score negativo de Drainers), você aborta a missão em 2 segundos.

### 4. Telemetria e FinOps Pessoal (`cv_analytics.csv`)
Toda vez que o Scanner avalia uma vaga, ele registra os dados num arquivo CSV. Isso permite que você aplique "Business Intelligence" sobre a sua própria carreira. No fim do mês, você sabe exatamente quantas vagas "Tier 1" você encontrou e qual a aderência do mercado.

---


## 💡 Princípio de Design (Para a comunidade)
*"Seu currículo é um deploy da sua vivência. A vaga é o ambiente de produção. Não tente fazer deploy de um container Linux num IIS Server. Use o Scanner."*
