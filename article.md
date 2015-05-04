A stochastic cellular automaton model of evolutionary divergence of quorum sensing
==================================================================================

**A work in progress**

Department of Molecular Microbiology and Biotechnology  
The George S. Wise Faculty of Life Sciences  
Tel-Aviv University

Yuval Langer  
Dr. Avigdor Eldar

Introduction
------------

Quorum sensing (QS) is the ability of bacteria to sense their own density.
A QS system is made of a signal and a signal specific receptor which regulates
the expression of QS sensitive genes.
Each bacteria continuously produce the QS chemical signal and export it outside
the cell.
At high bacteria density, the produced signal concentration reaches the
receptor’s activation threshold.
Various genes critical to group behaviour are expressed and others are
inhibited by QS.
Bacterial group behaviour is typically of the *public goods* type.
These are mostly extracellular products, e.g. surfactants which add motility,
scavenging materials such as siderophores or hydrolases that tear down
otherwise unreachable nutritious polymers.
Public goods benefit all the bacteria in the community.
The benefit is sufficient to overcome the cost of production only when large
enough numbers of neighbouring bacteria produce them as well.

Multiple bacterial species show intraspecific divergence of their QS systems.
The different alleles are called *pherotypes*.
Signals from a strain with one pherotype can activate their own receptor but
fail to activate and sometimes inhibit a receptor from a strain with a
different pherotype.

This divergence seems to be under strong selection, as implied by the
functional divergence and is also corroborated by rapid sequence divergence,
the signatures of diversifying selection, and the spread of divergent QS
systems through horizontal gene transfer.

A proposed model that explains how such diversity forms introduces an
evolutionary ratchet in which the order of divergence in QS signal or receptor
matters.
From the original pherotype population, a cheating population with a mutant
receptor that is not sensitive to the original signal will arise, while signal
switching is selected to regain cooperation and as an immunity to the cheater.

[!Fig 1, A and B - Eldar's QS explanation][eldar fig 1 a b]

The approach used by Eldar et al. to investigate the interactions between
strains was to create a set of differential equations.
This approach is amenable to mathematical analysis but disregards spatial
effects. (Eldar et al., 2011)

Stochastic cellular automata simulations were previously used to investigate
social interactions by QS in bacteria (Czaran et al. 2009).
In this work, a lattice of abstract cells compete with their immediate
neighbours according to the state of their microenvironment,
thus mimicking a kind of limited infinite island model.

The model used had only one QS system, examining the existence or loss of
signal, receptor or public goods genes, while leaving the effects and evolution
of "multi-lingual" quorum sensing systems.

In my project I've adapted Czaran's algorithm to incorporate Eldar's
theoretical model of competing pherotypes in order to investigate spatial
effects that are not shown in Eldar's system of differential equations.

Methods
-------

![Image: overview of the Eldarian model]

The model we use is a two-dimensional cellular automaton (CA) of toroidal
lattice topology.
Each of the 300x300 grid-points of the square lattice represent a site for a
single bacterium;
all the sites are always occupied, i.e., bacteria may replace each other, but
may not leave empty sites.
The inhabitants of the sites may differ at 2 genetic loci: locus S for signal
of specific pherotype ($[S_{1}]$ or $[S_{2}]$), and locus R for receptor of specific
pherotype ($[R_{1}]$ or $[R_{2}]$) which includes the signal receptor and the signal
transduction machinery that triggers the cooperative behaviour when the
critical signal concentration has been reached.
Each of these loci can harbour either an allele of one pherotype denoted by
subscript 1 ($[S_{1}]$, $[R_{1}]$), or of another pherotype denoted by subscript 2
($[S_{2}]$, $[R_{2}]$).
Thus the bacteria can have $[2^{2}=4]$ different genotypes.


Variable name                | Description
:--------------------------- |:-----------
[CooperationEffectThreshold] | Minimal number of cells that produce public goods in the Moore neighbourhood of a cell for the cell to benefit from those public goods
[SignalThreshold]            | Minimal number of cells in the Moore neighbourhood of a cell that produce a compatible signal pherotype to the cell's receptor for it to produce public goods
[BoardSize]                  | The number of columns the grid has (equal to the number of rows)
[CooperationCost]            | The metabolic cost of producing the public goods
[PublicGoodsEffect]          | The metabolic benefit of the public goods
[MutOddsS]                   | Probability of mutation in the S locus per competition
[MutOddsR]                   | Probability of mutation in the R locus per competition
[BasalCost]                  | The metabolic cost each of the cells pays
[D]                          | Diffusion rate
[Generations]                | Number of generations for each simulation
[SignalCost]                 | Cost of signal production
[ReceptorCost]               | Cost of receptor production
[PublicGoodsEffect]          | The fitness benefit achieved by sufficient public goods

Table: Parameters used in the simulation

### Fitness effects of cooperation



The product of the cooperating is supposed to be an excreted ‘public good’
molecule such as an exo-enzyme for extracellular food digestion.
It may increase the fitness of a bacterium, provided there are at least
$[CooperationEffectThreshold]$ bacteria (possibly, but not
necessarily, including itself) expressing the public goods as well within its
3x3-cell neighbourhood;
$[CooperationEffectThreshold]$ is the quorum threshold of cooperation.
An individual can only obtain a fitness benefit from cooperative behaviour in
its neighbourhood if at least
$[CooperationEffectThreshold]$ cooperators are present in that neighbourhood. On the other
hand, cooperation carries a fitness cost which is always paid by the
cooperator whether or not it enjoys the benefits of cooperation.
The cost of cooperation is the metabolic burden associated with
the production of the public good. That is, cooperation carries an inevitable fitness cost and a conditional fitness
benefit. Of course for cooperation to be feasible at all the
benefit has to outweigh the cost.

### Selection

Individuals compete for sites.
Competition is played out between randomly chosen pairs of neighbouring cells,
on the basis of their fitness:

$Fitness = [BasalCost]/(([CooperationCost] + [SignalCost] + [ReceptorCost])*(1 - [PublicGoodsEffect]))]$

If the cell produces public goods, $[CooperationCost]$ will be equal to 1,
otherwise it’ll be equal to the cost of producing public goods.
If there are a sufficient number of cooperators around the cell,
$[PublicGoodsEffect]$ will equal the public goods effect, from 0 to 1, where
bigger is better for the competitor, otherwise $[PublicGoodsEffect]$ will be 0.

Each of the competitor's Fitness is multiplied by a different uniform random
number between 0 and 1, and the result is compared.
The cell with the higher result is the winner of the competition.
If both cells are of the same strain, the competition stage is redundant and
only one of the selected cells will go through the mutation stage.

### Mutations

During the takeover of a site by the winner of the competition the invading
cell, i.e., the copy of the winner occupying the site of the loser, can change
any of its 2 alleles from pherotype 1 to 2 or vice versa.
The point in allowing allele changes both ways is to maintain the presence of
all different genes in the population so that the system doesn’t get stuck in
any particular genetic state because of the lack of alternative alleles.
Thus, each of the possible allele changes may have a positive probability.
Mutations are independent at the two loci – e.g., the quorum signal gene S can
be mutated without changing the response module R at the same time.

### Diffusion

Each competition step may be followed by a number $[D]$ of diffusion steps.
One diffusion step consists of the random choice of a site, and the 90 degree
rotation of the 2x2 subgrid with the randomly chosen site in its upper left
corner.
Rotation occurs in clockwise or anticlockwise direction with equal probability.
$[D]$ is the diffusion parameter of the model:
it is proportional to the average number of diffusion steps taken by a cell per
each competitive interaction it is engaged in.
Larger D means faster mixing in the population.
Since one diffusion move involves 4 cells, $[D=1.0]$ amounts to an expected
number of 4 diffusion steps per interaction per cell.

### Initial states and output

At $[t=0]$ the lattice is “seeded” by the first pherotype $[S_{1}R_{1}]$.
We simulate pairwise competitive interactions, mutations and diffusive
movements for N generations.
One generation consists of a number of competition steps equal to the number of
sites in the lattice, so that each site is updated once per generation on
average.
We have applied mutation rates of $[10^{-4}]$ both ways at each locus, which is
equivalent to an average of $[BoardSize^{2}*10^{-4}=9]$ mutation events per
generation for each locus within the whole habitat.

### Simulations

With the initial conditions specified above we follow the evolution (the change
in allele frequencies) of the two loci.
We investigate the qualitative or quantitative effects on the evolution of
quorum sensing of the crucial parameters of the model:
the metabolic cost of cooperation $[CooperationCost]$,
the intensity of diffusive mixing $[D]$,
the threshold of PG needed for the cooperation fitness effect
$[CooperationEffectThreshold]$
and the threshold of signal needed to produce public goods $[SignalThreshold]$.
The simulations have been run for 2000 generations.
During the simulations we record and plot the time series of the 4 different
genotype frequencies, from which the frequencies of the two functional alleles
can be calculated and plotted against time.
We've also repeated each simulation with a different RNG (random number generator) seed (seed=1 for the first and seed=2 for the repeat).
The strain frequency plots are available in the addenum.


[eldar fig 1 a b]: [images/eldar-fig-1--QS-explanation.jpg]

## Results

### Strain frequency figure $[CooperationCost]=10$

A hundred simulations, each with a different $[SignalThreshold]$ (changes vertically) and $[CooperationEffectThreshold]$ (changes horizontally).
Within each square the vertical axis denotes quantity of cells of each strain and the horizontal denotes generation.
Each colour represents a different strain: blue=S1R1, red=S1R2, orange=S2R2 and green=S2R1.


$[Diffusion]$ | $[CooperationCost]$ | $[CooperationEffectThreshold]$ | $[SignalThreshold]$ | $Description$
:------------ |:------------------- |:-----------------------------  |:------------------- |:------------
0             | 10                  | 5                              | 5                   | An equilibrium is reached between S1R1 and S2R2 at about generation 1200 with almost no cheating intermediate strains. At generation 270 we see the start of a persistent S2R2 population.
0             | 10                  | 1                              | 6                   | A case of rock-paper-scissors (RPS) appears in which the dominance of the S1R1 is replaced by S1R2, S1R2 is replaced by S2R2, S2R2 by S2R1 and back again to S1R1. After one cycle of such replacements, the dominant populations are of the cheating strains and a smaller population of the cooperators exists, while the game of RPS is kept throughout the generations.
0             | 10                  | 1                              | 7                   | The same as in (1,6), but after the first complete cycle of RPS the dominant populations are of the cooperating strains.
0             | 10                  | 3                              | 8                   | An equilibrium is quickly achieved between the original cooperator (S1R1) and its cheater (S1R2). The board snapshots show high population heterogeneity. but we can see for a few generations (380 to 570) that S2R2 invaded an S1R2 population unsuccessfully and went extinct. (The invading S2R2 population had a strong advantage over the S1R2 population, but because of the overall board's structure of many discontinuous islands, the S2R2 population did not have a way to the other S1R2 populations and died off due to its small size with !!!!)
0             | 30                  | 5                              | 5                   | An equilibrium between the two cooperating strains is achieved much faster. For a short duration at the first part of the simulation a population of cheaters to the original strain invades and went extinct.
0             | 30                  | 1                              | 6                   | The RPS cycling appears but, conrary to the simulation of the same thresholds but with $[CooperationCost]=10$, within the first complete cycle the dominance of the cheating strain pair (S1R2, S2R1) is achieved.
0             | 30                  | 1                              | 7                   | The same as the previous simulation.
0             | 30                  | 3                              | 9                   | The first cooperating population is quickly invaded by its cheater. The change of population densities seem to be leading to an equilibrium between each of the cheating and each of the cooperating strain pairs with the cheating on the upper hand.
0.2           | !!!                 | 5                              | 5                   | An equilibrium between the two cooperating strains is achieved much faster. For a short duration at the first part of the simulation a population of cheaters to the original strain invades and went extinct.
0.2           | !!!                 | 1                              | 6                   | The RPS cycling appears but, conrary to the simulation of the same thresholds but with $[CooperationCost]=10$, within the first complete cycle the dominance of the cheating strain pair (S1R2, S2R1) is achieved.
0.2           | !!!                 | 1                              | 7                   | The same as the previous simulation.
0.2           | !!!                 | 3                              | 9                   | The first cooperating population is quickly invaded by its cheater. The change of population densities seem to be leading to an equilibrium between each of the cheating and each of the cooperating strain pairs with the cheating on the upper hand.
0.4           | !!!                 | 5                              | 5                   | An equilibrium between the two cooperating strains is achieved much faster. For a short duration at the first part of the simulation a population of cheaters to the original strain invades and went extinct.
0.4           | !!!                 | 1                              | 6                   | The RPS cycling appears but, conrary to the simulation of the same thresholds but with $[CooperationCost]=10$, within the first complete cycle the dominance of the cheating strain pair (S1R2, S2R1) is achieved.
0.4           | !!!                 | 1                              | 7                   | The same as the previous simulation.
0.4           | !!!                 | 3                              | 9                   | The first cooperating population is quickly invaded by its cheater. The change of population densities seem to be leading to an equilibrium between each of the cheating and each of the cooperating strain pairs with the cheating on the upper hand.


TODO Describe general trends within the thresholds parameter space.
TODO Add another figure with specific simulation snapshots to which you'll refer from other places.
TODO Add captions & titles to the figures.
TODO Flip y axis of the grid figures.
TODO Add figures to repository and link to them from article

## Discussion

In my project I've explored Avigdor's model of signal diversification in a computerized spatial simulation, adapted to Avigdor's model from Czaran previous work. I ran the simulations with different parameters of signal threshold, public goods threshold, public goods costs, RNG seeds as duplicates and diffusion.

We've seen several possible outcomes to the simulations under different parameters. An equilibrium between the two cooperating strains (S1R1, S2R2) at about 1:1, a similar equilibrium of the two cheating strains (S1R2, S2R1) at about 1:1 ratio of the total population, RPS oscillations about the equilibrium point, a steady state of the original cooperator (S1R1) with its cheater invador (S1R2).
