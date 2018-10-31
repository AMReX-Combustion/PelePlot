
PelePlot
========

A gnuplot-like interface to yt's plotting capabilities for AMR datasets

NOTE: This repo needs a lot of work...

Contributions
-------------

To add a new feature to PelePlot, the procedure is:

1. Create a branch for the new feature (locally) ::

    git checkout -b AmazingNewFeature

2. Develop the feature, merging changes often from the development branch into your AmazingNewFeature branch ::
   
    git commit -m "Developed AmazingNewFeature"
    git checkout master
    git pull                     [fix any identified conflicts between local and remote "master" branches]
    git checkout AmazingNewFeature
    git merge master             [fix any identified conflicts between "master" and "AmazingNewFeature"]

3. Push feature branch to PeleAnalysis repository (if you have write access, otherwise fork the repo and
push the new branch to your fork)::

    git push -u origin AmazingNewFeature [Note: -u option required only for the first push of new branch]

4.  Submit a merge request through the github project page - be sure you are requesting to merge your branch to the master branch.



Acknowledgment
--------------
This research was supported by the Exascale Computing Project (ECP), Project
Number: 17-SC-20-SC, a collaborative effort of two DOE organizations -- the
Office of Science and the National Nuclear Security Administration --
responsible for the planning and preparation of a capable exascale ecosystem --
including software, applications, hardware, advanced system engineering, and
early testbed platforms -- to support the nation's exascale computing
imperative.

