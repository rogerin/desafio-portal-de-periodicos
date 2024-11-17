# SciFlow: Acesso Simples a Artigos Acadêmicos via WhatsApp

## Descrição

O **SciFlow** é uma solução inovadora que facilita o acesso a conteúdos acadêmicos de forma simples e intuitiva. Integrando APIs, tecnologia de comunicação e inteligência artificial, proporcionamos resumos de artigos acadêmicos diretamente pelo WhatsApp, eliminando barreiras de navegação em plataformas acadêmicas complexas.

---

## Arquitetura do Projeto

O projeto utiliza uma arquitetura baseada em serviços da AWS e ferramentas modernas para garantir escalabilidade, eficiência e acessibilidade:

1. **API Gateway**: Disponibiliza uma API REST para receber solicitações.
2. **AWS Lambda**: Realiza o processamento principal, incluindo:
   - **Crawler** no portal de periódicos para extrair informações.
   - Integração com a API da OpenAI para resumir os artigos.
3. **AWS EC2 com n8n**: Automação de comunicação, conectando:
   - WhatsApp para interagir com os usuários.
   - API Gateway para processar os temas enviados.

---

## Arquitetura Visual

![Arquitetura do Projeto](./src/img/arquitetura.png)

---

## Como Usar

### Passo 1: Enviar uma Mensagem
Envie uma mensagem para o número do WhatsApp:  
📱 **+55 88 99929-7262**

### Passo 2: Escolha o Tema
Digite o tema de um artigo que deseja pesquisar. Exemplos:
- **Saúde mental**
- **Internet das coisas**
- **Sustentabilidade**

### Passo 3: Receba o Resumo
A solução buscará artigos relevantes, resumirá o conteúdo e retornará diretamente pelo WhatsApp.

---

## Tecnologias Utilizadas

- **AWS API Gateway**: Disponibiliza a API REST.
- **AWS Lambda**: Executa o crawler e integra com a API da OpenAI.
- **AWS EC2**: Hospeda o n8n para gerenciar a comunicação.
- **WhatsApp API**: Interface para interação com os usuários.
- **OpenAI GPT-4**: Gera resumos simplificados dos artigos.

---

## Contato

Caso tenha dúvidas ou queira saber mais sobre o projeto, entre em contato pelo número 📱 **+55 88 99929-7262** ou envie um e-mail para [contato@sciflow.com](mailto:contato@sciflow.com).