# Demo Deplo

**Source:** `Generative AI Application Deployment and Monitoring - Demo Deplo.mp4`
**Duration:** 14:17
**Language:** en (detected with 100.0% confidence)

---

## Full Transcription

So in the next demo, we will pre-load an existing chain or model that has been already developed. We'll deploy that to a model serving endpoint, show how this can be done programmatically, and via the model serving UI, and once that endpoint is up and running, we'll query it using the different clients made available to us. So let's jump back into our Databricks environment to demo number two. Real-time model deployment. So the assumption here is that the model has been already created in Unity Catalog based on a build script. And what we're going to do at this point is just point to the model name, which is located under my catalog and my schema on the RAG app. Make sure to have MLflow point to the Databricks Unity Catalog registry. Do a quick sanity check that the model was created. Grab the last version, which is version one, because only one model of the version has been created. So with that information in hand, there are two ways, or even three, to deploy that given model or custom model to a model serving endpoint. Now in terms of authentication or accessing that endpoint, there are many ways that you can control who or what type of access control could access that endpoint. One of them is to host the Databricks access token as in via the secret and the host and the URL as Databricks secret. So that is one way. The other way is to use things such as instance profile or whatnot. But here for sake of simplicity, the assumption is that we recreated secrets containing the Databricks host. So the URL of where that endpoint is and the personal access token. And with that in mind, any request coming to that endpoint needs to be using that specific access token in order to consume the endpoint. Otherwise, the requests are going to be rejected. With the assumption that the model exists, sorry, it's already been logged in on Unity Catalog. You've defined your authentication method to the endpoint. So here we are just going to use our secrets and create our environment variables for the token and the host. The first, let's say the programmatic way because if we're thinking about automating things, the programmatic way to deploy the model is to use the Databricks SDK API. So as part of the SDK has a serving service made available with a couple of wrapper glasses or method. So the first thing that you need to do is define the configuration of your input. As part of this configuration, you can list all the models that you would want to deploy. Starting by the model name, so the three level namespace of the model, which version? Do I want my endpoint to scale to zero? So in case there's no request, scale it down and don't charge me for any CPU or GPU hour. The workload size, so there are many sizes going from small to large or even extra large. The environment variables, any environment variables. So if the chain you've logged needs to use specific environment variables to access also other services. This is where you would create these environment variables. And notice that we've used the secrets syntax to avoid exposing that in code. You could also set the traffic configuration route as well. So if you're serving multiple endpoints, you can set like how the traffic split would want to be for each one of the models or the served models and enabling the inference table if through this auto capture config parameters in which you define in which catalog do you want to store that inference table under which schema? And what would the prefix of the table be? So once you create this configuration object for the endpoint, you can create the endpoint using the workspace client from the data request SDK. So once you instantiate the client, you define a serving endpoint name automatically. We'll do a quick sanity check to see if the endpoint exists. And then if it doesn't, we will create one using the workspace client serving endpoints API, which expose a create and wait method. So if I execute, I'm going to run that script telling me that the endpoint doesn't exist and it's going to spin it up. So that might take depending on the availability, maybe seven to ten minutes. While the script is running, another thing that another way to programmatically deploy a model is to use the MLflow deploy client methods. So technically the way it works is you instantiate a client. You can either point to data breaks or your local host. And once that client is instantiated, you just use the create endpoint method by just telling it the endpoint name and the configuration of that endpoint. And that's it. So that's again another way to use the programmatically deploy any model under your MLflow or Unity catalog registry to a given endpoint. Now the other way to do that to create a serving to also create a serving endpoint is to do that via the serving UI. So if you go to the serving UI, you can also create the endpoint programmatically. Also another, let's say, shortcut to do that is if you go to your catalog, go directly to the model itself, which is here. I can also serve this model by a click of a button. So it will get me to the model serving UI and create this specific shortcut. What is UI exposing here? You give an endpoint the name and then you can create multiple entities. So here it pre-populated the entity with my model and a version. And the other thing that you can decide is the compute type. As you can see, if you're trying to deploy the language model directly or transformer model, you can serve that on a GPU type of hardware. Here again, because we're serving a chain and nothing's happening on that chain, expect we're just doing retrieval on the vector search level and we're doing the completion or generation using the foundation model API. It is a very common practice to deploy the chain on a very lightweight CPU. And you can decide the concurrency level. So based on how much request you're expecting to get between small, medium, large, enable that scale to zero, create your environment variables, set an instance profile. Again, if you only want specific AWS services to access that endpoint or if the endpoint needs to access other resources, it will use any given instance profile. And what you can also do is create new entities. And that entity could be another model. So it could be another version of your model. So let me pick another random model here. And I can choose the version and I can say that, okay, I want the traffic for that version to be 5050, etc. That's pretty much resume the UI. There's a couple of other options that I haven't gone to if you want to create an endpoint, which point to an external model as well. But the other thing that other capabilities is root optimization. So if you want to minimize the handshake for the network authentication, root optimization allows to do that. You can tag your end points as you as for any resource. All is recommended for tracking costs or attaching it to specific projects or product. And you can enable that inference table or the auto-acapture config. So here when you enable it, you just point to the catalog, the schema, and what the table prefix will be. What's going to happen here is it will just add the suffix with the underscore payload to that table prefix that you provide. That's it. So as you can see, there are many ways. You can quickly buy the model, get to the serving UI. You can go to the model serving endpoint and create an endpoint from scratch. What not? Let's take a quick look. Here, I can see that my endpoint is still provisioning. It's still trying to update. Let's give it a couple of minutes. Now that the endpoint is ready, I can go back to my notebook and start doing inference first using the SDK. So that's given that we created a rack system asking question about archive papers with regard to. So we'll ask the question of what is PBO for proximal policy optimization, which is an RLHF alignment technique. And the first way we can query the inference endpoint is also using the Databricks SDK, a workspace client, which via the serving class, which also exposes a query method. So with the query method, you just point to your serving endpoint name and provide the inputs. Now the format of the inputs is support different types. This is more of the tensor format. You can also have the data frame split or records. It's really up to you. So here I can see that I got my answers on proximal policy. The other way also I can invoke this endpoint is using the MLflow deploy clients. So the same thing, making sure you're pointing it to your Databricks deployment, is going to expose a predict method on the endpoint. So now that we did those inference, we can go and check how the inference table got populated with these two queries. So let me jump back to my serving endpoint and that endpoint that I just recently deployed. So once the endpoint is deployed, what you can see here in the endpoint page is the list of the models who have been deployed. You can also take a look at the hardware infrastructure metrics such as requests error rates, the CPU usage, the memory usage, the concur and CE levels and what not. All these hardware related system metrics are made available via also via API. And what you'll see here that the inference table is enabled and there will be a hyperlink to that inference table. And other things that you can also do via the UI is to query the endpoint via the UI. If you've provided an input signature, this is with Automatically like a template on how the input format should be can show up. So here I can send the requests as well using the DataFrame split and let's say format and I'm going to get my output in my predictions. Now let's take a quick look at how the inference table look like from the UI. So again, that table has been automatically created with it has a predefined schema. So the client requests ID, maybe on the application side, there might be a specific identifier that you want to track. That's something you would populate the Databricks request ID. So that is automatically generated by the system, the date, time stamp, status code, how much time the request took to process, what was in the payload of the request, what were the output, the sampling fraction and all the metadata associated to it. So I as a metadata important, it is because it will contain all the information with regards to the model and the model identifier, which was used under the hood. So let's just give it a couple of seconds for the inference table to persist the payloads. So once the payloads are persisted, let's do a quick check. Yeah, I can see the current request that I've made with the status code 200. So 200 means successful, other status code, my minutes fail. I can see my input query, which is what is ppo and I can see the response generated by my chain with model metadata information. So the model name, the endpoint name and the model version, which is what is going to allow you to do some online monitoring or an evaluation of your system and doing that also for a specific model ID or model version. So with this inference table enabled, this is going to be our main gateway to be able to monitor our endpoint in quasi real time or monitor the online performance of any deployed LLM or RAC chain in the Databricks infrastructure. So the benefits to conclude of the model serving is, as you've seen, it is a very easy simple API call or point and click where given that the infrastructure is managed for you, it reduces your operational costs and facilitates the ML life cycle. And as you can see, any data scientist can self serve himself without having to deal with infrastructure management or worry about spinning up containers or doing all the work of an ML engineer. The fact that the endpoint has auto scaling enabled and scaled to zero allows you to make sure that you can address potential peaks, concurrency peaks throughout the day and scale it to zero to minimize your cost whenever there's no request going to the endpoint. And it's that same API which can work for both custom models that you built yourself, foundational models and even external models.

---

## Timestamped Segments

**[00:00]** So in the next demo, we will pre-load an existing chain or model that has been already developed.

**[00:07]** We'll deploy that to a model serving endpoint, show how this can be done programmatically,

**[00:13]** and via the model serving UI, and once that endpoint is up and running,

**[00:18]** we'll query it using the different clients made available to us.

**[00:23]** So let's jump back into our Databricks environment to demo number two.

**[00:29]** Real-time model deployment. So the assumption here is that the model has been already created

**[00:37]** in Unity Catalog based on a build script. And what we're going to do at this point is just point

**[00:45]** to the model name, which is located under my catalog and my schema on the RAG app.

**[00:50]** Make sure to have MLflow point to the Databricks Unity Catalog registry.

**[00:57]** Do a quick sanity check that the model was created. Grab the last version, which is version

**[01:03]** one, because only one model of the version has been created. So with that information in hand,

**[01:10]** there are two ways, or even three, to deploy that given model or custom model to a model serving

**[01:16]** endpoint. Now in terms of authentication or accessing that endpoint, there are many ways that you can

**[01:25]** control who or what type of access control could access that endpoint. One of them is to host

**[01:34]** the Databricks access token as in via the secret and the host and the URL as Databricks secret.

**[01:42]** So that is one way. The other way is to use things such as instance profile or whatnot.

**[01:47]** But here for sake of simplicity, the assumption is that we

**[01:51]** recreated secrets containing the Databricks host. So the URL of where that endpoint is

**[01:57]** and the personal access token. And with that in mind, any request coming to that endpoint needs to

**[02:05]** be using that specific access token in order to consume the endpoint. Otherwise, the requests are

**[02:09]** going to be rejected. With the assumption that the model exists, sorry, it's already been logged in

**[02:15]** on Unity Catalog. You've defined your authentication method to the endpoint. So here we are just going to use

**[02:20]** our secrets and create our environment variables for the token and the host.

**[02:25]** The first, let's say the programmatic way because if we're thinking about automating things,

**[02:30]** the programmatic way to deploy the model is to use the Databricks SDK API.

**[02:36]** So as part of the SDK has a serving service made available with a couple of

**[02:42]** wrapper glasses or method. So the first thing that you need to do is define the configuration of your

**[02:49]** input. As part of this configuration, you can list all the models that you would want to deploy.

**[02:56]** Starting by the model name, so the three level namespace of the model, which version?

**[03:02]** Do I want my endpoint to scale to zero? So in case there's no request, scale it down and don't

**[03:08]** charge me for any CPU or GPU hour. The workload size, so there are many sizes going from small to large

**[03:16]** or even extra large. The environment variables, any environment variables. So if the chain you've logged

**[03:21]** needs to use specific environment variables to access also other services. This is where you would

**[03:26]** create these environment variables. And notice that we've used the secrets syntax to avoid exposing that

**[03:33]** in code. You could also set the traffic configuration route as well. So if you're serving multiple

**[03:39]** endpoints, you can set like how the traffic split would want to be for each one of the models or the

**[03:44]** served models and enabling the inference table if through this auto capture config parameters in which

**[03:52]** you define in which catalog do you want to store that inference table under which schema? And what would

**[03:59]** the prefix of the table be? So once you create this configuration object for the endpoint,

**[04:07]** you can create the endpoint using the workspace client from the data request SDK. So once you

**[04:13]** instantiate the client, you define a serving endpoint name automatically. We'll do a quick

**[04:18]** sanity check to see if the endpoint exists. And then if it doesn't, we will create one using the workspace

**[04:26]** client serving endpoints API, which expose a create and wait method. So if I execute, I'm going to run

**[04:33]** that script telling me that the endpoint doesn't exist and it's going to spin it up. So that might take

**[04:39]** depending on the availability, maybe seven to ten minutes. While the script is running,

**[04:46]** another thing that another way to programmatically deploy a model is to use the MLflow deploy

**[04:52]** client methods. So technically the way it works is you instantiate a client. You can either point to

**[04:59]** data breaks or your local host. And once that client is instantiated, you just use the create endpoint

**[05:06]** method by just telling it the endpoint name and the configuration of that endpoint. And that's it.

**[05:12]** So that's again another way to use the programmatically deploy any model under your MLflow or Unity

**[05:19]** catalog registry to a given endpoint. Now the other way to do that to create a serving to also create

**[05:28]** a serving endpoint is to do that via the serving UI. So if you go to the serving UI, you can also create

**[05:35]** the endpoint programmatically. Also another, let's say, shortcut to do that is if you go to your

**[05:41]** catalog, go directly to the model itself, which is here. I can also serve this model by a click of a

**[05:50]** button. So it will get me to the model serving UI and create this specific shortcut. What is UI

**[05:57]** exposing here? You give an endpoint the name and then you can create multiple entities. So here it

**[06:05]** pre-populated the entity with my model and a version. And the other thing that you can decide is

**[06:11]** the compute type. As you can see, if you're trying to deploy the language model directly or transformer

**[06:17]** model, you can serve that on a GPU type of hardware. Here again, because we're serving a chain and

**[06:23]** nothing's happening on that chain, expect we're just doing retrieval on the vector search level

**[06:28]** and we're doing the completion or generation using the foundation model API. It is a very common

**[06:33]** practice to deploy the chain on a very lightweight CPU. And you can decide the concurrency level. So

**[06:40]** based on how much request you're expecting to get between small, medium, large,

**[06:44]** enable that scale to zero, create your environment variables, set an instance profile. Again,

**[06:50]** if you only want specific AWS services to access that endpoint or if the endpoint needs to access

**[06:55]** other resources, it will use any given instance profile. And what you can also do is create new entities.

**[07:02]** And that entity could be another model. So it could be another version of your model. So let me pick

**[07:08]** another random model here. And I can choose the version and I can say that, okay, I want the traffic

**[07:14]** for that version to be 5050, etc. That's pretty much resume the UI. There's a couple of other options

**[07:22]** that I haven't gone to if you want to create an endpoint, which point to an external model as well.

**[07:28]** But the other thing that other capabilities is root optimization. So if you want to minimize the

**[07:34]** handshake for the network authentication, root optimization allows to do that. You can tag your end

**[07:40]** points as you as for any resource. All is recommended for tracking costs or attaching it to specific

**[07:47]** projects or product. And you can enable that inference table or the auto-acapture config. So here

**[07:53]** when you enable it, you just point to the catalog, the schema, and what the table prefix will be.

**[08:01]** What's going to happen here is it will just add the suffix with the underscore payload to that

**[08:05]** table prefix that you provide. That's it. So as you can see, there are many ways. You can

**[08:11]** quickly buy the model, get to the serving UI. You can go to the model serving endpoint and create

**[08:15]** an endpoint from scratch. What not? Let's take a quick look. Here, I can see that my endpoint is

**[08:21]** still provisioning. It's still trying to update. Let's give it a couple of minutes.

**[08:27]** Now that the endpoint is ready, I can go back to my notebook and start doing inference

**[08:39]** first using the SDK. So that's given that we created a rack system asking question about

**[08:46]** archive papers with regard to. So we'll ask the question of what is PBO for

**[08:53]** proximal policy optimization, which is an RLHF alignment technique.

**[08:58]** And the first way we can query the inference endpoint is also using the Databricks SDK,

**[09:05]** a workspace client, which via the serving class, which also exposes a query method. So with the

**[09:13]** query method, you just point to your serving endpoint name and provide the inputs. Now the format of

**[09:19]** the inputs is support different types. This is more of the tensor format. You can also have the data

**[09:26]** frame split or records. It's really up to you. So here I can see that I got my answers on proximal

**[09:33]** policy. The other way also I can invoke this endpoint is using the MLflow deploy clients. So the same

**[09:42]** thing, making sure you're pointing it to your Databricks deployment, is going to expose a predict

**[09:49]** method on the endpoint. So now that we did those inference, we can go and check how the inference

**[09:57]** table got populated with these two queries. So let me jump back to my serving endpoint and that endpoint

**[10:06]** that I just recently deployed. So once the endpoint is deployed, what you can see here in the endpoint

**[10:13]** page is the list of the models who have been deployed. You can also take a look at the hardware

**[10:20]** infrastructure metrics such as requests error rates, the CPU usage, the memory usage, the concur

**[10:26]** and CE levels and what not. All these hardware related system metrics are made available via

**[10:32]** also via API. And what you'll see here that the inference table is enabled and there will be a

**[10:39]** hyperlink to that inference table. And other things that you can also do via the UI is to query

**[10:47]** the endpoint via the UI. If you've provided an input signature, this is with Automatically

**[10:54]** like a template on how the input format should be can show up. So here I can send the requests

**[11:00]** as well using the DataFrame split and let's say format and I'm going to get my output in my

**[11:06]** predictions. Now let's take a quick look at how the inference table look like from the UI. So

**[11:14]** again, that table has been automatically created with it has a predefined schema. So the client

**[11:21]** requests ID, maybe on the application side, there might be a specific identifier that you want to

**[11:26]** track. That's something you would populate the Databricks request ID. So that is automatically generated

**[11:32]** by the system, the date, time stamp, status code, how much time the request took to process,

**[11:39]** what was in the payload of the request, what were the output, the sampling fraction and all the metadata

**[11:45]** associated to it. So I as a metadata important, it is because it will contain all the information

**[11:52]** with regards to the model and the model identifier, which was used under the hood. So let's just give it

**[11:59]** a couple of seconds for the inference table to persist the payloads. So once the payloads are

**[12:06]** persisted, let's do a quick check. Yeah, I can see the current request that I've made with the status

**[12:14]** code 200. So 200 means successful, other status code, my minutes fail. I can see my input query,

**[12:20]** which is what is ppo and I can see the response generated by my chain with model metadata information.

**[12:28]** So the model name, the endpoint name and the model version, which is what is going to allow you

**[12:34]** to do some online monitoring or an evaluation of your system and doing that also for a specific model

**[12:43]** ID or model version. So with this inference table enabled, this is going to be our main gateway

**[12:53]** to be able to monitor our endpoint in quasi real time or monitor the online performance

**[13:03]** of any deployed LLM or RAC chain in the Databricks infrastructure. So the benefits to conclude

**[13:12]** of the model serving is, as you've seen, it is a very easy simple API call or point and click

**[13:19]** where given that the infrastructure is managed for you, it reduces your operational costs and

**[13:26]** facilitates the ML life cycle. And as you can see, any data scientist can self serve himself without

**[13:34]** having to deal with infrastructure management or worry about spinning up containers or doing all the

**[13:42]** work of an ML engineer. The fact that the endpoint has auto scaling enabled and scaled to zero

**[13:48]** allows you to make sure that you can address potential peaks, concurrency peaks throughout the day

**[13:56]** and scale it to zero to minimize your cost whenever there's no request going to the endpoint.

**[14:03]** And it's that same API which can work for both custom models that you built yourself,

**[14:09]** foundational models and even external models.

