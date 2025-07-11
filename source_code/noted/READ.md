# noted; Plataforma de Produtividade Digital

Uma aplicação completa de cadernos digitais open source com sincronização na cloud, extensões para integração com outras ferramentas, e recursos de produtividade e criatividade, construída com Flask e MySQL.

## Tecnologias Utilizadas

- **Backend:** Python 3.8### Integrações e Extensibilidade

### Integrações Disponíveis
- Notion API para importação/exportação de páginas e bases de dados
- Obsidian para gráficos de conhecimento e vault compartilhado
- Google Calendar para sincronização de eventos e lembretes
- GitHub para armazenamento de snippets e código
- Dropbox/Google Drive para armazenamento de anexos

### Sistema de Extensões
- Framework de plugins com marketplace integrado
- API para desenvolvedores criarem extensões personalizadas
- Sistema de temas para personalização visual
- Extensões de produtividade (temporizador pomodoro, rastreador de hábitos)
- Extensões de diagramas e visualização de dados

### Pontos de Extensão
- Arquitetura de blueprints facilita adição de novos módulos
- Sistema de eventos para hooks de extensões
- Templates customizáveis para diferentes casos de uso
- API aberta com documentação completa
- SDK para desenvolvimento de extensões.5
- **Base de dados:** MySQL, SQLAlchemy 1.4.46
- **Frontend:** HTML, CSS, JavaScript
- **Autenticação:** itsdangerous 2.1.2, Werkzeug 2.2.3
- **Emails:** Flask-Mail 0.9.1
- **Formulários:** Flask-WTF 1.1.1, WTForms 3.0.1
- **Analytics:** Jupyter notebooks, pandas, papermill, nbconvert
- **Ambiente:** python-dotenv, venv

## Estrutura do Projeto

```
noted/
├── __init__.py        # Configuração da aplicação e inicialização
├── app.py             # Ponto de entrada da aplicação
├── config.py          # Configurações e variáveis de ambiente
├── forms.py           # Classes de validação de formulários
├── models.py          # Modelos SQLAlchemy para a base de dados
├── requirements.txt   # Dependências do projeto
├── notebooks/         # Notebooks Jupyter para análise de dados
├── routes/            # Blueprints e rotas da aplicação
│   ├── __init__.py
│   ├── admin.py       # Painel de administração
│   ├── auth.py        # Autenticação e gestão de utilizadores
│   ├── cart.py        # Funcionalidades do carrinho de compras
│   ├── checkout.py    # Processo de finalização de compra
│   ├── misc.py        # Páginas diversas (início, sobre, etc.)
│   ├── products.py    # Catálogo de produtos e categorias
│   └── api/           # Endpoints da API REST
├── services/          # Serviços da aplicação
│   ├── __init__.py
│   └── email_service.py  # Serviço de envio de emails
├── static/            # Ficheiros estáticos
│   ├── css/
│   ├── js/
│   ├── img/
│   └── fonts/
└── templates/         # Templates HTML
    ├── emails/        # Templates de email
    ├── pages/         # Páginas principais
    └── partials/      # Componentes reutilizáveis
```

## Ideia Base

A noted; é uma plataforma de cadernos digitais open source que oferece sincronização online, extensões para múltiplas ferramentas de produtividade e recursos criativos para o utilizador. Desenvolvemos este projeto com foco em:

- Ajudar a organizar qualquer tarefa, pequena ou grande
- Oferecer uma interface fácil de utilizar e minimalista
- Fornecer apenas o necessário, com extensões opcionais
- Focar na produtividade e no trabalho organizado

## Funcionalidades Principais

### Cadernos Digitais Sincronizados
- Criação e edição de notas ilimitadas
- Sincronização automática entre dispositivos via cloud
- Acesso offline com sincronização quando conectado
- Organização por categorias, tags e pastas
- Histórico de versões e edição colaborativa

### Integrações Externas
- Conexão com Notion para importar/exportar documentos
- Integração com Obsidian para gráficos de conhecimento
- Sincronização com Google Calendar para eventos e lembretes
- Plugins para outras ferramentas de produtividade
- API aberta para desenvolvedores criarem extensões

### Ferramentas de Criatividade
- Gerador de ideias baseado em IA
- Inspiração aleatória para desbloqueio criativo
- Diagramas integrados (compatível com Excalidraw, Xmind)
- Templates pré-definidos para diversos tipos de projetos
- Modos de visualização (kanban, lista, mapa mental)

### Interface Minimalista
- Design limpo focado no conteúdo
- Modo escuro/claro adaptativo
- Personalizações de layout e aparência
- Atalhos de teclado customizáveis
- Widgets de produtividade configuráveis

### Recursos de IA
- Assistente de escrita com sugestões contextuais
- Resumo automático de textos longos
- Categorização inteligente de notas
- Transcrição de áudio para texto
- Traduções integradas entre idiomas

### Autenticação de Utilizadores
- Registo com verificação por email
- Login e gestão de sessões
- Recuperação de senha
- Níveis de acesso (básico, premium, administrador)
- Autenticação de dois fatores

### Painel de Administração
- Dashboard com métricas de uso e engagement
- Gestão de utilizadores e permissões
- Monitoramento de performance e recursos
- Analytics com gráficos gerados via Jupyter notebooks
- Sistema de suporte ao utilizador integrado

## Configuração do Ambiente

1. Criar ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Instalar dependências (usando o script incluído):
   ```
   setup_venv.bat
   ```
   
   Ou manualmente:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install python-dotenv pandas matplotlib sqlalchemy mysql-connector-python
   pip install papermill nbformat==5.9.2 nbconvert jupyter_client
   ```

3. Configurar o ficheiro .env:
   ```
   SECRET_KEY=chave_secreta
   DATABASE_URI=mysql://username:password@localhost/db_noted
   MAIL_SERVER=smtp.exemplo.com
   MAIL_PORT=587
   MAIL_USERNAME=seu_email@exemplo.com
   MAIL_PASSWORD=sua_senha
   MAIL_USE_TLS=True
   MAIL_USE_SSL=False
   ```

4. Inicializar a base de dados:
   ```
   python ../init_sample_data.py
   ```

5. Executar a aplicação:
   
   Usando o script incluído (também inicia o WAMP):
   ```
   start_project.bat
   ```
   
   Ou manualmente:
   ```
   python app.py
   ```
   
   Ou usando Flask CLI:
   ```
   set FLASK_APP=app.py
   set FLASK_ENV=development
   flask run
   ```

## Endpoints da API

### Notebook API
- `/api/notebooks` - Listar, criar, atualizar cadernos digitais
- `/api/notebooks/<id>` - Operações em cadernos específicos
- `/api/notebooks/<id>/notes` - Listar, criar notas em um caderno
- `/api/notes/<id>` - Operações em notas específicas
- `/api/notes/<id>/attachments` - Gerenciar anexos de uma nota
- `/api/notes/<id>/versions` - Histórico de versões de uma nota
- `/api/categories` - Gerenciar categorias
- `/api/tags` - Gerenciar tags
- `/api/search` - Pesquisa avançada de conteúdo

### Integração API
- `/api/integrations` - Listar, configurar integrações disponíveis
- `/api/integrations/notion` - Operações específicas para Notion
- `/api/integrations/obsidian` - Operações específicas para Obsidian
- `/api/integrations/gcalendar` - Operações específicas para Google Calendar
- `/api/sync` - Sincronização manual de dados com serviços externos

### IA API
- `/api/ai/suggestions` - Obter sugestões de conteúdo
- `/api/ai/summarize` - Resumir texto longo
- `/api/ai/transcribe` - Transcrever áudio para texto
- `/api/ai/translate` - Traduzir conteúdo entre idiomas
- `/api/ai/ideas` - Gerar ideias criativas

### Admin API
- `/api/admin/users` - Gestão de utilizadores
- `/api/admin/stats` - Estatísticas gerais do sistema
- `/api/admin/usage` - Monitoramento de uso de recursos
- `/api/admin/extensions` - Gestão de extensões
- `/api/admin/system` - Configurações do sistema

## Rotas e Fluxo de Navegação

### Rotas Principais
- **/** - Página inicial com visão geral dos cadernos e recursos
- **/login** - Autenticação de utilizadores
- **/register** - Registo de novos utilizadores
- **/verify/<token>** - Verificação de email com token seguro
- **/account** - Página de conta do utilizador
- **/forgot-password** - Solicitar redefinição de senha
- **/reset-password/<token>** - Redefinir senha com token seguro
- **/notebooks** - Listagem de cadernos do utilizador
- **/notebooks/<id>** - Vista de um caderno específico
- **/notebook/<id>/edit** - Editor do caderno digital
- **/extensions** - Biblioteca de extensões e plugins
- **/integrations** - Configuração de integrações externas
- **/settings** - Configurações da conta e preferências

### Rotas de Administração
- **/admin/dashboard** - Painel principal de administração
- **/admin/analytics** - Análises e relatórios de uso
- **/admin/users** - Gestão de utilizadores
- **/admin/extensions** - Gestão de extensões
- **/admin/system** - Configurações do sistema

### Fluxos de Utilizador

#### Fluxo de Criação de Conteúdo
1. Login no sistema
2. Criação de novo caderno ou acesso a existente
3. Edição de conteúdo no editor principal
4. Utilização de ferramentas de IA e criatividade
5. Sincronização automática com a cloud
6. Compartilhamento ou exportação (opcional)

#### Fluxo de Integração
1. Acesso à seção de integrações
2. Seleção e autorização de serviços externos (Notion, Obsidian, etc.)
3. Configuração de sincronização e regras
4. Importação/exportação de dados

#### Fluxo de Autenticação
1. Registo de nova conta
2. Verificação por email
3. Login
4. Recuperação de senha (se necessário)

#### Fluxo de Administração
1. Login como administrador
2. Acesso ao painel de administração
3. Gestão de usuários e permissões
4. Monitoramento de uso do sistema
5. Visualização de métricas e analytics

## Testes

O projeto inclui testes para várias funcionalidades:
- **test_email.py**: Verifica configuração e envio de emails com Flask-Mail
- **test_cart_final.py**: Testes finais para o carrinho de compras
- **test_live_cart.py**: Testes em ambiente de produção para o carrinho
- **test_bulk_update.py**: Testes para atualizações em massa de produtos
- **test_categories.py**: Validação do sistema de categorias

### Sistema de Testes
Para executar os testes:
```
python -m pytest test_email.py -v
python -m pytest test_cart_final.py -v
```

O arquivo `TESTING_CHECKLIST.md` contém um guia completo para testar todas as funcionalidades do sistema antes de um lançamento.

## Contribuição

Para contribuir para este projeto:
1. Fazer fork do repositório
2. Criar um novo branch (`git checkout -b feature/nova-funcionalidade`)
3. Fazer commit das alterações (`git commit -am 'Adicionar nova funcionalidade'`)
4. Fazer push para o branch (`git push origin feature/nova-funcionalidade`)
5. Criar um Pull Request

## Arquitetura do Sistema

### Padrões de Design
- **Model-View-Controller (MVC)**: Separação clara entre dados (models.py), apresentação (templates) e lógica (routes)
- **Blueprints Flask**: Organização modular da aplicação em componentes reutilizáveis
- **Service Layer**: Camada de serviços para lógica de negócios complexa (ex: email_service.py)
- **ORM**: Uso de SQLAlchemy para abstração da base de dados e mapeamento objeto-relacional
- **Injeção de Dependências**: Utilização de context processors para disponibilizar dados globais

### Segurança
- Armazenamento de senhas com hash PBKDF2-SHA256
- Proteção contra CSRF em formulários
- Tokens seguros para verificação de email e redefinição de senha
- Controle de sessão com lifetime configurável e assinatura
- Validação de dados de entrada em formulários

### Banco de Dados
O esquema da base de dados inclui as seguintes tabelas principais:
- `users`: Informações de utilizadores e credenciais
- `notebooks`: Cadernos digitais dos utilizadores
- `notes`: Notas individuais dentro dos cadernos
- `categories`: Sistema de categorias para organização
- `tags`: Sistema de etiquetas para classificação cruzada
- `attachments`: Arquivos e mídia anexados às notas
- `versions`: Histórico de versões de notas
- `extensions`: Extensões instaladas
- `integrations`: Configurações de integrações com serviços externos
- `sharing`: Configurações de compartilhamento e colaboração
- `user_settings`: Preferências e configurações dos utilizadores
- `ai_usage`: Registros de uso dos recursos de IA
- `templates`: Modelos predefinidos para notas
- `noted_ai_suggestions`: Cache de sugestões geradas por IA

## Integrações e Extensibilidade

### Possíveis Integrações
- Gateways de pagamento (estrutura preparada no model `PaymentInfo`)
- APIs de envio para cálculo de frete
- Sistemas de CRM para gestão de clientes
- Ferramentas de marketing por email

### Pontos de Extensão
- Arquitetura de blueprints facilita adição de novos módulos
- Sistema de serviços permite adicionar novas funcionalidades
- Estrutura de templates modular com partials reutilizáveis

## Detalhes Técnicos

### Estrutura de Templates
Os templates seguem uma estrutura hierárquica organizada:
- `layout.html`: Template base com estrutura HTML, CSS e JS comuns
- `partials/`: Componentes reutilizáveis (navbar, footer, sidebar, etc.)
- `pages/`: Templates específicos para cada página
  - `pages/account/`: Área de utilizador
  - `pages/admin/`: Painel de administração
  - `pages/auth/`: Autenticação e registo
  - `pages/categories/`: Listagem de categorias
- `emails/`: Templates para mensagens de email
  - `base_email.html`: Layout base para todos os emails
  - `order_confirmation.html`, `registration.html`, `password_reset.html`

### Assets Estáticos
Organização de arquivos estáticos:
- `css/`: Estilos CSS
  - `globals.css`: Estilos globais
  - `layout.css`: Estrutura principal
  - `auth.css`: Estilos para páginas de autenticação
  - `cart.css`: Estilos para carrinho de compras
  - `breadcrumb.css`: Navegação por breadcrumb
  - `pages/`: Estilos específicos para páginas
  - `admin/`: Estilos para o painel administrativo
- `js/`: Scripts JavaScript
  - `script.js`: Funções globais
  - `admin/`: Scripts para área administrativa
  - `checkout/`: Scripts para o processo de checkout
  - `pages/`: Scripts específicos para páginas
- `img/`: Imagens
  - `logo-n.png`, `logo.png`: Logotipos da marca
  - `noted-vision.png`: Imagem conceitual
  - `categories/`: Imagens para categorias
  - `products/`: Imagens de produtos
  - `icons/`: Ícones do sistema
- `fonts/`: Fontes personalizadas
  - `meriva.ttf`, `meriva.otf`: Fonte principal da identidade visual

### Componentes JavaScript
- **Cart Management**: Manipulação assíncrona do carrinho via AJAX
- **Form Validation**: Validação cliente-side nos formulários
- **Admin Tables**: Sistema de tabelas dinâmicas com ordenação e filtros
- **Checkout Process**: Validação de campos e gerenciamento de estados
- **Dashboard Charts**: Visualização de dados com gráficos interativos

### Notebooks de Análise
Os notebooks Jupyter são utilizados para análises avançadas:
- `analytics.ipynb`: Análise de vendas e comportamento de usuários
- `graphics.ipynb`: Geração de visualizações para o dashboard

### Configurações de Segurança
- Sessões assinadas com SECRET_KEY
- Lifetime configurável das sessões (7 dias por padrão)
- Senhas armazenadas com algoritmo PBKDF2-SHA256
- Tokens temporários para links de verificação (1 hora)

### Scripts de Utilitário
- `setup_venv.bat`: Configuração automática do ambiente virtual
- `start_project.bat`: Inicialização do projeto e serviços necessários
- `init_sample_data.py`: Povoamento da base de dados com dados iniciais

## Otimizações Recentes

### Melhorias de Performance
- Otimização de consultas SQL com índices apropriados
- Utilização de lazy loading para relacionamentos SQLAlchemy
- Carregamento condicional de CSS e JavaScript por página
- Cache de contexto para categorias utilizadas globalmente

### Otimizações de Código
- Consolidação de arquivos CSS duplicados
- Remoção de arquivos de backup desnecessários
- Implementação de logging adequado em vez de prints de debug
- Validação de formulários padronizada

### Melhorias de UX
- Mensagens de feedback para ações do usuário
- Breadcrumbs para navegação intuitiva
- Persistência de carrinho entre sessões
- Validação de formulários em tempo real

## Escalabilidade

A arquitetura foi projetada considerando escalabilidade:

### Horizontal
- Separação clara entre camadas (models, views, controllers)
- Blueprints independentes que podem ser distribuídos
- Serviços desacoplados para lógica de negócios

### Vertical
- Otimização de consultas SQL com índices e joins adequados
- Lazy loading para carregar apenas os dados necessários
- Relacionamentos configurados para evitar N+1 queries

## Monitoramento e Manutenção

### Logging
- Sistema de logging incorporado para rastrear erros e eventos importantes
- Logs detalhados para operações críticas (pagamentos, emails, autenticação)

### Backups
- Estrutura de banco de dados disponível em `base-de-dados/db_noted.sql`
- Backup incremental com `V100_db_noted.sql`
- Amostras de dados para testes em `db_noted_conteudo-test.sql`

### Documentação
- `IMPLEMENTATION_SUMMARY.md`: Resumo da implementação do projeto
- `EMAIL_CUSTOMIZATION_GUIDE.md`: Guia para personalização de emails
- `EMAIL_SYSTEM_SUMMARY.md`: Detalhes do sistema de emails
- `JAVASCRIPT_NOTIFICATIONS_UPDATE.md`: Atualizações das notificações
- `TESTING_CHECKLIST.md`: Lista de verificação para testes

## Recursos Adicionais

### Requisitos de Sistema
- Python 3.8 ou superior
- MySQL 5.7 ou superior
- WAMP/XAMPP para ambiente de desenvolvimento local
- Navegador moderno com suporte a ES6

### Boas Práticas
- Código comentado seguindo convenções docstring do Python
- Estrutura de projeto seguindo padrões Flask recomendados
- Tratamento de exceções em operações críticas
- Separação clara de responsabilidades entre módulos

## Roadmap Futuro

### Funcionalidades Planejadas
- Editor de markdown avançado com formatação em tempo real
- Sistema colaborativo com edição simultânea
- Modo offline completo com sincronização inteligente
- Integração com mais plataformas (Trello, Asana, Todoist)
- Reconhecimento de escrita à mão (tablet/stylus)
- Captura e organização automática de pesquisas web
- Extensões para linguagens de programação e snippets
- Análise de produtividade e insights personalizados

### Melhorias Técnicas
- Migração para Flask 3.0
- Implementação de WebSockets para atualizações em tempo real
- Sistema de plugins com sandbox de segurança
- Otimização da sincronização em redes de baixa velocidade
- Implementação de criptografia end-to-end para notas privadas
- PWA (Progressive Web App) para experiência offline melhorada
- Framework para desenvolvimento de extensões de terceiros
- Otimizações de acessibilidade (WCAG 2.1)
- Suporte a Apple Pencil e dispositivos com stylus

## Resolução de Problemas

### Problemas Comuns
- **Erro de Sincronização**: Verificar conectividade e configurações de sincronização no perfil do usuário
- **Falha na Integração Externa**: Revisar permissões e tokens de acesso para serviços integrados
- **Problemas com a API de IA**: Verificar limites de uso diário e configurações de API no arquivo `.env`
- **Erro de Conexão à Base de Dados**: Verificar credenciais no `.env` e garantir que o serviço MySQL está em execução
- **Problemas de Renderização**: Verificar compatibilidade do navegador e plugins de extensão instalados
- **Sessões Não Persistentes**: Verificar configuração de SECRET_KEY e SESSION_TYPE

### Depuração
- Use o modo debug (`app.run(debug=True)`) para informações detalhadas de erros
- Verifique o log da aplicação para mensagens de erro
- Utilize os scripts de teste para validar componentes específicos

## Equipa e Contacto

Este projeto foi desenvolvido pela equipa noted;, uma marca dedicada à criação de produtos de papelaria de alta qualidade.

Para mais informações ou suporte:
- **Email**: suporte@noted-brand.com
- **Website**: https://www.noted-brand.com
- **Repositório**: https://github.com/noted-brand/ecommerce

---

## Conclusão

A noted; é uma plataforma inovadora de cadernos digitais que combina a simplicidade do minimalismo com o poder da sincronização na cloud, integrações com ferramentas populares e recursos de IA. Construída com tecnologias modernas e seguindo princípios de design centrado no utilizador, a plataforma oferece uma experiência fluida para organização pessoal e profissional.

O projeto demonstra a implementação de um sistema avançado para anotações digitais com Flask, abrangendo sincronização em tempo real, extensibilidade via plugins, integração com serviços externos populares, e recursos de IA para aumentar a produtividade e criatividade.

A arquitetura modular e extensível permite fácil manutenção e expansão, tornando este projeto uma base sólida para se tornar o hub central da vida digital organizada dos utilizadores. Nosso objetivo é proporcionar uma ferramenta que ajude as pessoas a organizar seus pensamentos, tarefas e projetos de forma eficiente e inspiradora.