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
# MAGIC # LAB - Create a ReAct Agent
# MAGIC
# MAGIC In this lab, we will create a virtual stock advisor agent that uses the **ReAct** prompting framework. This agent will reason and act based on the prompts and tools provided.
# MAGIC
# MAGIC Of course, the agent is built for demonstration purposes and the answers shouldn't be used as investment advice!x
# MAGIC
# MAGIC
# MAGIC **Lab Outline:**
# MAGIC
# MAGIC In this lab, you will need to complete the following tasks;
# MAGIC
# MAGIC * **Task 1 :** Define the agent brain
# MAGIC
# MAGIC * **Task 2 :** Define the agent tools
# MAGIC
# MAGIC * **Task 3 :** Define an agent logic
# MAGIC
# MAGIC * **Task 4 :** Create the agent 
# MAGIC
# MAGIC * **Task 5 :** Run the agent
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
# MAGIC Before starting the lab, run the provided classroom setup scripts. These scripts will install the required libraries and configure variables which are needed for the lab.

# COMMAND ----------

# MAGIC %pip install -U -qq langchain-databricks langchain==0.3.7 langchain_community==0.3.5 yfinance==0.2.41 wikipedia==1.4.0 youtube-search duckduckgo-search
# MAGIC
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-03LAB

# COMMAND ----------

# MAGIC %md
# MAGIC **Enable MLflow Auto-Log**

# COMMAND ----------

import mlflow
mlflow.langchain.autolog()

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
# MAGIC ## Task 1: Define the Brain of the Agent
# MAGIC
# MAGIC Let's start by defining the agent brain using one of the available LLMs on Databricks.
# MAGIC
# MAGIC * For this lab, use **databricks-meta-llama-3-3-70b-instruct** 
# MAGIC
# MAGIC * Define the maximum number of tokens

# COMMAND ----------

from langchain.agents import AgentType, initialize_agent
from langchain_databricks import ChatDatabricks

# define the brain
llm_llama = <FILL_IN>

# COMMAND ----------

# let's test the brain
llm_llama.invoke("Hi! How are you?")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 2 : Define Tools that the Agent Will Use
# MAGIC
# MAGIC For an agent, the toolset is a crucial component to complete the defined task. The agent will reason about the next action to take and use an appropriate tool to complete that action.
# MAGIC
# MAGIC For our stock advisor agent, we will use the following tools:
# MAGIC
# MAGIC * **Wikipedia tool**: For searching company details. [[LangChain Doc](https://python.langchain.com/docs/integrations/tools/wikipedia/)]
# MAGIC
# MAGIC * **DuckDuckGo Search tool**: This will be used for searching the latest news and updates about a stock.[[LangChain Doc](https://python.langchain.com/docs/integrations/tools/ddg/)]
# MAGIC
# MAGIC * **YouTube search tool**: This will be used to search for review videos about the latest financial reports. [[LangChain Doc](https://python.langchain.com/docs/integrations/tools/youtube/)]

# COMMAND ----------

# MAGIC %md
# MAGIC ### Wikipedia Tool

# COMMAND ----------

from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

api_wrapper = <FILL_IN>
tool_wiki = <FILL_IN>

# COMMAND ----------

# Test the Wikipedia tool
tool_wiki.run("Apple company history")

# COMMAND ----------

# MAGIC %md
# MAGIC ### DuckDuckGo Search Tool

# COMMAND ----------

# DuckDuckGo Search Tool
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

tool_news = <FILL_IN>

# COMMAND ----------

# Test DuckDuckGo tool
tool_news.run("Latest news about Apple stock")

# COMMAND ----------

# MAGIC %md
# MAGIC ### YouTube Search Tool

# COMMAND ----------

from langchain_community.tools import YouTubeSearchTool

tool_youtube = <FILL_IN>

# COMMAND ----------

# Test the YouTube search tool 
tool_youtube.run("Apple company stock")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Define Toolset
# MAGIC
# MAGIC Next, add all tools together to be used in the next step.

# COMMAND ----------

tools = <FILL_IN>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 3: Define Agent Logic
# MAGIC
# MAGIC An agent requires a planning prompt that defines how it should **reason and act**. LangChain provides a few ready-to-use prompt templates through its **[LangChain Hub](https://smith.langchain.com/hub)**, including those that follow the **ReAct (Reason + Act)** style.
# MAGIC
# MAGIC In this task, you'll pull a pre-defined ReAct-style prompt from LangChain Hub, which is designed to work with tool-using agents.
# MAGIC
# MAGIC > 💡 Using the Hub simplifies your code and ensures you're working with prompt templates that are community-tested and regularly maintained.
# MAGIC
# MAGIC 📚 [Learn more: LangChain Agent Executor Documentation](https://python.langchain.com/docs/how_to/agent_executor/#create-the-agent)

# COMMAND ----------

# Import LangChain Hub
from langchain import hub
# Pull a ReAct-style prompt for function/tool-calling agents
prompt = hub.pull("hwchase17/openai-functions-agent")
# Display the prompt structure
prompt = <FILL_IN>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 4: Create the Agent
# MAGIC
# MAGIC The final step is to create the agent using the LLM, planning prompt and toolset.

# COMMAND ----------

from langchain.agents import AgentExecutor, create_tool_calling_agent

agent = <FILL_IN>
agent_exec  = <FILL_IN>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 5: Run the Agent
# MAGIC
# MAGIC Let's test the agent!
# MAGIC
# MAGIC Note: YouTube search might not return the best results. For better results, you could use a paid API/Service that supports better search.
# MAGIC
# MAGIC **Use this prompt:**
# MAGIC <blockquote>
# MAGIC What do you think about investing in Apple stock? Provide an overview of the latest news about the company. Next, search a video on YouTube which reviews Apple's latest financials.
# MAGIC
# MAGIC Format the final answer as HTML.
# MAGIC </blockquote>
# MAGIC

# COMMAND ----------

response = <FILL_IN>
displayHTML(response["output"])

# COMMAND ----------

# MAGIC %md
# MAGIC It seems like the agent uses company name only when searching for videos. **Let's play with the prompt to get better results.**
# MAGIC
# MAGIC In real-world, the agent would be used in a conversational way and we would just chat with the agent to tweak the search query or to adjust the response in a desired format. 
# MAGIC
# MAGIC **Use this prompt:**
# MAGIC <blockquote>
# MAGIC What do you think about investing in Apple stock? Provide an overview of the latest news about the company. Next, search a video on YouTube which reviews Apple's latest financials.
# MAGIC
# MAGIC When searching on YouTube use such as "Apple  stock finance investment earnings valuation".
# MAGIC
# MAGIC Write a nice summary of the results.
# MAGIC
# MAGIC Format the final answer as HTML.
# MAGIC </blockquote>

# COMMAND ----------

response = <FILL_IN>
displayHTML(response["output"])

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lab, you successfully created a virtual stock advisor agent using the ReAct prompting framework. By defining the agent's brain, tools, logic, and execution flow, you demonstrated how the agent can interact with various data sources to provide investment insights.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# MAGIC <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/">Support</a>