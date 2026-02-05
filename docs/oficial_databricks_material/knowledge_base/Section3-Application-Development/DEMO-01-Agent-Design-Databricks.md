# 10 - Demo Agent Design in Databricks

**Source:** `10-Demo_ Agent Design in Databricks.mp4`
**Duration:** 08:28
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

So with that, let's go and jump to a demo, talk about agent design in Databricks, right? We're going to be building an agent. We're building two agents. We're going to build one agent that uses a couple tools to go and do something out there called the bricksio. And then we're going to create a second agent and instead of using kind of external tools, in this case, we're going to give it some context such as our own data set, something like that and have it do a little bit of data science on that. So we just talked about agents, talked about multimodal and where we think the industry is going to go when it comes to more complex cognitive architectures beyond just workflows and tasks. And that's agents and really leveraging that reasoning capability of the model. So what we're going to do now is we're going to jump into and do a demo and unlike kind of the multi stage AI system where we're manually stitching things together and controlling everything. The idea with agents is can we build the same system but in an autonomous way, give the control over to the LLM to go and make those decisions, plan and figure out what tools to use to go and complete the task. That's what we're going to do here. Now by the end of this demo, we should be able to understand how to build a semi-autonomated system with LLM agents to perform internet searches and data sets using chain. We're going to use tools for the task achieve by helping the agents use those tools, explore chain's built in agents for our workflows and then talk about how we can also give agents pandas data frame to do things like data sign. So in order to do that, we're going to be actually creating two agents. We're going to be creating one agent that named Bricso that interacts with the internet, does some internet search. And then we're going to create another agent called and believe data queue or data queue. And data queue is going to look at data frame and analyze that for it. Alright, so I ran this earlier but if you're ever working with us, remember to run the requirements in the classroom setups to make sure we have the libraries and the configurations in place. And once that we have that, we can then start our agent. With agents, we have tools and we have the brain. So you can think of it, you come from the software world, the brain now acts as your application and the tools acts as all the integrations your applications connected to. So in this case, we need a brain for agent which is typically going to be a large language model. So we need to go and define that large language model we're going to use. So here we're using link chain to load up a chat model. In this case, Databricks is chat model and we're using Databricks DBRX in this case. So there's our chat model. So pretty straightforward. And the next one that we have is the tools that we're going to give our agent. So depending on the task or what we want the agent to do, this is where we want to define the tool. Now another thing when I'm looking at tools is also what tools make sense from a security standpoint too. Do we sometimes it's better to only give a limited subset or only tools that it needs? I wouldn't try to give it tools to everything. So in this case, we give it a couple tools, we give it access to we load up a couple built in ones, we give it access to the Wikipedia API, we give it access to YouTube search, as well as duck.go search, and then we're going to go and also give it access to the Python Ripple environment so it can go and run Python code. And we go and define that tool here. So here's the name Python Ripple description and then the function that it goes and runs. And then we go and define that as a tool set. So here we provide through Wikipedia, YouTube, search, and Python Ripple environment. So there's our tools. We then define our planning logic. So how do we want the LLM to go and think in reason against all these actions? So in this case, we're doing what we call the reason action loop. So we're defining a prompt template for that. So answer the following questions as best as you can. You have the following tools. We pass through the tools and then use the following format. Here's our question. The thought, the input questions should answer. You should always think about what to do. And then the tools, the action takes to be one of the tools, action input to the tool, and then the result of the action and thought. So final answer when we get there and then begin. So we pass through the question and the thought, which is the agent scratchback. So this is the structure to go and create an agent for chain. We provide that as a prompt. Now we can go and create agent with that prompt. So here we're pulling in length chain agents, pulling in the agent executor. It's a react agent. We pass through the model, the tools and the starting prompt. And then we start the execution. So here's bricksio and just in the initializing the agent, the tools, the velocity of it. And then we can invoke it a question. So here we go to invoke a question. What would be a nice movie to watch in rainy weather? Follow these steps first decide what movie would you recommend? Second, show me the trailer video of the movie you suggest. And then next, collect data about the movie using a search tool. Draw a bar chart using Python libraries. If you can't find the latest data, use some dummy data. Just show your abilities and learners. Don't use this for Python to them. And then finally, finally, funny joke about agent. So you can see here, the agent goes out and starts processing. So we'll look at the previous and then we'll run it again and see what happens. So you can see here, it recommends this movie. So this is going straight from the LM and then goes and does a YouTube search to go and grab a trailer about it. Once it's done with that, it now says, okay, I need to go and collect some data about the movie, create a bar chart. And here you can see it decides that it goes to Python to create a bar chart. And then finally, it'll tell a funny joke, why don't secret agents like to play cricket because they don't like to be stumped? Uh, funny. And then final answer, I would recommend Shawshank Redemption. Here's a movie trailer. Here's a bar chart showing the ratings and some things like that. So you can see here the agent going through and completing the path. So let's run it again and we can see it live. I'm going to run it again. And you see here, it's going through and doing those tasks. So you can see here live as it goes step-by-step you each of these tasks. We might take a little while to go and do. So you can see here, mostly the search is what took the longest part. But once it got the search down, everything else it was able to do really quickly because it was local. There you go. Example that that's bricksio. What about data queue or data queue? So data queue is going to be another agent. Now, because this agent we want to go and have it process a data frame, we're going to first define that data frame. So we're loading that data set. In this case, we're loading the Spotify data set as a data frame. Then we're going to go and define the brains and tools again. The same brain we're still going to use DVRX instruct here or prefix here and put should be sanitized by removing back ticks and things there. And then we're going to use inside link chain. There is a special agent called a data frame agent that's what we're going to do here. So we're going to use that pass through our model, our data frame, and then we can then talk to the model. So here we go. We have our agent. We're going to go talk to the agent and vote what is the artist's name of the most popular country song? And you can see here it goes through to answer the question. I need to find a row with the highest popularity value where the tractor on our country. Then I'll extract artist name from that row. But here it goes in the Python. Does some calculations to go and find the country? Seems there's no country providing the data set. In this case, it isn't able to answer the question. We can go and try to run it again. In this case, we can see it struggling to get the concept idea of the genre of country. You can see that struggling with that and sometimes they'll work and sometimes wouldn't. We'll run it again. So in this case, it's unable to figure it out. Okay, in this case, it was able to. So here, the artist name of this popular country song, artist name of this popular country song is Zach Bryant. It's sorted by popularity and then grab that. You can see here is able to figure it out. So let's look at another example. In this case, what's the total number of rows? Pretty straightforward. And you can see here it goes through the data frame and it just looks at the shape of the data frame and looks at the rows. So pretty straightforward here as well. So here you can see, instead of us having to go and control all the components to find the interface for all the components, the ideal of agents is instead, we define tools and APIs and interfaces and we let the language model reason across those tools against the task and figure out how to go and solve that problem instead. And sometimes it works and sometimes it doesn't, but that's one of the cool things that is new when it comes to elements is this reasoning capability. And Brian, how do we go and build it? SDK and a framework around this. So in this case, we showed lane chains approach to this, but there's also a lot of other frameworks and things that are trying to tackle this more autonomous approach, things like auto-gen, I think auto-gbt, there's a lot of projects that are trying to go and tackle this problem of giving the control over to the L.

---

## Timestamped Segments

**[00:00]** So with that, let's go and jump to a demo, talk about agent design in Databricks, right? We're

**[00:03]** going to be building an agent. We're building two agents. We're going to build one agent that uses

**[00:08]** a couple tools to go and do something out there called the bricksio. And then we're going to create

**[00:12]** a second agent and instead of using kind of external tools, in this case, we're going to give it some

**[00:16]** context such as our own data set, something like that and have it do a little bit of data science

**[00:21]** on that. So we just talked about agents, talked about multimodal and where we think the

**[00:28]** industry is going to go when it comes to more complex cognitive architectures beyond just

**[00:34]** workflows and tasks. And that's agents and really leveraging that reasoning capability of the

**[00:40]** model. So what we're going to do now is we're going to jump into and do a demo and unlike kind of

**[00:44]** the multi stage AI system where we're manually stitching things together and controlling everything.

**[00:49]** The idea with agents is can we build the same system but in an autonomous way, give the control

**[00:54]** over to the LLM to go and make those decisions, plan and figure out what tools to use to go and complete

**[01:00]** the task. That's what we're going to do here. Now by the end of this demo, we should be able to

**[01:04]** understand how to build a semi-autonomated system with LLM agents to perform internet searches and

**[01:08]** data sets using chain. We're going to use tools for the task achieve by helping the agents use those tools,

**[01:15]** explore chain's built in agents for our workflows and then talk about how we can also give agents

**[01:20]** pandas data frame to do things like data sign. So in order to do that, we're going to be actually

**[01:24]** creating two agents. We're going to be creating one agent that named Bricso that interacts with the

**[01:29]** internet, does some internet search. And then we're going to create another agent called

**[01:34]** and believe data queue or data queue. And data queue is going to look at data frame and analyze that

**[01:40]** for it. Alright, so I ran this earlier but if you're ever working with us, remember to run the

**[01:45]** requirements in the classroom setups to make sure we have the libraries and the configurations in

**[01:49]** place. And once that we have that, we can then start our agent. With agents, we have tools and we have

**[01:55]** the brain. So you can think of it, you come from the software world, the brain now acts as your

**[01:59]** application and the tools acts as all the integrations your applications connected to. So in this case,

**[02:05]** we need a brain for agent which is typically going to be a large language model. So we need to go and

**[02:09]** define that large language model we're going to use. So here we're using link chain to load up a chat

**[02:14]** model. In this case, Databricks is chat model and we're using Databricks DBRX in this case. So

**[02:19]** there's our chat model. So pretty straightforward. And the next one that we have is the tools that we're

**[02:24]** going to give our agent. So depending on the task or what we want the agent to do, this is where we want

**[02:29]** to define the tool. Now another thing when I'm looking at tools is also what tools make sense from a

**[02:34]** security standpoint too. Do we sometimes it's better to only give a limited subset or only tools that

**[02:39]** it needs? I wouldn't try to give it tools to everything. So in this case, we give it a couple tools,

**[02:43]** we give it access to we load up a couple built in ones, we give it access to the Wikipedia API,

**[02:51]** we give it access to YouTube search, as well as duck.go search, and then we're going to go and also give

**[02:57]** it access to the Python Ripple environment so it can go and run Python code. And we go and define

**[03:02]** that tool here. So here's the name Python Ripple description and then the function that it goes and

**[03:07]** runs. And then we go and define that as a tool set. So here we provide through Wikipedia, YouTube,

**[03:13]** search, and Python Ripple environment. So there's our tools. We then define our planning logic. So how do

**[03:20]** we want the LLM to go and think in reason against all these actions? So in this case, we're doing what we

**[03:25]** call the reason action loop. So we're defining a prompt template for that. So answer the following questions

**[03:30]** as best as you can. You have the following tools. We pass through the tools and then use the following

**[03:34]** format. Here's our question. The thought, the input questions should answer. You should always

**[03:39]** think about what to do. And then the tools, the action takes to be one of the tools, action input to

**[03:43]** the tool, and then the result of the action and thought. So final answer when we get there and then

**[03:49]** begin. So we pass through the question and the thought, which is the agent scratchback. So this is

**[03:55]** the structure to go and create an agent for chain. We provide that as a prompt. Now we can go and create

**[04:01]** agent with that prompt. So here we're pulling in length chain agents, pulling in the agent executor.

**[04:05]** It's a react agent. We pass through the model, the tools and the starting prompt. And then we start

**[04:12]** the execution. So here's bricksio and just in the initializing the agent, the tools, the velocity of

**[04:17]** it. And then we can invoke it a question. So here we go to invoke a question. What would be a nice

**[04:23]** movie to watch in rainy weather? Follow these steps first decide what movie would you recommend? Second,

**[04:27]** show me the trailer video of the movie you suggest. And then next, collect data about the movie

**[04:31]** using a search tool. Draw a bar chart using Python libraries. If you can't find the latest data,

**[04:36]** use some dummy data. Just show your abilities and learners. Don't use this for Python to them.

**[04:41]** And then finally, finally, funny joke about agent. So you can see here, the agent goes out and starts

**[04:46]** processing. So we'll look at the previous and then we'll run it again and see what happens. So you can

**[04:50]** see here, it recommends this movie. So this is going straight from the LM and then goes and does a

**[04:56]** YouTube search to go and grab a trailer about it. Once it's done with that, it now says, okay,

**[04:59]** I need to go and collect some data about the movie, create a bar chart. And here you can see it decides

**[05:05]** that it goes to Python to create a bar chart. And then finally, it'll tell a funny joke, why don't

**[05:11]** secret agents like to play cricket because they don't like to be stumped? Uh, funny. And then

**[05:16]** final answer, I would recommend Shawshank Redemption. Here's a movie trailer. Here's a bar chart

**[05:21]** showing the ratings and some things like that. So you can see here the agent going through and

**[05:26]** completing the path. So let's run it again and we can see it live. I'm going to run it again.

**[05:32]** And you see here, it's going through and doing those tasks. So you can see here live as it goes step-by-step

**[05:37]** you each of these tasks. We might take a little while to go and do. So you can see here, mostly the

**[05:41]** search is what took the longest part. But once it got the search down, everything else it was able to

**[05:44]** do really quickly because it was local. There you go. Example that that's bricksio. What about data queue

**[05:51]** or data queue? So data queue is going to be another agent. Now, because this agent we want to go

**[05:56]** and have it process a data frame, we're going to first define that data frame. So we're loading that

**[05:59]** data set. In this case, we're loading the Spotify data set as a data frame. Then we're going to go

**[06:06]** and define the brains and tools again. The same brain we're still going to use DVRX

**[06:10]** instruct here or prefix here and put should be sanitized by removing back ticks and things there.

**[06:16]** And then we're going to use inside link chain. There is a special agent called a data frame agent

**[06:22]** that's what we're going to do here. So we're going to use that pass through our model, our data frame,

**[06:27]** and then we can then talk to the model. So here we go. We have our agent. We're going to go talk to the

**[06:32]** agent and vote what is the artist's name of the most popular country song? And you can see here it goes

**[06:36]** through to answer the question. I need to find a row with the highest popularity value where the tractor

**[06:40]** on our country. Then I'll extract artist name from that row. But here it goes in the Python.

**[06:46]** Does some calculations to go and find the country?

**[06:50]** Seems there's no country providing the data set. In this case, it isn't able to answer the question.

**[06:55]** We can go and try to run it again. In this case, we can see it struggling to get the

**[07:00]** concept idea of the genre of country. You can see that struggling with that and sometimes they'll

**[07:05]** work and sometimes wouldn't. We'll run it again. So in this case, it's unable to figure it out.

**[07:17]** Okay, in this case, it was able to. So here, the artist name of this popular country song,

**[07:21]** artist name of this popular country song is Zach Bryant. It's sorted by popularity and then grab that.

**[07:26]** You can see here is able to figure it out. So let's look at another example. In this case, what's the

**[07:30]** total number of rows? Pretty straightforward. And you can see here it goes through the data frame and

**[07:35]** it just looks at the shape of the data frame and looks at the rows. So pretty straightforward here as well.

**[07:39]** So here you can see, instead of us having to go and control all the components to find the interface

**[07:45]** for all the components, the ideal of agents is instead, we define tools and APIs and interfaces and we

**[07:51]** let the language model reason across those tools against the task and figure out how to go and solve

**[07:57]** that problem instead. And sometimes it works and sometimes it doesn't, but that's one of the cool

**[08:01]** things that is new when it comes to elements is this reasoning capability. And Brian, how do we go and

**[08:09]** build it? SDK and a framework around this. So in this case, we showed lane chains approach to this,

**[08:13]** but there's also a lot of other frameworks and things that are trying to tackle this more

**[08:17]** autonomous approach, things like auto-gen, I think auto-gbt, there's a lot of projects that are

**[08:22]** trying to go and tackle this problem of giving the control over to the L.

