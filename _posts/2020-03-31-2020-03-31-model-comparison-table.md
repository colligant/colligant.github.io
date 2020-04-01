---
layout: post
published: true
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
### Edited on Tue April 1.

All models below were trained with a batch size of 16, and the Casper ones 64.  They all have weight
decay on the conv. layers of 0.001 and fit three classes: irrigated, unirrigated, and uncultivated.
All trained with unweighted categorical cross entropy. The f1 is reported only for the irrigated
class.  The f1-score for the irrigated class that I'm trying to achieve is at least 90.

| Model saved in         |     acc | f1       | dataset   | feed     | lr_sch   |
|:--------:              |:-------:|:--------:|:--------: |:--------:|:--------:|
| 5m-params-full-year/   | 0.81    | 0.74     | full-year | RMinU    |  sd      |
| 5m-params-may-oct/     | 0.75    | 0.53     | may-oct   | RMinU    |  sd      |
| full-unet-full-year    | 0.81    | 0.69     | full-year | RMinU    |  sd      |
| full-unet-may-oct      | 0.78    | 0.49     | may-oct   | RMinU    |  sd      |
| recording-f1           | 0.85    | 0.75     | full-year | RMinU    |  ld      |
| model_0.903125         | 0.90    | 0.48     | full-year | RMinU    |  ld      |
|=====
{: .tablelines}

## Model descriptions

5m-params: UNet w two downsampling steps, ~5m params

full-unet: Full Unet architecture, but with ~8m params

model_0.903125: UNet, two downsampling steps, ~21m params (trained on Casper)

recordingf1: UNet, two downsampling steps, ~1m params. Why did this one do so well? Batch size 32.

## Lr schedules

sd: shorter decay time. The second code block in the [link post here]

ld: longer decay time.  The first code block in the [link post here]
