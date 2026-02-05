# Demo: Building and Logging Retrieval Agents

## Overview

This demo covers how to create a retrieval agent on Databricks, including:
1. Using a vector search index as a tool for the agent
2. Tracing the agent workflow for debugging
3. Logging and registering the agent in Unity Catalog Model Registry

## Learning Objectives

By the end of this demo, you should be able to:
- Test vector search functionality using AI Playground for rapid prototyping
- Build a retrieval agent using LangChain
- Use MLflow Tracing to monitor and debug agent interactions with defined tools
- Register the agent as a model in Model Registry

## Requirements

- Pre-created vector search endpoint (created in previous demo)
- Serverless compute version 4
- Required libraries: Vector Search SDK, MLflow Skinny, Databricks LangChain, LangChain

## Section 1: Testing with AI Playground

Before coding, you can test your vector search index using AI Playground for rapid prototyping.

### Steps:
1. Go to **AI/ML section** → Click **Playground**
2. Navigate to your catalog → Select your schema
3. Find the vector search index in the table section
4. Click **"Try in Playground"** option (top right)

### AI Playground Features:
- Chat conversation area with system prompt
- LLM model selection
- Tools section (vector search index auto-added)
- Resources listing showing retrieved chunks
- Click on resources to see the vector search index sections

This demonstrates a typical retrieval agent workflow without writing any code.

## Section 2: Building Agent with LangChain

### Important Notes:
- LangChain is used here but **not required** - you can use OpenAI SDK or other frameworks
- Using **"Agent as Code"** approach - agent code is saved to a file before logging

### Step 1: Enable MLflow Tracing

```python
mlflow.langchain.autolog()
```

MLflow Tracing is enabled by default, but this explicitly enables LangChain interaction tracking.

### Step 2: Create the LangChain Agent

```python
# Define LLM
# Using Databricks GPT open source model
llm = ChatDatabricks(
    endpoint="databricks-dbrx-instruct",
    max_tokens=...
    # Can also set temperature and other configurations
)

# Define Tool
# Vector Search Retrieval Tool
tool = VectorSearchRetrievalTool(
    index_name="...",
    description="...",
    num_results=3
)

# Memory (optional)
# In-memory saver for multi-turn conversations
checkpointer = MemorySaver()

# System Prompt
system_prompt = "You are a knowledge assistant responding in a clear professional way..."

# Create Agent
agent = create_agent(llm, tools=[tool], system_prompt=system_prompt)
```

### Step 3: Invoke the Agent

```python
# Input format follows OpenAI chat format
response = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is Orion?"}
    ]
})

# Get final response
final_message = response["messages"][-1].content
```

## Section 3: MLflow Tracing UI

MLflow Tracing provides visibility into agent workflow for debugging.

### Tracing UI Features:

**Summary Section:**
- Input and output
- Flow visualization: ChatDatabricks → Tool Decision → Vector Search → Response Generation

**Details View:**
- Click on each branch to see:
  - Input/Output for each step
  - Parameters used
  - Retrieved documents (3 documents returned)
  - System prompt
  - Tool calls
  - Final agent response

**Timeline View:**
- Shows latency of each step
- Great for debugging slow responses
- Identify performance bottlenecks

## Section 4: Logging Agent with MLflow

### Step 1: Create Configuration File

Create a YAML config file to avoid hardcoding resources:

```python
config = {
    "llm_endpoint_name": "...",
    "vector_search_index_name": "...",
    "num_results": 3
}

# Write to agent_config.yaml
with open("agent_config.yaml", "w") as f:
    yaml.dump(config, f)
```

### Step 2: Write Agent Code to File

Using "Agent as Code" approach - write agent code to `agent.py`:

```python
%%writefile agent.py

# Load configuration
config = load_config("agent_config.yaml")

# Build agent (same as above)
agent = create_agent(...)

# MLflow Model Interface
class RetrievalAgent(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input: ChatAgentRequest) -> ChatAgentResponse:
        # Invoke agent
        response = agent.invoke(model_input)
        return ChatAgentResponse(response)
```

Key points:
- `predict()` function is called when invoking the model
- Uses MLflow's `ChatAgentRequest` and `ChatAgentResponse` objects
- Standard input/response format for Model Registry

### Step 3: Log the Model

```python
model_name = "orion_knowledge_assistant"

mlflow.pyfunc.log_model(
    artifact_path="model",
    python_model="agent.py",  # Agent as code
    code_paths=["agent_config.yaml"],  # Extra config files
    input_example=input_example,
    pip_requirements=[...]
)
```

### Step 4: Register the Model

```python
uc_model_name = "catalog.schema.orion_knowledge_assistant"

mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name=uc_model_name
)
```

## Section 5: Viewing Model in Unity Catalog

Navigate to: **Catalog** → **Your Schema** → **Models** → **orion_knowledge_assistant**

### Model Registry Features:

**Overview Section:**
- Model versions
- Activity log

**Version Details:**
- Input parameters (top_p, max_tokens, max_output_tokens, etc.)
- Output format (object)
- Lineage information

**Artifacts Section:**
- `agent.py` - Main agent file
- `conda.yaml` - Requirements for conda
- `requirements.txt` - Pip requirements
- `code/` folder - Contains `agent_config.yaml`

The Model Registry is a **packaging environment** - it installs all requirements and dependencies, allowing the model to run anywhere.

## Section 6: Loading and Testing the Model

```python
# Load model from registry
model = mlflow.pyfunc.load_model(f"models:/{uc_model_name}/1")

# Use predict function
input_data = {"messages": [{"role": "user", "content": "What is Orion?"}]}
response = model.predict(input_data)
```

Note: Loading takes longer as it installs all dependencies and creates the inference environment.

## Summary

1. **AI Playground Testing** - Test vector search index without coding
2. **LangChain Agent** - Build retrieval agent (can use other frameworks too)
3. **MLflow Tracing** - Debug and monitor agent interactions
4. **Agent as Code** - Save agent code to file with configuration
5. **Model Registry** - Log, register, and version your agent
6. **Unity Catalog** - Governance and access control for your model
