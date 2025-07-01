ai-microservices-project/
│
├── src/                                # 💡 Tất cả các microservices chính
│   ├── backend/                        # Django: quản trị, auth, user
│   │   ├── project_admin/              # settings, urls, asgi
│   │   ├── users/                      # user models/views
│   │   ├── auth/                       # JWT Auth
│   │   ├── api/                        # DRF API views/serializers
│   │   ├── database/                   # Migrations, models
│   │   ├── manage.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│
│   ├── ml/                             # FastAPI + GraphQL + LangChain
│   │   ├── app/
│   │   │   ├── main.py                 # FastAPI + Strawberry GraphQL
│   │   │   ├── graphql/
│   │   │   │   ├── schema.py
│   │   │   │   ├── resolvers/
│   │   │   │   │   ├── vector_query.py
│   │   │   │   │   ├── graph_query.py
│   │   │   │   │   └── hybrid_chain.py
│   │   │   │   └── context.py
│   │   │   ├── langfuse_tracking/
│   │   │   ├── langsmith_traces/
│   │   │   ├── vectorstore/           # Qdrant connectors
│   │   │   ├── graphstore/            # Neo4j connectors
│   │   │   ├── chains/                # LangChain RAG pipelines
│   │   │   ├── config/
│   │   │   ├── models/
│   │   ├── configs/
│   │   ├── tests/
│   │   │   ├── db/
│   │   │   ├── sample/
│   │   │   ├── tools/
│   │   ├── utils/
│   │   │   ├── WDMParser/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│
│   ├── frontend/                      # Next.js web app
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/                  # Gọi API backend / ml
│   │   ├── public/
│   │   ├── styles/
│   │   ├── next.config.js
│   │   └── Dockerfile
│
├── shared/                            # 📦 Mã dùng chung giữa các service
│   ├── auth_utils/
│   ├── constants/
│   └── db_helpers/
│
├── scripts/                           # 🛠️ Công cụ, CLI, deploy
│   ├── deploy/
│   │   ├── terraform/                 # GCP infra
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── gcp_cloudbuild/
│   │   │   └── cloudbuild.yaml
│   │   └── deploy_to_gcp.sh
│   │
│   ├── db/
│   │   ├── init_postgres.sql
│   │   ├── init_neo4j.cypher
│   │   └── migrate_embeddings.py
│   │
│   ├── tools/
│   │   ├── embedding_generator.py
│   │   └── langfuse_analysis.py
│
├── configs/                           # ⚙️ Env, Docker, API Gateway config
│   ├── .env.backend
│   ├── .env.ml
│   ├── .env.frontend
│   ├── docker-compose.dev.yaml
│   ├── docker-compose.prod.yaml
│   ├── api_gateway.yaml
│   └── logging.yaml
│
├── notebooks/                         # 📓 Jupyter cho thử nghiệm ML, RAG
│   ├── exploration/
│   └── evaluation/
│
├── tests/                             # 🧪 Kiểm thử
│   ├── backend/
│   ├── ml/
│   └── shared/
│
├── docs/                              # 📘 Kiến trúc, API, triển khai
│   ├── architecture.md
│   ├── api_reference.md
│   ├── chain_designs.md
│   ├── db_schema.png
│   └── deployment_guide.md
│
├── docker-compose.yml
├── pyproject.toml / requirements.txt
├── .gitignore
└── README.md
