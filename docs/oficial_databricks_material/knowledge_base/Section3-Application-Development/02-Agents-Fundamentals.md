# 09 - Introduction to Agents

**Source:** `09-Introduction to Agents.mp4`
**Duration:** 16:17
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

What are agents, so if you think about it, we can use non-agentic and agentic workflows as an example. So far, for a lot of things that we've done in the software industry, everything is non-agentic. We have a workflow that workflow is defined into a set of stages or tasks like we did in the last module. We talked about the different intents that we go and build into chains, and we connect those chains together into systems, and that's how we go and complete some type of objective. And with generative AI, we can then implement some of these tasks using an LLM. But really, at the end, we're deciding the order of operations. For example, if I'm doing, should I invest in Nvidia stock, we start with the user prompt, and then with the user prompt, we process that and we determine some actions to do. That's hard-coded, some actions that we will do after that, and then the final output that we might go and do. And some of these actions might be LLM-based or not, but the really the idea here is the branching and the control logic of the order of operations is defined by us. Now, in an agentic workflow, things change a little bit. So if I go and say, should I invest in Nvidia stock, in this case, we have the prompt and the agent might go and figure that out. So instead of going to the internet to go and search about that, or to go and call an API to pull up Nvidia stock information or throw that into a notebook to go and research and process that and look at a trend. That can all be decided and designed and executed from the agent to go and figure that out on its own. So the agent does the research, writes the draft, figures out how to go and do that, and does it all on its own in an agentic workflow. It's really deciding these actions and looking at the results of those actions and decide what goes next. Whereas in an agentic workflow, we define this step and this step. So you can see here, this is now becoming a little less determinate. That's one of the big problems with a lot of the frameworks is because a lot of frameworks are designed to deal with determinate workflows. Whereas here, when we have the agent deciding what to do next, well, that's no longer determinate. It might end up in a loop. It might go and branch. It might go and do different things on its own and that makes it really challenging to go and build a framework right. So anyway, that's continuing the topic from the last section. But anyway, let's go and continue with agents, non-agentic and agentic workflows. So what is an agent, right? So really when we look at an agent, it's an application that can execute complex tasks by using a language model to define a sequence of actions to take, right? To reason on that task, right? For example, help me how to bake a cake, right? And then the agent will be based on what it knows about baking a cake. We're going to give us these set of steps or a recipe to go and complete that task. So far, we've discussed about compound AI systems with hard-coded calls, external tools and service. Agents replace that hard-coded sequence of actions with query-dependent sequences that can be chosen dynamically by the LLM. So these LLMs are now going to be doing some planning. They're going to be remembering where they are in that execution path. And in order to execute some of those things, they're going to use tools. So that's really what we have. We have this idea of the agent acting like a human, right? Emulating a human to go and do this task on its own. So what are some core components of a typical agentic or agent-based system? We have a task what we're actually asking it to go and do. We then have the LLM, which is acting as the reasoning engine or the brain. So I like to think instead of traditional software, we have application code. We now have an LLM acting as logic code, right? It goes and figures out high-level how to complete this task at access to brain, right? We have tools. So the LLM needs to go interact with systems. It might need to go out there and pull data from a database. It might need to go and do an API call to go and send out an email or something like that. So it needs tools, right? That's there. And then it needs memory and planning, right? So it needs to be able to define how it's going to plan those tasks, right? And figure out how to execute it. So that's the operating procedure or I like to think. In our world, we have like practices and operational processes, right? Think about planning is like, what is it's operational practice and processes, and then the memory is task management, project management, right? How does it keep track of everything that it's done, right? So far so it actually can get towards completing the task, right? Because there's a lot of sub-task that it might have to go and do on its own, right? So an example agent, let's talk about that example that we talked about with, should I invest in NVIDIA stock? So in this case, a hypothetical financial advisor agent where it acts like a financial advisor, right? Some sub-task that might need to do. Might need to decide what actions are needed in order of these actions should be done. They might need to go and look at what the current stock price is, what's the latest financials, what's the latest news about the company, what's the sentiment about it? So an agentic workflow might go and process a task, might use an LLM to understand the request to go and figure out what do I need to do to figure out it's the right time to invest in NVIDIA stock, right? I might decide I need to go and collect some data. So it goes out there, collect some financial stock price, news articles, right? And then it might do some data analysis on that data. So it might analyze and do some sentiment analysis. And once it's done with that, it'll generate its output to answer our question, right? So use that synthesized information into a coherent report that we can then use to go and make our decision on, right? For example, right? So that's an example of that. So how does it actually do all this? How does an agent decide which actions to take, right? So let's go into details of how does an agent think and how do we go and provide that into an LLM so that we can build these agentic systems. So there's agent reasoning, right? One thing that we found with LLM is that they have the ability not only to generate or be creative, but they also have the ability to reason and observe some type of output and makes observations on that, right? So the cognitive process in which artificial agents operating within domain of AI can analyze information, draw logical conclusions and make decisions autonomously, right? They're able to go and emulate a lot of these human cognitive abilities on tasks that it's learned through its training, right? So independent from language and framework, there are design patterns for agent reasoning. So that's what we're really going to be talking about here. It's like, how do I actually go and look at the workflow process and the process to give it to the model can enact like an agent? So we'll be talking about React. We'll be talking about tool use. We'll talk about planning. And then we'll talk about multi-agent calibration, which is becoming more popular this year as of right now. So the first pattern is React, which stands for Reason Act. If you look at Reason Act, the idea here is the model can reason on things, it can act on things. So for example, here, we might have some questions like aside from Apple Remote. What other device can control the program Outflow Remote was originally designed to interact with? Right, a standard question could be iPod, right? But a reasoning action could be, let's think step by step, Apple Remote was originally designed to interact with Apple TV. Apple TV can control by iPhone, iPad, and iPod touch. So the answer is iPhone, iPad, and iPod touch, right? So it's reasoning, right? That not only is it the remote, but it's also these things, right? We can also have action, right? Where it goes and acts on something. So it goes out and searches the internet for the answer, right? So Apple Remote is remote control introduced, right? It can go and search front-row and go and do some of those things. So the idea is how do we go and combine both of these things, right? The ability for it to reason on some output and the ability for it to go and decide to make an action to go and get some more information or something like that or the react pattern, right? So it enables the model to generate verbal reasoning traces and actions, right? The main stage using react agents are thought, reflect on the problem given, and the previous actions taken, act, choose the correct tool and input format to use, and then observe, evaluate the results of the action and generate the next thoughts, right? So you're really in this reason action loop, perform an action, look at the output, reason on the output, and then determine what to do next, right? Continue that again and again until it gets to a point where it reasons that it has completed the original task that we asked it to go and do. So that's the reason action loop. Now, we talk about actions, right? And part of that is we might want to give it access to other things, right? Sometimes the model on its own, with its internal knowledge just isn't enough to solve the problem, right? It needs to go to the internet, it needs to go to our internal data stores, it might need to go and do some actions, to go and do some API calls. So that's where we talk about connecting our L and giving it access to tools or integrations to other systems, right? So agents interact with external tools and APIs to perform specific tasks, right? Examples of tools are things like research and search tools for the internet and search engines, image generation tools to generate images to complete those tasks if we wanted to draw, document retrieval for grabbing information from our data stores, and then code generation if we wanted to go and write software and code or use software and code to do some tasks, right? So the agent's reasoning skills decide which tools it uses and how and when to use them, right? But depending on tools we give it, also controls what it can and can't do. The next is planning, right? So reasoning patterns, how do we want it to actually go and complete those tasks? So agents must be able to dynamically adjust their goals and plans based on changing conditions. So based on those observations that it gets during the reason action loop, it needs to be able to branch and decide different avenues to go and explore, right? So in real world scenarios, right? Real tasks have a lot of sub-tats, right? Sometimes those need to be orchestrated for yourself, right? You might have to go and manage that task or if you're a manager, you might need to distribute that task to other people to go and get that information back, right? So tasks can be single tasks, can be sequential, can be graph related, especially when it becomes more complex and things like that. So here we have an example of a query to have them generate a image that is a combination of this basketball player, slam dunking a basketball and this kid riding a scooter, right? And you can see based here, it did some analysis of the images by doing some image detection. And then once it got the image detection, it used another model to combine the pose, the extracted pose from one image into the style of another image to generate this output image, right? So you can see there in like reason against that, decided that need to do these things first to be able to do this next thing to then eventually get to the result that we wanted. So that's an example of that planning capability. So with that, that this planning capability is great for a single LM and a single agent, but there's a lot of experiments and people playing around with the idea that instead of just a single LM, what about having an LM talk to another LM or what we call multi agent collaboration? And what we've actually seen is in research, we can achieve really great things like here. I think one of the early examples of this is chat depth in which what they did was they created a CEO LLM that then hired other LLMs to act as different people in a software engineering team, right? Like a testing, a coding developer, documentation team, and things like that. And what they found is this allows us to scale to more complex tasks, right? And this pattern involves several agents working collaborative together to handle different aspects and each of those LLMs can then focus on that single task and what we find is that helps improve the performance of it. Right, there's also some research out there that has shown, especially when it comes to software development that if you use an LLM to judge the output of an LLM and work in this, I think if you remember partner pair programming, right, in school one that writes the code, one that evaluates the code, and if you do multiple cycles of this, you can achieve state-of-the-art performance with less powerful models. It's actually really cool research. But anyways, separate response to agents allows us modularization, allows the agents to specialize, and this helps us fine tune and get better performance out of our system. So what are some tools for building agents and these type of applications, right? And this is where there's a lot of excitement and there's a lot of challenges. And this year, I'm seeing a lot going on with that, right? So tools to build agents, so some notable tools and frameworks, right? There's lynching agents, of course, right? It provides a structure for building agents that can use tools and interact with the world, right? Auto GPT is really popular one. It's was based off ChatDev and it's really the idea of building agents or an LLM that controls other LLMs, right? So it's a really popular project out there to go and build that kind of system. OpenAI Function Calling, where a model is called with a set of functions defined in user query that Maul can then choose to go and call one of those functions. So very similar lynching agents, right? Except it's an openAI way of doing it. And there's also autogen, which is a framework about working with multiple agents. So defining different agents, their responsibilities, and then creating a graph structure of how these agents can talk together. And then we also have hugging face transform agents, right? Which is providing a natural language API for interacting with those transformers. Right, but really there's a lot of development and this is really where the challenge is when it comes to gender to the AI is, how do I build a framework and SDK around these systems that are non-deterministic that might not always be able to handle complex tasks? That might need a help of a human here and there. So there's really, we can't really get full autonomy on it. So there needs to be this human in the loop. How do you go and build a framework and SDK around there? But this is a snapshot of some of the popular ones today. So really, it's linked to a landscape of tools and frameworks, some that are open source. And really, we like to break it up. There's open source and propriet, when it comes to the framework, and then it comes to guided to unguided. So how much more do we want to manage the control of the flow versus how much autonomy do we want, right? With auto-GBT, you've got to being the more autonomous open source, right, and lane chain being more guided, right? So examples of that. So with that, let's go in and talk about a simple agent with lane chain. So in this case, we've defined a couple of tools. Remember the agent, we have LM, we need to give it tools. And then with that, we can then let the agent go out and do its thing, right? So in this case, we might go and build a application to go and deal with some weather information, right? So we give it some information, right? So here, we define two tools, a tool to calculate a circle circumference, given its radius, and then a tool here that does some retrieval that goes out and retrieves some weather information, right? And then with that, we can then go and give that as tools to the agent, right? So you can see here, we've defined the LM that we want to use or the brain, in this case, open AI, LM, and then we registered the two tools that we created, and then we give those tools to the agent and initialize the agent with those tools, right? And then it can go out and then do the thing, right? And I'll show this in the demo later. So really simple and straightforward, but then there's a lot of challenges here. One of them is that the agent can figure it out, one of those kind of things, right? So there's a lot of development here and figuring out what's the right way to structure the APIs and things like that. Okay, so that's cool. We can go and work with that. Now, what about multi-modal AI? So there's a lot of talk about AI's that are not only text-based but are also image, vision-based, right? An audio-based that you can talk to that can see the world and interact more than just via text, right, or digital, right? So multi-modal AI are models that go beyond text, right? They can go and look at images in tons of other things. So common today is image, audio, video, kind of information or multi-modal LMS. And these are current kind of state-of-the-art active models that are being developed, right? It's multi-modal retrieval where the models can understand more than just text. It can understand images and text, right? So there's a lot of challenges when it comes to each modality. There's a lot of development right now and creating embedding models and things that can span across multi-modal. Clip is a popular one for spanning across text and image data and things like that. And then we also have multi-modal generators, right? Models that not only can understand inputs and image and text but also can generate an image and text as well, right? So really they like the input side and the output side. So doing both. So multi-modal architectures, a sample of a couple of them. So how does it kind of work? So when it looks to multi-modal, we're trying to build something like that. We typically have to go and process our information before we can use it. So there's a lot of this pre-processing that we might do so that can be a set of images and text that we go and inject or in process. And then we can then process that with embedding model and put it into our vector store that then we can then leverage when we go and do our queries. So once we have that, we can then use that as the input into our multiple LM to go and generate images and responses, right? And you actually get to go and do this a little bit in your lab, right? But the key piece here is really these embedding models that are able to map between the image domain and the text domain, so that when we do a search, we can pull images and text that are related to that, and then a model that understands images and text to then process that and then generate outputs that are like that as well.

---

## Timestamped Segments

**[00:00]** What are agents, so if you think about it,

**[00:03]** we can use non-agentic and agentic workflows as an example.

**[00:07]** So far, for a lot of things that we've done in the software industry,

**[00:10]** everything is non-agentic.

**[00:12]** We have a workflow that workflow is defined

**[00:15]** into a set of stages or tasks like we did in the last module.

**[00:19]** We talked about the different intents

**[00:21]** that we go and build into chains,

**[00:22]** and we connect those chains together into systems,

**[00:25]** and that's how we go and complete some type of objective.

**[00:28]** And with generative AI,

**[00:29]** we can then implement some of these tasks using an LLM.

**[00:33]** But really, at the end,

**[00:35]** we're deciding the order of operations.

**[00:38]** For example, if I'm doing,

**[00:39]** should I invest in Nvidia stock,

**[00:41]** we start with the user prompt,

**[00:43]** and then with the user prompt,

**[00:44]** we process that and we determine some actions to do.

**[00:48]** That's hard-coded, some actions that we will do after that,

**[00:50]** and then the final output that we might go and do.

**[00:52]** And some of these actions might be LLM-based or not,

**[00:56]** but the really the idea here is the branching

**[00:58]** and the control logic of the order of operations

**[01:00]** is defined by us.

**[01:02]** Now, in an agentic workflow, things change a little bit.

**[01:06]** So if I go and say, should I invest in Nvidia stock,

**[01:09]** in this case, we have the prompt

**[01:10]** and the agent might go and figure that out.

**[01:12]** So instead of going to the internet to go and search about that,

**[01:15]** or to go and call an API to pull up Nvidia stock information

**[01:19]** or throw that into a notebook to go and research

**[01:22]** and process that and look at a trend.

**[01:24]** That can all be decided and designed and executed

**[01:28]** from the agent to go and figure that out on its own.

**[01:30]** So the agent does the research, writes the draft,

**[01:33]** figures out how to go and do that,

**[01:35]** and does it all on its own in an agentic workflow.

**[01:37]** It's really deciding these actions

**[01:39]** and looking at the results of those actions

**[01:41]** and decide what goes next.

**[01:42]** Whereas in an agentic workflow,

**[01:44]** we define this step and this step.

**[01:46]** So you can see here, this is now becoming a little less determinate.

**[01:50]** That's one of the big problems with a lot of the frameworks

**[01:52]** is because a lot of frameworks are designed

**[01:54]** to deal with determinate workflows.

**[01:56]** Whereas here, when we have the agent deciding what to do next,

**[01:59]** well, that's no longer determinate.

**[02:00]** It might end up in a loop.

**[02:01]** It might go and branch.

**[02:02]** It might go and do different things on its own

**[02:04]** and that makes it really challenging

**[02:06]** to go and build a framework right.

**[02:07]** So anyway, that's continuing the topic from the last section.

**[02:10]** But anyway, let's go and continue with agents,

**[02:13]** non-agentic and agentic workflows.

**[02:15]** So what is an agent, right?

**[02:16]** So really when we look at an agent,

**[02:18]** it's an application that can execute complex tasks

**[02:21]** by using a language model to define

**[02:23]** a sequence of actions to take, right?

**[02:24]** To reason on that task, right?

**[02:26]** For example, help me how to bake a cake, right?

**[02:29]** And then the agent will be based on what it knows

**[02:30]** about baking a cake.

**[02:31]** We're going to give us these set of steps or a recipe

**[02:33]** to go and complete that task.

**[02:35]** So far, we've discussed about compound AI systems

**[02:37]** with hard-coded calls, external tools and service.

**[02:40]** Agents replace that hard-coded sequence of actions

**[02:43]** with query-dependent sequences that can be chosen dynamically

**[02:46]** by the LLM.

**[02:48]** So these LLMs are now going to be doing some planning.

**[02:50]** They're going to be remembering where they are

**[02:51]** in that execution path.

**[02:53]** And in order to execute some of those things,

**[02:55]** they're going to use tools.

**[02:56]** So that's really what we have.

**[02:57]** We have this idea of the agent acting like a human, right?

**[03:00]** Emulating a human to go and do this task on its own.

**[03:03]** So what are some core components of a typical agentic

**[03:06]** or agent-based system?

**[03:07]** We have a task what we're actually asking it to go and do.

**[03:10]** We then have the LLM, which is acting as the reasoning

**[03:13]** engine or the brain.

**[03:14]** So I like to think instead of traditional software,

**[03:16]** we have application code.

**[03:17]** We now have an LLM acting as logic code, right?

**[03:20]** It goes and figures out high-level

**[03:21]** how to complete this task at access to brain, right?

**[03:24]** We have tools.

**[03:25]** So the LLM needs to go interact with systems.

**[03:28]** It might need to go out there and pull data from a database.

**[03:31]** It might need to go and do an API call to go and send out

**[03:34]** an email or something like that.

**[03:36]** So it needs tools, right?

**[03:38]** That's there.

**[03:38]** And then it needs memory and planning, right?

**[03:40]** So it needs to be able to define how it's

**[03:43]** going to plan those tasks, right?

**[03:44]** And figure out how to execute it.

**[03:46]** So that's the operating procedure or I like to think.

**[03:48]** In our world, we have like practices and operational

**[03:51]** processes, right?

**[03:52]** Think about planning is like, what is it's operational practice

**[03:55]** and processes, and then the memory is task management,

**[03:58]** project management, right?

**[03:59]** How does it keep track of everything that it's done, right?

**[04:02]** So far so it actually can get towards completing the task, right?

**[04:05]** Because there's a lot of sub-task that

**[04:06]** it might have to go and do on its own, right?

**[04:08]** So an example agent, let's talk about that example

**[04:11]** that we talked about with, should I invest in NVIDIA stock?

**[04:14]** So in this case, a hypothetical financial advisor agent

**[04:17]** where it acts like a financial advisor, right?

**[04:19]** Some sub-task that might need to do.

**[04:21]** Might need to decide what actions are needed in order

**[04:23]** of these actions should be done.

**[04:24]** They might need to go and look at what the current stock price is,

**[04:26]** what's the latest financials, what's the latest news

**[04:28]** about the company, what's the sentiment about it?

**[04:31]** So an agentic workflow might go and process a task,

**[04:33]** might use an LLM to understand the request to go and figure out

**[04:37]** what do I need to do to figure out

**[04:39]** it's the right time to invest in NVIDIA stock, right?

**[04:41]** I might decide I need to go and collect some data.

**[04:43]** So it goes out there, collect some financial stock

**[04:45]** price, news articles, right?

**[04:47]** And then it might do some data analysis on that data.

**[04:50]** So it might analyze and do some sentiment analysis.

**[04:52]** And once it's done with that, it'll generate its output

**[04:55]** to answer our question, right?

**[04:56]** So use that synthesized information

**[04:57]** into a coherent report that we can then use

**[05:01]** to go and make our decision on, right?

**[05:02]** For example, right?

**[05:04]** So that's an example of that.

**[05:06]** So how does it actually do all this?

**[05:09]** How does an agent decide which actions to take, right?

**[05:13]** So let's go into details of how does an agent think

**[05:16]** and how do we go and provide that into an LLM

**[05:19]** so that we can build these agentic systems.

**[05:22]** So there's agent reasoning, right?

**[05:23]** One thing that we found with LLM is that they have the ability

**[05:26]** not only to generate or be creative,

**[05:29]** but they also have the ability to reason

**[05:31]** and observe some type of output

**[05:34]** and makes observations on that, right?

**[05:35]** So the cognitive process in which artificial agents

**[05:38]** operating within domain of AI can analyze information,

**[05:41]** draw logical conclusions and make decisions autonomously, right?

**[05:44]** They're able to go and emulate a lot of these human

**[05:47]** cognitive abilities on tasks that it's learned through its training, right?

**[05:51]** So independent from language and framework,

**[05:53]** there are design patterns for agent reasoning.

**[05:55]** So that's what we're really going to be talking about here.

**[05:56]** It's like, how do I actually go and look at the workflow process

**[06:00]** and the process to give it to the model

**[06:03]** can enact like an agent?

**[06:04]** So we'll be talking about React.

**[06:06]** We'll be talking about tool use.

**[06:07]** We'll talk about planning.

**[06:08]** And then we'll talk about multi-agent calibration,

**[06:10]** which is becoming more popular this year as of right now.

**[06:14]** So the first pattern is React, which stands for Reason Act.

**[06:17]** If you look at Reason Act, the idea here is the model

**[06:20]** can reason on things, it can act on things.

**[06:23]** So for example, here, we might have some questions

**[06:26]** like aside from Apple Remote.

**[06:27]** What other device can control the program

**[06:30]** Outflow Remote was originally designed to interact with?

**[06:32]** Right, a standard question could be iPod, right?

**[06:34]** But a reasoning action could be,

**[06:36]** let's think step by step,

**[06:37]** Apple Remote was originally designed to interact

**[06:39]** with Apple TV.

**[06:40]** Apple TV can control by iPhone, iPad, and iPod touch.

**[06:43]** So the answer is iPhone, iPad, and iPod touch, right?

**[06:45]** So it's reasoning, right?

**[06:46]** That not only is it the remote, but it's also these things, right?

**[06:50]** We can also have action, right?

**[06:51]** Where it goes and acts on something.

**[06:53]** So it goes out and searches the internet for the answer, right?

**[06:56]** So Apple Remote is remote control introduced, right?

**[06:58]** It can go and search front-row and go

**[07:00]** and do some of those things.

**[07:01]** So the idea is how do we go and combine both of these things, right?

**[07:04]** The ability for it to reason on some output

**[07:06]** and the ability for it to go and decide to make an action

**[07:09]** to go and get some more information or something like that

**[07:11]** or the react pattern, right?

**[07:13]** So it enables the model to generate verbal reasoning traces

**[07:15]** and actions, right?

**[07:17]** The main stage using react agents are thought,

**[07:19]** reflect on the problem given, and the previous actions taken,

**[07:22]** act, choose the correct tool and input format to use,

**[07:25]** and then observe, evaluate the results of the action

**[07:27]** and generate the next thoughts, right?

**[07:29]** So you're really in this reason action loop,

**[07:31]** perform an action, look at the output,

**[07:33]** reason on the output, and then determine what to do next, right?

**[07:36]** Continue that again and again until it gets to a point

**[07:39]** where it reasons that it has completed the original task

**[07:42]** that we asked it to go and do.

**[07:44]** So that's the reason action loop.

**[07:45]** Now, we talk about actions, right?

**[07:47]** And part of that is we might want to give it access

**[07:49]** to other things, right?

**[07:50]** Sometimes the model on its own,

**[07:52]** with its internal knowledge just isn't enough

**[07:54]** to solve the problem, right?

**[07:55]** It needs to go to the internet,

**[07:56]** it needs to go to our internal data stores,

**[07:58]** it might need to go and do some actions,

**[08:00]** to go and do some API calls.

**[08:02]** So that's where we talk about connecting our L and giving it

**[08:06]** access to tools or integrations to other systems, right?

**[08:10]** So agents interact with external tools and APIs

**[08:12]** to perform specific tasks, right?

**[08:14]** Examples of tools are things like research and search tools

**[08:16]** for the internet and search engines, image generation tools

**[08:19]** to generate images to complete those tasks

**[08:21]** if we wanted to draw, document retrieval

**[08:23]** for grabbing information from our data stores,

**[08:26]** and then code generation if we wanted to go and write software

**[08:29]** and code or use software and code to do some tasks, right?

**[08:32]** So the agent's reasoning skills decide which tools it uses

**[08:36]** and how and when to use them, right?

**[08:38]** But depending on tools we give it,

**[08:40]** also controls what it can and can't do.

**[08:42]** The next is planning, right?

**[08:44]** So reasoning patterns, how do we want it to actually go

**[08:46]** and complete those tasks?

**[08:48]** So agents must be able to dynamically adjust their goals

**[08:50]** and plans based on changing conditions.

**[08:52]** So based on those observations that it gets

**[08:54]** during the reason action loop,

**[08:56]** it needs to be able to branch and decide

**[08:58]** different avenues to go and explore, right?

**[09:00]** So in real world scenarios, right?

**[09:02]** Real tasks have a lot of sub-tats, right?

**[09:04]** Sometimes those need to be orchestrated for yourself, right?

**[09:07]** You might have to go and manage that task or if you're a manager,

**[09:09]** you might need to distribute that task to other people

**[09:12]** to go and get that information back, right?

**[09:13]** So tasks can be single tasks, can be sequential,

**[09:16]** can be graph related, especially when it becomes more complex

**[09:19]** and things like that.

**[09:20]** So here we have an example of a query

**[09:24]** to have them generate a image that is a combination

**[09:28]** of this basketball player, slam dunking a basketball

**[09:31]** and this kid riding a scooter, right?

**[09:33]** And you can see based here, it did some analysis

**[09:37]** of the images by doing some image detection.

**[09:39]** And then once it got the image detection,

**[09:41]** it used another model to combine the pose,

**[09:43]** the extracted pose from one image into the style

**[09:46]** of another image to generate this output image, right?

**[09:48]** So you can see there in like reason against that,

**[09:50]** decided that need to do these things first

**[09:52]** to be able to do this next thing

**[09:54]** to then eventually get to the result that we wanted.

**[09:56]** So that's an example of that planning capability.

**[09:58]** So with that, that this planning capability is great

**[10:01]** for a single LM and a single agent,

**[10:03]** but there's a lot of experiments

**[10:05]** and people playing around with the idea

**[10:06]** that instead of just a single LM,

**[10:08]** what about having an LM talk to another LM

**[10:10]** or what we call multi agent collaboration?

**[10:13]** And what we've actually seen is in research,

**[10:15]** we can achieve really great things like here.

**[10:17]** I think one of the early examples of this is chat depth

**[10:20]** in which what they did was they created a CEO LLM

**[10:24]** that then hired other LLMs to act as different people

**[10:28]** in a software engineering team, right?

**[10:30]** Like a testing, a coding developer, documentation team,

**[10:33]** and things like that.

**[10:34]** And what they found is this allows us to scale

**[10:37]** to more complex tasks, right?

**[10:38]** And this pattern involves several agents

**[10:40]** working collaborative together to handle different aspects

**[10:43]** and each of those LLMs can then focus on that single task

**[10:46]** and what we find is that helps improve the performance of it.

**[10:49]** Right, there's also some research out there

**[10:50]** that has shown, especially when it comes to software development

**[10:54]** that if you use an LLM to judge the output of an LLM

**[10:57]** and work in this, I think if you remember partner pair programming,

**[11:00]** right, in school one that writes the code,

**[11:02]** one that evaluates the code,

**[11:03]** and if you do multiple cycles of this,

**[11:05]** you can achieve state-of-the-art performance

**[11:07]** with less powerful models.

**[11:09]** It's actually really cool research.

**[11:10]** But anyways, separate response to agents allows us

**[11:13]** modularization, allows the agents to specialize,

**[11:15]** and this helps us fine tune

**[11:17]** and get better performance out of our system.

**[11:20]** So what are some tools for building agents

**[11:23]** and these type of applications, right?

**[11:25]** And this is where there's a lot of excitement

**[11:27]** and there's a lot of challenges.

**[11:28]** And this year, I'm seeing a lot going on with that, right?

**[11:31]** So tools to build agents,

**[11:32]** so some notable tools and frameworks, right?

**[11:34]** There's lynching agents, of course, right?

**[11:35]** It provides a structure for building agents

**[11:37]** that can use tools and interact with the world, right?

**[11:40]** Auto GPT is really popular one.

**[11:41]** It's was based off ChatDev and it's really the idea

**[11:44]** of building agents or an LLM that controls other LLMs, right?

**[11:48]** So it's a really popular project out there

**[11:50]** to go and build that kind of system.

**[11:52]** OpenAI Function Calling, where a model is called

**[11:54]** with a set of functions defined in user query

**[11:56]** that Maul can then choose to go and call one of those functions.

**[12:00]** So very similar lynching agents, right?

**[12:01]** Except it's an openAI way of doing it.

**[12:03]** And there's also autogen, which is a framework

**[12:05]** about working with multiple agents.

**[12:07]** So defining different agents, their responsibilities,

**[12:09]** and then creating a graph structure

**[12:11]** of how these agents can talk together.

**[12:12]** And then we also have hugging face transform agents, right?

**[12:15]** Which is providing a natural language API

**[12:17]** for interacting with those transformers.

**[12:19]** Right, but really there's a lot of development

**[12:21]** and this is really where the challenge is

**[12:22]** when it comes to gender to the AI is,

**[12:23]** how do I build a framework and SDK around these systems

**[12:27]** that are non-deterministic that might not always

**[12:30]** be able to handle complex tasks?

**[12:32]** That might need a help of a human here and there.

**[12:34]** So there's really, we can't really get full autonomy on it.

**[12:37]** So there needs to be this human in the loop.

**[12:38]** How do you go and build a framework and SDK around there?

**[12:40]** But this is a snapshot of some of the popular ones today.

**[12:44]** So really, it's linked to a landscape of tools and frameworks,

**[12:46]** some that are open source.

**[12:48]** And really, we like to break it up.

**[12:49]** There's open source and propriet, when it comes to the framework,

**[12:52]** and then it comes to guided to unguided.

**[12:54]** So how much more do we want to manage the control

**[12:57]** of the flow versus how much autonomy do we want, right?

**[13:00]** With auto-GBT, you've got to being the more autonomous open

**[13:02]** source, right, and lane chain being more guided, right?

**[13:05]** So examples of that.

**[13:06]** So with that, let's go in and talk about a simple agent

**[13:09]** with lane chain.

**[13:10]** So in this case, we've defined a couple of tools.

**[13:12]** Remember the agent, we have LM, we need to give it tools.

**[13:14]** And then with that, we can then let the agent go out

**[13:16]** and do its thing, right?

**[13:17]** So in this case, we might go and build a application

**[13:20]** to go and deal with some weather information, right?

**[13:24]** So we give it some information, right?

**[13:25]** So here, we define two tools, a tool to calculate

**[13:29]** a circle circumference, given its radius,

**[13:32]** and then a tool here that does some retrieval that goes out

**[13:35]** and retrieves some weather information, right?

**[13:37]** And then with that, we can then go and give

**[13:39]** that as tools to the agent, right?

**[13:41]** So you can see here, we've defined the LM

**[13:43]** that we want to use or the brain, in this case, open AI, LM,

**[13:47]** and then we registered the two tools that we created,

**[13:50]** and then we give those tools to the agent

**[13:52]** and initialize the agent with those tools, right?

**[13:54]** And then it can go out and then do the thing, right?

**[13:56]** And I'll show this in the demo later.

**[13:59]** So really simple and straightforward, but then there's

**[14:02]** a lot of challenges here.

**[14:03]** One of them is that the agent can figure it out,

**[14:04]** one of those kind of things, right?

**[14:06]** So there's a lot of development here

**[14:07]** and figuring out what's the right way to structure the APIs

**[14:10]** and things like that.

**[14:11]** Okay, so that's cool.

**[14:12]** We can go and work with that.

**[14:13]** Now, what about multi-modal AI?

**[14:16]** So there's a lot of talk about AI's that are not only text-based

**[14:20]** but are also image, vision-based, right?

**[14:23]** An audio-based that you can talk to that can see the world

**[14:26]** and interact more than just via text, right, or digital, right?

**[14:30]** So multi-modal AI are models that go beyond text, right?

**[14:34]** They can go and look at images in tons of other things.

**[14:37]** So common today is image, audio, video, kind of information

**[14:41]** or multi-modal LMS.

**[14:43]** And these are current kind of state-of-the-art active models

**[14:46]** that are being developed, right?

**[14:47]** It's multi-modal retrieval where the models can understand

**[14:51]** more than just text.

**[14:52]** It can understand images and text, right?

**[14:54]** So there's a lot of challenges when it comes to each modality.

**[14:57]** There's a lot of development right now

**[14:58]** and creating embedding models and things

**[15:00]** that can span across multi-modal.

**[15:02]** Clip is a popular one for spanning across text and image data

**[15:06]** and things like that.

**[15:08]** And then we also have multi-modal generators, right?

**[15:10]** Models that not only can understand inputs and image and text

**[15:15]** but also can generate an image and text as well, right?

**[15:18]** So really they like the input side and the output side.

**[15:20]** So doing both.

**[15:21]** So multi-modal architectures, a sample of a couple of them.

**[15:23]** So how does it kind of work?

**[15:25]** So when it looks to multi-modal,

**[15:27]** we're trying to build something like that.

**[15:28]** We typically have to go and process our information

**[15:31]** before we can use it.

**[15:32]** So there's a lot of this pre-processing that we might do

**[15:34]** so that can be a set of images and text that we go

**[15:38]** and inject or in process.

**[15:42]** And then we can then process that with embedding model

**[15:44]** and put it into our vector store

**[15:46]** that then we can then leverage when we go and do our queries.

**[15:49]** So once we have that, we can then use that as the input

**[15:53]** into our multiple LM to go and generate images and responses,

**[15:57]** right?

**[15:58]** And you actually get to go and do this a little bit in your lab, right?

**[16:00]** But the key piece here is really these embedding models

**[16:02]** that are able to map between the image domain

**[16:04]** and the text domain, so that when we do a search,

**[16:06]** we can pull images and text that are related to that,

**[16:08]** and then a model that understands images and text

**[16:11]** to then process that and then generate outputs

**[16:13]** that are like that as well.

