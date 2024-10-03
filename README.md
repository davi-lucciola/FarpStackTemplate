# Farp Stack Template

## English

FastAPI + ReactJS + PostgreSQL (Farp Stack), template with authentication and authorization using Role-Based Access Control (RBAC) and Google authentication included.

### How It Works

#### About React
- The ReactJS frontend is served by the FastAPI backend through the function `api.routes.init_routes`. You just need to build the React app and configure the environment variable `REACT_BUILD_DIR` (by default, it watches the "dist" directory).

#### About Google Authentication
- To enable Google authentication, you need to access the [Google Credentials Console](https://console.cloud.google.com/apis/credentials) (create an organization if you do not have one) and create a new "OAuth 2.0 Client ID" to get the information needed to fill the environment variables: `GOOGLE_CLIENT_ID`, `GOOGLE_REDIRECT_URI`, `GOOGLE_CLIENT_SECRET`.

- Register the allowed redirect URI in the Google console, matching the one in the environment variable.

#### About Project Structure
- For each new feature, you will create a new module in the `api` root, following the MVC+Service architecture. The "view" acts as the controller, the service contains business rules, the model defines the PostgreSQL table and handle with data access (powered by [SQLAlchemy](https://www.sqlalchemy.org/)).

- Each module contains a `dto` folder to store the Pydantic models or TypedDict models.

#### About the Guards
- The `auth` module contains two guards: `AuthGuard` and `OwnerGuard`.
- The `AuthGuard` adds authentication to the route where you use it. You can assign roles to it to add authorization using `api.Roles`, which is an enum (it can be a single role or a list of roles).

- The `OwnerGuard` has the same behavior as `AuthGuard`, but you can provide a Model to allow users who have the role or are the owner of the resource to access the endpoint. The `resourceId` is verified by the default `id` path parameter when you add the owner guard. You also need to implement a class method `can_update` (implementing the `IBaseModel` interface from `api.models`) in the table model before using it with the `OwnerGuard`.

<hr>

## Português Brasil

FastAPI + ReactJS + PostgreSQL (Farp Stack), com autenticação e autorização utilizando Controle de Acesso Baseado em Papéis (RBAC) e autenticação do Google incluída.

## Como Funciona

### Sobre o React
- O frontend em ReactJS é servido pelo backend em FastAPI através da função `api.routes.init_routes`. Você só precisa compilar o app React e configurar a variável de ambiente `REACT_BUILD_DIR` (por padrão, ele observa o diretório "dist").

### Sobre a Autenticação do Google
- Para habilitar a autenticação do Google, você precisa acessar o [Google Credentials Console](https://console.cloud.google.com/apis/credentials) (crie uma organização se você não tiver uma) e criar um novo "OAuth 2.0 Client ID" para obter as informações necessárias para preencher as variáveis de ambiente: `GOOGLE_CLIENT_ID`, `GOOGLE_REDIRECT_URI`, `GOOGLE_CLIENT_SECRET`.

- Registre o URI de redirecionamento permitido no console do Google, correspondente ao que está na variável de ambiente.

### Sobre a Estrutura do Projeto
- Para cada nova funcionalidade, você criará um novo módulo na raiz do `api`, seguindo a arquitetura MVC+Service. A "view" atua como o controller, o service contém as regras de negócio, o model define o schema do documento MongoDB e lida com o acesso ao banco de dados (utilizando [SQLAlchemy](https://www.sqlalchemy.org/)).

- Cada módulo contém uma pasta `dto` para armazenar os models Pydantic ou TypedDict.

### Sobre os Guards
- O módulo `auth` contém dois guards: `AuthGuard` e `OwnerGuard`.
- O `AuthGuard` adiciona autenticação à rota onde é utilizado. Você pode atribuir roles a ele para adicionar autorização utilizando `api.Roles`, que é um enum (pode ser um único role ou uma lista de roles).

- O `OwnerGuard` tem o mesmo comportamento do `AuthGuard`, mas você pode fornecer um Model para permitir que usuários com o role ou o proprietário do recurso acessem o endpoint. O `resourceId` é verificado pelo parâmetro de caminho padrão `id` quando você adiciona o permission guard. Você também precisa implementar um método de classe `can_update` (implementando a interface `IBaseModel` de `api.models`) no model do documento antes de utilizá-lo com o `OwnerGuard`.
