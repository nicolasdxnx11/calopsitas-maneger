# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0-alpha] - 2025-06-28

### Adicionado
- Sistema completo de gerenciamento de plantéis de calopsitas
- Cadastro e autenticação de usuários com sistema "lembrar-me"
- Gestão completa de aves com upload de fotos
- Sistema de mutações genéticas com informações científicas
- Calculadora genética para simulação de cruzamentos
- Gestão de casais reprodutivos e ninhadas
- Catálogo virtual com sistema de requisições
- Dashboard com estatísticas e relatórios
- Interface responsiva com Bootstrap 5
- Banco de dados SQLite com SQLAlchemy ORM
- Sistema de controle de acesso por plantel

### Funcionalidades Principais
- **Sistema de Usuários**: Login, cadastro, controle de sessão
- **Gestão de Aves**: CRUD completo com fotos e histórico médico
- **Mutações Genéticas**: Catálogo com tipos de herança e informações detalhadas
- **Calculadora Genética**: Simulação científica de cruzamentos
- **Casais e Cruzamentos**: Formação de casais e controle de ninhadas
- **Catálogo Virtual**: Sistema de vendas com requisições
- **Dashboard**: Estatísticas e visão geral do plantel

### Tecnologias Implementadas
- Backend: Python Flask
- Frontend: HTML5, CSS3, JavaScript, Bootstrap 5
- Banco: SQLite com SQLAlchemy
- Autenticação: Flask-Login
- Upload: Flask-Uploads
- Validação: WTForms

### Estrutura do Projeto
```
calopsitas-manager/
├── app/
│   ├── models/          # Modelos do banco de dados
│   ├── routes/          # Rotas da aplicação
│   ├── templates/       # Templates HTML
│   ├── static/          # Arquivos estáticos
│   ├── forms/           # Formulários
│   └── genetica.py      # Módulo de cálculos genéticos
├── uploads/             # Pasta de uploads
├── instance/            # Configurações locais
├── requirements.txt     # Dependências
└── run.py              # Arquivo de execução
```

### Banco de Dados
- **usuarios**: Usuários do sistema
- **plantels**: Plantéis de criação
- **aves**: Cadastro de aves
- **mutacoes**: Catálogo de mutações
- **casais**: Casais reprodutivos
- **ninhadas**: Controle de ninhadas
- **requisicoes**: Requisições de compra
- Tabelas de relacionamento: ave_mutacao, ave_mutacao_portadora

### Sistema Genético
- Suporte a 4 tipos de herança:
  - Ligada ao sexo dominante (ex: Pérola)
  - Ligada ao sexo recessiva (ex: Lutino)
  - Autossômica dominante (ex: Arlequim)
  - Autossômica recessiva (ex: Cara Branca)
- Cálculos baseados na genética real das calopsitas (ZZ/ZW)
- Consideração de portadores e genótipos
- Probabilidades separadas por sexo

### Interface do Usuário
- Design responsivo com Bootstrap 5
- Navegação intuitiva por abas
- Formulários com validação
- Galeria de fotos
- Tabelas com ordenação
- Modais para ações rápidas

### Segurança
- Autenticação de usuários
- Controle de acesso por plantel
- Validação de formulários
- Sanitização de dados
- Proteção contra CSRF

### Configuração
- Variáveis de ambiente configuráveis
- Upload de arquivos com limite de tamanho
- Configuração de banco de dados
- Pasta de uploads configurável

## [0.9.0-beta] - 2025-06-27

### Adicionado
- Estrutura inicial do projeto
- Sistema básico de autenticação
- Modelos iniciais do banco de dados
- Interface básica

### Corrigido
- Problemas de configuração inicial
- Erros de importação
- Configuração do ambiente virtual

## [0.8.0-alpha] - 2025-06-26

### Adicionado
- Conceito inicial do projeto
- Estrutura de pastas
- Configuração básica do Flask

---

## Notas de Versão

### Build Alfa v1.0
Esta é a primeira versão funcional completa do sistema Calopsitas Manager. Todas as funcionalidades principais foram implementadas e testadas. O sistema está pronto para uso em ambiente de desenvolvimento.

### Próximas Versões Planejadas
- **Beta v1.1**: Melhorias na calculadora genética e sistema de notificações
- **Beta v1.2**: API REST e backup na nuvem
- **Release v1.0**: Versão estável para produção

### Compatibilidade
- Python 3.8+
- Navegadores modernos (Chrome, Firefox, Safari, Edge)
- Sistemas: Windows, Linux, macOS

### Limitações Conhecidas
- Calculadora genética pode precisar de ajustes finos
- Sistema de backup manual
- Sem integração com APIs externas
- Interface pode ser melhorada em dispositivos móveis 