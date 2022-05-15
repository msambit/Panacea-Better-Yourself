#!/usr/bin/env python
# coding: utf-8

# In[9]:


from sagemaker.huggingface import HuggingFaceModel
import sagemaker


# In[10]:


role = sagemaker.get_execution_role()
# Hub Model configuration. https://huggingface.co/models
hub = {
	'HF_MODEL_ID':'Nakul24/RoBERTa-Goemotions-6',
	'HF_TASK':'text-classification'
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
	transformers_version='4.17.0',
	pytorch_version='1.10.2',
	py_version='py38',
	env=hub,
	role=role, 
)


# In[11]:


# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
	initial_instance_count=1, # number of instances
	instance_type='ml.c5.large' # ec2 instance type
)


# In[15]:


parameters = {'return_all_scores':True}
predictor.predict({
	'inputs': "I am not well. It has not been a good week.", "parameters":parameters
}
)


# In[ ]:




