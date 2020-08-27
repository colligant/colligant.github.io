---
layout: post
published: true
---
Overarching goal: Train a model on the full dataset that does relatively 
well. The model should be one where I haven't commented out the first batch 
normalization layer. I need to include a validation split (why didn't I do
this in the first place?) Doing a 70/15/15 train test validation.

I need some way to keep all of the models organized, so here it is.

I'll be a bit lazier than my previous bookkeeping post and assume 
that the sampling is always random majority undersampling, and not
aggregate all of the information in a table. All of the training
data is the same; 6 "mean" images that have a 32-day temporal mean.

## fcnn-remote-train-all-bands/
2m parameter UNet, forgot to add the first batch norm,
weight decay of 1e-3. Trained for 100 epochs.

## fcnn-remote-train-all-bands-border-weights/
Same as above, but with a 1-px border around the irrigated
class that is assigned as uncultivated.

## remote-june29-bn-included-no-border-weights/
8m parameter UNet, first BN included (whoops!),
no border weight class. Weight decay of 0.001. 120
epochs of training. This model reached 0.77 f1 score
on the irrigated class.

## remote-june30-8mparams-no-weight-decay/
Same as above, except without weight decay.
I never finished training this model in accordance with the goal.

## remote-july6-2mparams-no-weight-decay/
Trained this model on the true data distribution (didn't balance
examples from each class per batch). It only reached 0.33 f1 on the irrigated
class. Not going down this route. I thought I could greatly reduce the number
of training steps by just "raster scanning" over the input images. 
Performance indicates otherwise. Re-extracting data, then retraining the
final model, and moving on.

## remote-july17-2mparams-weight-decay
Only reached ~0.5 f1. I was surprised by this as usually 
these models do much better.
This is the first model I trained after re-extracting
training/test/validation data. Doing this (stupidly) took like 5 days,
because I downloaded tiles over every single training polygon. This
was trained with a weight decay w/ constant 0.01 on every conv. layer.
Batch norm after every convolution and relu activations. Trained
for 200 epochs. 300 steps per epoch, and about the same
number of validation steps.

## remote-july17-2mparams-weight-decay
Same training parameters as above, but w/ a weight decay constant
of 0.001. 600 steps per epoch, 300 epochs. Different lr schedule.

## 0.01wd-nondvi-july28-2mparams-final-split-balanced
0.01 weight decay, unet w/ 2m params, no ndvi feature. Trained for
300 epochs reaching a test f1 of 



