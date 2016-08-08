# Team K&R's entry for the 2016 ICFP Programming Contest

## Team members

  * [Lindsey Kuper](http://composition.al)
  * [Alex Rudnick](http://alexr.cc)

## Background

[This year's ICFP Contest](http://icfpc2016.blogspot.jp/2016/08/task-description.html)
involved origami.  The idea was to "fold" sheets of origami paper in
such a way that they would match the (two-dimensional) silhouettes of
completed origamis.  Points were awarded based on how closely the
solutions matched the problem silhouettes.

There was another dimension to the contest, which involved submitting
your own problems for others to try and solve, but we didn't get that
far!

We finished at position **#84** on the
[leaderboard](http://2016sv.icfpcontest.org/leaderboard) (out of 293
registered teams, 201 of which actually scored points).  This was the
best-ever showing for Team K&R (although that was with the leaderboard
freeze several hours before the end of the contest; we might end up at
a higher or lower place than that).

## Our approach

After solving a few problems manually, we started out by trying to
simply "drop" an unfolded sheet of origami paper to cover the
silhouette.  We were able to score some points this way, especially
because some of the problems were themselves simply an unfolded sheet
of paper!  Then we tried folding in half once vertically, which
allowed us to more closely match the silhouette of narrower origamis.
The files `paper_drop_solution.py` and `fold_in_half_solution.py`
implement these initial experiments.

In `hv_folds.py` we attempted a more general solution.  Here, our
approach was to repeatedly fold the paper in half both horizontally
and vertically until we were close to the bounding box of the
silhouette, then move the resulting folded-up rectangle to fit over
the silhouette.  This worked well for problems with a tight
rectilinear bounding box whose width and height was close to 1 divided
by a power of two.  For others, it didn't work so well.

Then we added the ability to fold the paper once horizontally less
than halfway, and once vertically less than halfway.  This allowed us
to do reasonably well on problems with tight bounding boxes that were
between 0.5 and 1 on a side.

At some point, we figured out that we would be better able to match a
lot of silhouettes if we could rotate our folded-up rectangle to match
the diameter of the points of the silhouette.  `calipers.py`
implements diameter-finding.  Unfortunately, we ran into a lot of
trouble here with numerical instability.  Our rotation code worked
well for, for example, problems 5 and 6 (with judicious use of
`limit_denominator` from Python's `fractions` module), but for problem
7 the server complained that our solution's destination facets weren't
congruent with its source facets.  We think the calls to `math.cos`
and `math.sin` in the `rotate_polygon` function are at fault.

We also implemented a quick-and-dirty JavaScript visualizer in
`visualizer.js`.  Open `visualizer.html` in your browser to try it
out.  It displays problems and solutions by generating an SVG image.
`parse_problem.py` and `solution_to_json.py` convert problems and
solutions, respectively, to a JSON format that the visualizer can
understand.

## Final thoughts

Thanks to the organizers for making this contest possible!  We had a
lot of fun this year -- with feline assistance, of course:

![Mylk helps with our ICFP Contest submission.](https://pbs.twimg.com/media/CpJhBHUUAAAD_lV.jpg)





