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

A proprosed model that explains how such diversity forms introduces an
evolutionary ratchet in which the order of divergence in QS signal or receptor
matters.
The approach used by Eldar et el. to investigate the interactions between
strains was to create a set of differential equations.
This approach is amenable to mathematical analysis but disregards spatial
effects.
(Eldar et el., 2011)

Stochastic cellular automata simulations were used to investigate social
interactions in bacteria, in which a lattice of abstract cells compete with
their immediate neighbours according to the state of their microenvironment,
thus mimicking a kind of limited infinite island model.
[?]
The model used had only one pherotype [is it the QS system as a whole or the
signal itself?] of quorum sensing, examining the existence or loss of signal,
receptor or public goods genes, while leaving the effects of multi-lingual
quorum sensing systems. (Czaran et el. 2009).

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
of specific pherotype (S_{1} or S_{2}), and locus R for receptor of specific
pherotype (R_{1} or R_{2}) which includes the signal receptor and the signal
transduction machinery that triggers the cooperative behaviour when the
critical signal concentration has been reached.
Each of these loci can harbour either an allele of one pherotype denoted by
subscript 1 (S_{1}, R_{1}), or of another pherotype denoted by subscript 2
(S_{2}, R_{2}).
Thus the bacteria can have 2^2 = 4 different genotypes.

### Fitness effects of cooperation


### Parameters used in the simulation

------------------------------------------------
| Variable name | Description | Czaran variable |
=================================================
|  CooperationEffectThreshold | Minimal number of cells that produce public goods in the Moore neighbourhood of a cell for the cell to benefit from those public goods | `n_{q}` |
---------------------------------------------
| SignalThreshold | Minimal number of cells in the Moore neighbourhood of a cell that produce a compatible signal pherotype to the cell's receptor for it to produce public goods | `n_{e}` |
---------------------------------------------
| BoardSize | The number of columns the grid has (equal to the number of rows) | `N` |
---------------------------------------------
| CooperationCost | The metabolic cost of producing the public goods | `m_{C}` |
---------------------------------------------
| PublicGoodsEffect | The metabolic benefit of the public goods | `r`
---------------------------------------------
| MutOddsS | Probability of mutation in the S locus per competition | `\mu_{s}` |
---------------------------------------------
| MutOddsR | Probability of mutation in the R locus per competition | `\mu_{r}` |
---------------------------------------------
| BasalCost | The metabolic cost each of the cells pays | `M_{0}` |
---------------------------------------------
| D | Diffusion rate | `D` |
---------------------------------------------
| Generations | BoardSize^2 |
---------------------------------------------
| SignalCost | Cost of signal production | 3 |
---------------------------------------------
| ReceptorCost | Cost of receptor production | 1 |
---------------------------------------------
| PublicGoodsEffect | 0.6
---------------------------------------------

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

Fitness effects of quorum sensing
Cells carrying genotype S_{1} produce the S_{1} pherotype molecule,
whereas R_{1} genotypes will respond to a sufficient amount of S_{1} 
signal in their immediate environment.

### Selection
Individuals compete for sites. Competition is played out
between randomly chosen pairs of neighbouring cells, on the
basis of their fitness:

Fitness = BasalCost/((CooperationCost + SignalCost + ReceptorCost)*(1 - PublicGoodsEffect))

TODO

If the cell produces public goods, CooperationCost will be included:
only be included if the cell produces public goods.
PublicGoodsEffect will be equal to zero in the case of insufficient public goods.
PublicGoodsEffect will be equal to the 

Each of the competitor's Fitness is multiplied by a different uniform random number [0, 1) and the result is compared.
The cell with the higher result is the winner of the competition.
If both cells are of the same strain, one of the cells goes through the mutation stage, as a competition is meaningless.

### Mutations
During the takeover of a site by the winner of the competition
the invading cell, i.e., the copy of the winner occupying the site of
the loser, can change any of its 2 alleles from
pherotype 1 to 2 or vice versa. We call these allele changes
‘‘mutations’’, but in fact they can be due to either mutation or
some other process like transformation or even the immigration of
individuals carrying the ‘‘mutant’’ allele. [??]
The point in allowing
allele changes both ways is to maintain
the presence of all different genes in the
population so that the system doesn’t get stuck in any particular
genetic state because of the lack of alternative alleles. Thus, each of
the possible allele changes may have a positive probability.
Mutations are independent at the two loci – e.g., the quorum
signal gene S can be mutated without changing the response module R at
the same time.

### Diffusion
Each competition step may be followed by a number (D) of
diffusion steps. One diffusion step consists of the random choice of
a site, and the 90 degree rotation of the 2x2 subgrid with the randomly
chosen site in its upper left corner. Rotation occurs in clockwise or
anticlockwise direction with equal probability [19]. D is the
diffusion parameter of the model: it is proportional to the average
number of diffusion steps taken by a cell per each competitive
interaction it is engaged in. Larger D means faster mixing in the
population. Since one diffusion move involves 4 cells, D= 1.0
amounts to an expected number of 4 diffusion steps per interaction
per cell. In the simulations we use the range 0.0#D#1.0 of the
diffusion parameter, and occasionally much higher values
(D= 15.0) as well.
Initial states and output
At t =0 the lattice is ‘‘seeded’’ either by the ‘‘Ignorant’’ (csr)
genotype on all sites, or the initial state is a random pattern of all
the 8 possible genotypes present at equal proportions. We simulate
pairwise competitive interactions, mutations and diffusive movements
for N generations. One generation consists of a number of
competition steps equal to the number of sites in the lattice, so that
each site is updated once per generation on average. In the
majority of simulations we have applied mutation rates of 1024
both ways at each locus, which is equivalent to an average of 9
mutation events per generation within the whole habitat. The
three functional alleles have a positive cost of expression,
constrained by the relation mCwwmSwmR (the actual values
used throughout the simulations are given in Table 1).


### Simulations
With the initial conditions specified above we follow the
evolution (the change in allele frequencies) for both cooperation
and the two components of quorum sensing. We investigate the
qualitative or quantitative effects on the evolution of cooperation
and quorum sensing of the crucial parameters of the model: the
fitness reward of cooperation (r), the metabolic cost of cooperation
(mC), the intensity of diffusive mixing (D) and the quorum
threshold (nq). The simulations have been run until the relative
frequencies of the three focal alleles (C, S and R) approached their
quasi-stationary values. This could be achieved within 10.000
generations in most cases. The first few simulations have been
repeated 3 times with each parameter setting, using different
random number arrays, but since variation in the results was very
small at a lattice size of 3006300 in all cases, and each run took a
long time to finish, we stopped producing replicate runs.
During the simulations we record and plot the time series of the
8 different genotype frequencies, from which the frequencies of the
three functional alleles can be calculated and plotted against time.
Evaluation of the model outputs
