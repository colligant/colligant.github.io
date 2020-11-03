---
layout: post
published: false
---
first set the project:
```
earthengine set_project <your-project-name-here>
```

then create your model:
```
gcloud ai-platform models create <your-model-name-here> --project <your-project-name-here>
```
Look at model inputs and outputs:
```bash
saved_model_cli show --dir /path/to/your/saved/model/in/tf/format --tag_set serve --signature_def serving_default
```
output:
```
The given SavedModel SignatureDef contains the following input(s):
  inputs['input_1'] tensor_info:
      dtype: DT_FLOAT
      shape: (-1, -1, -1, 36)
      name: serving_default_input_1:0
The given SavedModel SignatureDef contains the following output(s):
  outputs['softmax'] tensor_info:
      dtype: DT_FLOAT
      shape: (-1, -1, -1, 3)
      name: StatefulPartitionedCall:0
Method name is: tensorflow/serving/predict
```

wrap the model's inputs and outputs with ops that
change datatypes and prepare the model for connecting w/ earthengine:
Remember to specify inputs and outputs given by the first command. 
In this case, input is "serving_default_input_1:0", and output is
"StatefulPartitionedCall:0", even though the layers aren't named as
such in the model definition.
```
earthengine model prepare --source_dir /path/to/your/saved/model/in/tf/format --dest_dir
/where/you/want/to/save/the/prepared/model --input '{"serving_default_input_1:0":"array"}' --output
'{"StatefulPartitionedCall:0":"irr"}'
```
Specify names "array" for the input (makes it easier when evaluating the model), and whatever you
want for the output.

Then, use gcloud/ai platform to upload the model to GCS:

```bash
gcloud ai-platform versions create v0_04 \
--project <your-project> \
--model fcnn_irr_model \                   
--staging-bucket <your-bucket> \                                          
--origin <where/you/saved/the/prepared/model \                                                                          
--framework "TENSORFLOW" \                     
--runtime-version 2.1 \                             
--python-version 3.7 \                                                                               
--config config.yaml \                                                                               
--machine-type n1-standard-4 <- use a gpu.
```
cat config.yaml:
autoscaling:
    minNodes: 10

Then you have the model up on ai platform and you can predict with it.
