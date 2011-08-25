"""
achrom - additive model of polypeptide chromatography
=====================================================

Summary
-------

The additive model of polypeptide chromatography, or achrom is the most basic
model for peptide retention time prediction. The main equation behind
achrom has the following form:

.. math::

    RT = (1.0 + m\,ln(N)) \sum_{i=1}^{i=N}{RC_i} + RT_0

Here, :math:`RC_i` is the retention coefficient of i-th amino acid
residue in a peptide, N is the total number of amino acid residues and
:math:`RT_0` is a constant retention time shift.

In order to use achrom, one needs to find the retention
coeffcients, using experimentally determined retention times for a training set
of peptide retention times, i.e. to *calibrate* the model.

Calibration:
------------

  :py:func:`get_RCs` - find a set of retention coefficients using a
  given set of peptides with known retention times and a fixed value of
  length correction factor.

  :py:func:`get_RCs_vary_lcf` - find the best length correction factor
  and a set of retention coefficients for a given peptide sample.

Retention time calculation:
---------------------------

  :py:func:`calculate_RT` - calculate the retention time of a peptide
  using a given set of retention coefficients.

Data:
-----

  :py:data:`RCs_guo_ph2_0` - a set of retention coefficients (RCs)
  from [#Guo1]_. Conditions: Synchropak RP-P C18 column (250 x 4.1 mm
  I.D.), gradient (A = 0.1% aq. TFA, pH 2.0; B = 0.1% TFA in acetonitrile) at
  1% B/min, flow rate 1 ml/min, 26 centigrades.

  :py:data:`RCs_guo_ph7_0` - a set of retention coefficients (RCs)
  from [#Guo1]_. Conditions: Synchropak RP-P C18 column (250 x 4.1 mm
  I.D.), gradient (A = aq. 10 mM (NH4)2HPO4 - 0.1 M NaClO4, pH 7.0; B
  = 0.1 M NaClO4 in 60% aq. acetonitrile) at 1.67% B/min, flow rate 1
  ml/min, 26 centigrades.
  
  :py:data:`RCs_meek_ph2_1` - a set of RCs from [#Meek]_. Conditions: Bio-Rad
  "ODS" column, gradient (A = 0.1 M NaClO4, 0.1% phosphoric acid in
  water; B = 0.1 M NaClO4, 0.1% phosphoric acid in 60%
  aq. acetonitrile) at 1.25% B/min, room temperature.
  
  :py:data:`RCs_meek_ph7_4` - a set of RCs from [#Meek]_. Conditions: Bio-Rad
  "ODS" column, gradient (A = 0.1 M NaClO4, 5 mM phosphate buffer in
  water; B = 0.1 M NaClO4, 5 mM phosphate buffer in 60%
  aq. acetonitrile) at 1.25% B/min, room temperature.
  
  :py:data:`RCs_browne_tfa` - a set of RCs found in
  [#Browne]_. Conditions: Waters mjuBondapak C18 column, gradient (A =
  0.1% aq. TFA, B = 0.1% TFA in acetonitrile) at 0.33% B/min, flow
  rate 1.5 ml/min.
  
  :py:data:`RCs_browne_hfba` - a set of RCs found in
  [#Browne]_. Conditions: Waters mjuBondapak C18 column, gradient (A =
  0.13% aq. HFBA, B = 0.13% HFBA in acetonitrile) at 0.33% B/min, flow
  rate 1.5 ml/min.
  
  :py:data:`RCs_palmblad` - a set of RCs from
  [#Palmblad]_. Conditions: a fused silica column (80-100 x 0.200 mm
  I.D.) packed in-house with C18 ODS-AQ; solvent A = 0.5% aq. HAc,
  B = 0.5% HAc in acetonitrile.
  
  :py:data:`RCs_yoshida` - a set of RCs from [#Yoshida]_. Conditions:
  TSK gel Amide-80 column (250 x 4.6 mm I.D.), gradient (A = 0.1% TFA
  in ACN-water (90:10); B = 0.1% TFA in ACN-water (55:45)) at 0.6%
  water/min, flow rate 1.0 ml/min, 40 centigrades.

Theory
------

The additive model of polypeptide chromatography, or the model of
retention coefficients was the earliest attempt to describe the dependence of
retention time of a polypeptide in liquid chromatography on its sequence
[#Meek]_, [#Guo1]_. In this model, each amino acid is assigned a number, or
a *retention coefficient* (RC) describing its retention properties. The
retention time (RT) during a gradient elution is then calculated as:

.. math::

    RT = \sum_{i=1}^{i=N}{RC_i} + RT_0,

which is a sum of retention coefficients of all amino acid residues in a
polypeptide. This equation can also be expressed in terms of linear
algebra:

.. math::
    
    RT = \overline{aa} \cdot \overline{RC} + RT_0,
    
where :math:`\\overline{aa}` is a vector of amino acid composition,
i.e. :math:`\\overline{aa}_i` is the number of amino acid residues of i-th
type in a polypeptide; :math:`\overline{RC}` is a vector of respective
retention coefficients.

In this formulation, it is clear that additive model gives the same results for
any two peptides with different sequences but the same amino acid
composition. In other words, **additive model is not sequence-specific**.

The additive model has two advantages over all other models of chromatography
- it is easy to understand and use. The rule behind the additive model is as
simple as it could be: **each amino acid residue shifts retention time by a
fixed value, depending only on its type**. This rule allows geometrical
interpretation. Each peptide may be represented by a point in 21-dimensional
space, with first 20 coordinates equal to the amounts of corresponding amino
acid residues in the peptide and 21-st coordinate equal to RT. The additive
model assumes that a line may be drawn through these points. Of course, this
assumption is valid only partially, and most points would not lie on the
line. But the line would describe the main trend and could be used to estimate
retention time for peptides with known amino acid composition.

This best fit line is described by retention coefficients and :math:`RT_0`.
The procedure of finding these coefficients is called *calibration*. There is `an
analytical solution to calibration of linear models
<http://en.wikipedia.org/wiki/Linear_regression>`_, which makes them
especially useful in real applications.

Several attempts were made in order to improve the accuracy of prediction by
the additive model (for a review of the field we suggest to read [#Baczek]_
and [#Babushok]_). The two implemented in this module are the logarithmic
length correction term described in [#MantLogLen]_ and additional sets of
retention coefficients for terminal amino acid residues [#Tripet]_.

Logarithmic length correction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This enhancement was firstly described in [#MantLogLen]_. Briefly, it was
found that the following equation better describes the dependence of RT on the
peptide sequence:

.. math::

    RT = \sum_{i=1}^{i=N}{RC_i} + m\,ln(N) \sum_{i=1}^{i=N}{RC_i} + RT_0

We would call the second term :math:`m\,ln(N) \sum_{i=1}^{i=N}{RC_i}` *the
length correction term* and m - *the length correction factor*. The simplified
and vectorized form of this equation would be:

.. math::
    
    RT = (1 + m\,ln(N)) \, \overline{RC} \cdot \overline{aa} + RT_0

This equation may be reduced to a linear form and solved by the standard
methods.

Terminal retention coefficients
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another significant improvement may be obtained through introduction of
separate sets of retention coefficients for terminal amino acid residues
[#Tripet]_. 

References
----------

.. [#Meek] Meek, J. L. Prediction of peptide retention times in high-pressure
   liquid chromatography on the basis of amino acid composition. PNAS, 1980,
   77 (3), 1632-1636.
   `Link <http://www.ncbi.nlm.nih.gov/pubmed/6929513>`_

.. [#Guo1] Guo, D.; Mant, C. T.; Taneja, A. K.; Parker, J. M. R.; Hodges,
   R. S.  Prediction of peptide retention times in reversed-phase
   high-performance liquid chromatography I. Determination of retention
   coefficients of amino acid residues of model synthetic peptides. Journal of
   Chromatography A, 1986, 359, 499-518.
   `Link. <http://dx.doi.org/10.1016/0021-9673(86)80102-9>`_
   
.. [#Baczek] Baczek, T.; Kaliszan, R. Predictions of peptides' retention times
   in reversed-phase liquid chromatography as a new supportive tool to improve
   protein identification in proteomics. Proteomics, 2009, 9 (4), 835-47.
   `Link. <http://dx.doi.org/10.1002/pmic.200800544>`_

.. [#Babushok] Babushok, V. I.; Zenkevich, I. G. Retention Characteristics of
   Peptides in RP-LC: Peptide Retention Prediction. Chromatographia, 2010, 72
   (9-10), 781-797.
   `Link. <http://dx.doi.org/10.1365/s10337-010-1721-8>`_
   
.. [#MantLogLen] Mant, C. T.; Zhou, N. E.; Hodges, R. S. Correlation of
   protein retention times in reversed-phase chromatography with polypeptide
   chain length and hydrophobicity. Journal of Chromatography A, 1989, 476,
   363-375. `Link. <http://dx.doi.org/10.1016/S0021-9673(01)93882-8>`_

.. [#Tripet] Tripet, B.; Cepeniene, D.; Kovacs, J. M.; Mant, C. T.; Krokhin,
   O. V.; Hodges, R. S. Requirements for prediction of peptide retention time
   in reversed-phase high-performance liquid chromatography:
   hydrophilicity/hydrophobicity of side-chains at the N- and C-termini of
   peptides are dramatically affected by the end-groups and location. Journal
   of chromatography A, 2007, 1141 (2), 212-25.
   `Link. <http://dx.doi.org/10.1016/j.chroma.2006.12.024>`_

.. [#Browne] Browne, C. A.; Bennett, H. P. J.; Solomon, S. The
   isolation of peptides by high-performance liquid chromatography
   using predicted elution positions. Analytical Biochemistry, 1982,
   124 (1), 201-208.

.. [#Palmblad] Palmblad, M.; Ramstrom, M.; Markides, K. E.; Hakansson,
   P.; Bergquist, J. Prediction of Chromatographic Retention and
   Protein Identification in Liquid Chromatography/Mass
   Spectrometry. Analytical Chemistry, 2002, 74 (22), 5826-5830.

.. [#Yoshida] Yoshida, T. Calculation of peptide retention
   coefficients in normal-phase liquid chromatography. Journal of
   Chromatography A, 1998, 808 (1-2), 105-112.
   
.. ipython::
   :suppress:

   In [1]: import pyteomics.parser; from pprint import pprint
"""

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license.php 

import operator
import numpy
import auxiliary
from parser import std_labels, peptide_length, amino_acid_composition

def get_RCs(peptides, RTs, length_correction_factor = -0.21,
            term_aa = False, **kwargs):
    """Calculate the retention coefficients of amino acids using
    retention times of a peptide sample and a fixed value of length
    correction factor.

    Parameters
    ----------
    sequence : list of str
        List of peptide sequences.
    RTs: list of float
        List of corresponding retention times.
    length_correction_factor : float, optional
        A multiplier before ln(L) term in the equation for the retention
        time of a peptide. Set to -0.21 by default.
    term_aa : bool, optional
        If True, terminal amino acids are treated as being
        modified with 'ntermX'/'ctermX' modifications. False by default.
    labels : list of str, optional
        List of all possible amino acids and terminal groups
        (default: 20 standard amino acids, N-terminal NH2- and
        C-terminal -OH);

    Returns
    -------
    RC_dict : dict
        Dictionary with the calculated retention coefficients.
        
        - RC_dict['aa'] -- amino acid retention coefficients.
        
        - RC_dict['const'] -- constant retention time shift.
        
        - RC_dict['lcf'] -- length correction factor.

    Examples
    --------
    >>> RCs = get_RCs(['A','AA'], [1.0, 2.0], 0.0, labels=['A'])
    >>> RCs['const'] = round(RCs['const'], 4) # Rounding for comparison
    >>> RCs == {'aa': {'A': 1.0}, 'lcf': 0.0, 'const': 0.0}
    True
    >>> RCs = get_RCs(['A','AA','B'], [1.0, 2.0, 2.0], 0.0, labels=['A','B'])
    >>> RCs['aa']['A'] = round(RCs['aa']['A'], 4)
    >>> RCs['aa']['B'] = round(RCs['aa']['B'], 4)
    >>> RCs['const'] = round(RCs['const'], 4)
    >>> RCs == {'aa':{'A': 1.0, 'B': 2.0},'const': 0.0, 'lcf': 0.0}
    True
    """

    labels = kwargs.get('labels', std_labels)

    # Make a list of all amino acids present in the sample.
    peptide_dicts = [
        amino_acid_composition(peptide, False, term_aa, labels=labels)
        for peptide in peptides]

    detected_amino_acids = set([aa for peptide_dict in peptide_dicts
                                for aa in peptide_dict])

    # Determine retention coefficients using multidimensional linear
    # regression. 
    composition_array = [
        [peptide_dicts[i].get(aa, 0.0) 
         * (1.0 + length_correction_factor
            * numpy.log(peptide_length(peptide_dicts[i])))
           for aa in detected_amino_acids]
        + [1.0] # Add free term to each peptide.
        for i in range(len(peptides))]

    # Add normalizing conditions for terminal retention coefficients. The
    # condition we are using here is quite arbitrary. It implies that the sum
    # of N- or C-terminal RCs minus the sum of corresponding internal RCs must
    # be equal to zero.
    if term_aa:
        for term_label in ['nterm', 'cterm']:
            normalizing_peptide = []
            for aa in detected_amino_acids:
                if aa.startswith(term_label):
                    normalizing_peptide.append(1.0)
                elif (term_label+aa) in detected_amino_acids:
                    normalizing_peptide.append(-1.0)
                else:
                    normalizing_peptide.append(0.0)
            normalizing_peptide.append(0.0)
            composition_array.append(normalizing_peptide)
            RTs.append(0.0)

    # Use least square linear regression.
    RCs, res, rank, s = numpy.linalg.lstsq(numpy.array(composition_array),
                                           numpy.array(RTs))

    if term_aa:
        for term_label in ['nterm', 'cterm']:
            RTs.pop()

    # Form output.
    RC_dict = {}
    RC_dict['aa'] = dict(
        zip(list(detected_amino_acids),
            RCs[:len(detected_amino_acids)]))        
    RC_dict['const'] = RCs[len(detected_amino_acids)]
    RC_dict['lcf'] = length_correction_factor

    # Find remaining terminal RCs.
    if term_aa:
        for term_label in ['nterm', 'cterm']:
            # Check if there are terminal RCs remaining undefined.
            undefined_term_RCs = [aa for aa in RC_dict['aa']
                                if not aa[1:].startswith('term')
                                and term_label + aa not in RC_dict['aa']]
            if not undefined_term_RCs:
                continue

            # Find a linear relationship between internal and terminal RCs.
            defined_term_RCs = [aa for aa in RC_dict['aa']
                              if not aa[1:].startswith('term')
                              and term_label + aa in RC_dict['aa']]
            
            a, b, r, stderr = auxiliary.linear_regression(
                [RC_dict['aa'][aa] for aa in defined_term_RCs],
                [RC_dict['aa'][term_label+aa] for aa in defined_term_RCs])

            # Define missing terminal RCs using this linear equation.
            for aa in undefined_term_RCs:
                RC_dict['aa'][term_label + aa] = a * RC_dict['aa'][aa] + b

    return RC_dict

def get_RCs_vary_lcf(peptides, RTs,
                term_aa = False,
                lcf_range = (-1.0, 1.0),
                **kwargs):
    """Find the best combination of a length correction factor and
    retention coefficients for a given peptide sample.

    Parameters
    ----------
    sequence : list of str
        List of peptide sequences.
    RTs : list of float
        List of corresponding retention times.
    term_aa : bool, optional
        If True, terminal amino acids are treated as being
        modified with 'ntermX'/'ctermX' modifications. False by default.
    lcf_range : 2-tuple of float, optional
        Range of possible values of the length correction factor.
    labels : list of str, optional
        List of labels for all possible amino acids and terminal groups
        (default: 20 standard amino acids, N-terminal NH2- and
        C-terminal -OH).

    Returns
    -------
    RC_dict : dict
        Dictionary with the calculated retention coefficients.
        
        - RC_dict['aa'] -- amino acid retention coefficients.
        
        - RC_dict['const'] -- constant retention time shift.
        
        - RC_dict['lcf'] -- length correction factor.

    >>> RC_dict = get_RCs_vary_lcf(['A', 'AA', 'AAA'], \
        [1.0, 2.0, 3.0], \
        labels=['A'])
    >>> RC_dict['aa']['A'] = round(RC_dict['aa']['A'], 4)
    >>> RC_dict['lcf'] = round(RC_dict['lcf'], 4)
    >>> RC_dict['const'] = round(RC_dict['const'], 4)
    >>> RC_dict == {'aa': {'A': 1.0}, 'lcf': 0.0, 'const': 0.0}
    True
    """
    labels = kwargs.get('labels', std_labels)

    best_r = -1.1
    best_RC_dict = {}

    min_lcf = lcf_range[0]
    max_lcf = lcf_range[1]
    step = (max_lcf - min_lcf) / 10.0
    while step > 0.1:
        lcf_grid = numpy.arange(min_lcf, max_lcf,
                                (max_lcf - min_lcf) / 10.0)
        for lcf in lcf_grid:
            RC_dict = get_RCs(peptides, RTs, lcf, term_aa, labels=labels)
            regression_coeffs = auxiliary.linear_regression(
                RTs, 
                [calculate_RT(peptide, RC_dict) for peptide in peptides])
            if regression_coeffs[2] > best_r:
                best_r = regression_coeffs[2]
                best_RC_dict = dict(RC_dict)
        min_lcf = best_RC_dict['lcf'] - step
        max_lcf = best_RC_dict['lcf'] + step
        step = (max_lcf - min_lcf) / 10.0

    return best_RC_dict

def calculate_RT(peptide, RC_dict):
    """Calculate the retention time of a peptide using a given set
    of retention coefficients.

    Parameters
    ----------
    peptide : str
        A peptide sequence.
    RC_dict :
        A set of retention coefficients, length correction factor and
        a fixed retention time shift.

    Returns
    -------
    RT : float
        Calculated retention time.

    Examples
    --------
    >>> RT = calculate_RT('AA', {'aa':{'A':1.1},'lcf':0.0,'const':0.1})
    >>> abs(RT - 2.3) < 1e-6      # Float comparison
    True
    >>> RT = calculate_RT('AAA', {'aa': {'ntermA':1.0, 'A':1.1, 'ctermA':1.2},\
        'lcf':0.0,\
        'const':0.1})
    >>> abs(RT - 3.4) < 1e-6      # Float comparison
    True
    """
    
    amino_acids = [aa for aa in RC_dict['aa']
                   if not (aa.startswith('cterm') or aa.startswith('nterm'))]

    # Check if there are retention coefficients for terminal amino acids.
    term_aa = False
    for aa in RC_dict['aa']:
        if aa.startswith('nterm') or aa.startswith('cterm'):
            term_aa = True
            break

    # Calculate retention time.
    peptide_dict = amino_acid_composition(peptide, False, term_aa,
                                          labels=amino_acids)
    length_correction_term = (
        1.0 + RC_dict['lcf'] * numpy.log(peptide_length(peptide_dict)))
    RT = 0.0
    for aa in peptide_dict:
        # if (aa not in RC_dict['aa'] and
        #     (aa.startswith('nterm') or aa.startswith('cterm'))):
        #     RT += peptide_dict[aa] * RC_dict['aa'][aa[5:]]
        # else:
            RT += peptide_dict[aa] * RC_dict['aa'][aa]
    RT *= length_correction_term
    RT += RC_dict['const']

    return RT

RCs_guo_ph2_0 = {'aa':{'K': -2.1,
                       'G': -0.2,
                       'L':  8.1,
                       'A':  2.0,
                       'C':  2.6,
                       'E':  1.1,
                       'D':  0.2,
                       'F':  8.1,
                       'I':  7.4,
                       'H': -2.1,
                       'M':  5.5,
                       'N': -0.6,
                       'Q':  0.0,
                       'P':  2.0,
                       'S': -0.2,
                       'R': -0.6,
                       'T':  0.6,
                       'W':  8.8,
                       'V':  5.0,
                       'Y':  4.5},
                 'lcf': 0.0,
                 'const': 0.0}
"""A set of retention coefficients from Guo, D.; Mant, C. T.; Taneja,
A. K.; Parker, J. M. R.; Hodges, R. S.  Prediction of peptide
retention times in reversed-phase high-performance liquid
chromatography I. Determination of retention coefficients of amino
acid residues of model synthetic peptides. Journal of Chromatography
A, 1986, 359, 499-518.

Conditions: Synchropak RP-P C18 column (250 x 4.1 mm I.D.), gradient
(A = 0.1% aq. TFA, pH 2.0; B = 0.1% TFA in acetonitrile) at 1% B/min,
flow rate 1 ml/min, 26 centigrades.

.. ipython::
   
   In [2]: pprint(pyteomics.achrom.RCs_guo_ph2_0)
"""

RCs_guo_ph7_0 = {'aa':{'K': -0.2,
                       'G': -0.2,
                       'L':  9.0,
                       'A':  2.2,
                       'C':  2.6,
                       'E': -1.3,
                       'D': -2.6,
                       'F':  9.0,
                       'I':  8.3,
                       'H':  2.2,
                       'M':  6.0,
                       'N': -0.8,
                       'Q':  0.0,
                       'P':  2.2,
                       'S': -0.5,
                       'R':  0.9,
                       'T':  0.3,
                       'W':  9.5,
                       'V':  5.7,
                       'Y':  4.6},
                 'lcf': 0.0,
                 'const': 0.0}
"""A set of retention coefficients from Guo, D.; Mant, C. T.; Taneja,
A. K.; Parker, J. M. R.; Hodges, R. S.  Prediction of peptide
retention times in reversed-phase high-performance liquid
chromatography I. Determination of retention coefficients of amino
acid residues of model synthetic peptides. Journal of Chromatography
A, 1986, 359, 499-518.

Conditions: Synchropak RP-P C18 column (250 x 4.1 mm I.D.), gradient
(A = aq. 10 mM (NH4)2HPO4 - 0.1 M NaClO4, pH 7.0; B = 0.1 M NaClO4 in
60% aq. acetonitrile) at 1.67% B/min, flow rate 1 ml/min, 26
centigrades.

.. ipython::
   
   In [2]: pprint(pyteomics.achrom.RCs_guo_ph7_0)
"""

RCs_meek_ph2_1 = {'aa':{'K': -3.2,
                        'G': -0.5,
                        'L': 10.0,
                        'A': -0.1,
                        'C': -2.2,
                        'E': -7.5,
                        'D': -2.8,
                        'F': 13.9,
                        'I': 11.8,
                        'H':  0.8,
                        'M':  7.1,
                        'N': -1.6,
                        'Q': -2.5,
                        'P':  8.0,
                        'S': -3.7,
                        'R': -4.5,
                        'T':  1.5,
                        'W': 18.1,
                        'V':  3.3,
                        'Y':  8.2},
                  'lcf': 0.0,
                  'const': 0.0}
"""A set of retention coefficients determined in Meek,
J. L. Prediction of peptide retention times in high-pressure liquid
chromatography on the basis of amino acid composition. PNAS, 1980, 77
(3), 1632-1636.

Conditions: Bio-Rad "ODS" column, gradient (A = 0.1 M NaClO4,
0.1% phosphoric acid in water; B = 0.1 M NaClO4, 0.1% phosphoric acid
in 60% aq. acetonitrile) at 1.25% B/min, room temperature.

.. ipython::
   
   In [2]: pprint(pyteomics.achrom.RCs_meek_ph2_1)
"""

RCs_meek_ph7_4 = {'aa':{'K':  0.1,
                        'G':  0.0,
                        'L':  8.8,
                        'A':  0.5,
                        'C': -6.8,
                        'E':-16.9,
                        'D': -8.2,
                        'F': 13.2,
                        'I': 13.9,
                        'H': -3.5,
                        'M':  4.8,
                        'N':  0.8,
                        'Q': -4.8,
                        'P':  6.1,
                        'S':  1.2,
                        'R':  0.8,
                        'T':  2.7,
                        'W': 14.9,
                        'V':  2.7,
                        'Y':  6.1},
                  'lcf': 0.0,
                  'const': 0.0}
"""A set of retention coefficients determined in Meek,
J. L. Prediction of peptide retention times in high-pressure liquid
chromatography on the basis of amino acid composition. PNAS, 1980, 77
(3), 1632-1636.

Conditions: Bio-Rad "ODS" column, gradient (A = 0.1 M NaClO4,
5 mM phosphate buffer in water; B = 0.1 M NaClO4, 5 mM phosphate buffer
in 60% aq. acetonitrile) at 1.25% B/min, room temperature.

.. ipython::
   
   In [2]: pprint(pyteomics.achrom.RCs_meek_ph7_4)
"""

RCs_browne_tfa = {'aa':{'K': -3.7,
                        'G': -1.2,
                        'L': 20.0,
                        'A':  7.3,
                        'C': -9.2,
                        'E': -7.1,
                        'D': -2.9,
                        'F': 19.2,
                        'I':  6.6,
                        'H': -2.1,
                        'M':  5.6,
                        'N': -5.7,
                        'Q': -0.3,
                        'P':  5.1,
                        'S': -4.1,
                        'pS':-6.5,
                        'R': -3.6,
                        'T':  0.8,
                        'pT':-1.6,
                        'W': 16.3,
                        'V':  3.5,
                        'Y':  5.9,
                        'pY': 3.5},
                  'lcf': 0.0,
                  'const': 0.0}
"""A set of retention coefficients determined in Browne, C. A.;
Bennett, H. P. J.; Solomon, S. The isolation of peptides by
high-performance liquid chromatography using predicted elution
positions. Analytical Biochemistry, 1982, 124 (1), 201-208.

Conditions: Waters mjuBondapak C18 column, gradient (A = 0.1% aq. TFA,
B = 0.1% TFA in acetonitrile) at 0.33% B/min, flow rate 1.5 ml/min.

.. ipython::
   
   In [2]: pprint(pyteomics.achrom.RCs_browne_tfa)
"""

RCs_browne_hfba = {'aa':{'K': -2.5,
                         'G': -2.3,
                         'L': 15.0,
                         'A':  3.9,
                         'C':-14.3,
                         'E': -7.5,
                         'D': -2.8,
                         'F': 14.7,
                         'I': 11.0,
                         'H':  2.0,
                         'M':  4.1,
                         'N': -2.8,
                         'Q':  1.8,
                         'P':  5.6,
                         'S': -3.5,
                         'pS':-7.6,
                         'R':  3.2,
                         'T':  1.1,
                         'pT':-3.0,
                         'W': 17.8,
                         'V':  2.1,
                         'Y':  3.8,
                         'pY':-0.3},
                   'lcf': 0.0,
                   'const': 0.0}
"""A set of retention coefficients determined in Browne, C. A.;
Bennett, H. P. J.; Solomon, S. The isolation of peptides by
high-performance liquid chromatography using predicted elution
positions. Analytical Biochemistry, 1982, 124 (1), 201-208.

Conditions: Waters mjuBondapak C18 column, gradient (A = 0.13% aq. HFBA,
B = 0.13% HFBA in acetonitrile) at 0.33% B/min, flow rate 1.5 ml/min.

.. ipython::
   
   In [2]: pprint(pyteomics.achrom.RCs_browne_hfba)
"""

RCs_palmblad = {'aa':{'K': -0.66,
                      'G': -0.29,
                      'L':  2.28,
                      'A':  0.41,
                      'C': -1.32,
                      'E': -0.26,
                      'D':  0.04,
                      'F':  2.68,
                      'I':  2.70,
                      'H':  0.57,
                      'M':  0.98,
                      'N': -0.54,
                      'Q':  1.02,
                      'P':  0.97,
                      'S': -0.71,
                      'R': -0.76,
                      'T':  0.37,
                      'W':  4.68,
                      'V':  2.44,
                      'Y':  2.78},
                'lcf': 0.0,
                'const': 0.0}
"""A set of retention coefficients determined in Palmblad, M.;
Ramstrom, M.; Markides, K. E.; Hakansson, P.; Bergquist, J. Prediction
of Chromatographic Retention and Protein Identification in Liquid
Chromatography/Mass Spectrometry. Analytical Chemistry, 2002, 74 (22),
5826-5830.

Conditions: a fused silica column (80-100 x 0.200 mm I.D.) packed
in-house with C18 ODS-AQ; solvent A = 0.5% aq. HAc, B = 0.5% HAc in
acetonitrile.

.. ipython::
   
   In [2]: pprint(pyteomics.achrom.RCs_palmblad)
"""

RCs_yoshida = {'aa':{'K':  2.77,
                     'G': -0.16,
                     'L': -2.31,
                     'A':  0.28,
                     'C':  0.80,
                     'E':  1.58,
                     'D':  2.45,
                     'F': -2.94,
                     'I': -1.34,
                     'H':  3.44,
                     'M': -0.14,
                     'N':  3.25,
                     'Q':  2.35,
                     'P':  0.77,
                     'S':  2.53,
                     'R':  3.90,
                     'T':  1.73,
                     'W': -1.80,
                     'V': -2.19,
                     'Y': -0.11},
               'lcf': 0.0,
               'const': 0.0}
"""A set of retention coefficients determined in Yoshida,
T. Calculation of peptide retention coefficients in normal-phase
liquid chromatography. Journal of Chromatography A, 1998, 808 (1-2),
105-112.

Conditions: TSK gel Amide-80 column (250 x 4.6 mm I.D.), gradient (A =
0.1% TFA in ACN-water (90:10); B = 0.1% TFA in ACN-water (55:45)) at
0.6% water/min, flow rate 1.0 ml/min, 40 centigrades.

.. ipython::
   
   In [2]: pprint(pyteomics.achrom.RCs_yoshida)
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()