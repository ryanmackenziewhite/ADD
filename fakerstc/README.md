faker-stc

FakerSTC aims to build on top of the Faker python module
to provide complete metadata models from which to generate fake data.
Similar projects can be found for Django, for instance, which
rely on a known schema to generate fake data.
FakerSTC will add additional level on complexity by allowing for
probability distribution functions (with known parameters) from which to sample
from, generating fake data according to a meta data type and with a distribution.

Structure
fakerstc
--- models (Meta data dictionary to describe a dataset)
--- pdfs (Probability distribution functions, e.g. GLM)
--- providers (Custom providers for sampling)
--- utils (Required utilities not provided by the default faker)

Envisioned use case(s):
    Repository of meta data information of administrative data sources
    Repository of code sets for classification according to field specifications
    Development of typical data pipelines
    Scaling of datasets for load testing of cloud native processing platforms
    Scaling of datasets with embedded pdfs (with known parameters) for testing optimization
    problems, e.g. GLM fits in single-threaded in-memory python up to out-of-core memory
    optimization problems using frameworks such as Spark.
    Simulated data from sampling known models, modeling of simulated data using DataSynthesizer
    to test use of non-parametric modeling and bayesian network.

Development notes:
    Meta data model
        Consider a well-defined data model
        that is a nested dictionary
        allows to serialize to JSON
        Same dictionary can be used in a DQ monitoring
        class which does the schema check against
        a loaded data model.
        requires two dictionaries (or more???)
            dictionary of custom providers
                key = custom provider class
                values = list of arguments, e.g. pdf
            dictionary of fakes
                key = name of provider class
                values = list of optional argument
        @TODO: Investigate use of Factory Boy. Also, see the wrapper class Faker for faker
        https://github.com/FactoryBoy/factory_boy/blob/master/factory/faker.py

    Custom providers
        Follow coding guidelines from Faker
        Accept a function (with arguments) for pdfs
        pdf takes values generated from provider to accept/reject
        Synthesizer needs to add custom provider and pass faker (generator)
        Find the module by name in fakerstc as in faker
        In order to use custom pdfs, first generate the fake values X
        pass the generated fakes to the pdf to compute the y
        pass y to custom provider whether to accept/reject. Does
        the custom provider need the list of fakes to generate
        and return a list of values. Unlike normal fakes which return a single
        value, this returns of list X with the generated values that
        are accepted from sampling.
        
     Pdfs
        Provider may contain a function as an object
        When adding custom provider, should be able to lookup
        by name the pdf. Should the pdf be a class or simply a
        call to the function?
        Pdf needs to take a list of providers which to generate
        values from. E.g., use a GLM model and return y and X
        where y is normal and X are fakes.
    Codesets
        Similar to the pdfs, a codeset should be added to a custom provider
        and use random.choice to select a random key from the codeset dictionary
    Synthesizers
        The simplest synthesizer just returns a row of values generated from faker.
        Consider GSBPM processes to be able to test in pipelines,
        e.g. imputation, which should alter the default synthesizer.
        Imputation -- fudge at random a row and within a row
        fudge a cell by placing null values.
        Record Linkage -- Use an existing list of names to generate different
        datasets. Randomly alter names in second data set.


    Faker defines everything inside the provider. For fakerstc use case, want to
    keep a directory of pdfs and codesets to add the custom providers

    Generate one row of data according to schema
    
    Need to work out an example of generating simple linear model, such that
    y = mx + b, and y is a normal distribution. Then we get, e.g.
    distribution of age in a population which is related to their weight.
    When sampling, we get the accepted value of the age and the accepted value of x.
    First, need to sample y within a normal distribution. For each y, sample x
    if y is in normal and x gives back y according to linear model, also x will end up
    as normal distribution. Afterwards, should fit the sample to ensure that y = mx + b.
    Once we have y = mx + b, just scale to GLM using OLS with arbitrarily large parameters.
    After that, can use a logit model for y and extend to the most generalized case and
    feed to an ANN.
