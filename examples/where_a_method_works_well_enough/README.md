# Finding the models where method X produces good enough results

Run only method X and some comparison method (which ideally is cached). Or I suppose it could be useful to compare against all methods in some cases? But for publication you probably really only care about comparing vs the most accurate method when determining adequacy. For benchmarking execution speed you might want to make sure that no other method yields similar results but faster.


What is the output? Do we need to produce list of models where method X was good enough and a list where it was not? Or just produce the output files and let user determine if method X was good enough?

We might want to make plots that show adequacy as a function of something, for example what was the adequacy ratio in hierarchical models vs non-hierarchical models?