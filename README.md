# Calopsitas Manager - Build Alfa v1.0

Sistema completo para gerenciamento de plantéis de calopsitas, incluindo controle de aves, mutações genéticas, cruzamentos e catálogo virtual.

## 🚀 Funcionalidades Implementadas

### ✅ Sistema de Usuários e Plantéis
- Cadastro e login de usuários
- Sistema "lembrar-me" funcional
- Criação automática de plantéis para novos usuários
- Controle de acesso por plantel

### ✅ Gestão de Aves
- Cadastro completo de aves com informações detalhadas
- Upload e gerenciamento de fotos
- Controle de disponibilidade e preços
- Histórico médico
- Árvore genealógica (pai/mãe)
- Status de venda (disponível, reservado, vendido)

### ✅ Sistema de Mutações Genéticas
- Cadastro de mutações com informações científicas
- Tipos de herança: ligada ao sexo (dominante/recessiva), autossômica (dominante/recessiva)
- Controle de mutações visíveis e portadoras
- Informações detalhadas: gene, símbolo, alelos, cor resultante

### ✅ Calculadora Genética
- Simulação de cruzamentos com probabilidades científicas
- Cálculos baseados na genética real das calopsitas (ZZ/ZW)
- Relatórios detalhados de probabilidades por sexo
- Suporte a múltiplas mutações simultâneas

### ✅ Gestão de Casais e Cruzamentos
- Formação de casais reprodutivos
- Controle de ninhadas e filhotes
- Histórico de cruzamentos realizados
- Estatísticas de reprodução

### ✅ Catálogo Virtual
- Sistema de requisições de compra
- Controle de disponibilidade
- Preços negociáveis
- Galeria de fotos das aves

### ✅ Dashboard e Relatórios
- Visão geral do plantel
- Estatísticas de aves por status e sexo
- Distribuição de mutações
- Histórico de requisições

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python Flask
- **Banco de Dados**: SQLite com SQLAlchemy ORM
- **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript
- **Autenticação**: Flask-Login
- **Upload de Arquivos**: Flask-Uploads
- **Validação**: WTForms

## 📋 Pré-requisitos

- Python 3.8+
- pip
- Git

## 🚀 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/nicolasdxnx11/calopsitas-maneger.git
cd calopsitas-maneger
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Inicialize o banco de dados**
```bash
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

6. **Execute o servidor**
```bash
python run.py
```

O sistema estará disponível em `http://localhost:5002`

## 📊 Estrutura do Banco de Dados

### Tabelas Principais
- **usuarios**: Usuários do sistema
- **plantels**: Plantéis de criação
- **aves**: Cadastro de aves
- **mutacoes**: Catálogo de mutações genéticas
- **casais**: Casais reprodutivos
- **ninhadas**: Controle de ninhadas
- **requisicoes**: Requisições de compra

### Relacionamentos
- Usuário → Plantel (1:1)
- Plantel → Aves (1:N)
- Ave → Mutações (N:N)
- Ave → Mutações Portadoras (N:N)
- Casal → Aves (1:2)
- Casal → Ninhadas (1:N)

## 🧬 Sistema Genético

### Tipos de Herança Suportados
1. **Ligada ao Sexo Dominante** (ex: Pérola)
   - Machos: ZZ, ZpZ, ZpZp
   - Fêmeas: ZW, ZpW

2. **Ligada ao Sexo Recessiva** (ex: Lutino)
   - Machos: ZZ, Z+Zl, ZlZl
   - Fêmeas: ZW, ZlW

3. **Autossômica Dominante** (ex: Arlequim)
   - Genótipos: AA, Aa, aa

4. **Autossômica Recessiva** (ex: Cara Branca)
   - Genótipos: AA, Aa, aa

### Cálculos de Probabilidade
- Baseados na genética real das calopsitas
- Consideração de portadores
- Probabilidades separadas por sexo
- Múltiplas mutações simultâneas

## 🔧 Configuração

### Variáveis de Ambiente
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui
DATABASE_URL=sqlite:///app.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Configurações de Upload
- Formatos aceitos: JPG, PNG, GIF
- Tamanho máximo: 16MB
- Pasta de destino: `uploads/`

## 📱 Interface do Usuário

### Design Responsivo
- Bootstrap 5 para layout responsivo
- Ícones FontAwesome
- Interface intuitiva e moderna
- Navegação por abas

### Funcionalidades da Interface
- Dashboard com estatísticas
- Formulários de cadastro intuitivos
- Galeria de fotos
- Tabelas com ordenação e filtros
- Modais para ações rápidas

## 🔒 Segurança

- Autenticação de usuários
- Controle de acesso por plantel
- Validação de formulários
- Proteção contra CSRF
- Sanitização de dados

## 📈 Próximas Versões

### Beta v1.1 (Planejado)
- [ ] Melhorias na calculadora genética
- [ ] Sistema de notificações
- [ ] Exportação de relatórios
- [ ] Backup automático do banco

### Beta v1.2 (Planejado)
- [ ] API REST para integração
- [ ] Sistema de backup na nuvem
- [ ] Relatórios avançados
- [ ] Integração com redes sociais

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Desenvolvedor

**Nicolas DXNX11**
- GitHub: [@nicolasdxnx11](https://github.com/nicolasdxnx11)

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Entre em contato via email

---

**Build Alfa v1.0** - Sistema funcional com todas as funcionalidades principais implementadas e testadas.
