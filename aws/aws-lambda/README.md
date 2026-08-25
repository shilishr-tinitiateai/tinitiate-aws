# AWS Lambda Operations (Python & AWS CLI)

Welcome to the **AWS Lambda Operations** module. This section provides production Python implementations and 17-section documentation templates for 12 AWS Lambda serverless operations, categorized across Basic, S3 Integration, and Advanced operation tiers.

---

## Operations Index

### 1. Basic Operations (`basic_operations/`)
Core Lambda handler boilerplate, event payload parsing, context object inspection, environment variables, and error handling:
- [01. Hello World](./basic_operations/01_hello_world/README.md)
- [02. Lambda Event Payload Parsing](./basic_operations/02_lambda_event/README.md)
- [03. Lambda Context Object](./basic_operations/03_lambda_context/README.md)
- [04. Lambda Environment Variables](./basic_operations/04_environment_variables/README.md)
- [05. Lambda Error Handling](./basic_operations/05_error_handling/README.md)

### 2. S3 Integration Operations (`s3_integration/`)
Event-driven processing workflows connecting Amazon S3 and AWS Lambda:
- [06. S3 Event Trigger Notification](./s3_integration/06_s3_trigger/README.md)
- [07. S3 File Processing](./s3_integration/07_s3_file_processing/README.md)
- [08. S3 Event Processing End-to-End Pipeline](./s3_integration/08_s3_event_processing/README.md)

### 3. Advanced Operations (`advanced_operations/`)
Shared Lambda layers, IAM execution role permissions, structured CloudWatch logging, and automated deployment script pipelines:
- [09. AWS Lambda Layers](./advanced_operations/09_lambda_layers/README.md)
- [10. Lambda IAM Execution Roles & Permissions](./advanced_operations/10_lambda_permissions/README.md)
- [11. Structured CloudWatch Logging](./advanced_operations/11_lambda_logging/README.md)
- [12. Lambda Packaging & Automated Deployment](./advanced_operations/12_lambda_deployment/README.md)

---

## Key Lambda Concepts
- **Serverless Architecture**: AWS manages infrastructure provisioning, scaling, patching, and container lifecycles.
- **Event-Driven Execution**: Functions execute in response to triggers (API Gateway, S3 ObjectCreated events, CloudWatch Cron schedules).
- **Stateless MicroVM Containers**: Function containers run ephemerally with access to temporary `/tmp` storage.
