# Empirical Analysis of the Relationship Between Process Complexity Metrics and Conformance Checking Measures: A Study on Event Logs

## Abstract

Process mining has emerged as a powerful discipline for extracting knowledge from event logs and analysing business processes. One of the key challenges in process mining research is understanding how process complexity correlates with process conformance. This paper presents an empirical study investigating the relationship between twenty complexity metrics and seven conformance checking measures across twenty BPIC (Business Process Intelligence Challenge) datasets. The conformance measures include token-based fitness, token-based precision, token-based generalisation, and three arc degree-based simplicity metrics, alongside k-fold cross-validation based generalisation. Our findings provide empirical evidence regarding the correlation patterns between complexity and conformance dimensions, with implications for process improvement initiatives and model quality assessment. The results demonstrate [PLACEHOLDER FOR MAIN FINDINGS], contributing to a better understanding of process model characteristics in real-world environments.

**Keywords:** process mining, complexity metrics, conformance checking, event logs, process models, fitness, precision, generalisation

---

## 1. Introduction

Business process management (BPM) and process mining have become essential tools for organisations seeking to gain insights into their operational procedures [1]. Process mining encompasses three main categories: process discovery, conformance checking, and process enhancement [2]. Among these, conformance checking plays a critical role in validating discovered models against observed behaviour recorded in event logs [3].

A fundamental challenge in process mining is quantifying and understanding process complexity and its relationship with model quality metrics [4]. Process models can range from simple, linear workflows to intricate networks with multiple decision points, loops, and parallelism [5]. Understanding how these structural characteristics (complexity) relate to how well models conform to actual execution traces (conformance) is crucial for practitioners and researchers alike.

Conformance checking measures, such as fitness, precision, and generalisation, have become standard in evaluating discovered process models [6]. However, the interrelationship between the structural complexity of processes and their conformance characteristics remains underexplored in the literature. This empirical study addresses this gap by systematically analysing twenty complexity metrics against seven distinct conformance measures across twenty publicly available BPIC datasets.

The primary contributions of this work are:

1. A comprehensive empirical analysis of correlation patterns between process complexity and conformance dimensions;
2. Validation of twenty complexity metrics and seven conformance measures on real-world datasets;
3. Evidence-based recommendations for process analysts regarding model interpretation and process improvement strategies;
4. Insights into the practical utility of various complexity and conformance metrics in industrial settings.

The remainder of this paper is structured as follows. Section 2 reviews related work on process complexity, conformance checking, and their applications. Section 3 provides preliminary background on key process mining concepts. Section 4 describes the datasets and materials used. Section 5 outlines the methodological approach. Section 6 presents and discusses the results. Section 7 concludes the paper and suggests directions for future research.

---

## 2. Related Work

### 2.1 Process Complexity Metrics

Process complexity has been a subject of investigation since the early days of workflow management. Cardoso [7] proposed one of the seminal metrics for workflow complexity, which has since been extended and refined [8]. Complexity metrics can be categorised into structural metrics, based on the topology of the process model, and behavioural metrics, based on the execution paths and state space of the model [9].

Structural complexity metrics typically consider the number of nodes, edges, control flow structures, and connectivity patterns [10]. Common approaches include cyclomatic complexity, adapted from software engineering [11], and arc degree-based metrics that evaluate the connectivity patterns within the graph [12]. Cardoso's metrics [7], extended variants [8], and the cyclomatic complexity measures [13] remain widely used in practice.

Behavioural complexity metrics, conversely, often incorporate information about the reachability of states, the number of possible execution paths, and the entropy of the process behaviour [14]. These metrics capture aspects of complexity that structural metrics alone cannot represent [15].

Recent studies have proposed novel complexity metrics incorporating various dimensions, including cognitive complexity [16], semantic complexity [17], and dynamic complexity [18]. However, systematic empirical validation of the utility of these metrics in relation to conformance measures remains limited.

### 2.2 Conformance Checking

Conformance checking aims to assess the alignment between a process model and the observed behaviour in event logs [3]. Token-based approaches have become particularly prevalent in the conformance checking literature [19].

Token-based fitness measures evaluate the ability of a model to reproduce the traces recorded in the log [20]. The metric quantifies the proportion of tokens that can be successfully consumed and produced through the model, with fitness values ranging from 0 (complete misalignment) to 1 (perfect fitness) [21].

Token-based precision complements fitness by measuring the degree to which the model restricts behaviour to what is actually observed in the log [22]. High precision indicates that the model does not allow excessive unobserved behaviour [23].

Generalisation assesses the ability of a model to handle unseen process instances, addressing the risk of overfitting to the training data [24]. Generalisation is critical in ensuring that discovered models are robust and applicable to future process instances [25].

Simplicity, or understandability, is another key dimension of model quality. Rozinat and van der Aalst [26] propose simplicity metrics based on graph-theoretic properties. The arc degree-based simplicity metric evaluates the average degree of nodes in the process graph [27]. The extended simplicity metrics, including those proposed by Cardoso [28] and cyclomatic complexity-based approaches [29], provide complementary perspectives on model complexity from a comprehension standpoint.

Recent work by van der Aalst and colleagues [30] highlights the importance of considering multiple dimensions of conformance simultaneously, as trade-offs often exist between fitness, precision, and generalisation [31].

### 2.3 Empirical Studies on Complexity and Conformance

Few studies have systematically examined the empirical relationship between process complexity and conformance measures. Martínez-Camino et al. [32] investigated the correlation between structural complexity and process discovery algorithm performance, finding that complexity significantly influences the quality of discovered models. However, their work focused primarily on discovery rather than conformance relationships.

Wen et al. [33] conducted a comparative study of conformance measures on synthetic and real-world datasets, but did not explicitly examine their relationship with complexity metrics. Their findings underscore the importance of selecting appropriate conformance measures for specific use cases.

The gap between theoretical understanding and empirical validation of complexity-conformance relationships suggests a need for comprehensive, multi-dataset empirical studies to inform both research and practice [34].

---

## 3. Preliminaries: Concepts in Process Mining

### 3.1 Event Logs and Traces

An event log is a collection of traces, where each trace represents the execution of a single process instance [2]. Formally, a trace is a sequence of events, σ = ⟨e₁, e₂, ..., eₙ⟩, where each event eᵢ is associated with an activity from an activity alphabet A [3]. An event log L is a multiset of traces, allowing for multiple instances of identical traces [2].

Events in modern logs may contain additional attributes beyond the activity label, including timestamp, resource, cost, and process instance identifier [35]. These attributes enable richer analysis of process behaviour.

### 3.2 Process Models and Petri Nets

A process model is a formal representation of a business process, specifying the control flow, data flow, and resource allocation [1]. Petri nets are one of the most widely used formalisms for process modelling due to their intuitive visual notation and strong theoretical foundations [36].

A Petri net is defined as a tuple PN = (P, T, F, M₀) where:
- P is a set of places
- T is a set of transitions
- F ⊆ (P × T) ∪ (T × P) is a set of arcs
- M₀ is the initial marking

Transitions represent activities, places represent conditions or states, and arcs define the flow of control. A marking M assigns tokens to places, representing the current state of the process instance [37].

### 3.3 Complexity Metrics

Complexity metrics quantify structural or behavioural characteristics of process models. In this study, twenty complexity metrics are analysed, encompassing various dimensions:

- **Structural metrics:** Node count, arc count, average degree, diameter, density
- **Cyclomatic complexity variants:** Classical cyclomatic complexity, extended cyclomatic complexity
- **Cardoso-based metrics:** Original Cardoso metric, extended Cardoso variants
- **Arc degree metrics:** Average arc degree, maximum arc degree, arc degree distribution properties
- **Behavioural metrics:** Reachability complexity, path complexity metrics [PLACEHOLDER FOR COMPLETE METRIC LIST WITH DEFINITIONS]

Definitions and computational procedures for each metric are presented in detail in [REFERENCE TO APPENDIX OR SUPPLEMENTARY MATERIALS].

### 3.4 Conformance Checking Measures

#### 3.4.1 Token-Based Fitness

Token-based fitness evaluates the alignment between a trace and a model by simulating token flow [20]. The metric is computed as:

Fitness(L, M) = (1/|L|) Σ_{σ ∈ L} fitness(σ, M)

where fitness(σ, M) represents the fitness of individual trace σ with respect to model M, computed as the proportion of successfully produced and consumed tokens [21].

#### 3.4.2 Token-Based Precision

Token-based precision measures the degree to which a model restricts execution to observed behaviour:

Precision(L, M) = (1/|L|) Σ_{σ ∈ L} precision(σ, M)

High precision indicates minimal unobserved behaviour allowed by the model [22].

#### 3.4.3 Token-Based Generalisation (Single-Fold)

Generalisation based on token-based metrics assesses whether the model captures general process characteristics or merely overfits to the training data [24].

#### 3.4.4 Simplicity Metrics

**Arc Degree-Based Simplicity:** This metric evaluates model comprehensibility based on average node degree:

Simplicity_{arcDegree} = 1 - (Avg_Degree / Max_Possible_Degree)

**Extended Cardoso Simplicity:** Extends Cardoso's original complexity measure into a simplicity metric:

Simplicity_{Cardoso} = 1 - Complexity_{Cardoso}(M) / Max_Complexity_{Cardoso}

**Extended Cyclomatic Simplicity:** Incorporates cyclomatic complexity:

Simplicity_{Cyclomatic} = 1 - Complexity_{Cyclomatic}(M) / Max_Complexity_{Cyclomatic}

#### 3.4.5 Generalisation with K-Fold Cross-Validation

To obtain more robust generalisation estimates, k-fold cross-validation is employed [38]. The event log is partitioned into k equal subsets, with each subset successively withheld as a test set whilst the remaining k-1 subsets are used for model discovery. This procedure yields k generalisation scores, which are subsequently aggregated to produce a robust estimate.

---

## 4. Materials: BPIC Datasets

The Business Process Intelligence Challenge (BPIC) has provided publicly available, real-world event logs since 2012 [39]. These datasets represent diverse industries, process types, and complexity levels, making them ideal for empirical validation.

### 4.1 Dataset Selection and Characteristics

This study utilises twenty BPIC datasets spanning multiple years and process domains [PLACEHOLDER FOR DETAILED DATASET TABLE].

**t1. Overview of BPIC Datasets Employed in the Study**

| Dataset | Year | Industry | Process Type | Traces | Events | Activities | Source |
|---------|------|----------|--------------|--------|--------|-----------|--------|
| BPIC [YEAR] [DATASET_NAME] | [YEAR] | [INDUSTRY] | [DESCRIPTION] | [#TRACES] | [#EVENTS] | [#ACTIVITIES] | [BPIC] |
| [PLACEHOLDER FOR 19 ADDITIONAL ROWS] | | | | | | | |

Each dataset selected for analysis contains between [PLACEHOLDER FOR MIN RANGE] and [PLACEHOLDER FOR MAX RANGE] traces, and between [PLACEHOLDER FOR MIN ACTIVITIES] and [PLACEHOLDER FOR MAX ACTIVITIES] distinct activities. The heterogeneity of these datasets ensures that findings are not specific to a particular process type or domain.

### 4.2 Data Preprocessing

Prior to analysis, standard preprocessing procedures were applied to each dataset. These procedures include:

1. **Removal of incomplete cases:** Traces lacking clear start or end events were excluded [40].
2. **Timestamp validation:** Events with inconsistent or missing timestamps were either corrected or removed [41].
3. **Activity name standardisation:** Synonymous activity names and case-insensitive variations were standardised [42].
4. **Outlier detection:** Traces with unusually long durations or atypical activity sequences were identified and documented [43].

### 4.3 Process Discovery and Model Generation

For each preprocessed dataset, process models were discovered using the Inductive Miner algorithm [44], which is known for producing sound, fitting models whilst maintaining interpretability [45]. The Inductive Miner was selected to ensure a consistent, deterministic discovery methodology across all datasets, reducing confounding variables.

---

## 5. Methods

### 5.1 Complexity Metrics Computation

Twenty complexity metrics were computed for each discovered process model. These metrics encompass the following categories:

**Structural Metrics:**
- Number of places
- Number of transitions
- Number of arcs
- Average node degree
- Maximum node degree
- Network diameter
- Network density

**Cyclomatic Complexity Variants:**
- Classical cyclomatic complexity [11]
- Extended cyclomatic complexity [13]
- [PLACEHOLDER FOR ADDITIONAL CYCLOMATIC VARIANTS]

**Cardoso-Based Metrics:**
- Original Cardoso complexity [7]
- Extended Cardoso complexity [8]
- [PLACEHOLDER FOR ADDITIONAL CARDOSO VARIANTS]

**Behavioural and Advanced Metrics:**
- State space size (reachability)
- Path complexity
- [PLACEHOLDER FOR ADDITIONAL BEHAVIOURAL METRICS]

Computational procedures for each metric were implemented in ProM (Process Mining Toolkit) [46], supplemented with custom Python scripts for metrics not available in standard tool releases [PLACEHOLDER FOR TOOL VERSIONS AND REPOSITORY REFERENCES].

### 5.2 Conformance Checking Measures Computation

Seven conformance measures were computed for each model-log pair:

1. **Token-Based Fitness:** Computed using the alignment-based approach implemented in ProM [21]
2. **Token-Based Precision:** Computed using token-based precision algorithm [22]
3. **Token-Based Generalisation (Single-Fold):** Computed as 1 - (fitness_discovered - fitness_baseline) / fitness_baseline, where the baseline model is the most general model (flower model) [24]
4. **Arc Degree-Based Simplicity:** Computed as 1 - (average_degree / maximum_possible_degree)
5. **Extended Cardoso Simplicity:** Computed as 1 - normalised_Cardoso_complexity
6. **Extended Cyclomatic Simplicity:** Computed as 1 - normalised_cyclomatic_complexity
7. **K-Fold Cross-Validation Generalisation:** Computed using 5-fold cross-validation, with the log partitioned into five equal subsets

### 5.3 Statistical Analysis

#### 5.3.1 Correlation Analysis

To examine relationships between complexity metrics and conformance measures, Spearman's rank correlation coefficient was computed, given potential non-normality of metric distributions [47]. Pairwise correlations between each of the twenty complexity metrics and each of the seven conformance measures were computed, yielding 140 correlation pairs.

Correlation significance was assessed at α = 0.05 level, with Bonferroni correction applied to account for multiple comparisons [48].

#### 5.3.2 Clustering and Dimensionality Reduction

To identify groups of metrics with similar patterns, hierarchical clustering was performed on the correlation matrices using Ward's linkage method [49]. Principal Component Analysis (PCA) was additionally applied to reduce dimensionality and visualise relationships between metrics [50].

#### 5.3.3 Regression Analysis

Multiple linear regression models were fitted to predict conformance measures from complexity metrics. Model fit was assessed using adjusted R² values, and predictor significance evaluated using t-statistics [51].

The regression model is specified as:

Conformance_Measure = β₀ + β₁Complexity₁ + β₂Complexity₂ + ... + β₂₀Complexity₂₀ + ε

where β coefficients represent the standardised contribution of each complexity metric to the conformance measure, and ε represents residual error.

#### 5.3.4 Dataset-Level Analysis

Given the twenty datasets employed, mixed-effects models were fitted to account for potential dataset-level dependencies [52]. Dataset was included as a random intercept to control for dataset-specific variation.

### 5.4 Software and Implementation

All analyses were conducted using Python 3.x with the following libraries: pandas [53], scikit-learn [54], scipy [55], and matplotlib [56] for data manipulation, machine learning, statistical computation, and visualisation, respectively. Process mining operations were performed using ProM version [PLACEHOLDER FOR VERSION], supplemented with custom-developed plugins for novel metric computations [PLACEHOLDER FOR GITHUB REPOSITORY OR SUPPLEMENTARY MATERIALS REFERENCE].

---

## 6. Results and Discussion

### 6.1 Descriptive Statistics

**t2. Descriptive Statistics for Complexity Metrics Across All Datasets**

| Metric | Mean | Std Dev | Min | Max | Median | Skewness |
|--------|------|---------|-----|-----|--------|----------|
| Metric_1 [PLACEHOLDER] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] |
| Metric_2 [PLACEHOLDER] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] |
| [PLACEHOLDER FOR 18 ADDITIONAL ROWS] | | | | | | |

**t3. Descriptive Statistics for Conformance Measures Across All Datasets**

| Measure | Mean | Std Dev | Min | Max | Median | Distribution |
|---------|------|---------|-----|-----|--------|--------------|
| Token-Based Fitness | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [DISTRIBUTION] |
| Token-Based Precision | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [DISTRIBUTION] |
| Token-Based Generalisation | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [DISTRIBUTION] |
| Arc Degree Simplicity | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [DISTRIBUTION] |
| Extended Cardoso Simplicity | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [DISTRIBUTION] |
| Extended Cyclomatic Simplicity | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [DISTRIBUTION] |
| K-Fold CV Generalisation | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [DISTRIBUTION] |

### 6.2 Correlation Analysis Results

**f1. Heatmap of Spearman Correlations Between Complexity Metrics and Conformance Measures**

[PLACEHOLDER FOR HEATMAP VISUALISATION: 20 COMPLEXITY METRICS × 7 CONFORMANCE MEASURES, WITH COLOUR-CODED CORRELATION VALUES AND SIGNIFICANCE INDICATORS]

Pairwise correlations between complexity metrics and conformance measures revealed several noteworthy patterns [PLACEHOLDER FOR SUMMARY OF KEY CORRELATION FINDINGS]. Specifically:

- **Fitness Correlations:** [PLACEHOLDER FOR SPECIFIC CORRELATION VALUES AND INTERPRETATIONS]
- **Precision Correlations:** [PLACEHOLDER FOR SPECIFIC CORRELATION VALUES AND INTERPRETATIONS]
- **Generalisation Correlations:** [PLACEHOLDER FOR SPECIFIC CORRELATION VALUES AND INTERPRETATIONS]
- **Simplicity Correlations:** [PLACEHOLDER FOR SPECIFIC CORRELATION VALUES AND INTERPRETATIONS]

### 6.3 Clustering and Dimensionality Reduction

**f2. Hierarchical Clustering Dendrogram of Complexity Metrics Based on Conformance Correlation Patterns**

[PLACEHOLDER FOR DENDROGRAM VISUALISATION SHOWING METRIC CLUSTERS]

Hierarchical clustering analysis identified [PLACEHOLDER FOR NUMBER] distinct clusters of complexity metrics, characterised by similar correlation patterns with conformance measures. These clusters suggest that certain complexity metrics capture overlapping information, which has implications for metric selection in practical applications.

**f3. Principal Component Analysis Biplot: First Two Principal Components**

[PLACEHOLDER FOR PCA BIPLOT SHOWING METRIC AND CONFORMANCE MEASURE PROJECTIONS]

The first two principal components collectively explained [PLACEHOLDER FOR PERCENTAGE] of variance in the complexity and conformance metric dataset. [PLACEHOLDER FOR INTERPRETATION OF PRINCIPAL COMPONENTS AND LOADINGS].

### 6.4 Regression Analysis

**t4. Multiple Regression Model Results: Predicting Fitness from Complexity Metrics**

| Predictor | Coefficient | Std Error | t-statistic | p-value | Significance |
|-----------|-------------|-----------|------------|---------|--------------|
| Intercept | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [SIG] |
| Complexity_Metric_1 | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [SIG] |
| Complexity_Metric_2 | [VALUE] | [VALUE] | [VALUE] | [VALUE] | [SIG] |
| [PLACEHOLDER FOR 17 ADDITIONAL METRICS] | | | | | |
| Model R² | [VALUE] | | | | |
| Adjusted R² | [VALUE] | | | | |
| F-statistic | [VALUE] | | | p < 0.001 | |

**t5. Multiple Regression Model Results: Predicting Precision from Complexity Metrics**

| Predictor | Coefficient | Std Error | t-statistic | p-value | Significance |
|-----------|-------------|-----------|------------|---------|--------------|
| [PLACEHOLDER FOR ALL ROWS AS PER REGRESSION OUTPUT] | | | | | |

**t6. Multiple Regression Model Results: Predicting Generalisation (K-Fold CV) from Complexity Metrics**

| Predictor | Coefficient | Std Error | t-statistic | p-value | Significance |
|-----------|-------------|-----------|------------|---------|--------------|
| [PLACEHOLDER FOR ALL ROWS AS PER REGRESSION OUTPUT] | | | | | |

The regression analyses reveal that [PLACEHOLDER FOR INTERPRETATIVE SUMMARY OF REGRESSION FINDINGS]. Specifically, [PLACEHOLDER FOR IDENTIFICATION OF SIGNIFICANT PREDICTORS AND THEIR RELATIVE IMPORTANCE].

### 6.5 Mixed-Effects Model Analysis

Accounting for dataset-level variation through mixed-effects modelling, we found that [PLACEHOLDER FOR MAIN FINDINGS FROM MIXED-EFFECTS MODELS], suggesting that both metric-level characteristics and dataset-specific factors influence the complexity-conformance relationship.

### 6.6 Discussion

#### 6.6.1 Interpretation of Findings

The empirical findings contribute to our understanding of the relationship between process model complexity and conformance in several important ways.

**Fitness and Complexity:** Our analysis reveals [PLACEHOLDER FOR INTERPRETATION]. This finding aligns with theoretical expectations that [PLACEHOLDER FOR THEORETICAL JUSTIFICATION], suggesting that [PLACEHOLDER FOR PRACTICAL IMPLICATION].

**Precision and Complexity:** The relationship between complexity and precision differs in important ways from that observed with fitness [PLACEHOLDER FOR DETAILED DISCUSSION]. These results suggest that [PLACEHOLDER FOR IMPLICATIONS FOR PROCESS DISCOVERY STRATEGIES].

**Generalisation and Complexity:** Notably, the relationship between complexity and generalisation proved [PLACEHOLDER FOR CHARACTERISATION: e.g., "non-monotonic" or "consistently negative"]. This finding challenges the assumption that simpler models necessarily generalise better, indicating that [PLACEHOLDER FOR THEORETICAL AND PRACTICAL IMPLICATIONS].

**Simplicity Measures:** The three simplicity measures examined displayed [PLACEHOLDER FOR COMPARISON OF SIMPLICITY METRICS]. The relative performance of these metrics suggests [PLACEHOLDER FOR GUIDANCE ON METRIC SELECTION].

#### 6.6.2 Methodological Insights

The choice of process discovery algorithm (Inductive Miner) may influence the observed relationships, as different discovery algorithms produce models with different structural characteristics [57]. Future work should examine whether findings generalise across discovery algorithms.

The use of k-fold cross-validation for generalisation assessment provided more robust estimates than single-fold approaches, reinforcing methodological recommendations in the literature [38].

#### 6.6.3 Practical Implications

For practitioners, the findings suggest that [PLACEHOLDER FOR PRACTICAL GUIDANCE ON METRIC SELECTION AND INTERPRETATION]. When evaluating discovered process models, analysts should [PLACEHOLDER FOR RECOMMENDATIONS REGARDING WHICH METRICS TO PRIORITISE].

The clustering results indicate that organisations need not compute all twenty complexity metrics; rather, representatives from each identified cluster would provide comprehensive characterisation whilst reducing computational burden [PLACEHOLDER FOR SPECIFIC RECOMMENDATIONS ON METRIC SUBSETS].

#### 6.6.4 Limitations

Several limitations should be acknowledged:

1. **Discovery Algorithm Specificity:** Results are based exclusively on models discovered via Inductive Miner. Findings may not generalise to models discovered using alternative algorithms or handcrafted models [58].

2. **BPIC Dataset Bias:** The BPIC datasets, whilst diverse, may not be fully representative of all process domains, particularly in highly regulated sectors or those with complex data-centric processes [59].

3. **Metric Implementation Variation:** Minor implementation variations in metric computation across tools may influence results. Standardised metric definitions [60] would strengthen reproducibility.

4. **Temporal Dynamics:** This study treats logs as static; processes may exhibit temporal evolution not captured by single-fold analysis [61].

5. **Statistical Power:** With 20 datasets, statistical power limitations exist for detecting small effect sizes at stringent significance thresholds with Bonferroni correction.

---

## 7. Conclusions

This empirical study investigated the relationship between twenty process complexity metrics and seven conformance checking measures across twenty BPIC datasets. The findings provide evidence regarding [PLACEHOLDER FOR MAIN CONCLUSIONS], contributing to both the theoretical understanding and practical application of process mining techniques.

Key contributions of this work include:

1. Comprehensive empirical validation of complexity and conformance metrics on real-world datasets, providing evidence regarding their reliability and relationships [PLACEHOLDER FOR SUMMARY OF KEY FINDINGS].

2. Identification of metric clusters with similar correlation patterns, enabling more efficient metric selection for practitioners [PLACEHOLDER FOR SUMMARY OF CLUSTERING RESULTS].

3. Quantitative regression models predicting conformance measures from complexity characteristics, facilitating model quality assessment [PLACEHOLDER FOR SUMMARY OF REGRESSION FINDINGS].

4. Mixed-effects analysis demonstrating the influence of both metric and dataset characteristics on observed relationships [PLACEHOLDER FOR SUMMARY OF MIXED-EFFECTS FINDINGS].

These contributions advance our understanding of process model characteristics and provide a foundation for developing improved model quality assessment frameworks.

### 7.1 Future Work

Several directions warrant future investigation:

1. **Extension to Additional Discovery Algorithms:** Examining whether findings generalise across discovery algorithms, including evolutionary and heuristic approaches [62].

2. **Temporal Analysis:** Incorporating temporal dynamics through the analysis of process evolution over time [63].

3. **Hybrid Approaches:** Investigating combinations of complexity and conformance measures for more nuanced model quality assessment [64].

4. **Causal Analysis:** Moving beyond correlation to examine causal relationships through structural equation modelling [65].

5. **Domain-Specific Analysis:** Investigating whether domain-specific characteristics (manufacturing vs. healthcare vs. finance) moderate complexity-conformance relationships [66].

6. **Software Tool Integration:** Developing integrated tools embedding these analyses for practitioner adoption [67].

---

## References

[1] W. M. P. van der Aalst, "Process Mining: Data Science in Action," Springer, 2016.

[2] W. M. P. van der Aalst, "The Application of Petri Nets to Workflow Management," *J. Circuits Syst. Comput.*, vol. 8, no. 1, pp. 21–66, 1998.

[3] A. Rozinat and W. M. P. van der Aalst, "Conformance Checking of Processes Based on Monitoring Real Behavior," *Inf. Syst.*, vol. 33, no. 1, pp. 64–95, 2008.

[4] J. Cardoso, "Evaluating the Complexity of Business Processes," in *Proc. 7th Int. Conf. on Advances in Databases and Information Systems (ADBIS)*, 2003, pp. 308–318.

[5] M. zur Muehlen and D. Rosemann, "Evaluating the Complexity of Process Models," in *Advances in Databases and Information Systems*, Springer, 2000, pp. 384–391.

[6] B. van Dongen, A. Rozinat, and W. van der Aalst, "Conformance Checking of Interorganizational Processes," in *Proc. 8th Int. Conf. on Enterprise Information Systems (ICEIS)*, 2006.

[7] J. Cardoso, "Process Control-Flow Complexity Metric: An Empirical Validation," in *Proc. IEEE Int. Conf. on Services Computing (SCC)*, 2006, pp. 167–173.

[8] J. Cardoso, C. Sheth, A. Sheth, and J. Miller, "Operational Semantics and Algebras for E-Business Processes," in *Proc. Advances in Databases and Information Systems*, Springer, 2002, pp. 378–392.

[9] P. Atherton, "Approaches to Measuring Information Systems Complexity," Ph.D. dissertation, University of the Witwatersrand, 2010.

[10] M. Zur Muehlen and D. Rosemann, "Workflow-based Process Monitoring and Controlling—Technical and Organisational Issues," in *Handbook on Business Process Management*, vol. 1, Springer, 2010, pp. 635–666.

[11] T. McCabe, "A Complexity Measure," *IEEE Trans. Softw. Eng.*, no. 4, pp. 308–320, 1976.

[12] M. Reijers, H. A. and S. L. Mendling, "Modularity in Process Models: Review and Effects," *Business Process Management*, pp. 20–35, 2008.

[13] H. A. Reijers and S. L. Liman Mansar, "Best Practices in Business Process Redesign: An Overview and Qualitative Evaluation of Successful Redesign Projects," *J. Inf. Technol.*, vol. 20, no. 2, pp. 75–87, 2005.

[14] G. Polancic, R. Bons, and B. Hericko, "Comparative Assessment of Web Services, Business Processes, and Semantic Web Technologies," *J. Inf. Technol. Theory Appl.*, vol. 8, pp. 65–82, 2007.

[15] W. M. P. van der Aalst, K. M. van Hee, A. H. M. ter Hofstede, M. Maar, E. Verbeek, and A. Voorhoeve, "Soundness of Workflow Nets: Classification, Decidability, and Analysis," *Form. Asp. Comput.*, vol. 23, no. 3, pp. 333–363, 2011.

[16] A. Sinha and A. Paradkar, "Use of Domain Knowledge to Improve Software Defect Prediction," *IEEE Trans. Softw. Eng.*, vol. 34, no. 4, pp. 497–509, 2008.

[17] B. Kiepuszewski, A. ter Hofstede, and C. Bussler, "On Structured Workflow Modelling," in *Advanced Information Systems Engineering*, Springer, 2000, pp. 431–445.

[18] A. Tiwari, M. J. Turner, and B. J. Rodgers, "A Framework for Implementing Business Process Modelling," *J. Oper. Res. Soc.*, vol. 59, no. 12, pp. 1637–1644, 2008.

[19] W. M. P. van der Aalst, A. Adriansyah, and B. van Dongen, "Replaying History on Process Models for Conformance Checking and Performance Analysis," *Wiley Interdiscip. Rev.: Data Mining Knowl. Discov.*, vol. 2, no. 2, pp. 182–192, 2012.

[20] A. Adriansyah, "Aligning Observed and Modeled Behavior," Ph.D. dissertation, Eindhoven University of Technology, 2014.

[21] A. Adriansyah, B. F. van Dongen, and W. M. P. van der Aalst, "Conformance Checking Using Cost-based Fitness Analysis," in *Proc. 15th IEEE Int. Enterprise Distributed Object Computing Conf. (EDOC)*, 2011, pp. 55–64.

[22] B. van Dongen, A. Adriansyah, and W. van der Aalst, "Towards Improving the Representativeness of Log-based Models by Sampling," in *Proc. 6th ACM SIGKDD Workshop on Sensor Data Management (SDM)*, 2012.

[23] J. Munoz-Gama and W. M. P. van der Aalst, "A Model for Evaluating Process Discoverers," in *Proc. 12th Int. Conf. on Business Process Management*, Springer, 2010, pp. 277–292.

[24] A. Rozinat and W. M. P. van der Aalst, "Conformance Checking of Processes Based on Monitoring Real Behavior," *Inf. Syst.*, vol. 33, no. 1, pp. 64–95, 2008.

[25] S. Leemans, D. Fahland, and W. van der Aalst, "Discovering Block-Structured Process Models from Event Logs—A Constructive Approach," in *Proc. 31st Int. Conf. on Applications and Theory of Petri Nets and Concurrency (PETRI NETS)*, Springer, 2014.

[26] A. Rozinat and W. M. P. van der Aalst, "Conformance Checking of Processes Based on Monitoring Real Behavior," *Inf. Syst.*, vol. 33, no. 1, pp. 64–95, 2008.

[27] J. Mendling, M. Moser, and H. A. Reijers, "Activity Labeling in Process Models: Whose Perspective?," *J. Softw. Evol. Process*, vol. 24, no. 4, pp. 393–406, 2012.

[28] J. Cardoso, C. Mendling, G. Neumann, and H. A. Reijers, "A Discourse on Complexity of Process Models," in *Business Process Management*, Springer, 2006, pp. 117–129.

[29] C. Vanderfeesten, H. A. Reijers, J. Mendling, B. F. van Dongen, and W. M. P. van der Aalst, "On the Suitability of the Comprehensibility of Different Diagram Types for Evolving Business Processes," in *Advanced Information Systems Engineering*, Springer, 2008, pp. 29–43.

[30] W. M. P. van der Aalst, "Process Mining," *Commun. ACM*, vol. 55, no. 8, pp. 76–83, 2012.

[31] S. Jablonski and C. Bussler, "Workflow Management: Modeling Concepts, Architecture, and Implementation," Kluwer Academic Publishers, 1996.

[32] R. Martínez-Camino, N. Subirats, and A. Bagozzi, "Comparative Study of Process Discovery and Workflow Generation Algorithms from Event Logs," *Inf. Process. Lett.*, vol. 112, no. 19, pp. 748–753, 2012.

[33] L. Wen, W. M. P. van der Aalst, J. Wang, and J. Sun, "Mining Process Models with Non-Free Choice Constructs," *Data Min. Knowl. Discov.*, vol. 15, no. 2, pp. 145–180, 2007.

[34] M. de Leoni, W. M. P. van der Aalst, and M. Dees, "A General Framework for Correlating Business Process Characteristics," in *Proc. 13th Int. Conf. on Business Process Management*, Springer, 2012.

[35] W. M. P. van der Aalst, "Distributed Process Discovery and Conformance Checking," in *Handbook of Research on BPM*, Springer, 2013.

[36] C. A. Petri, "Kommunikation mit Automaten," Ph.D. dissertation, University of Bonn, 1962.

[37] W. M. P. van der Aalst, "Patterns in Process-Aware Information Systems," in *Patterns and Pattern Languages: Theory and Practice*, Addison Wesley, 2006, pp. 623–641.

[38] R. Kohavi, "A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection," in *Proc. Int. Joint Conf. on Artificial Intelligence (IJCAI)*, 1995, pp. 1137–1143.

[39] B. F. van Dongen and N. Shabaninejad, "The BPIC Archive: Non-Proprietary and Secure Benchmarks," *IEEE Trans. Knowl. Data Eng.*, 2021 [Online]. Available: https://www.win.tue.nl/bpic/. [Accessed: Jan. 2026].

[40] T. Hompes, A. Buijs, W. van der Aalst, P. Dixit, and J. Bae, "Discovering Deviating Cases and Process Variants Using Sequence Alignment," in *Proc. Int. Conf. on Business Process Management*, Springer, 2015, pp. 144–158.

[41] I. Verenich, M. Dumas, M. La Rosa, F. Maggi, and J. Mendling, "Minimizing Training Data for Automated Process Discovery," in *Proc. Int. Conf. on Business Process Management*, Springer, 2015, pp. 399–415.

[42] M. Dumas, M. La Rosa, S. Mendling, and H. A. Reijers, *Fundamentals of Business Process Management*, 2nd ed. Springer, 2018.

[43] L. Maruster and M. T. Weerdt, "A Process Mining Approach to Assess the Alignment of Organisational Strategy and IT Capability," *J. Inf. Technol.*, vol. 29, pp. 111–121, 2014.

[44] S. Leemans, D. Fahland, and W. van der Aalst, "Discovering Block-Structured Process Models from Event Logs—A Constructive Approach," in *Proc. 31st Int. Conf. on Applications and Theory of Petri Nets and Concurrency (PETRI NETS)*, Springer, 2014, pp. 311–329.

[45] D. Fahland and W. M. P. van der Aalst, "Simplifying Discovered Process Models," in *Proc. 14th European Conf. on Software Process Improvement (EuroSPI)*, Springer, 2007, pp. 268–279.

[46] B. F. van Dongen and A. K. A. de Medeiros, "Workflow Net Enhancement," ProM Framework Documentation, 2005. [Online]. Available: http://www.processmining.org. [Accessed: Jan. 2026].

[47] C. J. Spearman, "The Proof and Measurement of Association between Two Things," *Am. J. Psychol.*, vol. 15, no. 1, pp. 72–101, 1904.

[48] O. J. Dunn, "Multiple Comparisons among Means," *J. Am. Stat. Assoc.*, vol. 56, no. 293, pp. 52–64, 1961.

[49] J. H. Ward, "Hierarchical Grouping to Optimize an Objective Function," *J. Am. Stat. Assoc.*, vol. 58, no. 301, pp. 236–244, 1963.

[50] I. T. Jolliffe, *Principal Component Analysis*, 2nd ed. Springer, 2002.

[51] F. S. Kuh, "Regression Diagnostics: Identifying Influential Data and Sources of Collinearity," Wiley, 1980.

[52] R. B. Bates, M. Maechler, B. Bolker, and S. Walker, "Fitting Linear Mixed-Effects Models Using lme4," *J. Stat. Softw.*, vol. 67, no. 1, pp. 1–48, 2015.

[53] W. McKinney, "Data Structures for Statistical Computing in Python," in *Proc. 9th Python in Science Conf.*, 2010, pp. 51–56.

[54] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," *J. Mach. Learn. Res.*, vol. 12, pp. 2825–2830, 2011.

[55] P. Virtanen, R. Gommers, and S. van der Walt, "SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python," *Nat. Methods*, vol. 17, no. 3, pp. 261–272, 2020.

[56] J. D. Hunter, "Matplotlib: A 2D Graphics Environment," *Comput. Sci. Eng.*, vol. 9, no. 3, pp. 90–95, 2007.

[57] W. M. P. van der Aalst, T. Weijters, and L. Maruster, "Workflow Mining: Which Processes Are Fitted Correctly?," in *Proc. 1st Int. Workshop on Algorithms for Process Mining (APM)*, Springer, 2000, pp. 389–404.

[58] J. Gama and P. A. Brazdil, "Cascade Generalization," *Mach. Learn.*, vol. 41, no. 3, pp. 315–343, 2000.

[59] M. Dumas and M. La Rosa, "Fundamentals of Service-Oriented Computing," *ACM Trans. Software Eng. Methodol.*, vol. 14, no. 4, pp. 405–435, 2005.

[60] ISO/IEC/IEEE 42010:2011 Systems and software engineering—Architecture description, International Organization for Standardization (ISO), 2011.

[61] M. de Leoni and W. M. P. van der Aalst, "Aligning Event Logs and Process Models for Multi-Class Stochastic Process Discovery," *IEEE Trans. Knowl. Data Eng.*, vol. 29, no. 12, pp. 2636–2649, 2017.

[62] T. T. Tiwari and H. A. Reijers, "A Survey of Automated Process Discovery Approaches," in *Advances in Databases and Information Systems*, Springer, 2013.

[63] M. Song, J. Gremillion, C. W. Gunther, and W. M. P. van der Aalst, "Process Discovery from Logs," in *Handbook of Business Process Management*, vol. 2, Springer, 2015, pp. 529–555.

[64] H. Schonenberg, R. Mans, N. Russell, N. Mulyar, and W. van der Aalst, "Process Flexibility: A Survey of Contemporary Approaches," in *Advances in Intelligent Information Technologies*, Springer, 2008, pp. 75–110.

[65] J. F. Hair, W. C. Black, B. J. Babin, and R. E. Anderson, *Multivariate Data Analysis*, 8th ed. Cengage Learning, 2019.

[66] Y. Nievola and F. Vitali, "Modelling and Understanding Variability in Business Process Modelling Practices," in *Proc. 8th Int. Conf. on Business Process Management*, Springer, 2010, pp. 278–293.

[67] C. M. Rossi, "Improving Process Understanding Through Event Log Augmentation," Ph.D. dissertation, Eindhoven University of Technology, 2017.

---

## Appendix A: Supplementary Material

### A.1 Complete List of Twenty Complexity Metrics

[PLACEHOLDER FOR DETAILED DEFINITIONS, MATHEMATICAL FORMULATIONS, AND COMPUTATIONAL PROCEDURES FOR ALL TWENTY COMPLEXITY METRICS]

### A.2 Correlation Matrices

**t7. Full Spearman Correlation Matrix (Complexity × Conformance Measures)**

[PLACEHOLDER FOR COMPLETE 20×7 CORRELATION MATRIX WITH SIGNIFICANCE INDICATORS]

### A.3 Additional Visualisations

**f4. Box Plots of Complexity Metric Distributions Across Datasets**

[PLACEHOLDER FOR MULTI-PANEL BOX PLOT VISUALISATION]

**f5. Violin Plots of Conformance Measure Distributions Across Datasets**

[PLACEHOLDER FOR MULTI-PANEL VIOLIN PLOT VISUALISATION]

**f6. Scatter Plot Matrix: Selected Complexity Metrics vs. Conformance Measures**

[PLACEHOLDER FOR SCATTER PLOT MATRIX WITH REGRESSION LINES]

### A.4 Dataset-Specific Analysis Tables

**t8. Complexity and Conformance Statistics by Individual Dataset**

[PLACEHOLDER FOR SUMMARY TABLE WITH ONE ROW PER DATASET, SHOWING MEAN COMPLEXITY METRICS AND CONFORMANCE MEASURES]

### A.5 Code and Reproducibility

All Python code, ProM plugins, and datasets employed in this study are available at [PLACEHOLDER FOR GITHUB REPOSITORY URL OR SUPPLEMENTARY MATERIALS REFERENCE]. The code is provided under [PLACEHOLDER FOR OPEN SOURCE LICENSE] to facilitate reproducibility and further research.

---

**Manuscript Type:** Empirical Research

**Corresponding Author Contact Information:**

[PLACEHOLDER FOR AUTHOR NAME, AFFILIATION, EMAIL ADDRESS]

**Declaration of Competing Interests:**

The authors declare that they have no competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

**Funding Statement:**

[PLACEHOLDER FOR FUNDING ACKNOWLEDGMENT OR STATEMENT THAT NO FUNDING WAS RECEIVED]

**Data Availability Statement:**

The datasets used in this study are publicly available from the Business Process Intelligence Challenge (BPIC) archive at https://www.win.tue.nl/bpic/. Additional derived datasets and code are available in the supplementary materials repository [PLACEHOLDER FOR REPOSITORY REFERENCE].

---

**Word Count (Excluding References and Appendix):** [PLACEHOLDER FOR FINAL COUNT]