# Demo: Building a Knowledge Assistant with Agent Bricks

## Overview

This demo covers how to build a knowledge assistant agent using **Agent Bricks**, a Databricks product that provides a declarative way of creating agents and improving agent quality through feedback and labeling sessions.

## Scenario

Creating a knowledge assistant for **Orion** (a humanoid robot company) to be used by field engineers. The assistant will answer questions about:
- Robot firmware
- Motor specifications
- Internal safety details and standards

The assistant uses internal documents as the knowledge source.

## Learning Objectives

By the end of this demo, you should be able to:
- Identify key components and requirements for creating a knowledge assistant using Agent Bricks
- Configure and create a knowledge assistant using Unity Catalog Volumes
- Implement agent testing and evaluate agent answers
- Improve agent quality through labeling sessions
- Apply best practices for creating high-performing agents

## Requirements

- Agent Bricks enabled
- Serverless compute version 4
- Unity Catalog Volume with documents (created by setup script)

## Section 1: Setup

The setup script creates a volume with documents for the knowledge base.

**Location:** `Catalog` → `DB Academy` → `Your Schema` → `Volumes` → `docs_volume` (8 documents)

## Section 2: Creating an Agent

### Steps:

1. Go to **Left Panel** → **Agents**
2. Select **Knowledge Assistant** agent type (for RAG architectures / document Q&A)
3. Fill in the configuration:

### Configuration Fields:

| Field | Description |
|-------|-------------|
| **Agent Name** | e.g., "Orion Knowledge Assistant" |
| **Description** | Description of the agent's purpose (required) |
| **Knowledge Sources** | UC Volumes or Vector Search (can add multiple) |
| **Instructions** | System prompt - define role and communication style |

### Knowledge Source Types:

- **UC Volumes** - Documents stored in Unity Catalog Volumes
- **Vector Search** - Pre-indexed text in Vector Search

You can combine multiple knowledge sources (e.g., documents in a volume + table in vector search).

### Adding Knowledge Source:

1. Select type: **UC Volume**
2. Navigate: `DB Academy` → `Your Schema` → `docs_volume`
3. Click **Confirm**
4. Add a name for the knowledge source
5. Describe the content (helps agent understand the resource)

### Instructions (System Prompt):

Add custom instructions defining:
- Agent role
- Response style
- Communication guidelines

4. Click **Create Agent** (takes 5-10 minutes)

## Section 3: Testing the Agent

After creation, the agent interface shows:
- Knowledge sources (with sync button for updates)
- Chat interface for testing

### Test Questions:

**Question 1:** "How does Orion verify compliance with the standard?"
- Agent processes through reasoning steps
- View sources to see information origin
- View trace to see inputs, outputs, and tool calls

**Question 2:** "What does the red blinking light under robot means?"
- Agent may not find specific information
- This is an opportunity to improve agent quality

## Section 4: Improving Agent Quality

### Use Cases for Improvement:
- Agent couldn't find specific information
- Change response style
- Fine-tune communication style
- Optimize based on user feedback

### Adding Examples with Guidelines:

1. Go to **Examples** tab
2. Add the question that needs improvement
3. Click the question to open guidelines window
4. Add specific guidelines:

**Example Guidelines:**
```
- Inform user there isn't a red light on the robot
- Ask user to restart Orion by removing and reinserting battery
- Request to re-check the light color
- Check if the light is blinking
```

5. Save guidelines
6. Test the question again - agent now follows guidelines

The agent still uses internal documents but follows the provided guidelines for specific scenarios.

## Section 5: Labeling Sessions for Expert Feedback

When you need expert feedback instead of doing it yourself, use **Labeling Sessions**.

### Creating a Labeling Session:

1. Ask questions that need expert review in the chat
2. Go to **Examples** tab
3. Click **Start Labeling Session**
4. Get shareable URL with configurable permissions

### How Labeling Sessions Work:

1. Share URL with subject matter experts
2. Experts see list of tasks (questions to review)
3. Experts review agent responses
4. Experts provide guidelines for each question

**Example Expert Guidelines:**
```
- Make it short, about three sentences
- Start with an interesting sentence
```

5. Click **Save** after providing guidelines

### Merging Expert Feedback:

1. Return to agent interface
2. Click **Merge** when expert is done
3. Click **Confirm**
4. Guidelines are merged to examples dataset
5. Test question again to verify improvement

### Benefits of Labeling Sessions:
- Experts don't need workspace access
- Collect high-quality labeled datasets
- Scalable feedback collection
- Improve agent quality iteratively

## Section 6: Cleanup

Delete the agent when done to free resources:
- Vector Search endpoint
- Model Serving endpoint

## Summary

1. **Declarative Agent Creation** - No code required, configure through UI
2. **Multiple Knowledge Sources** - Combine UC Volumes and Vector Search
3. **Testing Interface** - Built-in chat for testing with trace viewing
4. **Quality Improvement** - Add guidelines manually or through expert feedback
5. **Labeling Sessions** - Scalable way to collect expert feedback
6. **Iterative Refinement** - Merge feedback and continuously improve

## Key Components

| Component | Purpose |
|-----------|---------|
| Agent Bricks | Declarative agent creation platform |
| Knowledge Sources | UC Volumes or Vector Search indexes |
| Examples Tab | Store questions with guidelines |
| Labeling Sessions | Collect expert feedback via shareable URL |
| Merge Function | Apply expert guidelines to agent |
