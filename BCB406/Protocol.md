Protocol for the Manual Investigation
=====================================

The following is the protocol for the manual investigation of the snippets.
Both authors have followed the protocol during the manual assessment of the 406 clone pairs sampled from the WT3/T4 true clone pairs.

Instructions
------------

Consider the two snippets (methods) and answer the two questions:

1. Does each of the two snippets implement the functionality as its main or only purpose?
2. Are the two snippets (methods) Type-3 or Type-4 clones?

Question 1
----------

The functionality of each method should be checked against the specification as found in the respective table.
The two methods should be labelled as the following:

- **major** The method implements the whole functionality as its main or only purpose.
	It implements the functionality true to the specification.
- **incomplete** The method implements only part of the functionality as its main or only purpose.
	Some part of the functionality is missing and likely implemented in another method that calls the method of interest, or in another method that the method of interest calls.
- **minor** The method uses the functionality, but has a different main purpose.
- **wrong** The method does not implement the functionality true to the specification.
- **test** The method implements the functionality as part of a test.


Question 2
----------

We rely on the original definition of Type-3 and Type-4 clones:

A Type-3 clone is
- A clone with very similar source code, but with small changes made to the code to tailor it to some new function [Carter1993].
- A copied fragment with further modifications such as changed, added, or removed statements, in addition to variations in identifiers, literals, types, whitespace, layout and comments [Roy2009].

A Type-4 clone is
- A functionally identical clone, possibly with the originator unaware that there is a function already available that accomplishes essentially the same function [Carter1993].
- Two or more code fragments that perform the same computation but are implemented by different syntactic variants [Roy2009].

However, Type-4 clones as defined as above require identical functionality or the same computation.
Such a definition is not decidable in general and we only require that the two fragments are functionally similar.
As a definition for similar functionality we use the following:

  *Two code snippets are considered functionally similar when they achieve the same result or perform the same task, even if they differ in syntax, structure, or the specific steps they take to accomplish that task.*


In the definition from Roy et al. [Roy2009] we drop the requirement that they are implemented by different syntactic variants (due to the automatic classification, there should be no clones with similar syntactic variants in the sample).
There should be no Type-3 pair as all Type-3 pairs should have been filtered out by the automatic filter based on dissimilarity.
If there is, the pair needs close attention.

Based on the labels of the two methods, usually, the second question is only true for a major/major pair.
However, there may be cases where the two methods are labelled differently, but are still clones of each other.
Such cases need close attention.
