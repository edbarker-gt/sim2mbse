package test {

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
    sol = 101;
  }

  part structuralSummary : StructuralSummary {
    nodeCount = 22;
    elementCountsByType = "CQUAD4=10";
  }

  part subcase_1 : AnalysisCase {
    id = 1;
    label = "SUBCASE_1";
    analysisType = "LinearStatic";
    spc = "2";
    load = "2";
  }

  part provenance : ProvenanceRecord {
    sourceFiles = "test.bdf";
    timestamp = "2026-04-03T21:32:37+00:00";
  }

}
