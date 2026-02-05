# Gen AI Evaluation Techniques

## Slide 1: Evaluation Techniques
(Title Slide)

## Slide 2: Evaluating LLMs - We evaluate LLMs differently than classical ML and entire AI systems
Let’s dive into evaluation techniques. To really understand how to evaluate large language models (LLMs), it’s useful to first look at how traditional systems are evaluated. Evaluating LLMs is a bit different from classical models, and when we talk about evaluating entire AI systems, we want to assess not just the whole but also its individual components.
Previously, we discussed prompt safety and implementing guardrails. Now, we’ll turn our attention specifically to evaluating the LLM itself. Securing the overall system and evaluating the quality of the whole solution are separate topics that will come later. When evaluating an AI system, we look at factors like cost, user feedback, and security. For LLMs, we focus on the model component of the system, often using performance benchmarks, general metrics, and task-specific metrics to assess how well the LLM performs. In other words, we shift from evaluating the broader system to looking more closely at the LLM as a specialized component.

## Slide 3: Evaluation: LLMs vs. Classical ML - LLMs present new challenges
LLMs are deep learning models that need massive data and computing resources—far more than classical machine learning models. While classical models use clear metrics like accuracy or F1 score, evaluating LLMs is tougher because their output is language. Metrics like BLEU and ROUGE exist, but for many tasks, human or LLM-based judgment is also needed. Classical models are easier to interpret, whereas LLMs are black boxes with limited interpretability, though research is helping to improve this.

## Slide 4: Base Foundation Model Metrics: Loss - How well do models predict the next token?
When evaluating LLMs, the first metric used is loss. During training, the model tries to guess missing words in sentences, and as it improves, the loss value decreases. This means the model becomes better at predicting the next word and understanding grammar. However, just like with phone autocomplete, the model may generate grammatically correct words that don’t always make sense. Loss measures word prediction accuracy but doesn’t guarantee truly coherent or meaningful sentences, so more advanced evaluation methods are needed to overcome these limitations.

## Slide 5: Base Foundation Model Metrics: Perplexity - Is the model surprised that it was correct?
To improve evaluation beyond just loss, another metric used is perplexity. Perplexity measures how confident a model is in picking a particular word from all possible choices—lower perplexity means the model is more certain. This helps produce more fluent sentences because the model is better at choosing words that fit together, so the text flows more naturally. However, even with low perplexity, the model might still generate sentences that sound good but aren’t actually relevant to the task or question. So, while perplexity is a step up from just measuring loss, it still doesn’t guarantee meaningful or accurate answers for specific tasks.

## Slide 6: Base Foundation Model Metrics: Toxicity - How harmful is the out of the model?
Toxicity is another important metric, especially for production applications. It measures how harmful or mean a model’s output might be, which matters when the AI is interacting with customers or other systems. A polite or kind message gets a low toxicity score, while a mean or harmful message gets a high toxicity score. This metric is useful for filtering out hate speech or offensive content from models, making it a powerful tool for maintaining safe and friendly interactions.

## Slide 7: Task-specific Evaluation Metrics - Base-model metrics are applicable, but they aren’t specific enough
These metrics, while broadly useful, aren’t task specific—they don’t show how well a model does at things like question answering, summarization, or product recommendations. Metrics like loss, perplexity, and toxicity focus mainly on grammar and fluency, not on whether the sentences are actually useful for a particular task. This is a core challenge in AI system evaluation, since real-world tasks—like translation, code writing, or passing exams—require different benchmarks. That’s why tools such as MLflow now support more specialized evaluation for tasks like question answering and text summarization, giving us better metrics tailored to those specific challenges.

## Slide 8: LLM Evaluation Metrics: Task-specific - Using task-specific techniques to evaluate downstream performance
For tasks like question answering and text summarization, common NLP metrics include BLEU (which is used for translation tasks) and ROUGE (used for summarization). These metrics help measure how well a model performs on these specific tasks by turning the quality of the output into numerical scores, making it easier to compare and evaluate results objectively.

## Slide 9: Deep Dive: BLEU - BiLingual Evaluation Understudy
Here’s how BLEU works. BLEU stands for Bilingual Evaluation Understudy, and it’s used to compare the model’s generated output to a reference output—so it’s a supervised evaluation. You take a dataset with correct or good examples, then compare what the model produced to those references.

Specifically, BLEU looks at how many matching words (unigrams), two-word combinations (bigrams), and three-word combinations (trigrams) there are between the generated and reference answers. The more overlaps, the higher the BLEU score, which means the generated text is closer to the reference. Higher scores indicate better matches, and this makes it a popular way to compare generated text across different models or datasets.

## Slide 10: Deep Dive: ROUGE - Recall-Oriented Understudy for Gisting Evaluation (for N-grams)
Another widely used metric is ROUGE, which stands for Recall Oriented Understudy for Gisting Evaluation. ROUGE works by counting how many words overlap between the generated output and the reference, then dividing by the total possible matches to get a probability score. This makes it easy to compare different models’ performance using a standardized number.

There are various ROUGE versions: some check single words, bigrams, or even the longest common sequence of words. One variant, ROUGE-Lsum, ignores punctuation, which is helpful when comparing summary outputs to reference paragraphs. This flexibility allows ROUGE to handle different aspects of text comparison, especially useful for summarization tasks.

## Slide 11: Task-specific Evaluation Metric Similarities - What do BLEU and ROUGE have in common?
BLEU and ROUGE are both task-specific metrics used to evaluate the output of LLMs. They require benchmark datasets to compare the generated outputs against reference texts. Both metrics analyze n-grams (short sequences of words) rather than just individual words, and their scores depend on how well the model’s output matches the reference data. This comparison highlights the importance of having high-quality datasets for meaningful evaluation.

## Slide 12: Benchmarking: Types of Data - Evaluate with large generic data and your application’s data
This brings us to the topic of benchmarks. Most LLMs today are evaluated using metrics like BLEU and ROUGE against specially designed datasets that reflect different tasks. Early benchmarks, like Stanford QA, focused on tasks such as reading comprehension and answering questions from a given text. Now there are many different benchmarks covering a range of tasks, but these are usually quite general. In real-world applications, many organizations end up creating their own benchmarks to better reflect their specific needs and use cases.

## Slide 13: Benchmarking: Types of Data - Evaluate with large generic data and your application’s data (Continued)
Domain-specific reference datasets are important for tasks like Databricks documentation translation. For example, the internal localization process might use English paired with Spanish or Portuguese reference versions to benchmark translation accuracy. Many organizations develop their own datasets tailored to their needs, since public benchmarks are useful as proxies but rarely match perfectly with each company’s actual requirements. Custom datasets ensure evaluations are more relevant and accurate for specific real-world applications.

## Slide 14: Mosaic AI Gauntlet - Well-curated set of benchmarks
As we move from individual metrics to broader model comparisons, benchmarking—comparing models against standard datasets—is key. The Mosaic AI Gauntlet is Databricks' well-curated set of benchmarks.
The Gauntlet encompasses 35 different benchmark sources. These 35 benchmarks are organized into six broad categories to comprehensively assess a model's capabilities. These categories include reading comprehension, commonsense reasoning, problem solving, world knowledge, symbolic problem solving, and language understanding. By providing this broad, categorized evaluation, the Gauntlet gives us a detailed, holistic view of a model’s strengths and weaknesses across various critical AI tasks.

## Slide 15: Addressing Evaluation Challenges - The previous approaches are valuable, but leave us with gaps
When there are no reference datasets or clear metrics, it becomes difficult to evaluate generative AI systems. Many applications lack ground truth or benchmarks to define good results, so without something measurable, developers face a “chicken and egg” problem in building and validating these models.

## Slide 16: Addressing Evaluation Challenges - LLM-as-a-Judge
To handle complex cases without benchmarks, a common approach is to use an LLM as a judge. Since LLMs can reason and assess outputs, they can be asked to evaluate the responses of other models. Alternatively, human evaluators can review results, but using an LLM for evaluation has become a popular and efficient choice for these situations.

## Slide 17: LLM-as-a-Judge Basics - LLM-as-a-Judge techniques can utilize prompt engineering templating
For an LLM to act as a judge, it needs a few things: clear examples of good and bad outputs, human-provided instructions outlining what counts as “good,” and a grading rubric to use for evaluation. These elements help guide the LLM’s assessment process and ensure its judgments align with intended quality standards.

## Slide 18: LLM-as-a-Judge Basics - Limitations and how to address them
While LLM-as-a-Judge techniques offer immense scalability and cost savings, they are not without limitations. We must ask: Do we trust the metrics generated by other LLMs?
Possible limitations include the LLM-as-a-Judge's lack of understanding and contextual awareness. There is also a risk that the metrics generated might be based on inaccurate or hallucinatory outputs from the system being judged. Furthermore, issues of bias and ethical concerns can be introduced or reinforced if the judging model itself has inherent biases.
The most effective solution to combat these limitations is implementing a Human-in-the-loop strategy. This involves having human experts review the metrics generated by the LLM judges. Human review helps to improve accuracy, handle ambiguities, and ensures we maintain qualitative oversight over the automated process.

## Slide 19: MLflow (LLM) Evaluation - Efficiently evaluate retrievers and LLMs
To efficiently implement these LLM-as-a-Judge techniques, we turn to MLflow Evaluation. MLflow is a key tool for efficiently evaluating both retrievers and LLMs. MLflow offers several advantages for Gen AI evaluation:
First, it enables batch comparisons, allowing you to compare foundational models with fine-tuned models across many test questions simultaneously.
Second, it supports rapid and scalable experimentation. MLflow can automatically, rapidly, and at a low cost, evaluate the unstructured outputs—like text generated by LLMs.
Finally, this automated evaluation is cost-effective. By automating evaluations using LLMs, you can significantly save time and resources compared to relying solely on expensive and time-consuming human evaluation efforts.

## Slide 20: MLflow (LLM) Evaluation - Efficiently evaluate retrievers and LLMs (In Code and UI)
MLflow provides capabilities for both batch evaluation in code and interactive evaluation in the UI.
For batch evaluation (using code): You can utilize LLM-as-a-Judge methodology, employing foundation models to judge performance and scale beyond what is feasible with human evaluation alone. You can also validate your system against ground truth by efficiently evaluating output using large, curated datasets.
For interactive evaluation (using the UI): Developers can visually compare multiple models and prompts. This is crucial during development, allowing teams to iteratively test new queries and visually see how changes affect performance.

## Slide 21: MLflow's LLM-as-a-Judge Capabilities - An enhanced workflow for LLM-as-a-Judge evaluation

Templates are a good conceptual framework, but there's a lot of engineering around these ideas.

MLflow and its **evaluate** module make this process much easier, especially for custom metrics.

The enhanced workflow for using MLflow's LLM-as-a-Judge is streamlined into three main steps:

1. First, you create example evaluation records.
2. Second, you create a metric object. This object includes those examples, a description of the desired scoring criteria, specifies the judge model to be used, and defines the aggregations needed to evaluate the model across all provided records.
3. Finally, you evaluate the model against a reference dataset using the newly created custom metric.

**Speaker Notes:**
While the prompt templates we discussed earlier offer a good conceptual framework, there is significant engineering work required to deploy them effectively. MLflow and its specialized evaluate module make the LLM-as-a-Judge process much easier, especially when you need custom metrics. The enhanced workflow for using MLflow's LLM-as-a-Judge is streamlined into three main steps: First, you create example evaluation records. Second, you create a metric object. This object includes those examples, a description of the desired scoring criteria, specifies the judge model to be used, and defines the aggregations needed to evaluate the model across all provided records. Finally, you evaluate the model against a reference dataset using the newly created custom metric.