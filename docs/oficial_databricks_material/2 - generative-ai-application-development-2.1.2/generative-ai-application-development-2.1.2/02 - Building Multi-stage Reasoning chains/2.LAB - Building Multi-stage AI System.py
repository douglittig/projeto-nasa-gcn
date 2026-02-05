# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # LAB - Building Multi-stage AI System
# MAGIC
# MAGIC In this lab, you will construct a multi-stage reasoning system using Databricks' features and LangChain.
# MAGIC
# MAGIC You will start by building the first chain, which performs a search using a dataset containing product descriptions from Etsy. Following that, you will create the second chain, which creates an image for the proposed product. Finally, you will integrate these chains to form a complete multi-stage AI system.
# MAGIC
# MAGIC
# MAGIC **Lab Outline:**
# MAGIC
# MAGIC In this lab, you will need to complete the following tasks;
# MAGIC
# MAGIC * **Task 1:** Create a Vector Store
# MAGIC
# MAGIC * **Task 2:** Build the First Chain (Vector Store Search)
# MAGIC
# MAGIC * **Task 3:** Build the Second Chain (Product Image)
# MAGIC
# MAGIC * **Task 4:**  Integrate Chains into a Multi-chain System
# MAGIC
# MAGIC **📝 Your task:** Complete the **`<FILL_IN>`** sections in the code blocks and follow the other steps as instructed.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC * To run this notebook, you need to use one of the following Databricks runtime(s): **15.4.x-cpu-ml-scala2.12**

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# COMMAND ----------

# MAGIC %pip install -U -qq databricks-sdk databricks-vectorsearch langchain-databricks langchain==0.3.7 langchain-community==0.3.7
# MAGIC
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-02LAB

# COMMAND ----------

# MAGIC %md
# MAGIC **Other Conventions:**
# MAGIC
# MAGIC Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

# COMMAND ----------

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Dataset
# MAGIC
# MAGIC Before you start building the AI chain, you will need to load dataset and save to a Delta table. For this demo, we will use **[Bright Data's Etsy Dataset](/marketplace/consumer/listings/d84c2d77-8db2-432a-8acc-4e8935755d5c)** listed in Databricks Marketplace. Only product title and description will be used. The table will be created for you in the next code block.

# COMMAND ----------

# create product text table
vs_source_table_fullname = f"{DA.catalog_name}.{DA.schema_name}.product_text"
create_product_text_table(vs_source_table_fullname)

# show table
display(spark.sql(f"SELECT * FROM {vs_source_table_fullname}"))

# COMMAND ----------

# MAGIC %md
# MAGIC %md 
# MAGIC ## Create a Vector Store
# MAGIC
# MAGIC In this step, you will compute embeddings for the dataset containing information about the products and store them in a Vector Search index using Databricks Vector Search.
# MAGIC
# MAGIC **🚨IMPORTANT: Vector Search endpoints must be created before running the rest of the demo. These are already created for you in Databricks Lab environment.**
# MAGIC

# COMMAND ----------

# assign vs search endpoint by username
vs_endpoint_prefix = "vs_endpoint_"
vs_endpoint_name = vs_endpoint_prefix+str(get_fixed_integer(DA.unique_name("_")))
print(f"Assigned Vector Search endpoint name: {vs_endpoint_name}.")

# COMMAND ----------

# Index table name
vs_index_table_fullname = f"{DA.catalog_name}.{DA.schema_name}.product_embeddings"

# Store embeddings in vector store
create_vs_index(vs_endpoint_name, vs_index_table_fullname, vs_source_table_fullname, "product")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 1: Build the First Chain (Vector Store Search)
# MAGIC
# MAGIC In this task, you will create first chain that will search for product details from the Vector Store using a dataset containing product descriptions.
# MAGIC
# MAGIC **Instructions:**
# MAGIC    - Configure components for the first chain to perform a search using the Vector Store.
# MAGIC    - Utilize the loaded dataset to generate prompts for Vector Store search queries.
# MAGIC    - Set up retrieval to extract relevant product details based on the generated prompts and search results.
# MAGIC

# COMMAND ----------

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from langchain_databricks import ChatDatabricks, DatabricksVectorSearch

# Define the Databricks Chat model: llama-3
llm_llama = <FILL_IN>

Define the prompt template for generating search queries
prompt_template_vs = <FILL_IN>(
    """
    You are a hand-crafted product design expert and your task is to creative products that are very good and can be sold online.
#
    Write a product title and description that is similar to the following product title and item details.
#
    Maximum 300 words.
#
    Use the following product title and details as example;
#
    <context>
    {context}
    </context>
#
    Question: {input}
#
    Answer:
    """
)

# Construct the RetrievalQA chain for Vector Store search
def get_retriever(persist_dir=None):
    vsc = VectorSearchClient(disable_notice=True)
    vs_index = vsc.get_index(vs_endpoint_name, vs_index_table_fullname)
    vectorstore = <FILL_IN>
    return vectorstore.<FILL_IN>

# Construct the chain for question-answering
question_answer_chain = create_stuff_documents_chain(<FILL_IN>)
chain1 = <FILL_IN>

# Invoke the chain with an example query   
response = chain1.<FILL_IN>
print(response['answer'])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 2: Build the Second Chain (Optimization)
# MAGIC
# MAGIC In this step, you will create a second chain to enhance the product details generated by the first chain. This optimization process aims to make the descriptions more compelling and SEO-friendly. In a real-world scenario, this model could be trained on your internal data or fine-tuned to align with your specific business objectives.
# MAGIC
# MAGIC **Instructions:**
# MAGIC
# MAGIC - Define a second chain using `llama-3-70b-instruct`.  
# MAGIC
# MAGIC - Create a prompt to optimize the generated product description. For example:  
# MAGIC   *"You are a marketing expert. Revise the product title and description to be SEO-friendly and more appealing to Databricks users."*
# MAGIC
# MAGIC - Use `product_details` as the parameter to be passed into the prompt.  
# MAGIC
# MAGIC - Implement the chain and test it with a sample input.  
# MAGIC

# COMMAND ----------

# Define the Databricks Chat model usinf llama-3-3-70b-instruct
llm_llama3 = <FILL_IN>

# Define the prompt template for generating search queries
quality_optimization_prompt = PromptTemplate.<FILL_IN>

chain2 = <FILL_IN>
chain2.invoke({"product_details": "Query testing product with mobile app control"})

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 3: Integrate Chains into a Multi-chain System
# MAGIC
# MAGIC In this task, you will link the individual chains created in Task 2 and Task 3 together to form a multi-chain system that can handle multi-stage reasoning.
# MAGIC
# MAGIC **Instructions:**
# MAGIC
# MAGIC - Use Databricks **`Llama Chat model`** for processing text inputs, which is defined above in the first task.
# MAGIC
# MAGIC - Create a prompt template to generate an **`HTML page`** for displaying generated product details.
# MAGIC
# MAGIC - Construct the **`Multi-Chain System`**  by combining the outputs of the previous chains. **Important**: You will need to rename the out of the first chain and second chain while passing them to the next stage. This sequential chain should be as; **chain3 = chain1 > (`product_details`) > chain2 > `(optimized_product_details)` > prompt3**.  
# MAGIC
# MAGIC - Invoke the multi-chain system with the input data to generate the HTML page for the specified product.
# MAGIC

# COMMAND ----------

from langchain.schema.runnable import RunnablePassthrough, RunnableMap
from langchain_core.output_parsers import StrOutputParser
from IPython.display import display, HTML

# Define the prompt template for generating the HTML page
prompt_template_3 = PromptTemplate.from_template(
    """Create an HTML page for the following product details:
    
    Product Description: {optimized_product_details}

    Return a valid HTML code. Don't include html head or body tags.
    """
)


# Construct the multi-chain system
chain3 = (<FILL_IN>)

# Invoke the chain with question and query
query = {
    "input": "Custom embroidered blanket with mobile app control."      
}
output_html = chain3.<FILL_IN>

# Display the generated HTML output
display(HTML(output_html))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 5: Save the Chain to Model Registry in UC
# MAGIC
# MAGIC In this task, you will save the multi-stage chain system within our Unity Catalog.
# MAGIC
# MAGIC **Instructions:**
# MAGIC
# MAGIC - Set the model retistery to UC and use the model name defined.
# MAGIC
# MAGIC - Log and register the final multi-chain system.
# MAGIC
# MAGIC - To test the registered model, load the model back from model registery and query it using a sample query. 
# MAGIC
# MAGIC After registering the chain, you can view the chain and models in the **Catalog Explorer**.

# COMMAND ----------

from mlflow.models import infer_signature
import mlflow


# Set model registry to UC
mlflow.set_registry_uri("databricks-uc")
model_name = f"{DA.catalog_name}.{DA.schema_name}.multi_stage_lab"

with mlflow.start_run(run_name="multi_stage_lab") as run:
    signature = <FILL_IN>
    model_info = mlflow.langchain.log_model(
        chain3,
        loader_fn=<FILL_IN>
        artifact_path="chain",
        registered_model_name=<FILL_IN>
        input_example=query,
        signature=signature
    )

model_uri = <FILL_IN>
model = mlflow.<FILL_IN>

output_html = model.invoke(query)
display(HTML(output_html))

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lab, you've learned how to build a multi-stage AI system using Databricks and LangChain. By integrating multiple chains, you can perform complex reasoning tasks such as searching for product details and optimizing the response based on your business needs. This approach enables the development of sophisticated AI systems capable of handling diverse tasks efficiently.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# MAGIC <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/">Support</a>