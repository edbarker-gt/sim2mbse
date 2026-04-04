package simple_example {

  doc /*
    Baseline deterministic SysML v2-style model generated from
    Nastran exchange JSON.
  */

  part def SolverContext {
    attribute name : String;
    attribute version : String;
    attribute sol : Integer;
  }

  part def StructuralSummary {
    attribute nodeCount : Integer;
    attribute elementCountsByType : String;
  }

  part def MaterialSummary {
    attribute mid : Integer;
    attribute type : String;
  }

  part def AnalysisCase {
    attribute id : Integer;
    attribute label : String;
    attribute analysisType : String;
    attribute spc : String;
    attribute load : String;
  }

  part def ProvenanceRecord {
    attribute sourceFiles : String;
    attribute timestamp : String;
  }

  part solverContext : SolverContext {
    name = "NASTRAN";
    version = "unknown";
    sol = 0;
  }

  part structuralSummary : StructuralSummary {
    nodeCount = 20;
    elementCountsByType = "CBAR=10, CBEAM=2, CBUSH=1, CQUAD4=4";
  }

  part material_1 : MaterialSummary {
    mid = 1;
    type = "MAT1";
  }

  part subcase_1 : AnalysisCase {
    id = 1;
    label = "SUBCASE_1";
    analysisType = "";
    spc = "";
    load = "1";
  }

  part subcase_2 : AnalysisCase {
    id = 2;
    label = "SUBCASE_2";
    analysisType = "";
    spc = "";
    load = "2";
  }

  part subcase_3 : AnalysisCase {
    id = 3;
    label = "SUBCASE_3";
    analysisType = "";
    spc = "";
    load = "3";
  }

  part provenance : ProvenanceRecord {
    sourceFiles = "simple-example.bdf";
    timestamp = "2026-04-03T21:32:37+00:00";
  }

}
