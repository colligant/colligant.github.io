+++
title = "Carbon model super resolution!"
date = 2025-04-10T14:40:43Z
draft = True
+++

 - Describe the achievement in a few sentences and a nice visual
     - 2500x increase in resolution
     - 6000x normal LPJ runs
     - Visual showing the super resolution [global and regional]
 - describe the steps required to make the workflow go
    - meta-optimization goals: storage, file load, and compute time
    - optimizing the model
    - optimizing the slurm workflow & using dask
 - postmortem on this engineering effort
   - the blockers - and what I did to resolve them

Over the past few months I enabled running LPJ-EOSIM at a 2500x higher resolution, from approximately 50km resolution to 1km.
This involved running the model 400 million times across terabytes of sharded input data and collating 10s of terabytes of output. 

{{< rawhtml >}}
<div class="cog-map-container">
  <div id="map" class="cog-map"></div>
  <div id="divider"><span class="handle"></span></div>
</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/georaster"></script>
<script src="https://unpkg.com/georaster-layer-for-leaflet"></script>

<style>
.cog-map-container{position:relative;max-width:1000px;margin:2rem auto;border:1px solid #ccc;border-radius:8px;overflow:hidden;}
.cog-map         {height:500px;width:100%;}
.map-caption{
  text-align:center;
  font-size:0.9rem;
  color:var(--secondary);
  margin-top:0.5rem;
}
#divider{
  position:absolute;top:0;bottom:0;left:50%;width:14px;margin-left:-7px;
  cursor:ew-resize;z-index:1000;background:rgba(255,255,255,.4);backdrop-filter:blur(2px);
  display:flex;justify-content:center;align-items:center;user-select:none;
}
#divider .handle{
  width:4px;height:44px;border-radius:2px;background:#666;transition:background .2s;
}
#divider:hover .handle{background:#000;}
</style>

<script>
window.addEventListener('load', async () => {

  /* ----------------  map  ---------------- */
  const map = L.map('map').setView([37.8,-96],4);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
              {attribution:''}).addTo(map);

  /* ----------------  rasters  ------------ */
  const [bufA, bufB] = await Promise.all([
    fetch('/chelsa_conus.tif').then(r=>r.arrayBuffer()),
    fetch('/era5_mgpp_conus.tif').then(r=>r.arrayBuffer())
  ]);
  const [rasterA, rasterB] = await Promise.all([parseGeoraster(bufA),
                                                parseGeoraster(bufB)]);

  /* viridis LUT + colour fn factory */
  const LUT = [[68,1,84],[59,82,139],[33,145,140],[94,201,97],[253,231,37]];
  const makeColour = max => v => {
    const d=v[0]; if(d==null||isNaN(d)||d===0||d===-99999) return null;
    const t=Math.max(0,Math.min(d/max,1));
    const i=Math.floor(t*(LUT.length-1)), f=t*(LUT.length-1)-i,
          c0=LUT[i], c1=LUT[i+1]||c0;
    const r=Math.round(c0[0]+f*(c1[0]-c0[0])),
          g=Math.round(c0[1]+f*(c1[1]-c0[1])),
          b=Math.round(c0[2]+f*(c1[2]-c0[2]));
    return `rgb(${r},${g},${b})`;
  };

  /* layers */
  const left  = new GeoRasterLayer({georaster:rasterA,pixelValuesToColorFn:makeColour(0.35)});
  const right = new GeoRasterLayer({georaster:rasterB,pixelValuesToColorFn:makeColour(0.35)});
  left.addTo(map); right.addTo(map); map.fitBounds(left.getBounds());

  /* ----------------  slider  ------------- */
  const divider=document.getElementById('divider');
  const lC=left._container, rC=right._container;
  let split=0.5, dragging=false;

  function clipLayers(){
    const size = map.getSize(),
          pos  = split*size.x;

    // Convert container → layer coords so clips stay glued during zoom/pan
    const nw = map.containerPointToLayerPoint([0,0]);
    const se = map.containerPointToLayerPoint(size);
    const clipX = nw.x + pos;

    lC.style.clip = `rect(${nw.y}px, ${clipX}px, ${se.y}px, ${nw.x}px)`;
    rC.style.clip = `rect(${nw.y}px, ${se.x}px, ${se.y}px, ${clipX}px)`;
    divider.style.left = pos + 'px';
  }
  clipLayers();

  divider.addEventListener('pointerdown', e=>{
    dragging=true; divider.setPointerCapture(e.pointerId);
  });
  divider.addEventListener('pointerup',   e=>{
    dragging=false; divider.releasePointerCapture(e.pointerId);
  });
  divider.addEventListener('pointermove', e=>{
    if(!dragging) return;
    const box = map.getContainer().getBoundingClientRect();
    split = Math.max(0, Math.min(1, (e.clientX-box.left)/box.width));
    clipLayers();
  });

  map.on('move zoom resize zoomend moveend', clipLayers);
});
</script>

<p class="map-caption">
  Conterminous U.S. GPP for June 2016. High res is CHELSA driven LPJ, low res is ERA5 driven.
  0 values are set to NaN. Spatial differences are to be expected as the two input drivers are different.
</p>
{{< /rawhtml >}}


1) Introduction to LPJ-EOSIM
2) I/O refactoring and GPFS
3) Input data preparation
4) Computing parameters
5) SLURM distribution pipeline

The model (LPJ-EOSIM) is complex, requiring thousands of calibration steps before being able to model real-world quantities
accurately. Once it's properly "spun-up", it can be used to estimate some really interesting things, like how much CO<sub><small>2</small></sub> is absorbed by land vegetation every
year<small>[^1]</small>. 
LPJ has been around for ~25 years and historically has been run at a 0.5° (~50km) resolution, mostly for computational and
input data resolution issues. A 1km run can provide detailed information about where and when the model does well, and answer questions about the benefit of running
on high-resolution input data.

When I started at NASA, the model could only run with monthly datasets as input (think one timestep a month), and even this took ~24 hours. 
LPJ's original I/O scheme combined with GPFS didn't work with daily datasets, and using it on a 1km daily dataset would've literally been impossible. 

Once I realized this, I refactored the I/O module in LPJ to play a little more nicely with GPFS and rechunked the input netCDFs to align with our I/O strategy. I also refactored the way
outputs were written, only writing the necessary ones to disk. These modifications meant a global run<small>[^2]</small> now completed in ~20 minutes and was CPU-bound<small>[^3]</small>. 
The model was sped up ~100x on monthly datasets and went from being unusable with daily datasets to being fast. 

With these optimizations in hand running on a global 1km dataset was possible in a imaginable amount of time. 
At this point, the engineering switched from C development to workflow orchestration on Discover[^4].

First, I started with a base estimate of the number of times I'd need to run LPJ to accomplish a global 1-km run. An back of the envelope calculation for the number of cells was around $200\times10^6$<small>[^5]</small>, though this actually turned
out to be wrong by a factor of 2, probably because I didn't think about the fractal nature of coastlines. $400\times10^6$ is around 6000 native resolution LPJ runs. I'm confident that this
is more times than LPJ has been run in its lifetime. The scope of this was far greater than any number of simulations that we needed to run before - maybe we'd do 20 or so simulations at once and even this was a big ask of the cluster and 
distribution pipeline. The mental model had to be different: instead of relying on a continuously updated netCDF for [publishing data](https://www.earthdata.nasa.gov/data/alerts-outages/lpj-eosim-global-simulated-wetland-methane-flux-version-1-data-products), we'd need
to generate the input data for each model run on the fly and clean up afterward. This is a good time to dive into how LPJ reads data and how to move data efficiently on a GPFS cluster. 

LPJ expects a single netCDF for each input variable (precipitation, temperature, radiation) that starts at timestep $t_0$ and ends at $t_N$. 
N=13k for the CHELSA dataset (days between 1979 and 2016, inclusive, excluding leap days). We run a process-level embarrassingly parallel workflow with LPJ, where each process reads a
distinct set of cells from the input dataset, processes it, and writes a set of output files describing diagnostic variables (GPP for the cells in process 0, process 1, etc). 
The CHELSA meteorology dataset is roughly 40k$\times$20k cells and a good rule of thumb for number of cells per core that enables LPJ to run in a reasonable amount of time is ~500. 
Reading 500 cells per process from a single 40k$\times$20k raster with up to 500 processes is a good recipe for getting yourself kicked off the cluster. GPFS doesn't thrive when many
processes do I/O on the same directory, not the mention the same _file_ in that directory. 

The first task was to design a scheme to divide the global grid into palatable chunks for both LPJ and GPFS. I wrote a simple algorithm to iteratively grow slices of latitude into rectangles
containing at most 200k cells, the results of which are shown in the figure below.

![alt text](/sa_grid.png)*The grid split algorithm on South America.*

Why 200k? On a shared-resource cluster you want jobs that will run in a reasonable amount of time (1-4 hours) so they clear the queue quickly, but you
don't want to request so many resources that a single job's allocation sits in the queue for a long time. In addition, each LPJ process emits something like 35 files, so I needed to 
keep the number of CPUs per job small to reduce file load on the cluster since we're subject to hard limits. 

Once the splits were extracted from the global CHELSA rasters, I spun up `dask`-enabled clusters so I could apply arbitrary python logic to 
format the drivers for each split correctly. I designed the drivers to be ephemeral because persisting them on disk would've been too expensive. 

### Stress testing the parallelization pipeline
The pipeline for distributing LPJ across computing ecosystems evolved over many years and many supercomputers. Before I started, it was a few bash scripts that 
used environment variables and in-line config templates to configure a simulation. This version wasn't very flexible and was error-prone, so I rewrote it in
Python. I was mostly concerned with replicating the functionality while providing a better interface for users and developers, so I didn't question the choices it made.

Running something at thousands of times its intended usage will inevitably expose bottlenecks. I identified and fixed quite a few which really helped speed it up.

Here are the computational choices that it made that I fixed during this run to get speedup and usability improvements:

1) Compiled the LPJ model for each process. This involved copying the source code to a dir on `/tmp`, running `make`, and then using that 
binary _only_ for the owning process. I changed this to compile one binary per simulation because it was causing file load bloat (like 40k files in /tmp/ for no reason due
to hundreds of LPJ processes.
2) Used `srun -n 1 -c 1 ./lpj_binary conf.conf &` to parallelize the model on each node after requesting node-level resources. This works, but isn't how `srun` is made to be used, especially
for a single-core program. I changed this to use `srun --multi-prog`, which automatically takes care of parallelizing your tasks across whatever resources you've asked for. Discover doesn't do array jobs, so this
is the next-best thing. 
3) Requested multiple separate jobs and nodes for a single simulation. I changed this to request multiple nodes in one job for a single simulation. This allows more simulations to 
pump through the queue since we have a 25-job limit. 
4) Didn't use any sort of fast-access scratch. I used `$TMPDIR` to stage data for each simulation before reading it. This results in much lower I/O wait times.
5) Used bash and `SLURM` job dependencies exclusively for orchestration. I switched to using `python`, `dask`, and `SLURM`. A `prefect` + `dask` rewrite is incoming.
6) Included explicitly invalid grid cells in the config file. Soil types of water, ice, or bare soil are skipped in LPJ. Including these means the parallelization is a little less efficient.


### Blockers
- I was under a time crunch to get these simulations done, so I wrote some hacky code at times that was immediate tech debt. This is a reminder to slow down and follow DRY.
- I didn't test the algorithm for creating a global grid split and an edge case slipped by, leading to some re-runs. Note to self: tests for that sort of code are pretty important. Again, though,
with a time crunch it's tough.
- I should've questioned the assumptions of the old pipeline sooner.
- Misinterpretation of LPJ's internals meant I had to re-do part of the analysis.
 

[^1]: This is important for a variety of reasons, including estimating the buffer the land provides against anthropogenic CO<sub><small>2</small></sub> emissions. However, this is not the main point of this article. For an overview of what models like LPJ-EOSIM can do,
see \<insert multiple references here>.

[^2]: This is for a simple simulation protocol at a level of parallelization enabled by the aforementioned I/O refactoring and input chunking. 

[^3]: `-O3`means it screams. Probably could speed the model up more by applying simple optimizations and SIMD, but sometimes the lowest hanging fruits are the only ones you need to pick.

[^4]: Discover is a supercomputer at NASA Goddard that has made the Top500 list.

[^5]: 0.5°: 720x360 cells = 259200 total cells, 67420 of which are land surface. 1km: 40k by 20k cells, multiplied by (67420/259200) ~ $200\times10^6$.

