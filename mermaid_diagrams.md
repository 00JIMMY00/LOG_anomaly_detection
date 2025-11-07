# Log Anomaly Detection API - System Diagrams

## 1. Use Case Diagram

```mermaid
graph TB
    subgraph "Log Anomaly Detection System"
        UC1[Analyze Log Message]
        UC2[Check API Health]
        UC3[View API Documentation]
        UC4[Download Model]
        UC5[Configure Threshold]
    end
    
    User((User/Client))
    Admin((System Admin))
    HuggingFace[(Hugging Face<br/>Model Hub)]
    
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC5
    Admin --> UC4
    UC4 --> HuggingFace
    
    UC1 -.includes.-> UC5
```

---

## 2. Sequence Diagram - Log Analysis Flow

```mermaid
sequenceDiagram
    participant Client
    participant Router as log_router.py
    participant Controller as LogController
    participant Service as ModelService
    participant Model as DeBERTa Model
    
    Client->>+Router: POST /api/v1/analyze
    Note over Client,Router: {log_message, threshold}
    
    Router->>+Controller: analyze_log(request)
    
    Controller->>+Service: inference(log_message, threshold)
    
    Service->>Service: Check if model loaded
    
    alt Model Not Loaded
        Service-->>Controller: RuntimeError
        Controller-->>Router: Exception
        Router-->>Client: 503 Service Unavailable
    else Model Loaded
        Service->>+Model: Zero-shot classification
        Model-->>-Service: {labels, scores}
        
        Service->>Service: Apply threshold logic
        Service->>Service: Determine final label
        
        Service-->>-Controller: {label, confidence, is_anomaly}
        
        Controller->>Controller: Create LogResponse
        Controller-->>-Router: LogResponse
        
        Router-->>-Client: 200 OK + JSON Response
        Note over Client,Router: {label, confidence, is_anomaly}
    end
```

---

## 3. Sequence Diagram - Application Startup

```mermaid
sequenceDiagram
    participant Main as main.py
    participant Service as ModelService
    participant FS as File System
    participant HF as Hugging Face
    
    Main->>Main: Initialize FastAPI app
    Main->>Main: Configure CORS
    Main->>Main: Include routers
    
    Main->>+Service: startup_event()
    Service->>Service: Get singleton instance
    
    Service->>+FS: Check if model exists
    
    alt Model Exists Locally
        FS-->>-Service: Model found
        Service->>Service: Load from local path
        Service-->>Main: Model loaded successfully
    else Model Not Found
        FS-->>Service: Model not found
        Service-->>Main: Warning: Model not loaded
        Note over Main: Server starts but<br/>endpoints return 503
    end
    
    Main->>Main: Start uvicorn server
```

---

## 4. Data Flow Diagram (DFD) - Level 0 (Context Diagram)

```mermaid
graph LR
    User((User))
    Admin((Admin))
    
    System[Log Anomaly<br/>Detection API]
    
    ModelHub[(Hugging Face<br/>Model Hub)]
    LocalStorage[(Local Model<br/>Storage)]
    
    User -->|Log Messages| System
    System -->|Classification Results| User
    
    Admin -->|Download Command| System
    System -->|Model Request| ModelHub
    ModelHub -->|Model Files| System
    System -->|Save Model| LocalStorage
    LocalStorage -->|Load Model| System
```

---

## 5. Data Flow Diagram (DFD) - Level 1

```mermaid
graph TB
    subgraph "External Entities"
        User((User))
        Admin((Admin))
        HF[(Hugging Face)]
        Storage[(Local Storage)]
    end
    
    subgraph "Log Anomaly Detection System"
        P1[1.0<br/>Receive Request]
        P2[2.0<br/>Validate Input]
        P3[3.0<br/>Load Model]
        P4[4.0<br/>Classify Log]
        P5[5.0<br/>Apply Threshold]
        P6[6.0<br/>Format Response]
        P7[7.0<br/>Download Model]
        
        D1[(Model Cache)]
        D2[(Configuration)]
    end
    
    User -->|Log Message + Threshold| P1
    P1 -->|Request Data| P2
    P2 -->|Validated Data| P4
    
    Admin -->|Download Command| P7
    P7 -->|Fetch Model| HF
    HF -->|Model Files| P7
    P7 -->|Store Model| Storage
    
    Storage -->|Model Files| P3
    P3 -->|Loaded Model| D1
    D1 -->|Model Instance| P4
    
    D2 -->|Default Threshold| P2
    D2 -->|Labels Config| P4
    
    P4 -->|Classification Scores| P5
    P5 -->|Final Label| P6
    P6 -->|JSON Response| User
```

---

## 6. Component Diagram

```mermaid
graph TB
    subgraph "FastAPI Application"
        Main[main.py<br/>FastAPI App]
        Config[config.py<br/>Configuration]
        
        subgraph "Routers Layer"
            Router[log_router.py<br/>API Endpoints]
        end
        
        subgraph "Controllers Layer"
            Controller[log_controller.py<br/>Business Logic]
        end
        
        subgraph "Services Layer"
            Service[model_service.py<br/>Model Management]
        end
        
        subgraph "Models Layer"
            Schemas[schemas.py<br/>Pydantic Models]
        end
    end
    
    subgraph "External Components"
        Client[HTTP Client]
        MLModel[DeBERTa Model]
        Storage[(File System)]
    end
    
    Client -->|HTTP Request| Main
    Main --> Router
    Router --> Schemas
    Router --> Controller
    Controller --> Schemas
    Controller --> Service
    Service --> MLModel
    Service --> Storage
    Config -.->|Configuration| Service
    Config -.->|Configuration| Main
```

---

## 7. Class Diagram

```mermaid
classDiagram
    class FastAPIApp {
        +title: str
        +version: str
        +startup_event()
        +shutdown_event()
    }
    
    class LogRequest {
        +log_message: str
        +threshold: float
    }
    
    class LogResponse {
        +log_message: str
        +label: str
        +confidence: float
        +is_anomaly: bool
        +threshold: float
    }
    
    class HealthResponse {
        +status: str
        +model_loaded: bool
        +model_path: str
    }
    
    class LogController {
        -model_service: ModelService
        +analyze_log(request: LogRequest): LogResponse
        +get_health(): HealthResponse
    }
    
    class ModelService {
        -_instance: ModelService
        -_pipeline: Pipeline
        +load_model(force_reload: bool): bool
        +is_loaded(): bool
        +inference(log_message: str, threshold: float): dict
        +get_model_info(): dict
    }
    
    class LogRouter {
        +analyze_log(request: LogRequest): LogResponse
        +health_check(): HealthResponse
        +root(): dict
    }
    
    FastAPIApp --> LogRouter
    LogRouter --> LogController
    LogRouter --> LogRequest
    LogRouter --> LogResponse
    LogRouter --> HealthResponse
    LogController --> ModelService
    LogController --> LogRequest
    LogController --> LogResponse
    LogController --> HealthResponse
    ModelService --> "1" ModelService : Singleton
```

---

## 8. Deployment Diagram

```mermaid
graph TB
    subgraph "Client Environment"
        Browser[Web Browser]
        CLI[CLI/cURL]
        PythonClient[Python Client]
    end
    
    subgraph "Server Environment"
        subgraph "FastAPI Server :8000"
            App[FastAPI Application]
            Uvicorn[Uvicorn ASGI Server]
        end
        
        subgraph "File System"
            AppCode[app/ directory]
            ModelFiles[models/ directory]
            Config[Configuration Files]
        end
        
        subgraph "Runtime"
            Python[Python 3.8+]
            Transformers[Transformers Library]
            PyTorch[PyTorch]
        end
    end
    
    Browser -->|HTTP/HTTPS| Uvicorn
    CLI -->|HTTP/HTTPS| Uvicorn
    PythonClient -->|HTTP/HTTPS| Uvicorn
    
    Uvicorn --> App
    App --> AppCode
    App --> ModelFiles
    App --> Config
    App --> Transformers
    Transformers --> PyTorch
    Python -.runs.- App
```

---

## 9. State Diagram - Model Service

```mermaid
stateDiagram-v2
    [*] --> Uninitialized
    
    Uninitialized --> LoadingModel: load_model() called
    
    LoadingModel --> CheckingFiles: Check model directory
    
    CheckingFiles --> ModelNotFound: Files don't exist
    CheckingFiles --> LoadingFromDisk: Files exist
    
    ModelNotFound --> Uninitialized: Return False
    
    LoadingFromDisk --> ModelLoaded: Success
    LoadingFromDisk --> LoadError: Exception
    
    LoadError --> Uninitialized: Log error, Return False
    
    ModelLoaded --> Ready: Model cached in memory
    
    Ready --> Processing: inference() called
    Processing --> Ready: Return results
    
    Ready --> LoadingModel: load_model(force_reload=True)
    
    Ready --> [*]: shutdown_event()
```

---

## 10. Activity Diagram - Log Analysis Process

```mermaid
graph TD
    Start([Start]) --> ReceiveRequest[Receive POST /api/v1/analyze]
    ReceiveRequest --> ValidateInput{Validate Input}
    
    ValidateInput -->|Invalid| ReturnError1[Return 422 Validation Error]
    ReturnError1 --> End([End])
    
    ValidateInput -->|Valid| CheckModel{Is Model Loaded?}
    
    CheckModel -->|No| ReturnError2[Return 503 Service Unavailable]
    ReturnError2 --> End
    
    CheckModel -->|Yes| ExtractData[Extract log_message and threshold]
    ExtractData --> CallModel[Call DeBERTa Model]
    CallModel --> GetScores[Get classification scores]
    
    GetScores --> CompareThreshold{Confidence >= Threshold?}
    
    CompareThreshold -->|Yes| UseFirstLabel[Use primary label]
    CompareThreshold -->|No| UseSecondLabel[Use secondary label]
    
    UseFirstLabel --> DetermineAnomaly[Determine if anomaly]
    UseSecondLabel --> DetermineAnomaly
    
    DetermineAnomaly --> FormatResponse[Format JSON Response]
    FormatResponse --> LogResult[Log analysis result]
    LogResult --> Return200[Return 200 OK]
    Return200 --> End
```

---

## 11. Architecture Diagram - MVC Pattern

```mermaid
graph TB
    subgraph "Presentation Layer (View)"
        API[REST API Endpoints<br/>OpenAPI/Swagger UI]
    end
    
    subgraph "Controller Layer"
        Router[Router<br/>log_router.py]
        Controller[Controller<br/>log_controller.py]
    end
    
    subgraph "Model Layer"
        Schemas[Schemas<br/>Pydantic Models]
        Service[Service<br/>model_service.py]
        MLModel[ML Model<br/>DeBERTa]
    end
    
    subgraph "Configuration"
        Config[config.py<br/>Settings & Paths]
    end
    
    Client[Client] -->|HTTP Request| API
    API --> Router
    Router --> Schemas
    Router --> Controller
    Controller --> Service
    Service --> MLModel
    Config -.->|Provides Config| Service
    Config -.->|Provides Config| Controller
    
    MLModel -->|Results| Service
    Service -->|Results| Controller
    Controller -->|Response| Router
    Router -->|JSON| API
    API -->|HTTP Response| Client
```

---

## 12. Entity Relationship Diagram - Data Model

```mermaid
erDiagram
    LOG_REQUEST ||--|| LOG_RESPONSE : produces
    LOG_REQUEST {
        string log_message
        float threshold
    }
    
    LOG_RESPONSE {
        string log_message
        string label
        float confidence
        boolean is_anomaly
        float threshold
    }
    
    MODEL_SERVICE ||--o{ INFERENCE_RESULT : generates
    MODEL_SERVICE {
        string model_path
        boolean is_loaded
        object pipeline
    }
    
    INFERENCE_RESULT {
        string label
        float confidence
        boolean is_anomaly
        dict scores
    }
    
    HEALTH_STATUS ||--|| MODEL_SERVICE : monitors
    HEALTH_STATUS {
        string status
        boolean model_loaded
        string model_path
    }
    
    CONFIGURATION ||--|| MODEL_SERVICE : configures
    CONFIGURATION {
        string MODEL_NAME
        string MODEL_DIR
        float DEFAULT_THRESHOLD
        list CLASSIFICATION_LABELS
    }
```

---

## 13. Network Diagram - API Communication

```mermaid
graph LR
    subgraph "Client Side"
        WebApp[Web Application]
        Mobile[Mobile App]
        Script[Python Script]
        CURL[cURL/CLI]
    end
    
    subgraph "Network"
        HTTP[HTTP/HTTPS<br/>Port 8000]
    end
    
    subgraph "Server Side"
        CORS[CORS Middleware]
        Router[API Router]
        
        subgraph "Endpoints"
            E1[POST /api/v1/analyze]
            E2[GET /api/v1/health]
            E3[GET /api/v1/]
            E4[GET /docs]
        end
    end
    
    WebApp --> HTTP
    Mobile --> HTTP
    Script --> HTTP
    CURL --> HTTP
    
    HTTP --> CORS
    CORS --> Router
    
    Router --> E1
    Router --> E2
    Router --> E3
    Router --> E4
```

---

## 14. Flowchart - Model Download Process

```mermaid
flowchart TD
    Start([Start Download]) --> CheckArgs[Parse Command Line Args]
    CheckArgs --> CheckDir{Model Directory<br/>Exists?}
    
    CheckDir -->|No| CreateDir[Create Directory]
    CheckDir -->|Yes| CheckFiles{Model Files<br/>Exist?}
    
    CreateDir --> DownloadTokenizer
    
    CheckFiles -->|Yes| AskUser{Ask User:<br/>Re-download?}
    CheckFiles -->|No| DownloadTokenizer
    
    AskUser -->|No| Skip[Skip Download]
    AskUser -->|Yes| DownloadTokenizer
    
    DownloadTokenizer[Download Tokenizer<br/>from Hugging Face]
    DownloadTokenizer --> SaveTokenizer[Save Tokenizer Locally]
    
    SaveTokenizer --> DownloadModel[Download Model<br/>from Hugging Face]
    DownloadModel --> SaveModel[Save Model Locally]
    
    SaveModel --> Verify[Verify Files]
    Verify --> CheckVerify{All Files<br/>Present?}
    
    CheckVerify -->|Yes| Success[✓ Success Message]
    CheckVerify -->|No| Warning[⚠ Warning Message]
    
    Success --> End([End])
    Warning --> End
    Skip --> End
```

---

## Diagram Descriptions

### 1. **Use Case Diagram**
Shows the main interactions between users (clients and admins) and the system.

### 2. **Sequence Diagram - Log Analysis**
Illustrates the step-by-step flow when a client sends a log for analysis.

### 3. **Sequence Diagram - Startup**
Shows how the application initializes and loads the model on startup.

### 4. **DFD Level 0**
High-level view of data flow between external entities and the system.

### 5. **DFD Level 1**
Detailed view of internal processes and data stores.

### 6. **Component Diagram**
Shows the architectural components and their relationships.

### 7. **Class Diagram**
Displays the object-oriented structure of the application.

### 8. **Deployment Diagram**
Illustrates the physical deployment of the system.

### 9. **State Diagram**
Shows the different states of the ModelService throughout its lifecycle.

### 10. **Activity Diagram**
Details the workflow of analyzing a log message.

### 11. **Architecture Diagram**
Visualizes the MVC architecture pattern implementation.

### 12. **Entity Relationship Diagram**
Shows the data model and relationships between entities.

### 13. **Network Diagram**
Illustrates the network communication between clients and server.

### 14. **Flowchart**
Shows the model download process logic.

---

## How to View These Diagrams

### Option 1: GitHub/GitLab
Push this file to GitHub or GitLab - they render Mermaid diagrams automatically.

### Option 2: VS Code
Install the "Markdown Preview Mermaid Support" extension.

### Option 3: Online Editors
- [Mermaid Live Editor](https://mermaid.live/)
- Copy and paste individual diagrams

### Option 4: Documentation Tools
- MkDocs with mermaid plugin
- Docusaurus
- GitBook
