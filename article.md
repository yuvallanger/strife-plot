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


* CooperationEffectThreshold - was `q_{n}`
* SignalThreshold - `n_{e}`
* BoardSize - `N`
* `m_{S}`
* `m_{R}`
* `m_{C}`
* `r`
* MutOddsS - `\mu_{s}`
* MutOddsR - `\mu_{r}`
* BasalCost - M
* D - `D`

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

The fitness benefit of a QS system is an indirect one:
communication using a signalling system may spare unnecessary costs of 
futile attempts to cooperate whenever the
local density of potential cooperators is lower than the quorum nq.
For this communication benefit to be feasible, the QS machinery
altogether has to be much cheaper (in terms of metabolic costs)
than cooperation itself, otherwise constitutive (unconditional and
permanent) cooperation would be a better option for the
bacterium, and resources invested into QS would be wasted.
Thus the ordering of the metabolic fitness costs of cooperation and
QS are assumed to be mCwwmS§mR. The inactive alleles c, s
and r carry no metabolic cost: mc~ms~mr~0:
The effect of the quorum sensing genes on the
cooperation gene
The quorum signal is supposed to be the regulator of
cooperation: bacteria with a C.R genome (i.e., those carrying a
functional cooperation allele C and a working response module R)
will actually express the C gene (i.e., cooperate) only if there is a
sufficient quorum nq of signallers (.S. individuals) within their
neighbourhood. That is, C.R cells wait for a number of
‘‘promises’’ of cooperation in their 3x3-cell neighbourhood before
they switch to cooperating mode (produce the public good)
themselves. C.r genotypes do not have a functioning response
module, therefore they produce the public good constitutively.
Selection
Individuals compete for sites. Competition is played out
between randomly chosen pairs of neighbouring cells, on the
basis of the actual net metabolic burdens M(1) and M(2) they
carry. The net metabolic burden M(i) of an individual i is
calculated as the sum of the basic metabolic load M0 carried by all
individuals and the total metabolic cost me(i) of the actual gene
expressions at the three loci concerned (see Table 1), multiplied by
the unit complement of the cooperation reward parameter (1 – r) if
it is surrounded by a sufficient quorum of cooperators:
MðiÞ~½M0zmeðiÞ if # of cooperators in neighborhood
is below the quorum threshold nq
MðiÞ~½M0zmeðiÞð1{rÞ otherwise ð0vrv1Þ
Thus, successful cooperation reduces the total metabolic burden
in a multiplicative fashion. The relative fitness of individual i is
defined as its net metabolic burden relative to the basic metabolic
load as M0=MðiÞ. In practice, the outcome of competition is
determined by a random draw, with chances of winning weighted
in proportion to the relative fitnesses. The winner takes the site of
the loser, replacing it by a copy of itself.
Mutations
During the takeover of a site by the winner of the competition
the invading cell, i.e., the copy of the winner occupying the site of
the loser, can change one of its 3 alleles (chosen at random) from
functional to inactive or vice versa. We call these allele changes
‘‘mutations’’, but in fact they can be due to either mutation or
some other process like transformation or even the immigration of
individuals carrying the ‘‘mutant’’ allele. The point in allowing
allele changes both ways (losing and obtaining them) is to maintain
the presence of all six different genes (C, c, S, s, R, r) in the
population so that the system doesn’t get stuck in any particular
genetic state because of the lack of alternative alleles. Thus, each of
the six possible allele changes may have a positive probability.
Mutations are independent at the three loci – e.g., the quorum
signal gene S can be lost without losing the response module R at
the same time; the resulting mutant will be ‘‘mute’’ yet still able to
respond to quorum signals.
Diffusion
Each competition step may be followed by a number (D) of
diffusion steps. One diffusion step consists of the random choice of
a site, and the 90u rotation of the 262 subgrid with the randomly
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
Simulations
With the initial conditions specified above we follow the
evolution (the change in allele frequencies) for both cooperation
and the two components of quorum sensing. We investigate the
qualitative or quantitative effects on the evolution of cooperation
and quorum sensing of the crucial parameters of the model: the
fitness reward of cooperation (r), the metabolic cost of cooperation
(mC), the intensity of diffusive mixing (D) and the quorum
threshold (nq). The simulations have been run until the relative
Cooperation and Cheating
PLoS ONE | www.plosone.org 3 August 2009 | Volume 4 | Issue 8 | e6655
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
The simulation results are recorded as 10.000-generation time
series of genotype frequencies and spatial patterns of the
genotypes. With regard to allele frequencies we asked the following
question: are the genes for cooperation (C) and quorum sensing (S
and R) selected for beyond their respective mutation-selection
equilibria based on the metabolic selection coefficients sC = (MC
2M0)/MC, sS = (MS 2M0)/MS and sR = (MR 2M0)/MR and the
(uniform) mutation rate m ? For example, relative frequencies of
the cooperating allele above its mutation-selection equilibrium
^qC~m=ðsCzmÞ indicate a net fitness benefit of cooperation and
thus positive selection for the C allele. ^qS and ^qR can be
calculated the same way.
