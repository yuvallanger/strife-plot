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

Quorum sensing (QS) is the ability of bacteria to sense their own concentration.
A QS system is made of a signal and a signal specific receptor which regulates
the expression of QS sensitive genes.
Each bacteria continuously produce the QS chemical signal and export it outside
the cell.
When enough bacteria produce enough signal and the
receptor’s threshold is reached, various genes critical to group behaviour
are expressed and others are inhibited.
The genes responsible for group behaviour are called "public goods",
extracellular products, e.g. surfactants which add motility, scavenging
materials such as siderophores, hydrolases that tear down otherwise unreachable
nutritious polymers, which benefit each bacteria only when large enough numbers
of neighbouring bacteria produce them as well.

“Multiple bacterial species show intraspecific
divergence of their QS systems, where signals from one strain can
activate their own receptor but fail to activate and sometimes inhibit
a receptor from a different strain (2–7)."

In gram positive bacteria, evolutionary close species exhibit high diversity of
their quorum sensing machinery.
"This divergence seems to be under strong selection, as implied by the
functional divergence and is also corroborated by rapid sequence divergence
(8–9), the signatures of diversifying selection (10–11), and the spread of
divergent QS systems through horizontal gene transfer (3, 12)."

A proposed model that explains how such diversity forms introduces an
evolutionary ratchet in which the order of divergence in QS signal or receptor
matters.
The approach used by Eldar et al. to investigate the interactions between
strains was to create a set of differential equations.
This approach is amenable to mathematical analysis but disregards spatial
effects.
(Eldar et al., 2011)

Stochastic cellular automata simulations were used to investigate social
interactions in bacteria, in which a lattice of abstract cells compete with
their immediate neighbours according to the state of their microenvironment,
thus mimicking a kind of limited infinite island model.
[?]
The model used had only one pherotype [is it the QS system as a whole or the
signal itself?] of quorum sensing, examining the existence or loss of signal,
receptor or public goods genes, while leaving the effects of multi-lingual
quorum sensing systems. (Czaran et al. 2009)

In my project I've adapted Czaran's algorithm to incorporate Eldar's
theoretical model of competing pherotypes in order to investigate spatial
effects that are not shown in Eldar's system of differential equations.

Methods
-------

The simulation consists of a toroid board for which both the width and the
height are equal to N=300 [?], a total of N^2=90000 cells.
Each cell has two QS related loci, one loci for the receptor and another for
the signal.
There are two possible receptor alleles, R_{1} and R_{2} and two possible
signal alleles, S_{1} and S_{2}.
[here be Eldar's diagrams]
The each generation of the simulation follows two stages:

A competition stage and a diffusion stage.

Within the competition stage, a cell is drawn out of the whole board and

![Image: overview of the Eldarian model]

The model we use is a two-dimensional cellular automaton (CA) of toroidal
lattice topology.
Each of the 300x300 grid-points of the square lattice represent a site for a
single bacterium;
all the sites are always occupied, i.e., bacteria may replace each other, but
may not leave empty sites.
The inhabitants of the sites may differ at 2 genetic loci: locus S for signal
of specific pherotype ($S_{1}$ or $S_{2}$), and locus R for receptor of specific
pherotype ($R_{1}$ or $R_{2}$) which includes the signal receptor and the signal
transduction machinery that triggers the cooperative behaviour when the
critical signal concentration has been reached.
Each of these loci can harbour either an allele of one pherotype denoted by
subscript 1 ($S_{1}$, $R_{1}$), or of another pherotype denoted by subscript 2
($S_{2}$, $R_{2}$).
Thus the bacteria can have $2^{2}=4$ different genotypes.


Variable name | Description
:--------------|:-----------
CooperationEffectThreshold | Minimal number of cells that produce public goods in the Moore neighbourhood of a cell for the cell to benefit from those public goods
SignalThreshold | Minimal number of cells in the Moore neighbourhood of a cell that produce a compatible signal pherotype to the cell's receptor for it to produce public goods
BoardSize | The number of columns the grid has (equal to the number of rows)
CooperationCost | The metabolic cost of producing the public goods
PublicGoodsEffect | The metabolic benefit of the public goods
MutOddsS | Probability of mutation in the S locus per competition
MutOddsR | Probability of mutation in the R locus per competition
BasalCost | The metabolic cost each of the cells pays
D | Diffusion rate
Generations | Number of generations for each simulation
SignalCost | Cost of signal production
ReceptorCost | Cost of receptor production
PublicGoodsEffect | 0.6

Table: Parameters used in the simulation

### Fitness effects of cooperation



The product of the cooperating is supposed to be an excreted ‘public good’
molecule such as an exo-enzyme for extracellular food digestion.
It may increase the fitness of a bacterium, provided there are at least
$CooperationEffectThreshold$ [was `q_{n}`] bacteria (possibly, but not
necessarily, including itself) expressing the public goods as well within its
3x3-cell neighbourhood;
$CooperationEffectThreshold$ is the quorum threshold of cooperation.
An individual can only obtain a fitness benefit from cooperative behaviour in
its neighbourhood if at least
$CooperationEffectThreshold$ cooperators are present in that neighbourhood. On the other
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

$Fitness = BasalCost/((CooperationCost + SignalCost + ReceptorCost)*(1 - PublicGoodsEffect))$

If the cell produces public goods, $CooperationCost$ will be equal to 1,
otherwise it’ll be equal to the cost of producing public goods.
If there are a sufficient number of cooperators around the cell,
$PublicGoodsEffect$ will equal the public goods effect, from 0 to 1, where
bigger is better for the competitor, otherwise $PublicGoodsEffect$ will be 0.

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

Each competition step may be followed by a number $D$ of diffusion steps.
One diffusion step consists of the random choice of a site, and the 90 degree
rotation of the 2x2 subgrid with the randomly chosen site in its upper left
corner.
Rotation occurs in clockwise or anticlockwise direction with equal probability.
$D$ is the diffusion parameter of the model:
it is proportional to the average number of diffusion steps taken by a cell per
each competitive interaction it is engaged in.
Larger D means faster mixing in the population.
Since one diffusion move involves 4 cells, $D=1.0$ amounts to an expected
number of 4 diffusion steps per interaction per cell.

### Initial states and output

At $t=0$ the lattice is “seeded” by the first pherotype $S_{1}R_{1}$.
We simulate pairwise competitive interactions, mutations and diffusive
movements for N generations.
One generation consists of a number of competition steps equal to the number of
sites in the lattice, so that each site is updated once per generation on
average.
We have applied mutation rates of $10^{-4}$ both ways at each locus, which is
equivalent to an average of $BoardSize*BoardSize*10^{-4}=9$ mutation events per
generation for each locus within the whole habitat.

### Simulations

With the initial conditions specified above we follow the evolution (the change
in allele frequencies) of the two loci.
We investigate the qualitative or quantitative effects on the evolution of
quorum sensing of the crucial parameters of the model:
the metabolic cost of cooperation $CooperationCost$,
the intensity of diffusive mixing $D$,
the threshold of PG needed for the cooperation fitness effect
$CooperationEffectThreshold$
and the threshold of signal needed to produce public goods $SignalThreshold$.
The simulations have been run for 2000 generations.
During the simulations we record and plot the time series of the 4 different
genotype frequencies, from which the frequencies of the two functional alleles
can be calculated and plotted against time.
