## Estrutura do Projeto

```text
noted/
├── requirements.txt   # Dependências do projeto
├── database/          # Esquema e dados de teste MySQL
├── docs/              # Documentação e notas
├── notebooks/         # Análises Jupyter
├── scripts/           # Scripts de configuração e arranque
└── noted/             # Pacote da aplicação Flask
    ├── __init__.py
    ├── app.py
    ├── config.py
    ├── models.py
    ├── routes/
    ├── services/
    ├── static/
    └── templates/
```

## Ideia do Produto 

A noted; é uma plataforma de cadernos digitais open source que oferece sincronização online, extensões para múltiplas ferramentas de produtividade e recursos criativos para o utilizador. Desenvolvemos este projeto com foco em:

- Ajudar a organizar qualquer tarefa, pequena ou grande
- Oferecer uma interface fácil de utilizar e minimalista
- Fornecer apenas o necessário, com extensões opcionais
- Focar na produtividade e no trabalho organizado

## Funcionalidades Principais do Software do Produto

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
   ```

3. Configurar o ficheiro .env:
   ```
   SECRET_KEY=chave_secreta
   DATABASE_URI=mysql+pymysql://username:password@localhost/db_noted
   MAIL_SERVER=smtp.exemplo.com
   MAIL_PORT=587
   MAIL_USERNAME=seu_email@exemplo.com
   MAIL_PASSWORD=sua_senha
   MAIL_USE_TLS=True
   MAIL_USE_SSL=False
   ```

4. Inicializar a base de dados:
   ```
   Execute `database/db_noted.sql` in MySQL Workbench and then `database/test-content.sql` for sample data.
   ```

5. Executar a aplicação:
   
   Usando o script incluído (também inicia o WAMP):
   ```
   scripts\start_project.bat
   ```
   
   Ou manualmente:
   ```
   python -m noted.app
   ```
   
   Ou usando Flask CLI:
   ```
   set FLASK_APP=noted.app
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

### Fluxos de Utilizador 

#### Fluxo de Criação de Conteúdo no Software
1. Login no sistema
2. Criação de novo caderno ou acesso a existente
3. Edição de conteúdo no editor principal
4. Utilização de ferramentas de IA e criatividade
5. Sincronização automática com a cloud
6. Compartilhamento ou exportação (opcional)

#### Fluxo de Integração no Software
1. Acesso à seção de integrações
2. Seleção e autorização de serviços externos (Notion, Obsidian, etc.)
3. Configuração de sincronização e regras
4. Importação/exportação de dados

#### Fluxo de Autenticação no Website
1. Registo de nova conta
2. Verificação por email
3. Login
4. Recuperação de senha (se necessário)

#### Fluxo de Administração no Website
1. Login como administrador
2. Acesso ao painel de administração
3. Gestão de usuários e permissões
4. Monitoramento de uso do sistema
5. Visualização de métricas e analytics
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
- `scripts\setup_venv.bat`: Configuração automática do ambiente virtual
- `scripts\start_project.bat`: Inicialização do projeto e serviços necessários
  
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

---

## Conclusão

A noted; é um website inovador de cadernos digitais. Construído com tecnologias modernas e seguindo princípios de design centrado no utilizador.

A arquitetura modular e extensível permite fácil manutenção e expansão do website, tornando este projeto uma base sólida para se tornar um verdadeiro produto de venda para qualquer empresa.
