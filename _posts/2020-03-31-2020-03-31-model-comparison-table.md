---
layout: post
published: true
updated: Thu Apr 9
---
<style>
.tablelines table, .tablelines td {
        border: 2px solid #999;
	padding: 0.5rem;
	background: white;
	border-color: lightgray;

}
.tablelines th {
	font-weight: bold;
	background: lightgray;
}
.tablelines body {
    margin: 0;
    width: 100%;
    padding: 0;
}
</style>

# Mon Mar 31 16:10:45 MDT 2020

All models below were trained with a batch size of 16, and the Casper ones 64.  They all have weight
decay on the conv. layers of 0.001 and fit three classes: irrigated, unirrigated, and uncultivated.
All trained with unweighted categorical cross entropy. The f1 is reported only for the irrigated
class.  The f1-score for the irrigated class that I'm trying to achieve is at least 90.

All of the models were tested on the same data for the two types of sampling: full-year and may-oct.

| Model saved in         |     acc | f1       | dataset             | feed     | lr_sch   |
|:--------:              |:-------:|:--------:|:--------:           |:--------:|:--------:|
| 5m-params-full-year/   | 0.81    | 0.74     | full-year           | RMinU    |  sd      |
| 5m-params-may-oct/     | 0.75    | 0.53     | may-oct             | RMinU    |  sd      |
| full-unet-full-year    | 0.81    | 0.69     | full-year           | RMinU    |  sd      |
| full-unet-may-oct      | 0.78    | 0.49     | may-oct             | RMinU    |  sd      |
| recording-f1           | 0.85    | 0.75     | full-year           | RMinU    |  ld      |
| model_0.903125         | 0.90    | 0.48     | full-year           | RMinU    |  ld      |
| recurrent_0.862.h5     | 0.86    | 0.84     | full-year-centroids | RMinURandomStartDate    |  ld      |
| recurrent_0.878.h5     | 0.88    | 0.77     | full-year-centroids | RMinURandomStartDate    |  ld      |
| small-unet-full-year   | 0.89    | 0.75     | full-year           | RMinU    |  sd      |
| larger-unet-full-year-centroid-all-bands   | 0.84    | 0.77     | full-year-centroids-all-bands      | RMinU    |  sd      |
| smaller-unet-random_start_date   | 0.85    | 0.81     | full-year-centroids-all-abands      | RMinURandomStartDate    |  sd      |
| full-unet-random_start_date-diff-lr-with-centroids   | 0.96    | 0.89     | full-year-centroids-all-bands      | RMinURandomStartDate    |  diff-lr      |
|=====
{: .tablelines}
Model "full-unet-random_start_date-diff-lr-with-centroids" has 85% precision, 93% recall for the
irrigated class. This is pretty much the best we're gonna do (I might train a model with
focal loss just to see what happens). Now I need to comprehensively evaluate out-of-time-domain 
prediction.




## Datasets:
All datasets that have 'centroid' appended are trained with data where tiles are extracted over the
centroid of each training polygon and in a raster scan. This results in ~60000 training instances
of which 5639 are irrigated. small-unet-full-year-centroids trains for 100 steps per epoch instead
of iterating over the entire irrigated dataset (which would be ~500 steps per epoch: 5639 is the min
number of example, multiply that by 3 classes = ~16000 instances, divided by batch size 32 is ~500)
for the sake of extracting test statistics more often. The way I have it set up, after 100 steps the
entire ~16000 file corpus (n_irrigatedxn_classes) is reshuffled, so there's no guarantee that each
epoch sees unique irrigated data. This is kind of unsatisfying, so I'll change it soon so that there
are no repeats in irrigated samples until there are all exhausted, no matter if it takes multiple
epochs to exhaust them.

I could possibly put all of the files into a queue of sorts, and then just sequentially empty the
queue. If the queue is empty, just repopulate it at the end of each epoch.


## Feed: How the data is fed into the model per epoch
RMinU: Random majority undersampling 

RandomStartDate: Random start index for raster ingested into model

## Model descriptions

5m-params: UNet w two downsampling steps, ~5m params

full-unet: Full Unet architecture, but with ~8m params

model_0.903125: UNet, two downsampling steps, ~21m params (trained on Casper)

recurrent_0.862: Recurrent UNet with three downsampling steps (trained on Casper), ~9m params.

recurrent_0.878: Same as above.

larger-unet-full-year-centroid-all-bands: ~1m params, trained on centroids only, not data
extracted with raster scan. 63 band model. This corresponds to 9 7 band rasters. Steps 
per epoch: 100.

smaller-unet-random_start_date: ~1m params, data extracted with raster scan and centroid
oversampling. Steps per epoch: 237, batch size 40.

recordingf1: UNet, two downsampling steps, ~1m params. Batch size 32. Why did this one do so well
compared to the same model with many more parameters? Overfitting?

## Lr schedules

sd: shorter decay time. The first code block in [this]({% post_url 2020-03-27-2020-03-27-model-comparison %}) post.

ld: longer decay time. The second code block in [this]({% post_url 2020-03-27-2020-03-27-model-comparison %}) post.

### "Diff-lr"
```python
def lr_schedule(epoch):
    lr = 1e-3
    rlr = 1e-3
    if epoch > 25:
        rlr = lr / 2
    if epoch > 50:
        rlr = lr / 4
    if epoch > 75:
        rlr = lr / 6
    if epoch > 100:
        rlr = lr / 8
    if epoch > 125:
        rlr = lr / 16
    return rlr
```
