# End-to-end Application Evaluation

## Slide 1: End-to-end App. Evaluation

**Title:** End-to-end App. Evaluation
**Type:** Lecture

*(Visual: Databricks logo, Title text, Abstract graphic)*

**Speaker Notes:**
In this lecture on End-to-end Application Evaluation, we explore how to evaluate AI systems as a whole, including performance metrics, custom metrics, human feedback, and the Mosaic AI Agent Framework.

---

## Slide 2: AI System Architecture - Remember that AI systems are made up of smaller parts

**Title:** AI System Architecture
**Subtitle:** Remember that AI systems are made up of smaller parts

*(Visual: RAG architecture diagram showing Document Embedding, User Query, and Generation-Model components)*

We previously talked about how to evaluate components of an AI system, but **what about the system as a whole?**

**Speaker Notes:**
Let's dive into end-to-end application evaluation. Remember, AI systems are made up of smaller parts, and we've already discussed how to evaluate those individual components. But it's also important to consider how to evaluate the entire system as a whole, not just its separate pieces.

---

## Slide 3: Evaluating the Whole System - What do we evaluate when it comes to the entire system?

**Title:** Evaluating the Whole System
**Subtitle:** What do we evaluate when it comes to the entire system?

*(Visual: RAG architecture diagram)*

**Key Evaluation Areas:**
*   **Cost** metrics
    *   Resources
    *   Time
*   **Performance**
    *   Direct value
    *   Indirect value
*   **Custom** metrics for your own use case

**Speaker Notes:**
When evaluating an entire AI system, there are usually two main concerns: cost metrics and performance metrics. Cost metrics cover things like how much infrastructure is needed and how much time processing takes, while performance metrics measure the actual value delivered to customers, such as how useful or frequently used the product is. Often, teams create custom metrics tailored to their specific use cases to get a clearer sense of the system's total impact.

---

## Slide 4: Performance Metrics

**Title:** Performance Metrics

*(Title Slide - dark background)*

**Speaker Notes:**
Now let's dive into performance metrics for evaluating AI systems.

---

## Slide 5: Evaluating RAG Pipeline - Let's start by performance metrics

**Title:** Evaluating RAG Pipeline
**Subtitle:** Let's start by performance metrics

*   When evaluating RAG solutions, we need to **evaluate each component separately and together**.
*   Components to evaluate:
    *   Chunking: method, size
    *   Embedding model
    *   Vector store
        *   Retrieval and re-ranker
    *   Generator

*(Visual: Three gauge icons showing Chunking Performance, Retrieval Performance, and Generator Performance)*

**Speaker Notes:**
Now that we've covered LLM-specific evaluation techniques like LLM-as-a-Judge and MLflow, we turn our attention to evaluating the entire RAG pipeline. To understand RAG performance, we need to evaluate each component separately and together. The RAG architecture, as a compound AI system, has several key components we need to evaluate:
- Chunking: The method and size used to split source documents.
- Embedding model: The model used to convert text into vectors.
- Vector store: This includes the performance of the retrieval mechanism and any re-ranker components used to refine results.
- Generator: The final LLM used to synthesize the response based on the retrieved context.
Each component contributes to the end-to-end performance, requiring specific metrics.

---

## Slide 6: Evaluation Metrics - Retrieval and generation related metrics

**Title:** Evaluation Metrics
**Subtitle:** Retrieval and generation related metrics

*(Visual: Diagram showing relationships between Query, Ground Truth, Context, and Response with questions:)*
- Is the answer relevant and accurate?
- Is the context related to the query?
- Is the response supported by the context?

**Speaker Notes:**
In RAG evaluation, we focus on retrieval and generation-related metrics, all tied back to the Ground Truth—the ideal answer. This diagram helps us visualize the four relationships we must measure:
1. Query to Context: Is the context related to the query?
2. Context to Response: Is the response supported by the provided context?
3. Query to Response: Is the answer relevant and accurate to the original query?
4. And, implicitly, Response to Ground Truth and Context to Ground Truth, which measure accuracy and completeness against known facts.
The next few slides detail the specific metrics used to measure these relationships.

---

## Slide 7: Context Precision - Retrieval related metrics

**Title:** Context Precision
**Subtitle:** Retrieval related metrics

**Context Precision:**
*   Signal-to-noise ratio for the retrieved context.
*   Based on **Query** and **Context(s)**.
*   It assesses whether the chunks/nodes in the retrieval context ranked higher than irrelevant ones.

**Example:**
*   **Query:** What was Einstein's role in the development of quantum mechanics?
*   **Ground Truth:** Einstein contributed to the development of quantum theory, including his early skepticism and later contributions to quantum mechanics.
*   **High Context Precision:** [The contexts specifically mention contributions to quantum theory]
*   **Low Context Precision:** [The contexts broadly discuss Einstein's life and achievements without specifically addressing his contributions to quantum mechanics.]

**Speaker Notes:**
Our first metric, Context Precision, is retrieval-related and measures the signal-to-noise ratio of the retrieved context. It is based on the relationship between the Query and the retrieved Context(s). Context Precision assesses whether the highly ranked chunks or nodes in the retrieval context are more relevant than irrelevant ones. For example, if your query is about Einstein's role in quantum mechanics, a high precision context would specifically mention his contributions to quantum theory, while a low precision context might broadly discuss his life and achievements without focusing on the query's specific technical area.

---

## Slide 8: Context Relevancy - Retrieval related metrics

**Title:** Context Relevancy
**Subtitle:** Retrieval related metrics

**Context Relevancy:**
*   Measure the relevancy of the retrieved context.
*   Based on both the **Query** and **Context(s)**.
*   It does not necessarily consider the factual accuracy but focuses on how well the answer addresses the posed question

**Example:**
*   **Query:** What was Einstein's role in the development of quantum mechanics?
*   **High context relevancy:** Einstein initially challenged the quantum theory but later contributed foundational ideas to quantum mechanics.
*   **Low context relevancy:** Einstein was known for his pacifist views during the early 20th century and became a U.S. citizen in 1940.

**Speaker Notes:**
Context Relevancy is another retrieval-related metric that measures the relevancy of the retrieved context. Like precision, it is based on the Query and the Context(s). However, relevancy does not necessarily consider factual accuracy. Instead, it focuses on how well the retrieved context addresses the posed question. For example, if the query is about Einstein and quantum mechanics, context that details his initial challenges to quantum theory or his foundational ideas would be highly relevant, even if it doesn't represent the 'ground truth' of his final accepted contributions. Conversely, context about his pacifist views or citizenship status would be low relevancy.

---

## Slide 9: Context Recall - Retrieval related metrics

**Title:** Context Recall
**Subtitle:** Retrieval related metrics

**Context Recall:**
*   Measures the extent to which all relevant entities and information are retrieved and mentioned in the context provided.
*   Based on **Ground Truth** and retrieved **Context(s)**.

**Example:**
*   **Query:** What significant scientific theories did Einstein contribute to?
*   **Ground truth:** Einstein contributed to the theories of relativity and had insights into quantum mechanics.
*   **High-recall context:** Einstein contributed to relativity and quantum mechanics.
*   **Low-recall context:** Einstein contributed to relativity.

**Speaker Notes:**
Our third retrieval metric is Context Recall. Recall measures the extent to which all relevant entities and information are retrieved and mentioned in the context provided. This metric is based on comparing the Ground Truth against the retrieved Context(s). If the ground truth about Einstein mentions both his contributions to relativity and insights into quantum mechanics, a high-recall context will retrieve and mention both of those key facts. A low-recall context might only retrieve information about relativity, missing the quantum mechanics aspect entirely.

---

## Slide 10: Faithfulness - Generation related metrics

**Title:** Faithfulness
**Subtitle:** Generation related metrics

**Faithfulness:**
*   Measures the factual accuracy of the generated answer in relation to the provided context.
*   Based on the **Response** and retrieved **Context(s)**.

**Example:**
*   **Query:** Where and when was Einstein born?
*   **Context:** Albert Einstein (born 14 March 1879) was a German-born theoretical physicist, widely held to be one of the greatest and most influential scientists of all time.
*   **High faithfulness answer:** Einstein was born in Germany on 14th March 1879.
*   **Low faithfulness answer:** Einstein was born in Germany on 20th March 1879.

**Speaker Notes:**
Shifting now to generation-related metrics, we look at Faithfulness. This metric assesses the quality of the final generated response. Faithfulness measures the factual accuracy of the generated answer in relation to the provided context. It is specifically based on the relationship between the Response and the retrieved Context(s). A high faithfulness answer is supported by the context; for instance, if the context says Einstein was born on March 14th, a faithful answer will state March 14th. If the response provides an answer that contradicts the context—say, stating March 20th, it shows low faithfulness, regardless of whether March 20th might be factually correct outside of that specific context.

---

## Slide 11: Answer Relevancy - Generation related metrics

**Title:** Answer Relevancy
**Subtitle:** Generation related metrics

**Answer Relevancy:**
*   Assesses how pertinent and applicable the generated response is to the user's initial query.
*   Based on the alignment of the **Response** with the user's intent or **Query** specifics.

**Example:**
*   **Query:** What is Einstein known for?
*   **High relevancy answer:** Einstein is known for developing the theory of relativity.
*   **Low relevancy answer:** Einstein was a scientist.

**Speaker Notes:**
The next generation metric is Answer Relevancy. Answer Relevancy assesses how pertinent and applicable the generated response is to the user's initial query. It is based on the alignment of the Response with the user's intent or the specific details of the Query. For example, if the query asks what Einstein is known for, a high relevancy answer will specifically mention his major theoretical achievements, such as developing the theory of relativity. A low relevancy answer might simply state he was a scientist, which is true but doesn't fully address the intent of the question.

---

## Slide 12: Answer Correctness - Generation related metrics

**Title:** Answer Correctness
**Subtitle:** Generation related metrics

**Answer Correctness:**
*   Measures the accuracy of the generated answer when compared to the ground truth.
*   Based on the **Ground Truth** and the **Response**.
*   Encompasses both semantic and factual similarity with the ground truth.

**Example:**
*   **Ground truth:** Albert Einstein was awarded the Nobel Prize in Physics in 1921 for his explanation of the photoelectric effect.
*   **High answer correctness:** Einstein received the Nobel Prize in Physics in 1921 for his work on the photoelectric effect.
*   **Low answer correctness:** Einstein won the Nobel Prize in Physics in the 1930s for his theory of relativity.

**Speaker Notes:**
Finally, we have Answer Correctness. This metric measures the accuracy of the generated answer when compared directly to the ground truth. It is based on the Ground Truth and the Response. Answer Correctness encompasses both semantic and factual similarity with the ground truth. If the ground truth states Einstein won the Nobel Prize in Physics in 1921 for his work on the photoelectric effect, a high correctness answer will match those facts. A low correctness answer might misstate the year or mention a different theory, like relativity in the 1930s.

---

## Slide 13: Custom Metrics

**Title:** Custom Metrics

*(Title Slide - dark background)*

**Speaker Notes:**
We have discussed many standardized metrics, but often, the most important evaluation criteria are unique to your business case. This leads us to the topic of Custom Metrics. These metrics are essential when evaluating the overall AI system, as opposed to just the LLM components. Custom metrics are frequently related to the specific business goals and constraints defined for your AI system.

---

## Slide 14: Custom Metrics for System Evaluation - Frequently related to business goals and constraints for the AI system

**Title:** Custom Metrics for System Evaluation
**Subtitle:** Frequently related to business goals and constraints for the AI system

*   What is important to your use case?
    *   Do you care about *serving latency*?
    *   Are you concerned with *total cost*?
    *   Are you expecting your system to *increase product demand*?
    *   What about *customer satisfaction*?

*   **Note:** custom metrics can be useful for individual components, too.

**Quick Activity:** Define your own system-wide custom metric to ensure your AI system is providing the value that you expect.

**Speaker Notes:**
Custom metrics are important for system evaluation because standard metrics often don't match a business's specific needs or customer values. Only the business truly understands what matters to its users and tasks, so metrics should reflect what is valuable for them—like latency for chatbots, total cost (including infrastructure and engineering), speed to market, scalability, or customer satisfaction. Sometimes, companies need to release products early (like in beta) just to gather real-world feedback and data for evaluation. Ultimately, creating a system-wide custom metric ensures the AI delivers the value that's expected for the business's unique context.

---

## Slide 15: Custom Metrics in MLflow - Built-in capabilities for integrating custom metrics into component monitoring

**Title:** Custom Metrics in MLflow
**Subtitle:** Built-in capabilities for integrating custom metrics into component monitoring

*   Beyond the predefined metrics, MLflow allows users to **create custom LLM evaluation metrics**.
*   Frequently uses **LLM-as-a-Judge** methodology to evaluate a defined custom metric

*(Visual: Code example showing professionalism metric definition with scoring criteria for different scores 0-3)*

**Speaker Notes:**
To measure LLM performance in ways that matter specifically to you, it's useful to develop your own system or evaluation rubric—such as scoring the professionalism or tone of the output if that's important. Tools like MLflow make it possible to create these custom metrics and use an LLM as a judge, which can scale efficiently and isn't overly expensive. While human evaluation data is often more accurate, using LLMs for judging works well for most organizations' needs.

---

## Slide 16: Human Feedback and Monitoring

**Title:** Human Feedback and Monitoring

*(Title Slide - dark background)*

**Speaker Notes:**
Now let's discuss the importance of human feedback and monitoring in AI system evaluation.

---

## Slide 17: Offline vs. Online Evaluation - Evaluating LLMs prior to prod and within prod

**Title:** Offline vs. Online Evaluation
**Subtitle:** Evaluating LLMs prior to prod and within prod

*   We've been talking about how we evaluate systems and components in static environments.
*   Sometimes we might want to evaluate online performance – performance after the systems have been deployed
*   This will provide real-time feedback on user experience with the LLM
*   Metrics to consider: A/B testing results, direct feedback, indirect feedback

| Offline Evaluation | Online Evaluation |
|-------------------|-------------------|
| 1. Curate a benchmark dataset | 1. Deploy the application |
| 2. Use task-specific evaluation metrics | 2. Collect real user behavior data |
| 3. Evaluate results using reference data or LLM-as-judge | 3. Evaluate results using how well the users respond to the LLM system |

**Speaker Notes:**
It's important to understand the difference between online and offline evaluation. Everything discussed so far—like benchmark testing or using LLMs as judges—falls under offline evaluation, which happens before releasing a product to users, to ensure the system works as expected. But the most important feedback comes from online evaluation, which means observing real users in production and tracking how they interact with the system's outputs. This live data shows whether people actually use and like the results, and it guides improvements for future offline evaluations and model development, creating a valuable feedback loop.

---

## Slide 18: Human Feedback - Collect data from users and experts

**Title:** Human Feedback
**Subtitle:** Collect data from users and experts

*   Often developers are not the experts of the domain
*   Models' output need to be **evaluated by human** experts
*   Models' outputs and associated feedback need to be collected and stored in a structured manner
*   Feedback can be **explicit or implicit**:
    *   **Explicit feedback:** Direct and intentional input from users. Such as ratings, comments and review.
    *   **Implicit feedback:** Gathered indirectly by observing user behavior and interactions. Such as engagement metrics and behavioral data.

**Speaker Notes:**
Regardless of how sophisticated our automated LLM evaluation is, Human Feedback remains indispensable for collecting real-time data from users and domain experts. Often, the developers are not the domain experts, meaning the model's output must be evaluated by human experts to ensure accuracy and quality. These outputs and their associated feedback must be collected and stored in a structured manner to inform future model improvements.
Human feedback can be categorized as:
- Explicit feedback: This is direct and intentional input from users, such as ratings, comments, and reviews.
- Implicit feedback: This is gathered indirectly by observing user behavior and interactions, such as engagement metrics or other behavioral data.

---

## Slide 19: Ongoing Evaluation of Components - AI systems are made up of smaller parts

**Title:** Ongoing Evaluation of Components
**Subtitle:** AI systems are made up of smaller parts

*   Systems need to be monitored on an ongoing basis
*   This will help detect drift in components and the system as a whole
*   Databricks provides the **Lakehouse Monitoring** solution
*   There will be more detail in the next course

**Speaker Notes:**
Online evaluation requires continuous monitoring of systems to detect data drift and changes in components or overall performance. Databricks supports this with tools like Lakehouse Monitoring, which integrates with services such as model serving to track API calls, user requests, and interactions. These monitoring tools help collect valuable feedback and support an ongoing improvement loop, especially within operations and system monitoring processes.

---

## Slide 20: Mosaic AI Agent Framework - Agent Evaluation

**Title:** Mosaic AI Agent Framework
**Subtitle:** Agent Evaluation

*(Title Slide - dark background with orange subtitle)*

**Speaker Notes:**
To bring together all these evaluation needs, from model security to component quality and human feedback—Databricks offers specific tools within the Mosaic AI Agent Framework. This framework is explicitly designed to handle the complexity of compound AI systems, including RAG and agent-based chains.

---

## Slide 21: Mosaic AI Agent Framework - A framework for creating, deploying and evaluating agents

**Title:** Mosaic AI Agent Framework
**Subtitle:** A framework for creating, deploying and evaluating agents

Mosaic AI Agent Framework:

*   A **suite of tooling** designed to help developers **build and deploy high-quality Generative AI applications**.
*   Makes it easy for developers to **evaluate the quality of their RAG application**, iterate quickly with the ability to test their hypothesis, redeploy their application easily, and have the appropriate governance and guardrails to ensure quality continuously.

**Speaker Notes:**
The Mosaic AI Agent Framework is a comprehensive suite of tooling designed to help developers successfully build and deploy high-quality Generative AI applications. It simplifies the process by making it easy for developers to achieve three main goals:
1. Evaluate the quality of their RAG application effectively.
2. Iterate quickly, enabling them to test hypotheses and redeploy their application with ease.
3. Implement the necessary governance and guardrails to continuously ensure quality in production.

---

## Slide 22: Mosaic AI Agent Framework - Agent Evaluation features

**Title:** Mosaic AI Agent Framework
**Subtitle:** Agent Evaluation features

*   **Trace agent behavior** in each step
*   Quickly evaluate chain quality with RAG specific **metrics**, unified between offline dev loop & online monitoring
*   Collect **human feedback** with easy-to-use **Review App**
*   **Databricks LLM Judges:** Proprietary models to assess RAG quality and identify root cause of low quality

*(Visual: Screenshots of Databricks UI showing trace views and Review App interface)*

**Speaker Notes:**
The Agent Evaluation features within the framework provide crucial visibility and control:
First, they allow you to trace agent behavior in each step, which is vital for debugging complex workflows.
Second, they let you quickly evaluate chain quality using RAG-specific metrics, unifying the offline development loop with online monitoring.
Third, the framework includes an easy-to-use Review App to efficiently collect human feedback.
And finally, it leverages Databricks LLM Judges, which are proprietary models used to assess RAG quality and help identify the root cause of any low-quality performance.
