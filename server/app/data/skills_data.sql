INSERT INTO skill_categories (category, skills) VALUES
('Languages & Scripting', ARRAY[
  'python', 'javascript', 'typescript', 'sql', 'html', 'css', 'c++', 'go', 'java', 'graphql',
  'bash', 'powershell', 'xml', 'json', 'yaml', 'shell scripting', 'markdown', 'latex',
  'coffeescript', 'perl', 'r', 'swift', 'kotlin', 'objective-c', 'scala', 'assembly', 'vb.net', 'matlab'
]),
('Frontend Frameworks & Libraries', ARRAY[
  'react', 'react native', 'flutter', 'next.js', 'vue.js', 'angular', 'svelte', 'redux', 'vite', 'webpack',
  'storybook', 'material-ui', 'chakra-ui', 'bootstrap', 'jquery', 'd3.js', 'preact', 'lit', 'tailwind', 'stencil.js', 'alpine.js'
]),
('Mobile Development', ARRAY[
  'android', 'ios', 'xamarin', 'cordova', 'expo', 'jetpack', 'android studio', 'xcode', 'bloc pattern', 'dart', 'material design', 'mvvm'
]),
('Backend & API', ARRAY[
  'node.js', 'express.js', 'nestjs', 'adonisjs', 'hapi.js', 'flask', 'django', 'fastapi', 'rest', 'soap', 'grpc',
  'ruby on rails', 'laravel', 'symfony', 'sinatra', 'phoenix framework', 'blazor', 'grails', 'spring boot', 'dotnet core',
  'microservices', 'soa', 'rest apis'
]),
('Databases & Storage', ARRAY[
  'postgresql', 'mysql', 'mongodb', 'oracle', 'redis', 'sqlite', 'cassandra', 'elasticsearch', 'supabase',
  'firebase', 'dynamodb', 'neo4j', 'snowflake', 'bigquery', 'couchdb', 'influxdb', 'arangodb', 'clickhouse', 'duckdb'
]),
('ORMs & Data Layers', ARRAY[
  'mongoose', 'prisma', 'sequelize', 'typeorm', 'active record', 'sqlalchemy', 'entity framework'
]),
('Cloud & Infrastructure', ARRAY[
  'aws', 'azure', 'gcp', 'firebase hosting', 'heroku', 'netlify', 'vercel', 'digitalocean', 'linode',
  'cloudflare', 'fly.io', 'render', 'lightsail', 'elastic beanstalk', 'cloudformation', 'kustomize',
  'terraform', 'ansible', 'vault', 'pulumi', 'helm', 'kubernetes', 'argocd', 'docker', 'docker-compose'
]),
('DevOps & CI/CD', ARRAY[
  'jenkins', 'circleci', 'gitlab-ci', 'travis-ci', 'buildkite', 'codeship', 'bazel', 'spinnaker',
  'ci/cd', 'version control', 'github actions', 'npm', 'pnpm', 'yarn', 'monorepo'
]),
('Security & Identity', ARRAY[
  'oauth2', 'saml', 'jwt', 'rsa', 'mfa', 'sso', 'okta', 'auth0', 'hashicorp', 'fortinet', 'check point',
  'crowdsec', 'openvpn', 'pfsense', 'zero trust', 'zscaler', 'crowdstrike', 'siem', 'burp suite',
  'nmap', 'wireshark', 'shodan', 'fail2ban', 'pki', 'authn', 'authz', 'rbac', 'abac', 'federated login', 'oidc', 'passkeys'
]),
('Testing & QA', ARRAY[
  'jest', 'mocha', 'chai', 'pytest', 'selenium', 'cypress', 'junit', 'testng',
  'postman', 'newman', 'playwright', 'testing-library', 'robot framework', 'tox', 'mockito',
  'unit testing', 'tdd', 'bdd', 'cucumber', 'gherkin', 'karma', 'ava', 'testcafe',
  'browserstack', 'sauce labs', 'pact', 'contract testing'
]),
('Data Science & AI', ARRAY[
  'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'matplotlib', 'seaborn',
  'huggingface', 'langchain', 'openai', 'llamaindex', 'llms', 'spacy', 'nltk', 'prophet', 'polars',
  'weaviate', 'pgvector', 'ray', 'mlflow', 'llmops', 'vectordb', 'pinecone', 'embeddings', 'chatgpt',
  'anthropic', 'gemini', 'langchain.js', 'llama2'
]),
('Project & Tools', ARRAY[
  'jira', 'confluence', 'notion', 'miro', 'obsidian', 'slack', 'figma', 'lucidchart', 'draw.io',
  'asciidoc', 'clickup', 'ms project', 'vscode', 'intellij', 'eclipse', 'netbeans'
]),
('Operating Systems', ARRAY[
  'linux', 'ubuntu', 'centos', 'alpine linux', 'pop!_os', 'raspbian', 'macos', 'windows server'
]),
('Dev Practices & Concepts', ARRAY[
  'agile', 'scrum', 'scrum master', 'devops', 'pair programming', 'design patterns',
  'object-oriented programming', 'domain-driven design', 'clean architecture', 'event sourcing',
  'serverless', 'edge computing', 'technical documentation', 'shift left', 'infrastructure scanning',
  'openapi', 'swagger', 'graphql federation', 'json:api', 'cors'
]),
('Certifications & Frameworks', ARRAY[
  'comptia a+', 'comptia network+', 'comptia security+', 'comptia linux+', 'comptia cloud+',
  'aws certified cloud practitioner', 'aws certified developer – associate',
  'aws certified solutions architect – associate', 'microsoft azure fundamentals',
  'google cloud digital leader', 'certified kubernetes administrator (cka)',
  'certified scrummaster (csm)', 'pmp', 'itil'
]),
('Soft Skills', ARRAY[
  'problem solving', 'critical thinking', 'communication', 'teamwork', 'adaptability', 'creativity', 'empathy',
  'resilience', 'leadership', 'collaboration', 'initiative', 'accountability', 'emotional intelligence',
  'attention to detail', 'time management', 'decision making', 'negotiation', 'conflict resolution',
  'persuasion', 'self-motivation', 'active listening', 'work ethic', 'positive attitude',
  'customer service', 'reliability', 'flexibility', 'organization', 'multitasking', 'interpersonal skills',
  'cultural awareness', 'curiosity', 'learning agility', 'stress management', 'presentation skills',
  'facilitation', 'mentorship', 'patience', 'openness to feedback', 'growth mindset',
  'collaborative mindset', 'emotional regulation', 'strategic thinking', 'vision', 'coachability',
  'professionalism', 'sense of humor', 'trustworthiness', 'adaptable communication', 'perspective-taking',
  'innovation', 'cross-functional communication', 'initiative taking', 'influence', 'self-reflection',
  'goal setting', 'delegation', 'empowerment', 'meeting deadlines', 'helpfulness', 'respect',
  'inclusivity', 'diplomacy', 'transparency', 'assertiveness', 'decision ownership', 'self-awareness',
  'confidentiality', 'supportiveness', 'analytical thinking', 'proactivity', 'honesty', 'self-discipline',
  'humility', 'consensus-building', 'resolving ambiguity'
]);