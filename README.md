# Backend Developer Technical Assessment

This repository contains complete implementations for all three tasks in the backend developer technical assessment.

## Project Structure

```
├── django_project/          # Task 1: Real-Time Content & Event Platform
│   ├── content_platform/    # Django project settings
│   ├── posts/              # Posts app with WebSocket support
│   └── collections/        # Collections app with CRUD operations
├── auth_service/           # Task 2: Authentication Microservice
│   ├── main.py            # FastAPI application
│   ├── models.py          # Pydantic models
│   ├── database.py        # SQLAlchemy database configuration
│   └── auth_utils.py      # Authentication utilities
├── data_pipeline/         # Task 3: Event-Driven Data Pipeline
│   ├── README.md          # Architecture documentation
│   └── architecture_diagram.py  # Diagram generator
└── requirements.txt       # Python dependencies
```

## Task 1: Real-Time Content & Event Platform (Django)

### Features Implemented
- ✅ **Post Model**: Complete CRUD operations for Posts with title and body fields
- ✅ **Collection Model**: Create, list, update, and delete Collections with name and owner
- ✅ **Post Management**: Add/remove Posts to/from Collections
- ✅ **REST API**: Full HTTP API for all operations
- ✅ **Real-time Notifications**: WebSocket support for live updates
- ✅ **Authentication**: User-based ownership and permissions

### API Endpoints

#### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{id}/` - Get a specific post
- `PUT /api/posts/{id}/` - Update a post
- `DELETE /api/posts/{id}/` - Delete a post

#### Collections
- `GET /api/collections/` - List user's collections
- `POST /api/collections/` - Create a new collection
- `GET /api/collections/{id}/` - Get a specific collection
- `PUT /api/collections/{id}/` - Update a collection
- `DELETE /api/collections/{id}/` - Delete a collection
- `POST /api/collections/{id}/add_post/` - Add post to collection
- `POST /api/collections/{id}/remove_post/` - Remove post from collection

#### WebSocket
- `ws://localhost:8000/ws/notifications/` - Real-time notifications

### Setup Instructions

```bash
# Navigate to Django project
cd django_project

# Install dependencies
pip install -r ../requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

### WebSocket Testing

Connect to the WebSocket endpoint to receive real-time notifications:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/notifications/');
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

## Task 2: Authentication Microservice (FastAPI)

### Features Implemented
- ✅ **Email/Password Authentication**: Signup and login functionality
- ✅ **Google OAuth2 Integration**: Complete OAuth2 flow
- ✅ **JWT + JWE Tokens**: Secure session management
- ✅ **Protected Endpoints**: Token-based access control
- ✅ **Extensible Design**: Ready for additional social providers
- ✅ **Database Integration**: SQLAlchemy with SQLite/PostgreSQL support

### API Endpoints

#### Authentication
- `POST /auth/signup` - Register with email and password
- `POST /auth/login` - Login with email and password
- `GET /auth/google` - Initiate Google OAuth2 login
- `GET /auth/google/callback` - Handle Google OAuth2 callback

#### Protected Endpoints
- `GET /auth/me` - Get current user information
- `GET /auth/verify` - Verify access token

### Setup Instructions

```bash
# Navigate to auth service
cd auth_service

# Install dependencies
pip install -r ../requirements.txt

# Set up environment variables
cp env_example.txt .env
# Edit .env with your actual values

# Run the service
python main.py
```

### Environment Variables

Create a `.env` file with the following variables:

```env
# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-here
JWE_SECRET_KEY=your-super-secret-jwe-key-here

# Google OAuth2 Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# Database Configuration
DATABASE_URL=sqlite:///./auth_service.db
```

### Usage Examples

#### Email/Password Signup
```bash
curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123", "full_name": "John Doe"}'
```

#### Email/Password Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'
```

#### Access Protected Endpoint
```bash
curl -X GET "http://localhost:8000/auth/me" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Task 3: Complex Event-Driven Data Pipeline

### Architecture Overview

The data pipeline is designed to handle high-volume events with the following components:

#### 1. Event Ingestion Layer
- **Apache Kafka**: High-throughput message broker
- **Kafka Connect**: Data ingestion from various sources
- **Load Balancer**: Distribute incoming events
- **Rate Limiting**: Prevent system overload

#### 2. Lightweight Processing Layer
- **Kafka Streams**: Real-time stream processing
- **Redis**: In-memory caching and enrichment
- **Event Validation**: Schema validation and data quality
- **Deduplication**: Remove duplicate events

#### 3. Heavy Processing Layer
- **Apache Spark**: Distributed data processing
- **Celery**: Asynchronous task processing
- **Worker Pools**: Parallel processing capabilities
- **Dead Letter Queue**: Failed event handling

#### 4. Data Storage Layer
- **Data Lake**: Raw event storage (S3/HDFS)
- **Data Warehouse**: Processed data storage
- **Analytics Database**: Query-optimized storage
- **Metadata Store**: Data lineage tracking

#### 5. Monitoring & Observability
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and alerting
- **Jaeger**: Distributed tracing
- **ELK Stack**: Log aggregation

### Key Features

#### Scalability
- Horizontal scaling for all components
- Auto-scaling based on queue depth
- Event partitioning for parallel processing

#### Fault Tolerance
- Kafka topic replication
- Exponential backoff retry logic
- Circuit breakers for failure isolation
- Regular data backups

#### Performance Optimization
- Efficient batch loading
- Redis caching for fast lookups
- Optimized database indexing
- Data compression

#### Monitoring & Alerting
- Throughput metrics (events/second)
- Latency tracking (end-to-end)
- Error rate monitoring
- Resource utilization tracking

### Data Flow

```
Event Sources → API Gateway → Kafka → Kafka Streams → Spark → Data Warehouse
     ↓              ↓           ↓          ↓           ↓           ↓
Rate Limiting   Validation  Deduplication  Enrichment  Transform  Batch Load
     ↓              ↓           ↓          ↓           ↓           ↓
Load Balancer   Schema Check  Caching    Real-time   Heavy       Analytics
                              Redis      Processing  Processing   Storage
```

### Event Schema

```json
{
  "event_id": "uuid",
  "event_type": "user_action",
  "timestamp": "2024-01-01T00:00:00Z",
  "user_id": "user123",
  "data": {
    "action": "click",
    "page": "/home",
    "session_id": "session456"
  },
  "metadata": {
    "source": "web",
    "version": "1.0"
  }
}
```

### Deployment Options

#### Docker Compose
```yaml
version: '3.8'
services:
  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
    ports:
      - "9092:9092"
  
  spark-master:
    image: bitnami/spark:latest
    environment:
      SPARK_MODE: master
    ports:
      - "8080:8080"
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

#### Kubernetes
- Helm charts for easy deployment
- ConfigMaps for environment configuration
- Secrets for secure credential storage
- Ingress for load balancing

### Testing Strategy

#### Unit Tests
- Individual component testing
- Mock external dependencies
- Data quality validation

#### Integration Tests
- End-to-end pipeline testing
- Performance benchmarking
- Failure scenario testing

#### Load Testing
- High-volume event simulation
- Stress testing under peak load
- Performance degradation analysis

## Security Considerations

### Data Protection
- Encryption in transit and at rest
- Role-based access control
- Comprehensive audit logging
- Data masking in logs

### Infrastructure Security
- Network security (VPC, firewalls)
- Multi-factor authentication
- Secure secrets management
- Compliance with regulations

## Cost Optimization

### Resource Management
- Auto-scaling during low usage
- Spot instances for non-critical workloads
- Data lifecycle management
- Storage compression

### Monitoring Costs
- Resource usage tracking
- Optimization alerts
- Cost allocation by team
- Budget limits and alerts

## Getting Started

### Prerequisites
- Python 3.8+
- Docker (for data pipeline components)
- Redis (for caching)
- PostgreSQL (optional, for production)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd assessment

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp auth_service/env_example.txt auth_service/.env
# Edit auth_service/.env with your values

# Run Django migrations
cd django_project
python manage.py makemigrations
python manage.py migrate

# Start services
python manage.py runserver  # Django (Task 1)
cd ../auth_service
python main.py              # FastAPI (Task 2)
```

### Testing

```bash
# Run Django tests
cd django_project
python manage.py test

# Run FastAPI tests
cd ../auth_service
pytest

# Generate architecture diagrams
cd ../data_pipeline
python architecture_diagram.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please create an issue in the repository or contact the development team. # Django-Assesment
